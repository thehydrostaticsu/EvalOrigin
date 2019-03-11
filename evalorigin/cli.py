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
