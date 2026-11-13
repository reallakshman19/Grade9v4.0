# CORE2 local read-only audit — 2026-10-30

**Status:** HOLD. Unappointed diagnostic, **not** an Owner-approved independent academic assessment. No source edits, public uploads or learner release.

Start with `03_ARCHITECTURE_AND_FIX_PLAN.md` for direct answers to the skill/blueprint/golden questions, then `04_QUESTION_BY_QUESTION_VERDICTS.md` for 78 individual identities.

- `01_NEUTRAL_ONLY_PRECOMPARISON.json`: first neutral-packet assessment saved **before opening author scores, solutions, operations and dispute conclusions**. 38 provisional scores, 40 non-scored/HOLD; SHA-256: `9e46ae6edf545fbc5eac61c36ae668f7a870408ff5dc81169f5dc0f88855b0f6`. The accompanying `.sha256` records its hash. Not signed by an appointed reviewer.
- `02_POST_EXPOSURE_RECONCILIATION.json`: all 78 comparison records, author proposals, owner selected slots, exact local source/figure/paper/key dependency references and hash cross-checks. Retains the initial result unchanged.
- `02B_POST_EXPOSURE_SUPPLEMENT_NOT_BLIND.json`: 9 extra post-exposure assessments, explicitly **NOT blind** and separate from first pass.
- `03_ARCHITECTURE_AND_FIX_PLAN.md`: technical root causes, exact code locations, proposed architecture, HOLDs, replacements and acceptance tests.
- `04_QUESTION_BY_QUESTION_VERDICTS.md`: one row per exact identity with scores/solution or explicit missing figure/source HOLD.
- `05_CHECK_CORE2_CONTRACT.py`: read-only reproducible static gate checker for the four ZIP inputs.
- `06_REPRODUCIBLE_GATE_RESULTS.json`: result of running the static checker. Current status: **7 PASS, 8 HOLD**. A nonzero exit is expected while HOLDs remain.
- `07_GOLDEN_FIELD_CROSSWALK.json`: machine-readable source-to-golden field map, fail-closed transformations and required acceptance tests.

To reproduce gate checks locally with Python 3:

```bash
python 05_CHECK_CORE2_CONTRACT.py \
  --owner "WPE_CORE2_R2_FULL_OWNER_REVIEW_PACKAGE(1).zip" \
  --organized "WPE_D3_Organized_2026-10-30.zip" \
  --skills "SMART_LABELLING_QRT_HARDENING_R2_CANDIDATE(1).zip" \
  --golden "core 2 template.zip" \
  --out "gate_results_rechecked.json"
```

The script is diagnostic only. It does not call the internet, alter originals, invoke agents, score questions or award acceptance.

### Source-custody distinction

79/79 retained exam records' *local raw-source file hash claims* matched bytes inside the candidate archive. That confirms local correspondence only; it does not authenticate exam paper/key provenance. The old R1 key readback reports six retained local JEE row matches, still awaiting a distinct official-custody witness. Do not merge these two gates.

### Current coverage

Owner R1 review selection: 14 conditional, 7 vacant, 0 independently admitted. Earlier coder freeze: 13 conditional, 8 vacant. No final 21-question qualification, no Core1A/Core1B initiation; D3.1 remains paused.
