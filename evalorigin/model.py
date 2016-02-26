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
