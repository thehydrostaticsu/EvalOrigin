"""Deterministic Markdown report rendering for compiled packs.

The report is the human-facing companion to the JSON pack. It is fully
derived from the pack, so identical packs render identical Markdown.
"""

from __future__ import annotations

from typing import List

from .model import Pack

_VERDICT_BADGE = {
    "pass": "PASS",
    "warn": "WARN",
    "block": "BLOCK",
}


def _table(headers: List[str], rows: List[List[str]]) -> str:
    line = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join([line, sep, *body])


def _fmt(value: object, width: int = 48) -> str:
    text = "" if value is None else str(value)
    text = text.replace("|", "\\|").replace("\n", " ")
    if len(text) > width:
        text = text[: width - 1] + "\u2026"
    return text or "\u2014"


def render_pack(pack: Pack) -> str:
    """Render a compiled pack to a Markdown release report."""
    gate = pack.gate
    lines: List[str] = []

    lines.append(f"# EvalOrigin Report - `{pack.pack_id}`")
    lines.append("")
    lines.append(f"**Gate verdict:** {_VERDICT_BADGE.get(gate.verdict, gate.verdict.upper())}")
    lines.append("")
    lines.append(f"- Risk score: `{gate.score:.2f}`")
    lines.append(f"- Total cases: `{gate.total_cases}`")
    lines.append(f"- Blocking cases: `{gate.blocking_cases}`")
    lines.append(f"- Entrypoints: {', '.join('`' + e + '`' for e in pack.entrypoints) or '_none_'}")
    lines.append("")
    lines.append("## Gate reasons")
    lines.append("")
    for reason in gate.reasons:
        lines.append(f"- {reason}")
    lines.append("")

    lines.append("## Severity distribution")
    lines.append("")
    if gate.by_severity:
        rows = [[sev, str(count)] for sev, count in sorted(gate.by_severity.items())]
        lines.append(_table(["Severity", "Cases"], rows))
    else:
        lines.append("_No cases compiled._")
    lines.append("")

    lines.append("## Regression cases")
    lines.append("")
    if pack.cases:
        rows = [
            [
                _fmt(c.case_id, 20),
                _fmt(c.entrypoint, 24),
                _fmt(c.severity, 10),
                _fmt(c.origin, 24),
                _fmt(c.given),
                _fmt(c.expect),
            ]
            for c in pack.cases
        ]
        lines.append(
            _table(
                ["Case", "Entrypoint", "Severity", "Origin", "Given", "Expect"],
                rows,
            )
        )
    else:
        lines.append("_No cases compiled._")
    lines.append("")

    lines.append("## Rubrics")
    lines.append("")
    for rubric in pack.rubrics:
        lines.append(f"### `{rubric.entrypoint}` - {rubric.rubric_id}")
        lines.append("")
        rows = [
            [c.key, f"{c.weight:.2f}", c.check, _fmt(c.description, 60)]
            for c in rubric.criteria
        ]
        lines.append(_table(["Criterion", "Weight", "Check", "Description"], rows))
        lines.append("")

    lines.append("## Replay fixtures")
    lines.append("")
    if pack.fixtures:
        rows = [
            [_fmt(f.fixture_id, 20), _fmt(f.case_id, 20), _fmt(f.entrypoint, 24)]
            for f in pack.fixtures
        ]
        lines.append(_table(["Fixture", "Case", "Entrypoint"], rows))
    else:
        lines.append("_No fixtures compiled._")
    lines.append("")

    return "\n".join(lines) + "\n"
