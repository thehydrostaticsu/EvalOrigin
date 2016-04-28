"""Core data model for EvalOrigin.

All artifacts are plain dataclasses with deterministic ``to_dict`` methods so
that serialized output is byte-stable across runs. Ordering of keys and
collections is fixed; no timestamps or random identifiers leak into the
compiled artifacts unless supplied explicitly by the input.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def stable_id(*parts: str) -> str:
    """Return a short deterministic identifier for the given parts."""
    joined = "\x1f".join(parts)
    digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return digest[:12]


@dataclass(frozen=True)
class TraceStep:
    """A single observed step inside an execution trace."""

    index: int
    op: str
    input: Any = None
    output: Any = None
    status: str = "ok"
    detail: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "op": self.op,
            "input": self.input,
            "output": self.output,
            "status": self.status,
            "detail": self.detail,
        }

    @classmethod
    def from_dict(cls, raw: Dict[str, Any], fallback_index: int) -> "TraceStep":
        return cls(
            index=int(raw.get("index", fallback_index)),
            op=str(raw.get("op", "step")),
            input=raw.get("input"),
            output=raw.get("output"),
            status=str(raw.get("status", "ok")),
            detail=str(raw.get("detail", "")),
        )


@dataclass(frozen=True)
class Trace:
    """An ordered execution trace with an outcome."""

    trace_id: str
    entrypoint: str
    outcome: str
    steps: List[TraceStep] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    expected: Any = None
    actual: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "entrypoint": self.entrypoint,
            "outcome": self.outcome,
            "tags": sorted(self.tags),
            "expected": self.expected,
            "actual": self.actual,
            "steps": [s.to_dict() for s in self.steps],
        }

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "Trace":
        steps_raw = raw.get("steps", []) or []
        steps = [TraceStep.from_dict(s, i) for i, s in enumerate(steps_raw)]
        steps.sort(key=lambda s: s.index)
        return cls(
            trace_id=str(raw.get("trace_id") or raw.get("id") or "trace"),
            entrypoint=str(raw.get("entrypoint", "unknown")),
            outcome=str(raw.get("outcome", "unknown")),
            steps=steps,
            tags=list(raw.get("tags", []) or []),
            expected=raw.get("expected"),
            actual=raw.get("actual"),
        )

    @property
    def failing_steps(self) -> List[TraceStep]:
        return [s for s in self.steps if s.status.lower() in ("error", "fail", "failed")]


@dataclass(frozen=True)
class Incident:
    """A production or CI failure that seeds regression coverage."""

    incident_id: str
    title: str
    severity: str
    entrypoint: str
    trace: Trace
    signature: str = ""
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "severity": self.severity,
            "entrypoint": self.entrypoint,
            "signature": self.signature,
            "notes": self.notes,
            "trace": self.trace.to_dict(),
        }

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "Incident":
        trace = Trace.from_dict(raw.get("trace", {}) or {})
        return cls(
