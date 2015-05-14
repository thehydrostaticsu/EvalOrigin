.PHONY: help compile report gate cases rubric fixtures inspect check go-build go-vet demo clean

PY ?= python
IN ?= examples/fixtures/incidents.json examples/fixtures/traces.jsonl
OUT ?= examples/output

help:
	@echo "EvalOrigin targets:"
