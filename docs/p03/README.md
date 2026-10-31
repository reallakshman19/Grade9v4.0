# P0.3 — Native Smart Labelling R2 → QRT Physics Blueprint → WPE adapter binding

**Implementation scope:** Cross-stage *read-only* candidate binding, not a new Smart Skill, not a replacement QRT reviewer, and not an automatic Core1A/Core1B qualification. This is a continuation of master Issue #1 and the R2 revised execution plan.

## Source boundaries
- Native `smart-labelling-qrt-contract/v2` (SL1/SL2), a distinct QRT decision, original `PHYS-QRT-BLUEPRINT 0.2.0`, `PHYS-TOPIC-WPE` adapter, `core1a-source-handoff/v1`.
- The original WPE adapter expressly says `Owner-local only; never commit to a public repository`; do not paste exam text or bundled figures into this public repo.
- Original archives stay outside the branch. Version and SHA256 pins for **specific source artifacts** are recorded as provenance metadata, not owner approval.
- Candidate SL2 labels never count as QRT review, and passing native technical checks never counts as release.

## Plan
1. Record authoritative candidates and byte pins without publishing the upstream originals.
2. Implement read-only `grade9qa qrt-bind` contract checking question ID sets, SL1→SL2 legacy binding, QRT Blueprint/adapter exact version and cell, cognitive operation and five-factor demand consistency, native contract identity and optional Core1A handoff.
3. Report diagnostics as errors, HOLD or preparation-only; no subject-derived teaching claims.
4. Add synthetic fixtures/testing for mismatches, reversed operations, bad demand totals, absent QRT review and unlinked handoff.
5. Test on actual Owner candidate sources **locally**; keep independent approval as HOLD.

## Release gates
Independent source custody + QRT adjudication + qualified Physics warrants + construction binder B1–B7 + learner runtime and Owner release are not implemented in this slice. **Draft PR; no academic approval inferred.**