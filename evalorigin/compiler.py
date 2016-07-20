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
            cases.append(_case_from_trace(trace, origin="trace-failure", severity="high"))
        elif is_golden:
            cases.append(_case_from_trace(trace, origin="golden-path", severity="medium"))

    for incident in incidents:
        cases.append(
            _case_from_trace(
                incident.trace,
                origin=f"incident:{incident.incident_id}",
                severity=incident.severity,
            )
        )

    # Deterministic order: severity desc, then entrypoint, then case_id.
    cases.sort(
        key=lambda c: (-SEVERITY_RANK.get(c.severity, 0), c.entrypoint, c.case_id)
    )
    # De-duplicate identical case ids while preserving order.
    seen: Dict[str, RegressionCase] = {}
    for c in cases:
        seen.setdefault(c.case_id, c)
    return list(seen.values())


def compile_rubric(entrypoint: str, cases: List[RegressionCase]) -> Rubric:
    """Build a weighted rubric for one entrypoint.

    Weights are normalised so the criteria sum to 1.0. The criteria set adapts
    to what the cases actually exercise: an output-equality check always
    exists; error-freedom and step-budget checks are added when the cases
    carry the relevant signals.
    """
    scoped = [c for c in cases if c.entrypoint == entrypoint]
    criteria: List[RubricCriterion] = [
        RubricCriterion(
            key="output_matches",
            description="Candidate output equals the pinned expectation.",
            weight=3.0,
            check="equals(expect)",
        ),
        RubricCriterion(
            key="no_error_status",
            description="No step reports an error or failed status.",
            weight=2.0,
            check="all_steps_ok",
        ),
    ]
    if any(c.steps > 0 for c in scoped):
        max_steps = max((c.steps for c in scoped), default=0)
        criteria.append(
            RubricCriterion(
                key="within_step_budget",
                description=f"Execution completes within {max_steps} recorded steps.",
                weight=1.0,
                check=f"steps<={max_steps}",
            )
        )
    if any(c.severity in ("critical", "high") for c in scoped):
        criteria.append(
            RubricCriterion(
                key="severity_guard",
                description="High/critical origin cases must pass without waivers.",
                weight=2.0,
                check="no_waiver_on_high",
            )
        )

    total = sum(c.weight for c in criteria) or 1.0
