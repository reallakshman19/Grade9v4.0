# P0 Core2 original Shared SVG diagnostic — exact-source candidate repair

**Draft PR #15**, stacked on [PR #14](https://github.com/reallakshman19/Grade9v4.0/pull/14). WPE is the Physics pilot within Grade9 v4.0's planned Physics/Mathematics/Chemistry platform.

**Scope:** repair the **diagnostic assumption**, not authored textbook figure geometry, QRT construction, source admission or learner HTML. The source Owner must accept the patch into the original Shared code and regenerate a new signed/trusted native render receipt. No academic/release status changes.

## New discovery in already supplied Owner files

The original `Input sources(4).zip`, SHA-256 `ed0880d9ff314853c084834f2a8ac4ced69d2b8f5b019612ca999a1222b20565`, contains **original editable SVG source candidates** corresponding to all four figure-warning IDs (fig_06_incline_block, fig_07_incline_fbd, fig_09_overhanging_chain, fig_10_spring_block_wall). They were *not* included in the three HTML/index/receipt attachments, but they **are** in the separately supplied source archive. This corrects an overly broad earlier statement that no source SVGs were supplied. The complete native WPE `manifest.json`, `bank.json`, `records.json` and canonical figure-to-question bindings are still absent. Source extraction does NOT certify printed-page equivalence or independent JEE exam provenance.

| Owner SVG source | Original exact byte SHA-256 |
|---|---|
| `fig_06_incline_block.svg` | `c5a896866e7fcca2b2dd82e8408394e655ab8b4ef8edda3a3eb6d80cbad6ccd5` |
| `fig_07_incline_fbd.svg` | `98c664df1595322694f974c7fde38699fc337a6f7829786b00e0dd5fd133e6bd` |
| `fig_09_overhanging_chain.svg` | `40510540074ad29b0f7634e680f8235356f64dbe969eb28b164edb7e30a00aa0` |
| `fig_10_spring_block_wall.svg` | `c0a90c6fffcc88731316cb17fe34439e4bdccceda7a34d8deb585a2ba1d61bbc` |

**Reproduced exact original checker discrepancy:** on the four **original source asset bytes** at a 400px reference column, 12px font floor, original `Shared/tools/render_core.py` function `_figure_text_findings` flags each as `label(s) run outside the viewBox`. It also separately produces a **minimum-text-size warning** for each (NOT cleared by a clipping-only patch).

Independent Chromium 1280×850 host at 400 CSS px SVG width, using original source bytes and transformed `getBBox/getScreenCTM` glyph bounds:

| Original figure | Original clipping assertion | Minimum margin inside source viewBox | Browser clipping at that viewport |
|---|---|---:|---|
| `REP-TB-FIG-06-INCLINE-BLOCK` | YES | +35.58 SVG units | None measured |
| `REP-TB-FIG-07-INCLINE-FBD` | YES | +24.80 | None measured |
| `REP-TB-FIG-09-OVERHANGING-CHAIN` | YES | +20.50 | None measured |
| `REP-TB-FIG-10-SPRING-BLOCK-WALL` | YES | +4.90 | None measured |

These values are specific to the source SVGs in Chromium, and should not be combined with the earlier slightly different **rendered page** measurements. They do not prove full tablet/print/zoom readability, independent scientific accuracy, or that the native render receipt has been corrected.

## Engineering patch in this PR

`src/grade9qa/native_svg_checker_patch.py` patches only the original `_figure_text_findings` function in a **separate candidate renderer source copy**. The utility pins the exact original Owner Shared source SHA-256:

`0ec1acc79750f24af2000adeb2549068414032ddcc72347b4bae97551fcceb06`

The replacement:

1. Parses XML instead of treating `&#956;` or `&#8658;` as multiple visible glyphs.
2. Applies parent/child affine SVG `translate`, `rotate`, `scale`, and `matrix` transforms rather than treating local x as global x.
3. Honors start/middle/end anchors and does not inflate all semibold titles' advance widths merely because of their stroke weight.
4. Retains the independent *minimum CSS text-size* warning and still flags out-of-viewBox estimates. Malformed SVG, unsupported transforms, nested complex `tspan` and missing coordinates result in explicit **browser/author review**, never silent PASS.
5. Does NOT draw figures, rewrite questions/solutions, change the canonical Blueprint or topic adapter, append a fake Shared receipt, or waive original author requirements.

### Owner-local reproduction

```bash
python -m grade9qa.native_svg_checker_patch \
  --original-renderer '/owner/Shared/tools/render_core.py' \
  --out '/private/render_core.svg-checker-candidate.py' \
  --receipt '/private/checker-patch-provenance.json' \
  --svg-archive '/owner/Input sources(4).zip' \
  --svg-audit-out '/private/source-svg-candidate-audit.json'
```

This command fails closed if original Shared source hash, original SVG archive hash or any of four SVG byte pins has changed. The four-SVG evidence report includes only IDs, digests and counts of candidate clipping, minimum-font and unreviewed-geometry warnings. **The test suite cannot independently reproduce an authoritative native WPE build without the original product manifest and source registry.** The real-source browser contrast is a separate diagnostic, not a claim the new checker has been merged or was run in canonical Shared.

## Evidence and tests

**22 new synthetic pytest tests** validate XML entities, positive/nested affine transforms, true edge overflow, font-size warning preservation, unsupported transforms/complex tspans, corrupt source bytes, collision/overwriting protection and no publication of private figure text. **362 pytest passed**, Python 3.11 and 3.12.

The Owner-private source comparison can be downloaded separately. No textbook SVG, original examination paper/option/answer or figure content has been committed to GitHub.

## Source-authoring and release obligations unchanged

- Six native `REPRESENTATION` component gaps still exist: `TB-WPE-ILL-01, 02, 03, 05, 06, 11`. Four existing SVG source candidates do not prove that any of these six question records should reference an existing figure, nor authorize a solution-only FBD in the pre-attempt prompt. Full native bank/manifest/records required for component repair.
- Even if the four clipping warnings are reproducibly eliminated after an authorized original Shared patch and native rebuild, the separate **small-font** and 12.7-inch tablet/print/zoom/readability gates must be resolved; the current original 10-gap receipt remains authoritative and unchanged.
- Trusted first-answer/server answer custody remains unresolved from #13; static HTML answer templates remain inspectable.
- The 79-source complete owner identity ledger, independently authenticated exam question + official key + figure, selected WPE topic adapter compatible with the Physics QRT Blueprint and independent QRT/Physics/Shared reviews are still missing. **Zero academically admitted Core2 examination questions.**
- Draft, unmerged, no learner release.

**Status: original SVG source identified and clipping diagnostic repair candidate implemented; original Shared integration NOT_PERFORMED, academic HOLD, release HOLD.**
