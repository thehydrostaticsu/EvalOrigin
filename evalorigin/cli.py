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

