# Grade9 v4: the story (Oracle: this Claude session, D:\CodeD\grade9v4)

**Status:** first draft, 1 Nov 2026. Not yet played back or agreed by the Owner.
Built from: ORACLE_CHECKPOINT_20261101.md, ORACLE_HANDOVER_20261101.md (written by the previous Codex Oracle), Start_here.md, and the v3.5 story `C:/t/handover/G9V35-STORY.md` (which holds the Owner's own words up to 29 Oct).

## What the Owner wants (from the v3.5 record; later words win)
- A self-study course for the Owner's child (Grade 10, towards JEE Main): Physics, Maths, Chemistry. Explain why, break ideas down, apply. Textbook quality, private use.
- QRT grid: 7 kinds of thinking x 4 levels; hard levels first. "One tile = Common blueprint + Topic adapter"; one Physics blueprint per cell; blueprint grows only from real gaps.
- Each hard question gets: a real exam question, a teaching part, the learner's own try.
- 29 Oct: D3.1 split into six sub-tiles by physics idea; scan 18 real questions for blueprint gaps; then D4.1, then D3.2.
- v4 (Owner-scoped, recorded by the Codex Oracle): order is question page first, Owner OK, then teaching part, Owner OK, then fresh try. Work, Power and Energy stays the Physics pilot; v4 must later serve Maths and Chemistry with their own rules.

## The 79 exam questions: what agents must do with them (Owner, 1 Nov: "so that you know"; source: `WPE_Source_to_Core1A_Concept/CONCEPT_REPORT.md` + A1's earlier plan pasted by the Owner)
**Two routes meet at the teaching part:**
- **Question bank route:** identity and custody (SL1), then the decisive thinking demand (SL2), then the grid cell (QRT).
- **Book route:** exact source units, a claim ledger and construction requirements (the source-to-Core1A dossier; one example so far, WPE-N01).
- **Order of authoring:** completed question page (Core2) + Owner OK, then teaching part (Core1A) + Owner OK, then fresh try (Core1B). Book preparation may run in parallel.

**Honest count (A1's plan, as pasted):**
- 79 records = 78 distinct questions (one alias).
- 38 have provisional first-pass scores.
- 26 wait for original figures; 4 are NSEP navigation-only; 1 is missing a collision datum; 9 are not assessed.
- Target 21 places on the question page: 14 conditional picks, 7 vacant (3 Recall, 3 Explain, 1 Justify), 0 admitted.
- The 9 cards already rendered are 8 textbook + 1 practice question, not exam questions.
- "79 collected ≠ 79 authored; 9 rendered ≠ 9 exam questions done."

**A1's six steps (the agreed direction for agents):**
1. Freeze and reuse the existing work: the 9 cards, the reader, the manifest, the fixtures and the sources. Fix the known figure defects and the save-before-reveal weakness. No duplicate questions.
2. One source-of-truth ledger: 79 records to 78 questions. For each, record whether it has extraction, an original figure, an official key, SL1/SL2, QRT and a native record. Match the 16 unresolved identities.
3. Bind the Physics Blueprint and the WPE topic adapter.
   - The Owner selects and pins one adapter; there are 5 to 6 distinct candidates.
   - Build the resolver (topic × operation × level → blueprint cell + adapter capability). Unsupported cases are HOLD/FAIL.
   - Level 1/2 questions are not forced into level 3/4 cells.
4. Review the 14 conditional picks: original paper, key and figures; a sealed independent first solve; SL2 scores; QRT decision. Priority disputes: M62, M73, M79, M81, M101; missing graphs for M56, M61, M69. Vacancies stay vacant until a real question fits.
5. **One genuine golden exam question end to end:** reviewed records into the native manifest, bank and records; render with the existing Core2 renderer; test answer type, figure, hints, working, accessibility, print, offline use and attempt saving.
6. Scale through the four review lots by each question's actual blocker.

**A question counts as done only when all six are true:**
- source, options, paper and key are authenticated;
- the independent physics and SL1/SL2/QRT reviews are accepted;
- the blueprint and the selected adapter are pinned;
- the native record and figure exist;
- the renderer, answer-exposure and learner-attempt QA have passed;
- independent academic and Owner approval is recorded.

**Where R18/R19 sit:** step 4. R18 covered 9 of the 14; R19 covers the last 5. Steps 2 and 3 are still open.
- **Clash to settle:** A1's plan says 79 → 78 is reconciled, but R18's README says "the full original 79-record Owner source ledger remains unsupplied".

## Road map
Newton's laws (done, accepted) → Work, Power and Energy (pilot, in progress) → Motion in a straight line → rest of Physics → Maths → Chemistry.

## What the learner can open today
- Newton's-laws study page (accepted 25 Oct; one pulley picture wrong).
- v3.5 sub-tile pages for the first three "work" ideas (private artifacts, waiting for the Owner's look).
- v4: the corrected question-page reader for Work, Power and Energy: 8 textbook questions + 1 practice question (`workspace/output/WPE_Core2_Reader_Fix_R1_20261031/rendered/core2.html`). Not independently checked.

## What happened in v4 (30 Oct to 1 Nov)
- Whole v3.5 workspace migrated into this repo; checks mostly pass (2 fail on Windows symlinks).
- Agent onboarding pages written.
- Reader fixed: incline picture, audit notes moved out of what the learner sees.
- A ChatGPT agent (A1-G9v4) produced five repair packages (R13 to R17) about the reader's missing or wrong pictures. R17, the newest, has six open items, all on hold: 3 "this question needs no picture" proposals, 2 new drawings, 1 question that never says the starting speed.
- A1 was asked once to stop after three lots and hand over; no reply verified. Drive "Handoffs" folder chosen for the exchange; nothing uploaded.
- Teaching parts: 10 preparation notes, no new lesson. Sub-tile work (D3.1) is paused.

## Where it does not fit the Owner's intent
1. Since 29 Oct nothing new has reached the learner except the reader fix. v4 effort went into migration, onboarding and paperwork.
2. The picture repairs are on their fifth round: a repair loop.
3. The previous Oracle's notes are dense with codes and hashes, which the Owner rejected on 28 Oct.

## 1 Nov, 04:30: A1 chat read in the built-in browser (tab "tab-1")
- A1 has gone past R17: R18 (9 exam candidates in 3 batches, draft PR 18) is done but not downloaded locally. Its last answer proposes R19 (the last 5 candidates). The visible chat shows no request to stop and hand over, and no handover reply.
- A1 itself recommends that the next milestone be one exam question admitted and rendered, not more reports. That matches the Owner's intent.
- Eight stacked draft PRs (11 to 18) sit on the PUBLIC Grade9v4.0 repo.
- Owner asked for a buddy-runner handover plan: draft runbook `C:/t/handover/G9V4-RUNBOOK.md` (not agreed).

## 1 Nov, 04:24: Owner decision
- Owner: "You will work standing for owner." "Let A19 be done via buddy runner (New agent) and let outgoing agent check the process and the output." Outputs live in `D:\CodeD\grade9v4\chatgpt` (R18 ZIP not there yet; R18 read from public PR 18).
- R19 = review of the last 5 exam candidates (M39, M44, M60, M101, WEP07-03) plus the pick closest to first admission. Brief: `workspace/output/WPE_Core2_R19_20261101/BRIEF.md`. Local agent started (Opus, background) 04:24.
- Next: when it returns, read the output myself, then send `R19_FOR_A1.md` (no question text) to A1 in tab-1 for the process and output check, then report to the Owner.

## Plan (superseded by the decision above)
Not agreed yet. Proposed: buddy runner on every A1 return; A1 stops review-only rounds; next milestone is one exam question taken end to end into the reader.

## 1 Nov, 04:32: R19 returned, sent to A1
- R19 files: `workspace/output/WPE_Core2_R19_20261101/` (R19_REVIEW.md, R19_REGISTER.csv, R19_FOR_A1.md, PROCESS.md). All 5 HOLD.
  - M39: SYNTHESIZE D3 holds, MODEL competing.
  - M44: collisions out of scope.
  - M60, M101 and WEP07-03: APPLY D2, not the proposed hard levels.
- Closest to first admission: WEP07-03 (NSEP; the only one with an official paper and key), as a labelled APPLY D2. It needs: an Owner decision, the 61/611 paper code closed, exact text, a native render with QA, Owner approval. Next best: M39.
- My brief's fault: it disclosed WEP07-03's key, so that solve was not blind.
- Sent R19_FOR_A1.md plus 5 questions (per-ID agree/disagree, process faults, the first-admission pick, the 79→78 ledger clash, the R18 ZIP name) to A1, verified in chat. A1 started a read-only audit. Next: read A1's reply and reconcile.

## BENCHMARK for every step (Owner, 1 Nov: "this is bench mark")
The Owner's model of a finished step is the reader-fix return (Codex Oracle, 31 Oct):
- **One link the Owner can open:** `workspace/output/WPE_Core2_Reader_Fix_R1_20261031/rendered/core2.html`, also linked from the V4 home page `index.html`.
- **Short bullets saying what changed, in visible terms:** incline geometry and the downward displacement arrow corrected; the picture fits desktop and mobile with no sideways scroll; learner-facing admin prose removed and kept as review notes; links added on the home page.
- **One line of proof:** "12 browser checks passed".
- **One line of honesty:** "Originals preserved; other inherited findings remain open. Routine closed."
**Rule:** every step ends like this. A page to open, 3 to 5 visible changes, proof, and what is still open. A pile of review markdown is not an output.
- **Oracle check, 1 Nov 04:3x:** I opened it myself in the built-in browser. 9 cards (8 textbook + 1 synthetic), 3 pictures, no horizontal scroll at 684 px. The incline picture has the 4 kg block, a 37° angle, an s = 3 m arrow pointing down the slope, and μ = 0.2. Small flaw: the "37°" degree sign touches the angle arc. Both home-page links work.
- **R19 does not meet this benchmark:** its output is review markdown, with no page. The next step must produce an openable page (the first admitted exam question in the reader).

## 1 Nov, ~04:45: Owner "ok fix these with local or new agent, whichever is optimal ... stand in mode"
- A1's audit (tab-1): AGREE with R19 as provisional triage; NSEP Q57 = YES as the first engineering pilot, NO as an immediate admission (the Physics blueprint covers only D3/D4, so a D2 route or exception is the Owner's call). 79→78 was overstated: the full 79-row ledger (WPE_CORE2_R2_FULL_OWNER_REVIEW_PACKAGE.zip) was never supplied; the tracker has 63 identified + 16 unresolved. R18 ZIP name: WPE_CORE2_R18_NEXT_THREE_EXAM_BATCHES_PRIVATE_REVIEW_20261101.zip (Owner to download).
- Split: **local builder** (Claude, background) builds reader R2 = R1 + NSEP Q57 card (APPLY D2, multi-correct, key behind the attempt) + the 37° label fix. Brief: `workspace/output/WPE_Core2_Reader_R2_NSEP_20261101/BRIEF.md`. R1 is untouched; the home page is not relinked until the Oracle checks.
- **New ChatGPT agent B2-G9v4** (chat https://chatgpt.com/c/6ae689c7-e5ac-83ed-8882-71b8112343d7, browser tab "seed") onboarded as the independent checker. First task: a sealed blind solve of Q57 (no key given) + QRT cell. Next: check the built page.
- The Oracle's own solve of Q57 is a, b, c, d (matches the official key).
- B2 blind solve (sealed, no key): a, b, c, d = official key. Cell: B2 says MODEL D3 (7/10); R1 and R19 say APPLY D2 (5). Dispute recorded for the Owner and passed to the builder; badge stays APPLY D2 for now.
- **04:5x: R2 built**: `workspace/output/WPE_Core2_Reader_R2_NSEP_20261101/rendered/core2.html`, 10 cards, 29/29 browser checks. Oracle opened it: the attempt gate works (C ticked → working unlocks); the 37° label is clear; no sideways scroll. Physics correct. Paper code printed as 61.
- B2 page check: physics PASS. Learner fixes: duplicate (A)(a); jargon concept chip; wrong family chip; source vs provenance; review status in the title; difficulty rationale in the solution; hints + solution unlock together.
- One repair round sent to the builder (card-level items 1–6). Renderer-wide items are left for the Owner: the title review status; separate hint/solution reveal.
- **Repair round done:** 5 of 6 fixes made, 30/30 checks. The Oracle reopened the page: no (A)(a) duplicate; concept and family chips correct. The Source chip is still "Owner-supplied question" (needs a renderer change). The V4 home page now links R2 above R1 (backup of the old home page: R2/review/V4_HOME_BEFORE.html). Repair rounds on this card are now closed.
- **Owner decisions pending:** (1) the NSEP cell, APPLY D2 vs MODEL D3; (2) hints unlocking before the full working, page-wide (renderer change); (3) the "candidate, independently unreviewed" title wording and the source chip (renderer); (4) admission of Q57 itself.
- **Owner, 1 Nov ~04:52: "Yes, hints first".** The builder is building R3 (`workspace/output/WPE_Core2_Reader_R3_HintsFirst_20261101/`): after an attempt, hints unlock one rung at a time; the full answer and working sit behind their own button. Any renderer change is a candidate copy, not installed in Shared. Still pending from the Owner: the NSEP cell; the title/source wording.
- **R3 built** (46/46 checks): `workspace/output/WPE_Core2_Reader_R3_HintsFirst_20261101/rendered/core2.html`. The Oracle tried it: before the attempt only the attempt button; after it, hints (one at a time) above a separate "Show full answer and working". The home page now links R3 first. The renderer change is in R3's copy only (review/RENDERER_CHANGE.md), not installed in Shared.
- Side effect to settle: R1/R2 let hints open BEFORE an attempt; R3 locks them until the attempt (my brief's assumption). Owner choice.
- Browser note: the A1 chat tab was reused for the page; chats are still reachable by URL (A1 6ae5c904…, B2 6ae689c7…).
- **Owner, 1 Nov ~05:53: "Allow before attempt"**: hints are usable before the attempt; the full answer is locked until the attempt plus its own button. Builder is updating R3 in place.
- **R3 updated** (47/47 checks). The Oracle tried it: before the attempt H0 opens ('What is U at the release point?') and the full answer refuses; after the attempt the full answer opens only on its button (a fresh textbook card stayed closed). The home page already links R3.
- **Owner, 1 Nov ~06:03: "Apply, level 2"** for NSEP Q57; the cell dispute is closed. The builder is updating the card's difficulty line in R3. Admission is still the Owner's (HOLD).
- **Owner, ~06:10: next exam question = the swing question M39** (JEE Main 2024, 27 Jan, Shift 2), after finding and checking its official paper and key. The NSEP card's difficulty line now records the Owner's APPLY D2 (47/47 checks).
- A source agent (Sonnet, web, read-only) is searching for the NTA final key and question IDs; it writes to `workspace/output/WPE_Core2_M39_Source_20261101/SOURCE_CHECK.md`. A first web search found only coaching-site copies.
- B2 blind solve of M39: B = 2tan⁻¹(1/2), SYNTHESIZE D3 (7/10), agreeing with R19 and the Oracle. Wrong routes for the hints: a = g or g cosθ at the extreme; adding g to v²/L at the bottom.
- Next: once the key is VERIFIED (or PARTIAL, with an Owner call), the builder adds the M39 card to R3, then the Oracle checks and reports.
- **06:12: M39 official key = PARTIAL.** The NTA final key (12.02.2024) was read, but no question-ID mapping was found. 27 Jan S2 Physics question ID 533543501 was DROPPED, and it could be this question. Coaching keys say B. Owner call needed before building.
- **Owner asked for a handover note:** written to `D:/CodeD/grade9v4/ORACLE_HANDOVER_20261101_CLAUDE.md` (working files, methodology, step-by-step procedures A–H, next steps, pitfalls).
