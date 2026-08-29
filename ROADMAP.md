# Roadmap

EvalOrigin turns failures into durable evaluation assets. The milestones below
track the shape of the compiler and its companion runner.

## Delivered

- [x] Deterministic trace/incident compile pipeline with content-hashed ids
- [x] Release-gate scoring model with pass/warn/block verdicts and exit codes
- [x] JSON and Markdown pack outputs, including rubric and fixture generation
- [x] Go companion `compiler/` module and `evalgate` command at gate parity

## Exploring

- Multi-pack diffing to surface newly introduced or resolved regressions.
- Rubric templates keyed by entrypoint family for shared scoring conventions.
- Trace redaction profiles for sensitive payload fields at load time.
- HTML report theme built from the amber/charcoal identity.
