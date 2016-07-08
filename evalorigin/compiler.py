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


def _case_from_trace(trace: Trace, origin: str, severity: str) -> RegressionCase:
    """Derive a single regression case from a trace.

    ``given`` is the entry input (first step input, or the trace expected/actual
    envelope). ``expect`` prefers the declared expected value; when absent it
    falls back to the last successful output before failure.
    """
    given = None
    if trace.steps:
        given = trace.steps[0].input
    if given is None:
        given = trace.expected if trace.expected is not None else trace.actual

    expect = trace.expected
    if expect is None:
        good = [s for s in trace.steps if s.status.lower() == "ok"]
        if good:
            expect = good[-1].output

    case_id = "case-" + stable_id(trace.trace_id, trace.entrypoint, origin)
    return RegressionCase(
        case_id=case_id,
        entrypoint=trace.entrypoint,
        given=given,
        expect=expect,
        origin=origin,
        severity=severity,
        steps=len(trace.steps),
    )


def compile_cases(
    traces: Iterable[Trace],
    incidents: Iterable[Incident],
) -> List[RegressionCase]:
    """Compile regression cases from raw traces and incidents.

    Failing traces and every incident become cases. Passing traces are kept
    only when tagged ``golden`` so healthy paths can be pinned intentionally.
    """
    cases: List[RegressionCase] = []

    for trace in traces:
        is_fail = trace.outcome.lower() in ("fail", "failed", "error") or trace.failing_steps
        is_golden = "golden" in {t.lower() for t in trace.tags}
        if is_fail:
