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
