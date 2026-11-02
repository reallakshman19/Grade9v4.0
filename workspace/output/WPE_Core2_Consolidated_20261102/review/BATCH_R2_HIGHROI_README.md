# Core-2 High-ROI Batch R2 — Oracle author audit, not independent academic review

**Scope:** Existing WPE/Core2 WBS 4.3.1–4.3.2, [Grade9v4.0 Issue #1](https://github.com/reallakshman19/Grade9v4.0/issues/1). Owner directive: **batch work, not micro-prompts; high ROI, no revamp**. Base commit `90615716979d4172a5953cabf124c92de83912cf`.

## Whole-bank screen

74 displayed entries (73 labelled source + one authored control), 16 prior flags, **63 entries whose pre-attempt hint contains "Crux Move"**. A crux disclosure can collapse the learner decision. 29 high-impact question entries now receive specifically authored **student-safe scaffolds**, preserving each original `question.hints[]` untouched. The remaining 41 crux-disclosure records without scaffolds still require a separate candidate review; this is NOT complete all-bank clearance.

## Constrained scientific correction, no changes to original stems

- **EX-M101:** Springs with *same force* and *same extension* were mixed with unrelated conservative-field/path independence and gravitational steps. Replaced the authored explanation and independent check with (W_F=F²/(2k)) versus (W_x=kx²/2). Correct choice A remains coaching-proposed pending source/key custody.
- **EX-M61:** Removed unsupported definitive coaching key B as a scientific assertion because (K=8-U(x)) depends on the exact source graph. `HOLD` for authentic figure and key. No inferred force-orientation result.
- **EX-M2:** (sqrt(60)=7.745966...) rounds to 7.75, whereas 7.74 is the nearest listed choice, not the rounded value.
- **JEE-2026-04-06-S1-Q28:** Resisted air work (W=-9.9875 J) rounds to (-9.99 J), while (-9.98 J) is the nearest supplied choice; no exact official key claim.
- **TB-WPE-ILL-11:** Missing initial kinetic energy handled in (K_f=K_i+4mgl/9); release-from-rest 4mgl/9 remains a special case.
- **EX-M39:** Replaced mathematically unreliable “small-angle (θ=1) rad” check with exact trig substitution (θ=2 atan(1/2)), (sinθ=4/5, cosθ=3/5).

**No independent academic admission** comes from these fixes. `EX-M6` remains source/Physics-conflicted; `WEP07-03` remains QRT disputed. All 16 source audit flags retain their review HOLDs in `audit_flags.csv`; individual dispositions are reported in `review/BATCH_R2_HIGHROI_AUDIT.json`.

## Technical boundary

Only the review-candidate `selected_bank.review.json` and the exact embedded reader JSON changed, plus a **small hint-rendering selector** that uses `question.scaffolds[]` for the 29 scaffolded questions and retains the original source-hint route for others. No new renderer, framework, source question, stem, option, figure, question ID, cognitive label, response state machine, navigation or CSS modification. Original hints **remain exact** in their source custody fields.

Retained fields on all 74: ID, exact stem, stem digest, options, figure ref, question type, proposed QRT operation and band, category, origin and old question.hints. Author-added scaffolds are explicitly `AUTHORED_PEDAGOGICAL`.

## Execution and return

Engineering tests: `python -m pytest -q tests/test_wpe_core2_batch_r2.py` plus full Python QA on PR head; actual CI results required. Independent science review: NOT_RUN. Live student browser trial: NOT_RUN. Publication and promotion: HOLD pending scoped reviewer/Owner release.

**No academic approval inferred from software validation.**
