"""Input loaders for traces and incidents.

Supported formats:

* ``.json``  - a single object or an array of objects.
* ``.jsonl`` - one JSON object per line (blank lines ignored).

A record is routed to an :class:`Incident` when it carries an ``incident_id``
or a ``severity``/``title`` pair; otherwise it is parsed as a bare
:class:`Trace`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Tuple

from .model import Incident, Trace


def _iter_records(path: Path) -> Iterable[dict]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
        return
    data = json.loads(text)
    if isinstance(data, list):
        yield from data
    elif isinstance(data, dict):
        # Allow a wrapper object with "traces"/"incidents" arrays.
        if "traces" in data or "incidents" in data:
