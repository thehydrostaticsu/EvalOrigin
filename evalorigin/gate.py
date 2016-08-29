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
