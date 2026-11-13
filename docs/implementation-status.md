# Grade9 v4.0 implementation status

**Product scope correction (2026-10-31):** Grade9 v4.0 targets **Physics, Mathematics and Chemistry**. WPE / WEP-01 is only the initial Physics pilot. Existing `schemas/v1` bundle/construction topic IDs and `qrt-bind` are Physics/WPE-specific; a **v2 candidate intake** is implemented in PR #7, while canonical multi-subject integration, Mathematics/Chemistry Blueprints, and cross-subject curriculum qualification **are not yet implemented**. See [product-scope.md](product-scope.md).

Master: [Issue #1](https://github.com/reallakshman19/Grade9v4.0/issues/1).

Stacked draft PRs: [#2](https://github.com/reallakshman19/Grade9v4.0/pull/2) → [#3](https://github.com/reallakshman19/Grade9v4.0/pull/3) → [#4](https://github.com/reallakshman19/Grade9v4.0/pull/4) → [#5](https://github.com/reallakshman19/Grade9v4.0/pull/5) → [#6](https://github.com/reallakshman19/Grade9v4.0/pull/6) → [#7](https://github.com/reallakshman19/Grade9v4.0/pull/7) → [#9](https://github.com/reallakshman19/Grade9v4.0/pull/9) → [#10](https://github.com/reallakshman19/Grade9v4.0/pull/10) → [#11](https://github.com/reallakshman19/Grade9v4.0/pull/11).

- [x] P0.0/P0.1: Grade9QA CLI, structural records, source-incomplete synthetic example
- [x] P0.2a: read-only Shared six-Core authority audit
- [x] P0.2b: complete 292-file external Shared fingerprint and original authority readbacks
- [x] P0.3: read-only native SL1/SL2 R2 to QRT Physics/WPE version and operation binding
- [x] **P0.4a: B1–B7 machine evidence engine**, separate v1 witness schema, standalone `bridge-witness`, archival `bridge-legacy`, full direct `qualify --witness` noncompensatory FAIL/HOLD propagation
- [x] Original archived D3.1 and D3.6 witness candidate status accounted for without publishing question content
- [ ] **P0.4b: independent semantic/Physics/QRT/Shared review receipts and validated native learner runtime** — HOLD
- [ ] P1: owner-qualified end-to-end WEP-01 pilot (Core1A worked reasoning, fresh Core1B reconstruction and independent Core2 question)
- [x] **P0.5a:** initial three-subject v2 candidate intake schema, subject-scoped sources/warrants/constructions, adapter/Blueprint pin validation, fail-closed `subjects-audit`, 31 synthetic/migration-isolation tests; **no native or academic approval**
- [x] **P0.5b engineering preview:** reversible/read-only v1 WEP-01→v2 candidate source/ref migration, strict input and external source-byte hashing, historical status preservation, legacy alias HOLD, native Shared subject-discovery report reconciliation; 43 new tests. [PR #9](https://github.com/reallakshman19/Grade9v4.0/pull/9).
- [ ] **P0.5b academic/native acceptance:** Shared canonical intake and subject workspace installation, verified reviewer receipts, Owner-approved old Blueprint/adapter aliases, approved Mathematics and Chemistry Blueprints/content, subject runtime; [Issue #8](https://github.com/reallakshman19/Grade9v4.0/issues/8) remains open.
- [ ] P2: full canonical v2 subject integration; Physics WEP-02–10 expansion; independent Mathematics and Chemistry subject adapter pilots (topics not yet selected)
- [ ] P3: publication and learner-facing release

No user-supplied hash, synthetic fixture, preview screenshot, candidate D3 label or CI success constitutes academic approval.

- [x] **P0.5c preflight:** direct read-only `CoreContracts.json` workspace inspection, six-Core role claims, truthful validator limitations, gate/library presence, native Shared report count reconciliation, and safe subject mappings; [draft PR #10](https://github.com/reallakshman19/Grade9v4.0/pull/10).
- [x] Local synthetic native Shared check demonstrated that **three CONTRACT_ONLY subjects can pass discovery with zero libraries**, which is NOT subject implementation or academic readiness.
- [ ] P0.5c acceptance: actual Owner-provided complete Physics/Mathematics/Chemistry subject roots, accepted native contract and library packages, approved discipline-specific Blueprints, source/proof/chemical warrants and independent governance receipts; **HOLD**.

- [x] **P1 pilot evidence triage:** original Owner-supplied WPE D3.1.1 witness/Physics review/source register/handoff/browser-hub metadata readback, plus two genuine authored WEP-01 Core1A/Core1B draft variant comparisons, 30 new synthetic regression tests; [draft PR #11](https://github.com/reallakshman19/Grade9v4.0/pull/11). No source text imported.
- [ ] **P1 academic qualification:** select independently reviewed WEP-01 Core1A/B variant; QRT construction-family operation/band decision; exact qualified Physics warrants; real first-answer learner state and independent Shared approvals. **HOLD**.
