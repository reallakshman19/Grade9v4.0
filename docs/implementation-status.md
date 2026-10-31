# Grade9 v4.0 implementation status

**Product scope correction (2026-10-31):** Grade9 v4.0 targets **Physics, Mathematics and Chemistry**. WPE / WEP-01 is only the initial Physics pilot. Existing `schemas/v1` bundle/construction topic IDs and `qrt-bind` are Physics/WPE-specific; subject-neutral contracts, Mathematics and Chemistry Blueprints, and cross-subject curriculum qualification **are not yet implemented**. See [product-scope.md](product-scope.md).

Master: [Issue #1](https://github.com/reallakshman19/Grade9v4.0/issues/1).

Stacked draft PRs: [#2](https://github.com/reallakshman19/Grade9v4.0/pull/2) → [#3](https://github.com/reallakshman19/Grade9v4.0/pull/3) → [#4](https://github.com/reallakshman19/Grade9v4.0/pull/4) → [#5](https://github.com/reallakshman19/Grade9v4.0/pull/5) → [#6](https://github.com/reallakshman19/Grade9v4.0/pull/6) → [#7](https://github.com/reallakshman19/Grade9v4.0/pull/7).

- [x] P0.0/P0.1: Grade9QA CLI, structural records, source-incomplete synthetic example
- [x] P0.2a: read-only Shared six-Core authority audit
- [x] P0.2b: complete 292-file external Shared fingerprint and original authority readbacks
- [x] P0.3: read-only native SL1/SL2 R2 to QRT Physics/WPE version and operation binding
- [x] **P0.4a: B1–B7 machine evidence engine**, separate v1 witness schema, standalone `bridge-witness`, archival `bridge-legacy`, full direct `qualify --witness` noncompensatory FAIL/HOLD propagation
- [x] Original archived D3.1 and D3.6 witness candidate status accounted for without publishing question content
- [ ] **P0.4b: independent semantic/Physics/QRT/Shared review receipts and validated native learner runtime** — HOLD
- [ ] P1: owner-qualified end-to-end WEP-01 pilot (Core1A worked reasoning, fresh Core1B reconstruction and independent Core2 question)
- [x] **P0.5a:** initial three-subject v2 candidate intake schema, subject-scoped sources/warrants/constructions, adapter/Blueprint pin validation, fail-closed `subjects-audit`, 31 synthetic/migration-isolation tests; **no native or academic approval**
- [ ] **P0.5b:** canonical v1→v2 subject migration, native Shared subject dispatch, independent Mathematics/Chemistry Blueprints and selected topics
- [ ] P2: subject-neutral v2 contracts; Physics WEP-02–10 expansion; independent Mathematics and Chemistry subject adapter pilots (topics not yet selected)
- [ ] P3: publication and learner-facing release

No user-supplied hash, synthetic fixture, preview screenshot, candidate D3 label or CI success constitutes academic approval.
