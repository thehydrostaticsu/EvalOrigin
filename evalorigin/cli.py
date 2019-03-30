"""Command-line interface for EvalOrigin.

Commands
--------
``compile``  Compile traces/incidents into a JSON pack.
``cases``    Emit only the regression cases as JSON.
``rubric``   Emit rubrics as JSON (optionally scoped to one entrypoint).
``fixtures`` Emit replay fixtures as JSON.
``gate``     Compile and print the gate verdict; exit code encodes the verdict.
``report``   Render a Markdown release report.
``inspect``  Summarize inputs without compiling a full pack.

Exit codes for ``gate``: 0 = pass, 10 = warn, 20 = block.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .compiler import compile_pack
from .gate import GateConfig
from .loader import dumps_canonical, load_sources
from .report import render_pack

_GATE_EXIT = {"pass": 0, "warn": 10, "block": 20}


def _build_gate_config(args: argparse.Namespace) -> GateConfig:
    block_sevs = tuple(s.strip().lower() for s in args.block_severities.split(",") if s.strip())
    return GateConfig(
        block_severities=block_sevs or ("critical",),
        warn_threshold=args.warn_threshold,
        block_threshold=args.block_threshold,
    )


def _write(text: str, out: Optional[str]) -> None:
    if out and out != "-":
        import os
        parent = os.path.dirname(out)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text if text.endswith("\n") else text + "\n")
    else:
        sys.stdout.write(text if text.endswith("\n") else text + "\n")


def _add_common(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("inputs", nargs="+", help="JSON/JSONL trace or incident files")
    sub.add_argument("-o", "--out", default="-", help="output path (default stdout)")
    sub.add_argument("--name", default="pack", help="logical pack name for id derivation")


def _add_gate_opts(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("--block-severities", default="critical",
                     help="comma list of severities that force a block verdict")
    sub.add_argument("--warn-threshold", type=float, default=0.35)
    sub.add_argument("--block-threshold", type=float, default=0.65)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evalorigin",
        description="Trace-to-evaluation compiler: turn failures into gates.",
    )
    parser.add_argument("--version", action="version", version=f"evalorigin {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_compile = sub.add_parser("compile", help="compile a full JSON pack")
    _add_common(p_compile)
    _add_gate_opts(p_compile)

    p_cases = sub.add_parser("cases", help="emit regression cases as JSON")
    _add_common(p_cases)

    p_rubric = sub.add_parser("rubric", help="emit rubrics as JSON")
    _add_common(p_rubric)
    p_rubric.add_argument("--entrypoint", default=None, help="scope to one entrypoint")

    p_fixtures = sub.add_parser("fixtures", help="emit replay fixtures as JSON")
    _add_common(p_fixtures)

    p_gate = sub.add_parser("gate", help="print gate verdict (exit code encodes verdict)")
    _add_common(p_gate)
    _add_gate_opts(p_gate)

    p_report = sub.add_parser("report", help="render a Markdown release report")
    _add_common(p_report)
    _add_gate_opts(p_report)

    p_inspect = sub.add_parser("inspect", help="summarize inputs without compiling")
    p_inspect.add_argument("inputs", nargs="+", help="JSON/JSONL trace or incident files")

    return parser


def _cmd_inspect(inputs: List[str]) -> int:
    traces, incidents = load_sources(inputs)
    failing = sum(1 for t in traces if t.outcome.lower() in ("fail", "failed", "error") or t.failing_steps)
    summary = {
        "sources": list(inputs),
        "traces": len(traces),
        "failing_traces": failing,
        "incidents": len(incidents),
        "entrypoints": sorted({t.entrypoint for t in traces} | {i.entrypoint for i in incidents}),
