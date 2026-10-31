# Grade9 v4.0 — WPE Academic Qualification Backbone

The candidate validator and read-only Smart Skills report adapter are being developed in [draft PR #2](https://github.com/reallakshman19/Grade9v4.0/pull/2), following [master specification #1](https://github.com/reallakshman19/Grade9v4.0/issues/1).

## Implemented in P0.0–P0.1 and early Smart Skills adaptation

- Python 3.11+ installable package and `grade9qa` command.
- Eight versioned evidence JSON Schemas.
- Local bundle loading, schema errors, type-aware references, duplicate IDs and prerequisite cycles.
- Numeric D1–D4 rubric-band consistency checks (not academic validity).
- Sample WEP-01 **synthetic candidate**, pytest suite, and Python 3.11/3.12 CI.
- The new `smart-audit` reads native Smart Labelling R2 reports without asserting qualification; native skills are **not** installed by this repository.
- Academic release and B1–B7 engines deliberately report **HOLD** until P0.2–P0.4 evidence controls are implemented.

## Run locally

```bash
python -m pip install -e ".[dev]"
grade9qa validate --bundle examples/wpe-n01-candidate/bundle.json --out out/validation.json
grade9qa bridge --bundle examples/wpe-n01-candidate/bundle.json --out out/bridge.json
grade9qa qualify --bundle examples/wpe-n01-candidate/bundle.json --out out/qualification.json
grade9qa report --bundle examples/wpe-n01-candidate/bundle.json --json out/report.json --md out/report.md
grade9qa smart-audit --report path/to/native-r2-report.json --out out/smart-audit.json
python -m pytest -q
```

See [readme.txt](readme.txt) for **“1. Correct workflow placement”** and [Smart Skills integration](docs/smart-skills-integration.md) for the R2 candidate adoption rules.

The sample has mechanically valid candidate records. `qualify` intentionally returns exit code **3 (HOLD)**. This is not a software defect. No source scan, official paper, answer key or academically approved lesson is provided.

## P0.2b complete inventory and native authority report adapter (stacked PR #4)

The 292-file `Shared.zip` is **external** and has not been republished in this public repo. The read-only tools create a deterministic per-file SHA-256 inventory and summarize the original Shared auditors' **native reports**. They **never grant academic approval**.

```bash
grade9qa shared-manifest --archive /path/to/Shared.zip --shared-root /path/to/Shared --out out/shared-full-manifest.json

# The following inputs must be outputs of the original Shared auditors, not reports invented by Grade9QA:
grade9qa shared-authorities --core core-authority.json --review review-audit.json --release release-audit.json --out out/native-authorities.json
```

Exit 3 means the evidence is mechanically usable but platform/academic qualification remains **HOLD**; exit 1 means contradiction/invalid evidence; exit 2 means unreadable inputs. A native audit with **zero receipts** cannot establish a reviewed record or authorized learner release. See [P0.2b instructions](docs/p02b/README.md) and [draft PR #4](https://github.com/reallakshman19/Grade9v4.0/pull/4). 

## Shared platform audit (stacked PR #3)

The existing Shared platform is **not yet copied into this public repository**. Its 292-file owner-supplied archive is summarized by 16 selected immutable source fingerprints in `docs/shared-baseline-pins.json`.

```bash
grade9qa shared-audit --shared-root /path/to/extracted/Shared --archive /path/to/Shared.zip --out out/shared-audit.json
```

This reads the external archive/snapshot, checks selected source fingerprints, six-Core authority invariants, cognitive operation mapping and Grade 9 Physics scope. It never executes upstream code or grants approval. Exit **3** means mechanical audit completed but independent integration/academic review remains **HOLD**.

See [Shared compatibility audit](docs/shared-compatibility-audit.md) and the [stacked PR #3](https://github.com/reallakshman19/Grade9v4.0/pull/3). The parent PR #2 must merge first.

## Layout

- `schemas/v1/`: source, warrant, construction, lesson, assessment, approval, bundle, report.
- `src/grade9qa/`: CLI and partial validators; academic gates unimplemented and blocked.
- `examples/wpe-n01-candidate/`: entirely synthetic test evidence.
- `tests/`: automatic regressions.
- `docs/`: architecture, schema rules, import policy and independent reviewer checklist.

## Non-negotiable boundaries

Hash verification is not Physics approval; a shared formula is not teaching-to-reconstruction equivalence; D3/D4 demand is not a school grade; a green build is not permission for student release. Do not invent review receipts, exam authenticity or D1/D2 standards. Source archives remain outside this public repo pending proper permission and custody.

See [AGENTS.md](AGENTS.md) for coding-agent instructions and [implementation status](docs/implementation-status.md) for open phases.
