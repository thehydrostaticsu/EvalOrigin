"""EvalOrigin: a trace-to-evaluation compiler.

EvalOrigin converts execution traces and failure incidents into durable
evaluation artifacts: regression cases, scoring rubrics, replay fixtures,
release-gate summaries, and shippable JSON/Markdown packs.

The package is dependency-free and targets Python 3.11+. The heavy scoring
kernel is mirrored by a companion Go module under ``compiler/`` for teams
that embed the gate directly in CI runners.
"""

from .model import (
    Trace,
    TraceStep,
    Incident,
    RegressionCase,
    Rubric,
    RubricCriterion,
    Fixture,
    GateSummary,
    Pack,
)
from .compiler import compile_pack, compile_cases, compile_rubric
from .gate import evaluate_gate, GateConfig

__all__ = [
    "Trace",
    "TraceStep",
    "Incident",
    "RegressionCase",
    "Rubric",
    "RubricCriterion",
    "Fixture",
    "GateSummary",
    "Pack",
    "compile_pack",
    "compile_cases",
    "compile_rubric",
    "evaluate_gate",
    "GateConfig",
]

__version__ = "1.0.2"
