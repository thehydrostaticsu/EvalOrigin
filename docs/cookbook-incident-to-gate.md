# Cookbook: from incident to gate

```
python -m evalorigin compile examples/fixtures/incidents.json -o pack/
```

The pack holds cases, rubrics, fixtures, and a report. Wire `gate` into the
release job so the same failure cannot ship twice.
