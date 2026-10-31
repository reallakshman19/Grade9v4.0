# P0 Core2 — preserve existing HTML; reconcile 79-source candidates; resolve Physics QRT cells

**Status:** engineering checks implemented in [draft PR #12](https://github.com/reallakshman19/Grade9v4.0/pull/12), stacked on draft PR #11. **No new native Core2 HTML, textbooks, examination questions, or source-to-Core1A material authored. No academic admission or release.**

This review slice is **Physics/WPE only** in the planned Physics, Mathematics and Chemistry platform. Never reuse its Physics force/work-sign conventions in Mathematics or Chemistry.

## What already exists (do not reproduce)

- Source inventory report: **79 claimed exam source records, 78 claimed distinct exam identities**. Alias `EX-M4` ↔ `JEE-2026-04-05-S2-Q28` belongs to one counting home. The complete original Owner 79-row disposition ledger is **not supplied**, so its 79→78 underlying records cannot be independently reconstructed in this branch.
- Existing private review queues: **79 positions** across four lots (20/20/20/19). **63 identifiable source leads**, **16 unspecified positions that are NOT source records**, split 14 conditional primary, 6 secondary-only, 43 unplaced.
- Source review target: **21 places = 14 conditional candidates + 7 vacant** (three RETRIEVE, three EXPLAIN, one JUSTIFY), **zero independently admitted**.
- Previously rendered native Core2: **9 cards, 8 private textbook candidates + 1 synthetic control**, produced by the existing **Shared `render_core/2`**; these are not proven identical to any of the 79 exam-source records. Existing receipt is `draft:true`, `held_to:REFERENCE`, digest `a13a70605acf789d`, 10 representation/figure gaps. Do not subtract 9 from 79. No third-party source/stem imported into this PR.
- Existing source-to-Core1A handoff, two golden fixture candidates, existing QRT Blueprint and WPE topic adapters remain Owner-local and are not replaced. A native `render-receipt.json` does not prove academic authority.

## Actual native QRT mismatch: read before assigning more authoring

The original `QRT(4).zip` contains:

| Original Owner member | Identity/version | SHA-256 | Native coverage |
|---|---|---|---|
| `physics-blueprint.D3-D4.json` | `PHYS-QRT-BLUEPRINT 0.2.0` | `e6030a5933a803ddc39708414e6831c89c9565def78c09c99f58f95052c2b45f` | 14 D3/D4 QRT cells |
| `topic-adapter.work-power-energy.json` | `PHYS-TOPIC-WPE 0.1.0` | `899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b` | Only `D3.1` RETRIEVE cell; `DRAFT_OWNER_REVIEW` |
| `subtiles/adapter/wpe.v0.2.2.json` | `PHYS-TOPIC-WPE 0.2.2` | `5a7985ba9cd004259115c0a53f986401838af02df730f3e05e47ac9eae80a4ff` | `D3.1.1–D3.1.3`; targets Blueprint `0.2.1`, NOT `0.2.0` |

The 14 conditional leads occupy APPLY D3, MODEL D3, REPRESENT D3, SYNTHESIZE D3, JUSTIFY D3 and JUSTIFY D4. None is on `D3.1`. There is **no existing pinned current-adapter cell** for any of the 14 proposed placements under the `0.1.0` / `0.2.0` source pair. This is an **adapter coverage and Owner-selection gap**, not a verdict that the questions are invalid.

**Owner authority must choose one exact byte-pinned candidate and authorize any compatible extension. Do not silently combine the six available candidates/five distinct hashes, change common Blueprint text, or claim a 0.2.1 subtile adapter matches 0.2.0.** Lack of D1/D2 Blueprint cells is a HOLD, not permission to inflate an exam question's difficulty.

## New read-only commands

```bash
# Uses the ACTUAL existing Owner-local metadata files: no question text printed.
grade9qa core2-inventory-audit \
  --lots '/local/WPE_CORE2_FOUR_LOTS_20261031/four-lot-register.json' \
  --selections '/local/WPE_CORE2_FOUR_LOTS_20261031/CORE2_21_SELECTION_PLACES.csv' \
  --native '/local/WPE_CORE2_EXISTING_RENDER_AUDIT_20261031.json' \
  --out out/core2-inventory-audit.json

# First extract the exact original QRT members locally (do not add them to public Git).
# No --selected-adapter-sha256 until Owner selection and independent identity review.
grade9qa core2-cell-audit \
  --blueprint '/local/qrt/physics-blueprint.D3-D4.json' \
  --adapter '/local/qrt/topic-adapter.work-power-energy.json' \
  --entries examples/core2-p0/selection-14-hold.json \
  --out out/core2-cell-audit.json
```

The second command expects **real reviewed entry metadata**: source ID, independently supported operation/band, WEP topic family and capability references. The example entries deliberately have `topic_family:null` and empty capability refs, because the existing review return has not adjudicated those facts. Neither command infers correctness from the name alone. Matching hypothetical refs can establish **structural candidate compatibility only**, never signed review or academic approval.

The resolver checks 14 Blueprint cell templates, WPE-specific discipline, Blueprint/adapter version pin, Owner-selected candidate hash, present adapter cell, WEP family foreign keys and candidate capability refs. It rejects or holds wrong family/capability, unrelated subject, unselected adapter, missing/unsupported D1/D2 cell, native subtile family joins absent from v0.2.x source, and duplicate candidate IDs. **Both commands always retain academic HOLD, never produce a canonical bank/manifest or native render, and do not update existing source records.**

## Required next actions (real blockers)

1. **Owner + QRT:** identify the exact candidate adapter SHA and whether to extend its WPE cells; separately review any common Physics Blueprint version gap. This requires independent choice, not code promotion.
2. **Source custodian:** supply original 79-row disposition register and authenticated original paper/key/figure version evidence. The 16 placeholders are NOT known missing questions.
3. **Independent academic reviewers:** sealed first solve, SL1/SL2 and QRT, Physics warrants, exact WEP family/capability for the conditional 14, and disposition on all seven vacancies. Negative cases M62/M73/M79/M81/M101 and figure holds M56/M61/M69 require special attention.
4. **Native authoring:** once **one authentic source question is independently admitted**, use the already-existing Shared `bank.json`, `records.json`, `manifest.json`, native `render_core/2` and version pins, not a new standalone HTML approach.
5. **Runtime QA:** close the current 10 render-receipt gaps and enforce **durable first-answer persistence before any solution materialization**. Client-only disclosure is not cryptographic secrecy. Check figure alt/print/search/offline leakage.
6. **Owner/Shared academic governance:** independent signed or authenticated acceptance and release receipts. An engineering PASS is not sufficient.

Test coverage in `tests/test_core2_p0.py` includes source/lot mutation, fake vacant sources, duplicate exam IDs, wrong WEP family, wrong capability ref, alternate adapter version, forged native acceptance, D1/D2 rejection and source privacy.

**No academic approval inferred from software validation. No public examination stems, figures, option content or worked answers committed.**
