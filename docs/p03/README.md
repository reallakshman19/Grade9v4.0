# P0.3 — Native SL1/SL2 R2 → QRT → Physics/WPE binding

**Engineering status:** read-only candidate binding implemented and tested. **Academic status:** HOLD.

This phase does NOT install or reimplement native Smart Skills, overwrite the common Physics Blueprint, issue independent QRT decisions, rewrite source-to-Core1A dossiers, publish examination question text or qualify B1–B7.

## External source versions

- `SMART_LABELLING_QRT_HARDENING_R2_CANDIDATE(2).zip`: native SL1/SL2 v2.0.0-candidate, input v1 overlays and `smart-labelling-qrt-contract/v2`.
- `QRT(4).zip`: `PHYS-QRT-BLUEPRINT` v0.2.0, `DRAFT_OWNER_REVIEW`; seven operations and 14 D3/D4 cells.
- `QRT(4).zip` `builds/PHY-WPE-D3.7/topic-adapter.work-power-energy.json`: `PHYS-TOPIC-WPE` v0.1.x draft, target `PHYS-QRT-BLUEPRINT 0.2.0`.
- `WPE_CONSTRUCTION_HANDOFF_SKILL_R1_CANDIDATE.zip`: source-to-Core1A preparation schema `core1a-source-handoff/v1`, example `PREP-WPE-N01-WORK-DIRECTION-R1`, status CANDIDATE and zero reviewed question links.
- Exact original archive and selected artifact SHA-256 pins are in `docs/p03/upstream-artifact-pins.json`. These hashes are from Owner-supplied files and are **not independent signatures**.

Original WPE QRT adapter files contain exam question text and explicitly prohibit public publication (`privacy: Contains exam question text. Owner-local only; never commit to a public repository`). Only metadata, code and synthetic tests are committed.

## CLI: inspect candidate inputs already created by native tools

```bash
grade9qa qrt-bind \
  --sl1 /local/sl1.json \
  --sl2 /local/sl2.json \
  --contract /local/native-r2-sidecar.json \
  --blueprint /local/physics-blueprint.D3-D4.json \
  --adapter /local/topic-adapter.work-power-energy.json \
  --handoff /local/core1a-source-handoff.json \
  --native-sl1-report /local/native-sl1-report.json \
  --native-sl2-report /local/native-sl2-report.json \
  --out out/qrt-wpe-bind.json
```

The `--handoff`, `--native-sl1-report` and `--native-sl2-report` inputs are optional, but missing native evidence remains HOLD. The sidecar MUST be generated and checked by native R2 preparation/checkers; the v4 adapter checks only **metadata consistency** and should never be used in place of the native security/semantic checks.

- Exit `1`: contradictory/malformed bindings.
- Exit `2`: unreadable input file/IO.
- Exit `3`: consistent candidate or incomplete review -> HOLD. **No `0` success/approval path.**

## Mechanical checks implemented

1. SL1/SL2 original overlay schema IDs and R2 v2 sidecar schema ID.
2. Exactly matched SL1/SL2/sidecar question ID sets, no duplicate question IDs.
3. Legacy item-digest equality without reinterpretation or rewriting of native digest algorithms.
4. Sidecar presence of native per-record payload digest pins, never self-signed approval.
5. Proposed cognitive operation from seven canonical IDs and its five 0–2 rubric factors/total/band.
6. SL2 `QRT-{OP}-{D3/D4}` candidate cell maps to common Physics Blueprint `D3.{column}`/`D4.{column}`, and to a matching topic adapter cell.
7. Blueprint version, Blueprint/adapter binding and draft/approval state. A D1/D2 record remains `SPEC_PENDING`.
8. Source-to-Core1A preparation schema, decisive move and zero-join distinction.
9. Native checker report presence/schema/selected-gate status, **without** claiming JSON is trusted executable evidence.
10. No original stem, figure, private learner response or review content copied into the output; only IDs, cell mapping, byte fingerprints and diagnostic codes.

## Local source-shape readback, 2026-10-31

A local **structural smoke** used the native synthetic `tests/seeds/sl1.json` and `sl2.json` from the Owner-supplied R2 ZIP, original D3.7 Blueprint/adapter files from `QRT(4).zip`, and example source-to-Core1A handoff. The test sidecar was assembled **only for structural inspection**, not prepared/validated as a qualified native R2 contract.

- One synthetic source question, proposed `JUSTIFY` / `D3` with factor total 6.
- Corresponds to common Blueprint `D3.7`; WPE D3.7 adapter cell exists.
- Result: `mechanical_status:HOLD`, `qualification_status:HOLD`, `core1a_preparation:SOURCE_PREPARATION_ONLY`.
- Blockers: missing independent QRT decision; no native checker report for this bundle; draft Blueprint/adapter; Core1A handoff not approved and has zero question links; source-exam custody is not independently verified.

This is NOT a complete genuine question adjudication or a physics qualification. The structural alignment is informative but cannot prove the scientific sufficiency of any construction.

## P0.3 approval gates still missing

- [ ] Independently trusted Owner baseline/redistribution permission for Shared, R2, QRT and WPE source materials.
- [ ] Real native R2 checked sidecar plus trusted checker artifact and exact source/key/figure custody.
- [ ] Independent first assessment and QRT source-role decision for each real question; **SL2 PROPOSED is not QRT approved**.
- [ ] Qualified Physics warrants and independently reviewed `PHYS-QRT-BLUEPRINT`/WPE topic adapter.
- [ ] Actual bound construction with Core1A/Core1B non-exam task identity separation and B1–B7 reviewed passage evidence.
- [ ] Existing Shared governance/academic authorizations and learner runtime checks.

**No academic approval or learner release is inferred from matching IDs, a six-point D3 score, local hashes, or a green CI run.**
