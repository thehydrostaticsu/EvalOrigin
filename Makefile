.PHONY: help compile report gate cases rubric fixtures inspect check go-build go-vet demo clean

PY ?= python
IN ?= examples/fixtures/incidents.json examples/fixtures/traces.jsonl
OUT ?= examples/output

help:
	@echo "EvalOrigin targets:"
	@echo "  make compile   - compile a full JSON pack to $(OUT)/pack.json"
	@echo "  make report    - render a Markdown report to $(OUT)/report.md"
	@echo "  make gate      - print the gate verdict (exit code encodes verdict)"
