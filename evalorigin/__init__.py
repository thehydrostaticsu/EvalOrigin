"""EvalOrigin: a trace-to-evaluation compiler.

EvalOrigin converts execution traces and failure incidents into durable
evaluation artifacts: regression cases, scoring rubrics, replay fixtures,
release-gate summaries, and shippable JSON/Markdown packs.

The package is dependency-free and targets Python 3.11+. The heavy scoring
kernel is mirrored by a companion Go module under ``compiler/`` for teams
that embed the gate directly in CI runners.
"""
