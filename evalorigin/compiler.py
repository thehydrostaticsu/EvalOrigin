"""Compilation stages that turn traces and incidents into pack artifacts.

The compiler is a deterministic pipeline:

    traces/incidents  ->  regression cases  ->  rubrics + fixtures  ->  gate  ->  pack

Every stage is pure with respect to its inputs. Identifiers are derived by
hashing stable fields so re-running the compiler on the same input yields
byte-identical artifacts.
"""

from __future__ import annotations

from typing import Dict, Iterable, List

from .gate import GateConfig, evaluate_gate
from .model import (
    Fixture,
    Incident,
    Pack,
    RegressionCase,
    Rubric,
    RubricCriterion,
    Trace,
    stable_id,
)

# Severity ordering used to sort and to seed default rubric weights.
SEVERITY_RANK = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}


