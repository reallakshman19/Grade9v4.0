# Grade9 v4.0 — WPE Academic Qualification Backbone

The first implementation is underway in [draft PR #2](https://github.com/reallakshman19/Grade9v4.0/pull/2), following [master specification #1](https://github.com/reallakshman19/Grade9v4.0/issues/1).

## Implemented in P0.0–P0.1

- Python 3.11+ installable package and `grade9qa` command.
- Eight versioned evidence JSON Schemas.
- Local bundle loading, schema errors, type-aware references, duplicate IDs and prerequisite cycles.
- Numeric D1–D4 rubric-band consistency checks (not academic validity).
- Sample WEP-01 **synthetic candidate**, pytest suite, and Python 3.11/3.12 CI.
- Academic release and B1–B7 engines deliberately report **HOLD** until P0.2–P0.4 evidence controls are implemented.

## Run locally

```bash
python -m pip install -e ".[dev]"
grade9qa validate --bundle examples/wpe-n01-candidate/bundle.json --out out/validation.json
grade9qa bridge --bundle examples/wpe-n01-candidate/bundle.json --out out/bridge.json
grade9qa qualify --bundle examples/wpe-n01-candidate/bundle.json --out out/qualification.json
grade9qa report --bundle examples/wpe-n01-candidate/bundle.json --json out/report.json --md out/report.md
python -m pytest -q
```

The sample has mechanically valid candidate records. `qualify` intentionally returns exit code **3 (HOLD)**. This is not a software defect. No source scan, official paper, answer key or academically approved lesson is provided.

## Layout

- `schemas/v1/`: source, warrant, construction, lesson, assessment, approval, bundle, report.
- `src/grade9qa/`: CLI and partial validators; academic gates unimplemented and blocked.
- `examples/wpe-n01-candidate/`: entirely synthetic test evidence.
- `tests/`: automatic regressions.
- `docs/`: architecture, schema rules, import policy and independent reviewer checklist.

## Non-negotiable boundaries

Hash verification is not Physics approval; a shared formula is not teaching-to-reconstruction equivalence; D3/D4 demand is not a school grade; a green build is not permission for student release. Do not invent review receipts, exam authenticity or D1/D2 standards. Source archives remain outside this public repo pending proper permission and custody.

See [AGENTS.md](AGENTS.md) for coding-agent instructions and [implementation status](docs/implementation-status.md) for open phases.
