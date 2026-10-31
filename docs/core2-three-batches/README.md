# WPE Core2 — three private Owner review batches (R17)

**Draft PR #17**, stacked on PR #16. **This work covers the six existing private textbook Core2 representation candidates only**, not 6 newly admitted examination questions, not the 79-record original exam inventory, and not the 21-place Core2 examination selection. It preserves all nine original `render_core/2` cards and the ten-gap original receipt.

## Exactly three batches

| Private batch | Original record IDs | Artifacts | Review/authority status |
|---|---|---|---|
| **01 — applicability/waiver** | `TB-WPE-ILL-01`, `-02`, `-06` | Separate Owner decision CSV and explicitly **NOT-APPLIED** waiver rationale proposals | No native waiver, no approval |
| **02 — neutral editable SVG drafts** | `TB-WPE-ILL-03`, `-11` | Two independent answer-free SVG **candidates**, separate PNG previews and source-hash/figure-binding quarantine register | No figure_ref linked to native bank; Owner/Physics review pending |
| **03 — source/Physics exception** | `TB-WPE-ILL-05` | Extracted-problem fingerprint, detailed Physics dependency and editable review disposition | Starting speed absent in extracted question; must authenticate original printed text |

All three source-authoring steps are governed by original Shared **`BP-CORE2-SOURCE-QUESTION@1.11.0`**, which labels REPRESENTATION **EXPECTED** and allows a written **per-question** applicability waiver through `extensions["grade9v3:component_waivers"]["REPRESENTATION"]`. The existing solution-only FBD and chain diagrams remain post-attempt. This branch does not apply a waiver or change the native bank.

## Original source evidence used; never copy the textbook into Git

- Original private **`Input sources(4).zip`**, SHA-256 `ed0880d9ff314853c084834f2a8ac4ced69d2b8f5b019612ca999a1222b20565`.
- Original source member `work_energy_power_extracted/work_energy_power.md`, SHA-256 `a33f19b308ea81c7eb527546e44b4adf26aed7116013ac01218cc1bbb8`.
- Original user-supplied native `core2(3).html`, SHA-256 `44d052d8e163ab7e15e8ca13aba1cd90482cbb42df096a14a5a4e72c1f58a6a5`.
- Original `render-receipt.json`, SHA-256 `8c5dcff73495b393927e55b902aa753fe7f9e014da3584a7790715c76e5c46bd`; native draft digest `a13a70605acf789d` and 10 gaps unchanged.

**Batch 01:** ILL-01 vector component data may be adequate; ILL-02 already has a derived solution-only FBD, not a neutral pre-attempt visual; ILL-06 supplies a circular kinematic law, where an added circle might be decorative or hint at protected working. An independent reviewer must affirm question-by-question nonapplicability or instead request a neutral diagram. Printed-page equivalence and printed JEE labels are unverified.

**Batch 02:** ILL-03 SVG contains only the source-given **linear force law** and source-given `x=0..2.0 m` bounds, no shaded area/integral/work result. After visual quality inspection, the initial exaggerated slope was corrected to the actual relative 10→11 N change without printing the derived end value. ILL-11 SVG illustrates the **initial** overhanging chain with 2ℓ/3 on a smooth table; no final slipping state, kinetic-energy formula or energy-account diagram. The original answer-bearing `REP-TB-FIG-09-OVERHANGING-CHAIN` remains post-attempt. These are **original editable private review candidates**, not copies of source figures and not authorized native assets.

**Batch 03:** The extracted ILL-05 prompt does not specify initial speed, while source working uses a result corresponding to release from rest. From ordinary smooth-incline mechanics, an independent reviewer must address the unknown `v0` in `v_bottom² = v0² + 2gℓ sinθ` and `P_bottom = mg sinθ · v_bottom`. The expression is a **reviewer diagnostic**, not evidence the printed source stated rest. Do not rewrite, infer `v0=0`, generate a purported correct answer for the current stem, waive a source inconsistency, or mark the problem admitted.

## New public code; private question/asset separation

`src/grade9qa/core2_three_batch_gate.py` verifies exactly **3/2/1 original question IDs**, no duplicate identity, original source/HTML/receipt hash pins if supplied, absence of applied waivers or native figure_refs, retained source/Physics HOLD, exact private SVG byte hashes, accessible SVG title/desc and simple answer/external-content rejection rules. It returns only record IDs and SHA-256 hashes; **no original textbook stems, existing source drawings or private author figures are committed publicly**. A PASS-like technical match remains **academic HOLD**.

Owner-local private bundle: `WPE_CORE2_R17_THREE_BATCHES_PRIVATE_REVIEW_20261101.zip` (conversation attachment) with three separate ZIPs, editable CSVs, candidate SVGs and PNG previews, source-hash register and 3/2/1 batch manifests. Each draft asset is specifically marked **NOT IN NATIVE**.

### Reproduce locally

```bash
python -m grade9qa.core2_three_batch_gate \
  --private-root '/owner/WPE_CORE2_R17_THREE_BATCHES_20261101' \
  --sources '/owner/Input sources(4).zip' \
  --native-html '/owner/core2(3).html' \
  --render-receipt '/owner/render-receipt.json' \
  --out '/private-out/core2-r17-three-batch-audit.json'
# Exit 3 = review HOLD, not failure/academic acceptance.
```

## Checks, limitations and next external decisions

- **15 new synthetic tests**, including unauthorized waiver application, forged source correction, altered SVG bytes, inserted answer code/result, changed six IDs, duplicate records and missing original SHA pins. **390 repository tests** passed on Python 3.11 and 3.12 (375 before + 15).
- Do not treat a phrase-based SVG leak check as complete solution confidentiality. Static HTML exposes original answer templates; genuine release requires original native Shared and server-controlled answer custody or approved alternative.
- **No** source-authenticity verification of actual printed textbook or exam paper, independent Physics/QRT/Owner review, source SVG approval, native `manifest.json`/`bank.json`/`records.json` editing, Shared waiver, figure_ref binding, successful canonical re-render or new native receipt. All original ten gaps remain officially **open**.
- The original source material's JEE labels are not independently authenticated exams. These are **textbook illustration candidates**, not the 79 examination-source records and not extra Core2 admitted questions.
- WPE is the Physics pilot in the broader three-subject product; this gate is not a Mathematics/Chemistry Blueprint or adapter.

**Academic admission HOLD · Owner native authoring HOLD · Original Shared receipt unchanged · Learner release HOLD.**
