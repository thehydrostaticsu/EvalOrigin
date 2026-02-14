"""Release-gate evaluation.

The gate consumes compiled regression cases and produces a deterministic
verdict: ``pass``, ``warn``, or ``block``. The verdict is driven by a small,
explainable scoring model rather than opaque heuristics so CI logs can quote
the exact reasons.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .model import GateSummary, RegressionCase

_SEVERITY_WEIGHT = {"critical": 1.0, "high": 0.7, "medium": 0.4, "low": 0.2, "info": 0.05}


@dataclass(frozen=True)
class GateConfig:
    """Thresholds that control the gate verdict.

    ``block_severities`` lists severities whose presence forces a ``block``.
    ``warn_threshold`` and ``block_threshold`` compare against the weighted
    risk score, a value in ``[0, 1]`` where higher means riskier.
    """

    block_severities: tuple[str, ...] = ("critical",)
    warn_threshold: float = 0.35
    block_threshold: float = 0.65


def _risk_score(cases: List[RegressionCase]) -> float:
    if not cases:
        return 0.0
    total = sum(_SEVERITY_WEIGHT.get(c.severity, 0.3) for c in cases)
    return min(1.0, total / len(cases))


def evaluate_gate(cases: List[RegressionCase], config: GateConfig) -> GateSummary:
    """Compute the gate verdict for a set of regression cases."""
    by_severity: Dict[str, int] = {}
    for c in cases:
        by_severity[c.severity] = by_severity.get(c.severity, 0) + 1

    score = _risk_score(cases)
    reasons: List[str] = []

    blocking = sum(by_severity.get(s, 0) for s in config.block_severities)
    verdict = "pass"

    if blocking > 0:
        verdict = "block"
        reasons.append(
            f"{blocking} case(s) at blocking severity {sorted(config.block_severities)}"
        )
    elif score >= config.block_threshold:
        verdict = "block"
        reasons.append(f"risk score {score:.2f} >= block threshold {config.block_threshold}")
    elif score >= config.warn_threshold:
        verdict = "warn"
        reasons.append(f"risk score {score:.2f} >= warn threshold {config.warn_threshold}")
    else:
        reasons.append(f"risk score {score:.2f} below warn threshold {config.warn_threshold}")

    if not cases:
        reasons = ["no regression cases compiled; nothing to gate"]

    return GateSummary(
        verdict=verdict,
        score=score,
        total_cases=len(cases),
        blocking_cases=blocking,
        by_severity=by_severity,
        reasons=reasons,
    )

# draft note 1408
