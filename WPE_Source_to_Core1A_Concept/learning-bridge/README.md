# WPE D3/D4 — source-to-learning bridge (author proposal)

**2026-11-02 · Existing Core1A/Core1B practice is NOT a D3/D4 coverage demonstration.** This folder supplies a missing middle layer between selected difficult question *themes* and the reasoning a child must first learn. These are newly authored instructional proposals, **not** original examination questions, QRT findings, native academic admissions, or a new learner webpage.

## Verified against this repository snapshot

| Item | Observed |
|---|---:|
| R1 pilot places | 21 |
| Pending candidate IDs | 14 |
| Vacant places | 7 |
| Admitted examination items | **0** |
| Pilot candidates whose proposed operation and D-band both match the consolidated review reader | **3** |
| Pilot candidates whose operation or D-band conflicts with the consolidated review reader | **8** |
| Pilot candidate IDs absent from that reader | **3** |

**Important nuance:** eight classification conflicts are *disagreements between two unapproved records*, **not corrected QRT classifications**. `EX-M81`, `EX-M44` and `EX-M60` are absent from the consolidated reader, not necessarily absent from every source package. `WEP07-03` has a substantive D2/D4 and operation conflict; its source/key and original multi-selection nature need separate custody and review. Existing pilot slots are left untouched.

The exact pilot selections and reader classifications are compared side by side in [P0_P1_CONSTRUCTION_BRIDGE.json](P0_P1_CONSTRUCTION_BRIDGE.json). That JSON also pins the Git *blob SHAs* of the four inputs examined. Disagreements remain in an explicit `CONFLICT_IN_READER` state, not an automatically “fixed” classification.

## Eight reusable constructions, not eight exam-question copies

| Priority | Construction | Source-theme link examples | Ready-to-author status |
|---|---|---|---|
| P0 | WPE-C01 · Multi-force work–energy ledger | EX-M105, EX-M24, TB-WPE-ILL-02 | **Full guided + fresh-task author pack** |
| P0 | WPE-C02 · Spring contact and motion phases | EX-M24, TB-WPE-ILL-12, EX-M18 | **Full guided + fresh-task author pack** |
| P0 | WPE-C03 · Constant power and changing speed | EX-M62, EX-M79, EX-M69 | Construction specification |
| P0 | WPE-C04 · Distributed mass / centre of mass | EX-M73, WEP07-02, TB-WPE-ILL-11 | Construction specification |
| P0 | WPE-C05 · Graph: area, slope, or time shape | EX-M56, EX-M61, EX-M69 | Construction specification; exact exam graphs not qualified |
| P0 | WPE-C06 · Vertical circle and contact constraint | EX-M39, EX-N31, EX-M18, EX-M6 | Construction specification |
| P1 | WPE-C07 · Conveyor and mass flow | EX-M16 | Construction specification |
| P1 | WPE-C08 · Springs at fixed force vs extension | EX-M101 | Construction specification |

Source-theme links after the R1 selection are *proposals*, not independently verified operation-level QRT joins. The matrix deliberately avoids claiming that a specific exam stem matches a construction without original-question confirmation.

## Two usable author packs

- [WPE-C01 — Multi-force ledger](MULTIFORCE_LEDGER_LEARNING_PACK.md): guide = horizontal box with motor pull/friction; genuinely new task = scooter up a ramp requiring motor, friction, gravity and normal-force decisions.
- [WPE-C02 — Spring contact](SPRING_CONTACT_LEARNING_PACK.md): guide = spring launch followed by a smooth region; genuinely new task = spring launch **then a rough strip** with changed equations after loss of contact.

Each author pack contains **six Core1B stages**: Predict → Attempt → Reconstruct → Diagnose → Repair → Boundary test. Both reserve the independent task as a distinct problem, with an **author-only worked reference** and an explanation rubric. Those reference answers are in repository documentation only: **do not embed them into a public pre-attempt client bundle or claim secure answer protection from a static page**.

For a student, the essential format is:

> **Before help:** “What do you predict? Draw or describe your model. Solve the new case and explain the decisive decision.”  
> **After the saved attempt:** “Compare each step, find the first model error, repair it, then test one changed physical condition.”

This is more than selecting MCQ options or writing eight arbitrary characters. It permits playful, age-appropriate open reasoning while keeping an honest distinction between guided teaching and independently witnessed reconstruction.

## The current five foundational pairs remain distinct

The previous five pairs teach work sign, momentum/kinetic energy, energy reachability, potential-energy slope and spring-driven cart momentum. They remain useful foundations but do **not** establish the missing D3/D4 constructions above.

The earlier B3/B4 review (`physics/wpe/learn-challenge-wpe02-b3-b4-review.json`) references older page/map blob SHAs. The exact current page/map SHAs differ. **That review is historical, not a current acceptance finding**; it must not be quietly reused as a contemporary PASS or FAIL.

## Usage and limits

1. Start teaching with WPE-C01 and WPE-C02 as fresh, independent *proposals* after ordinary subject/scientific sanity checks. They do not alter the existing source bank.
2. Expand the other four high-reuse P0 specifications into the same two-task, six-stage self-tutor format.
3. Resolve the pilot/source-reader classification discrepancies **as a separate provenance task** without blocking unrelated child-friendly reasoning drafts or treating authored tasks as admission evidence.
4. If native release is intended, complete the existing independent subject/QRT, curriculum adapter, paper/key custody and Owner requirements before claiming acceptance.

The page `physics/wpe/learn-challenge.html` and pilot `RECEIVED_selection_21_places.json` are **not modified by this bridge**. No academic approvals, scores or coverage cells have been created.
