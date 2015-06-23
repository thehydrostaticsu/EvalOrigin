<p align="center">
  <img src="docs/assets/logo.svg" alt="EvalOrigin: a trace collapsing into an evaluation gate" width="440">
</p>

# EvalOrigin

A trace-to-evaluation compiler. Feed it the execution traces and incidents your
system already produces, and it compiles them into durable evaluation assets:
regression cases, weighted rubrics, replay fixtures, and a release gate with an
exit code your CI can read. The same inputs always compile to byte-identical
output, so a pack is a stable artifact you can commit and diff.

The Python package is the reference compiler. A companion Go module under
`compiler/` reimplements the gate at parity, so the verdict can run in a Go
pipeline without a Python runtime.

## The pipeline

Every stage is a pure function of its inputs. Identifiers are content-hashed,
