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
