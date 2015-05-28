.PHONY: help compile report gate cases rubric fixtures inspect check go-build go-vet demo clean

PY ?= python
IN ?= examples/fixtures/incidents.json examples/fixtures/traces.jsonl
OUT ?= examples/output

help:
	@echo "EvalOrigin targets:"
	@echo "  make compile   - compile a full JSON pack to $(OUT)/pack.json"
	@echo "  make report    - render a Markdown report to $(OUT)/report.md"
	@echo "  make gate      - print the gate verdict (exit code encodes verdict)"
	@echo "  make cases     - emit regression cases"
	@echo "  make rubric    - emit rubrics"
	@echo "  make fixtures  - emit replay fixtures"
	@echo "  make inspect   - summarize inputs"
	@echo "  make demo      - regenerate every artifact under $(OUT)"
	@echo "  make check     - compile Python and build/vet the Go module"

compile:
	$(PY) -m EvalOrigin compile $(IN) --name demo -o $(OUT)/pack.json

