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
