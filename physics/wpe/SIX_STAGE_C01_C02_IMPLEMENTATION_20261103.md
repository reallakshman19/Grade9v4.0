# WPE · Two interactive six-stage journeys · 3 Nov 2026

**Purpose:** make the author-created C01 and C02 learning constructions usable by a child in the existing WPE Learn → Challenge page. These are **student practice candidates**, **not** native admissions or independent B3/B4 approvals.

## Learner location

- [WPE Learn → Challenge](learn-challenge.html#construction-lab), immediately below the five existing foundation lessons.
- The WPE chapter [learning tile](index.html) also links to the two journeys.
- C01: multi-force work–energy, transferring a level-floor box guide into a scooter-on-ramp challenge.
- C02: unattached spring contact followed by rough ground, transferring a smooth spring-cart guide into an explicitly two-region challenge.

## Six-step user interaction

1. **Predict.** Write an explanation before a hint or model is available.
2. **Attempt.** Complete a topic-specific calculation/ledger and written reasoning. Submitting locks the first model. Hints are deliberately unavailable here.
3. **Reconstruct.** After the locked first attempt, optionally view two non-answer hints, then explicitly open a complete worked model with reasoning criteria. Model data is fetched only on that request.
4. **Diagnose.** Choose a possible misconception and explain it, including the option to describe why one's original attempt already works.
5. **Repair.** Write a revised model/calculation; this is stored as a **separate** record, not a rewrite of the first.
6. **Boundary test.** Answer a changed-condition question independently before revealing its worked check.

A two-click clear control deletes a single journey without deleting attempts on the original five foundations. The UI stores each journey in the browser under `g9:wpe:six-stage-lab:v1:C01` or `g9:wpe:six-stage-lab:v1:C02`. A progress meter counts **completed reflection journeys only**, not correctness or mastery.

## Source and answer separation

- Authored basis: `WPE_Source_to_Core1A_Concept/learning-bridge/MULTIFORCE_LEDGER_LEARNING_PACK.md` and `SPRING_CONTACT_LEARNING_PACK.md`, both pinned by Git blob in `construction-lab-map.json`. Original exam tasks are not copied or replayed.
- Independent task/student-facing text: `learn-challenge.html`.
- UI controls, local browser record and gated fetch: `construction-lab.js`.
- **Learner-facing** worked reconstructions and changed-condition explanations: `construction-lab-answers.json`, requested only after the locked attempt / boundary response.
- The original **author-only** review packs remain in the author bridge and are not linked from the public student page.
- **Security limitation:** a public static JSON file can be fetched manually and localStorage can be tampered with. This is a **UX disclosure gate**, not secured assessment or independent evidence of a first attempt. The page explicitly explains the limitation.

## Verification and independent academic status

- `tests/test_wpe_construction_lab.py`: verify exact authored pack blobs, two tasks, static source limits, six stages, post-attempt models and unchanged five original foundations.
- `tools/wpe_learn_challenge_ui.py`: Chromium desktop/mobile end-to-end journeys, pre-attempt model absent, first-attempt lock, optional hints, reconstruction, diagnosis, repair, boundary response, reload, confirmation and clearing.
- Native Core1A/Core1B: NOT_ACCEPTED; QRT: NOT_RUN; Owner: PENDING; admitted: 0. No grading algorithm is applied to free-text reasons.

## Draft routing PR #40

The separate draft `#40` introduces review-only source-question navigation involving `preview/question-status.html`, a manifest and source JSON that carry separate review constraints. **This implementation does not merge PR #40**, modify those source records or claim that the proposed C01/C02 theme links are qualified native prerequisites. The lab link can be incorporated into a later fully reconciled routing experience.
