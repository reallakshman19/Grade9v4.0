# Original Shared Core2 SVG warnings — source-preserving browser geometry audit

**Draft PR #14**, stacked on [PR #13](https://github.com/reallakshman19/Grade9v4.0/pull/13). **Academic HOLD / Shared native waiver NOT_PERFORMED / learner release HOLD.**

Grade9 v4.0 is a three-subject Physics/Mathematics/Chemistry platform; these findings are only for the **Physics WPE Core2 pilot**. This is **not another QRT Blueprint or WPE topic adapter**, nor a duplicate HTML output.

## Original evidence — preserve exact bytes

The actual Owner-provided `core2(3).html` is the original **nine-card** native `WPE-CORE2-NATIVE-INTEGRATION-R1` draft, `render_core/2` digest `a13a70605acf789d`. It is neither an approved examination bank nor proof of real first-attempt protection.

| Owner-local original | SHA-256 |
|---|---|
| `core2(3).html` | `44d052d8e163ab7e15e8ca13aba1cd90482cbb42df096a14a5a4e72c1f58a6a5` |
| `render-receipt.json` | `8c5dcff73495b393927e55b902aa753fe7f9e014da3584a7790715c76e5c46bd` |

**Original receipt has 10 gaps:** six `AUTHOR_COMPONENT`/missing `REPRESENTATION` records; four `AUTHOR_FIGURE_TEXT` warning records. The source original Shared `_figure_text_findings` estimates label extent as `len(inner) * size * 0.52` (or bold factor 0.58) and does not calculate nested SVG transforms, actual glyph text metric or browser layout. It may conservatively report overflow in valid translated/centered diagrams.

## Measured, not inferred, at 1280×850 Chromium

The original, unpatched HTML was loaded locally in isolated Chromium. The original **author-only** materialization hook was used *solely to display after-attempt SVGs for measurement*; solution-only figures **were absent from the live DOM before this diagnostic action**. No published learner security claim is derived.

Each `text` element's `getBBox()` is mapped into its parent SVG user coordinates using `svg.getScreenCTM().inverse().multiply(text.getScreenCTM())`. All four had **positive minimum margins** inside the browser's SVG viewBox.

| Original figure ID | Labels measured | Minimum transformed SVG margin | Browser finding |
|---|---:|---:|---|
| `REP-TB-FIG-06-INCLINE-BLOCK` | 4 | 35.58 units | INSIDE_VIEWBOX |
| `REP-TB-FIG-07-INCLINE-FBD` | 6 | 25.45 units | INSIDE_VIEWBOX |
| `REP-TB-FIG-09-OVERHANGING-CHAIN` | 5 | 20.27 units | INSIDE_VIEWBOX |
| `REP-TB-FIG-10-SPRING-BLOCK-WALL` | 6 | 5.77 units | INSIDE_VIEWBOX |

**Disposition:** `BROWSER_VS_HEURISTIC_DISCREPANCY_NOT_WAIVED`. This suggests the original warning may be a **renderer diagnostic false positive** at the tested viewport; it does not mean the figure has passed every 12.7-inch tablet/print/zoom/accessibility condition, that author SVGs match published figures, or that native checks have been changed. The narrow margin on the spring-block title deserves an explicit print/zoom review. Do **not** enlarge/redraw the viewBox merely to satisfy a text-length heuristic. Never move the derived FBD to pre-attempt.

### Six native missing `REPRESENTATION` records — unchanged

- `TB-WPE-ILL-01`
- `TB-WPE-ILL-02`
- `TB-WPE-ILL-03`
- `TB-WPE-ILL-05`
- `TB-WPE-ILL-06`
- `TB-WPE-ILL-11`

For these six, the original representation requirement has not been satisfied. No source-supported diagram/waiver can be invented from the rendered HTML. The author must supply editable original native `manifest.json`, `bank.json`, `records.json`, native SVG/representation assets, role/band/component constraints and source custody; if no visual is legitimately required, an appropriately signed and justified native component-waiver decision must come through the Owner's original Shared workflow.

## Code and reproduction

`src/grade9qa/core2_figure_geometry.py` has a private Chromium-based **read-only** inspection routine plus a pure, testable metadata-only receipt evaluator. Requires an Owner-local Chromium and Python Playwright only when actually running the browser; standard CI tests do not use browser or proprietary question data.

```bash
python -m grade9qa.core2_figure_geometry \
  --original-html '/owner-local/core2(3).html' \
  --original-receipt '/owner-local/render-receipt.json' \
  --chromium /usr/bin/chromium \
  --out '/owner-private-review/figure-geometry.json'
```

No original HTML, question stems, answer keys, figure SVG source, question options or illustrations are uploaded to public GitHub. The JSON reports four figure IDs, counts and margins, plus six missing record IDs—not text.

**11 synthetic regression tests** in `tests/test_core2_figure_geometry.py` cover original receipt continuity, nine-card identity, six missing component records, true clipping fail-closed, wrong digest, incomplete browser evidence, original-file overwrite prevention, text privacy, and non-waiver. **340 tests passed** on Python 3.11 and 3.12 at the implementation head.

## What remains to reach a truly gap-free, native release

1. Original SVG asset authors and native renderer maintainers inspect the four discrepancy cases. If the checker is wrong, revise its text-bound heuristic in original Shared with matching native test fixtures **under Owner authorization**, preserving true clipping detection. Do not just suppress errors.
2. Author/review the six original `REPRESENTATION` components or provide formally justified native waivers. Existing derived solution-only FBD is *not* approved as a stem/preview representation.
3. Rebuild from original `manifest.json` and exact figures; get a **new trusted Shared render receipt** plus independent 12.7-inch tablet, print, keyboard/assistive tech and visual QA.
4. Complete protected first-attempt production architecture from #13; static answer templates remain readable in source.
5. Supply independently authenticated original examination paper/key/figure and source custody, Owner-selected compatible Physics Blueprint/WPE adapter, QRT/Physics decisions and Shared academic approvals. All original Core2 exam admissions remain **zero**.

**Status: four original warnings have measured counterevidence, not four formally closed defects; six authored component requirements are still unmet.** No PR merged. No native content republished.
