# WPE Core2 — six actual native representation component gaps

**Draft PR #16**, stacked on [draft PR #15](https://github.com/reallakshman19/Grade9v4.0/pull/15). Physics WPE pilot only; no native bank or textbook/examination figure copied to GitHub. **All original academic and learner release gates remain HOLD.**

## Corrected contract understanding

I inspected **original Owner Shared.zip**, SHA-256 `16b6fba6c349923d1744badf0c53f5debdbbe4e25eae7f02413a7baeee76667b`, specifically original `Shared/web/interactive-page-blueprints.v1.json` (SHA-256 `75f6bd43b31dfdf555fb26e8b36417e9c830a563898264dbe917d4254828653e`) and `Shared/tools/web_blueprint_contract.py`.

The active **`BP-CORE2-SOURCE-QUESTION@1.11.0`** requires content review of `REPRESENTATION` at **`EXPECTED`** level, not unconditional `REQUIRED`. Native authoring guidance says a question-aligned visual should be added only if materially helpful; if merely decorative or leaking a protected solution, the **record's author may explicitly waive this component with a written, question-specific applicability reason**.

The native extension key is `extensions["grade9v3:component_waivers"]["REPRESENTATION"]`. That is a **record-scoped applicability mechanism**, not global permission to delete all visuals, bypass a missing source answer, waive REQUIRED components, or claim academic approval.

Original `Shared/tools/web_blueprint_contract.py` synthetic native contract check:
- Without waiver: 1 missing `REPRESENTATION` diagnostic.
- With a specific synthetic waiver: 0 missing `REPRESENTATION` diagnostics, while 4 other original Blueprint component shortfalls remain.
- **0 actual waivers were applied. No native approval receipt was issued.**

## Six source-record proposals — reviewed independently before any native edits

| Original native record | Recommendation for Owner review | Conditions |
|---|---|---|
| `TB-WPE-ILL-01` | **WAIVER_PROPOSAL** | Component-form vectors may be sufficient; extra diagram could introduce a misleading spatial projection. Reviewer must confirm visual genuinely nonessential. |
| `TB-WPE-ILL-02` | **WAIVER_PROPOSAL** | Existing `REP-TB-FIG-03-FBD-STRING-RAISING` is a **solution-only** FBD containing derived relations; never move to stem. Owner decides if a neutral schematic adds enough value to justify authoring. |
| `TB-WPE-ILL-03` | **AUTHOR_NEUTRAL_CANDIDATE** | A force-vs-position representation may help. Must contain only stem-provided function/interval; no computed work, integral result, or unstated assumptions. |
| `TB-WPE-ILL-05` | **SOURCE_PHYSICS_HOLD** | The supplied extraction does not state initial speed but the working assumes rest. An SVG/waiver cannot repair underdetermination. Independent printed-source and Physics review first. |
| `TB-WPE-ILL-06` | **WAIVER_PROPOSAL** | Given circular acceleration law may already be self-sufficient; review whether an extra diagram would be decorative or leading. |
| `TB-WPE-ILL-11` | **AUTHOR_SAFE_SOURCE_PROJECTION** | Existing `REP-TB-FIG-09-OVERHANGING-CHAIN` is solution-only and answer-bearing. A neutral source-checked chain configuration must not expose final kinetic energy or energy-account derivation. |

These remain **3 proposed scoped waivers, 2 proposed neutral SVG authoring routes, 1 unqualified Physics/source HOLD**, *not* 3 waivers granted, 2 SVGs constructed, or 5 native gaps closed.

## Source and runtime evidence

Exact original `core2(3).html` SHA-256: `44d052d8e163ab7e15e8ca13aba1cd90482cbb42df096a14a5a4e72c1f58a6a5`.

Exact original `render-receipt.json` SHA-256: `8c5dcff73495b393927e55b902aa753fe7f9e014da3584a7790715c76e5c46bd`, original render_core/2 digest `a13a70605acf789d`, `draft:true`, `held_to:REFERENCE`, **10 gaps: six missing `AUTHOR_COMPONENT/REPRESENTATION` and four remaining figure-checker findings**.

Original nine Core2 cards are unchanged. The two existing FBD/chain figures are within HTML **post-attempt solution templates**, not visible pre-attempt. A source-independent script now checks both figure refs and that neither was promoted to pre-attempt DOM. There is no original native WPE bank/manifest/records supplied; the source SVG candidates and PDF/textbook extraction alone are not enough to edit those records safely.

### Reproduce against Owner-local original files

```bash
# Extract the existing original Shared/web/interactive-page-blueprints.v1.json
# privately from Owner Shared.zip. No original asset goes into Git.
python -m grade9qa.core2_representation_policy \
  --original-html '/owner-local/core2(3).html' \
  --render-receipt '/owner-local/render-receipt.json' \
  --shared-web-blueprints '/owner-local/Shared/web/interactive-page-blueprints.v1.json' \
  --out '/owner-private-review/six-representation-decisions.json'
# Exit 3 means academic HOLD, not an error or accepted waiver.
```

`src/grade9qa/core2_representation_policy.py` validates exact original HTML, receipt and Blueprint file SHA pins; the original nine-card identity and ten-gap list; six specific IDs; and two solution-only figures. Its output contains only original IDs and **our own proposed reviewer rationales**, never copied original textbook/examination stem, diagram source or answer.

`tests/test_core2_representation_policy.py` adds 13 synthetic negative/semantic tests (bad source SHA, changed BP level, loss of applicability provision, changed six IDs, new first-attempt solution leak, counterfeit approval and private text nonpublication). All other original engineering tests retained.

## Owner's next decisions and subsequent implementation

Use the separate private **`WPE_CORE2_R16_SIX_REPRESENTATION_OWNER_REVIEW_20261101.zip`** decision spreadsheet to mark **ACCEPT / REVISE / REJECT / HOLD** per item with source, reviewer and timestamp; the archive includes no original question or diagram bytes.

After independent Physics/source judgment:
1. Apply accepted **question-specific waivers**, with written reason, to the *original native* bank/records only. Reject unsound waivers. Author approved **new neutral pre-attempt SVGs** and question-specific figure bindings for nonwaived cases. **Never promote FBD/chain solution diagrams to pre-attempt.**
2. Resolve ILL-05's source/Physics incompleteness by checking the printed problem and reviewing its necessary initial condition. **Never silently supply rest as a given**.
3. Have Owner/native Shared maintainer accept or reject separate figure-checker patch in PR #15; original four warnings are still open, and source readability needs review.
4. Rebuild and rerun original Shared after obtaining native WPE `bank.json`, `records.json`, `manifest.json` and source SVG asset registry. Produce a *new* render receipt and independent tablet/print/zoom/first-answer QA.
5. The Physics QRT Blueprint/WPE adapter Owner selection, complete 79-source disposition ledger, independent original exam paper/key/figure admission, B1–B7 and Shared academic/release are separate, unchanged HOLDs.

**Neither the new program nor a developer test PASS is an academic, owner, canonical native or learner-release authorization. All PRs remain draft and unmerged.**