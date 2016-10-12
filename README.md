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
so re-running on the same traces reproduces the same pack.

<p align="center">
  <img src="docs/assets/pipeline.svg" alt="Traces and incidents compile into regression cases, then rubrics and fixtures, then a release gate that emits pass, warn, or block" width="720">
</p>

```
traces + incidents  ->  regression cases  ->  rubrics + fixtures  ->  gate  ->  pack
```

A failing trace becomes a regression case. Every incident becomes one too. A
passing trace is pinned only when it carries a `golden` tag, so healthy paths
enter the pack on purpose rather than by accident. Cases are sorted by severity,
then entrypoint, then id, and de-duplicated by content hash.

## What an operator does

- Compile a full pack to JSON: `python -m evalorigin compile <inputs> --name demo -o pack.json`
- Print the release verdict and let the exit code gate CI: `python -m evalorigin gate <inputs>`
- Render a Markdown release report: `python -m evalorigin report <inputs> -o report.md`
- Emit a single artifact type: `cases`, `rubric` (optionally `--entrypoint X`), or `fixtures`
- Summarize inputs before committing to a compile: `python -m evalorigin inspect <inputs>`

Inputs are `.json` (a single object, an array, or a `{"traces": [...], "incidents": [...]}` wrapper)
or `.jsonl` with one record per line. A record is read as an incident when it
carries an `incident_id`, or a `severity` paired with a `title` or `trace`;
otherwise it is parsed as a bare trace. The bundled fixtures live in
`examples/fixtures/` (`traces.jsonl`, `incidents.json`) and a full set of
compiled outputs sits in `examples/output/`.

## The gate

The verdict is `pass`, `warn`, or `block`, driven by an explainable score rather
than an opaque heuristic, so the reasons print alongside it. Any case at a
blocking severity forces a `block`. Otherwise a weighted risk score in `[0, 1]`
is compared against two thresholds:

| Verdict | Condition | Exit code |
|---------|-----------|-----------|
| `pass`  | score below the warn threshold, no blocking cases | 0 |
| `warn`  | score at or above the warn threshold (default 0.35) | 10 |
| `block` | a blocking-severity case, or score at or above the block threshold (default 0.65) | 20 |

Blocking severities and thresholds are configurable:

```bash
python -m evalorigin gate examples/fixtures/incidents.json examples/fixtures/traces.jsonl \
  --block-severities critical,high --warn-threshold 0.4 --block-threshold 0.7
```

## Rubrics

Each entrypoint gets a weighted rubric whose criteria adapt to what its cases
actually exercise. An output-equality check and an error-freedom check always
exist. A step-budget check is added when cases record steps, and a severity
guard is added when any case is `high` or `critical`. Weights are normalised so
the criteria sum to `1.0`.

## Run it

Requires Python 3.11 or newer. The package has no dependencies.

```bash
python -m evalorigin compile examples/fixtures/incidents.json examples/fixtures/traces.jsonl \
  --name demo -o examples/output/pack.json

python -m evalorigin report examples/fixtures/incidents.json examples/fixtures/traces.jsonl \
  --name demo -o examples/output/report.md
```

The `Makefile` wraps the common flows: `make compile`, `make report`, `make gate`,
`make cases`, `make rubric`, `make fixtures`, `make inspect`, and `make demo` to
regenerate every artifact under `examples/output/`. `make check` compiles the
Python package and builds and vets the Go module.

### Go gate at parity

```bash
cd compiler
go build ./...
```

The `compiler/` module carries the gate logic and an `evalgate` command that
mirrors the Python verdict, so the release decision can run inside a Go build.

## Layout

```
evalorigin/
├─ evalorigin/            Python package (stdlib only)
│  ├─ model.py            dataclasses with deterministic to_dict
│  ├─ loader.py           JSON / JSONL loaders, canonical serialization
│  ├─ compiler.py         cases -> rubrics + fixtures -> gate -> pack
│  ├─ gate.py             risk score and pass / warn / block verdict
│  ├─ report.py           deterministic Markdown rendering
│  └─ cli.py              argparse CLI and gate exit codes
├─ compiler/              Go module: gate at parity + evalgate command
├─ examples/              fixtures/ inputs and output/ compiled artifacts
├─ docs/assets/           logo.svg and pipeline.svg
└─ pyproject.toml  Makefile  ROADMAP.md  CHANGELOG.md  LICENSE
```

## Determinism

Serialized output is byte-stable across runs and machines. Collections are
pre-sorted, keys are emitted in a fixed order, and no timestamps or random ids
leak into a pack unless the input supplies them. That is what makes a pack safe
to commit and diff: a changed pack means the traces changed, not the compiler.

## License

Apache-2.0. See [LICENSE](LICENSE). Milestones that are done live in
[ROADMAP.md](ROADMAP.md); the change history is in [CHANGELOG.md](CHANGELOG.md).

<!-- draft note 50 -->
