"""Release-gate evaluation.

The gate consumes compiled regression cases and produces a deterministic
verdict: ``pass``, ``warn``, or ``block``. The verdict is driven by a small,
explainable scoring model rather than opaque heuristics so CI logs can quote
the exact reasons.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

