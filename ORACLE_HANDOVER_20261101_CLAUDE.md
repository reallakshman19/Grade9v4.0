# Grade9 v4 — Oracle handover (Claude session, 1 Nov 2026, 06:15 Dubai)

**Who wrote this:** the Claude Code Oracle for Grade9 v4, working in **stand-in mode** for the Owner since 04:24 on 1 Nov 2026.
**Who reads it:** any agent taking over, including a novice. Read all of section 1 before you do anything.
**Supersedes:** nothing. It continues `ORACLE_CHECKPOINT_20261101.md` and `ORACLE_HANDOVER_20261101.md`, the Codex Oracle's notes from 04:12.
**Privacy:** this file holds no question text, options or keys. Keep it that way. It sits in the Git working tree; it is untracked and has not been committed.

---

## 1. What the Owner wants, in plain words

1. **The product.** A private self-study course for the Owner's child: Grade 10, working towards JEE Main, in Physics, Maths and Chemistry. Work, Power and Energy (WPE) is the Physics pilot.
2. **How a topic is built: the QRT grid.**
   - The grid crosses 7 kinds of thinking (Recall, Explain, Apply, Model = choose the model, Represent = translate between representations, Synthesize = multi-step, Justify) with 4 levels (D1 to D4).
   - The level comes from 5 factors scored 0 to 2 each: concept, representation, chain length, algebra, trap.
   - The bands are D1 0–2, D2 3–5, D3 6–7, D4 8–10.
3. **Every hard question gets three parts, built in this order, each needing the Owner's OK before the next:**
   1. the real exam question page, **Core2**;
   2. a teaching part, **Core1A**;
   3. the learner's fresh try, **Core1B**.
4. **The Owner's benchmark for every step** (Owner, 1 Nov: "this is bench mark"). A step is finished only when it ends with:
   - **one page the Owner can open**;
   - **3 to 5 bullets of visible changes**;
   - **one line of proof**, such as "47/47 browser checks passed";
   - **one line saying what is still open**.

   A pile of review markdown is **not** an output.
5. **The Owner hates:**
   - codes in messages (say "the swing question", not "EX-M39");
   - paperwork for its own sake;
   - repair loops;
   - parallel lines of work;
   - long messages.
6. **A question counts as DONE only when all six of these are true:**
   - its source, options, paper and official key are authenticated;
   - independent physics and cognitive (SL1/SL2/QRT) reviews are accepted;
   - the Physics Blueprint and the selected WPE adapter are pinned;
   - its native record and figure exist;
   - the renderer, answer-exposure and learner-attempt checks have passed;
   - independent academic approval **and the Owner's approval** are recorded.

   Today **zero** questions are DONE.

---

## 2. Where things stand right now

| Item | State |
|---|---|
| **Learner page (current)** | `workspace/output/WPE_Core2_Reader_R3_HintsFirst_20261101/rendered/core2.html`, linked first on the V4 home page `index.html`. It has 10 cards: 8 textbook, 1 synthetic control, and **NSEP 2025 Q57**, the first real exam question. |
| **Hints behaviour (Owner decisions)** | Hints open at any time, one rung per click (Owner: "Yes, hints first", then "Allow before attempt"). The full answer and working need an attempt **plus** a press of "Show full answer and working". Page state survives a reload. |
| **NSEP Q57** | Official key a, b, c, d. Two blind solves agree (the earlier sealed R1 review, and checker B2). Its cell is **APPLY · D2**, the Owner's decision. The page shows NSEP as its source, and the paper prints code 61. **Not admitted** (needs the Owner's approval). |
| **Next question (Owner's pick)** | **The swing question, M39**: JEE Main 2024, 27 Jan, Shift 2, single correct, no figure. Blind solves by R19, B2 and the Oracle all give option **B**. Cell: SYNTHESIZE · D3 (7/10). **Waiting** for the official NTA key check. |
| **Official key search for M39** | **PARTIAL** (06:12). NTA's official final key for Session 1 (as on 12.02.2024, https://nta.ac.in/Download/Notice/Notice_20240212120843.pdf) was read, but no source shows this question's NTA question or option IDs, so nothing could be mapped. **Risk:** one 27 Jan Shift 2 Physics MCQ, ID 533543501, was **dropped** by NTA, and this question may be that one. Coaching keys (ALLEN, Cracku) give option B; that is not official. Details: `workspace/output/WPE_Core2_M39_Source_20261101/SOURCE_CHECK.md`. |
| **Exam inventory** | 79 records, about 78 questions. Of these: 14 conditional picks, 7 vacant places (3 Recall, 3 Explain, 1 Justify) and 0 admitted. The full 79-row ledger was **never supplied**; A1 admitted that its "79 → 78 reconciled" claim was overstated. |
| **R19 review of the last 5 picks** | All 5 are on HOLD. M39 is SYNTHESIZE D3. M44 involves a collision, which is out of the WPE scope. M60, M101 and NSEP Q57 are APPLY D2. |
| **Shared renderer** | **Untouched.** The hints change exists only in R3's private copy; see `R3/review/RENDERER_CHANGE.md` and `render_core.diff`. Installing it in Shared is a separate decision for the Owner. |

### Decisions still waiting for the Owner
1. The card title wording "candidate, independently unreviewed", and the source chip "Owner-supplied question". Both are renderer-wide.
2. Admission of NSEP Q57: the Owner looks at the page, then approves.
3. Whether to install the hints change into the canonical Shared renderer.
4. What to do if M39's official key turns out NOT_FOUND or PARTIAL.
5. The collision scope for M44 and M60.
6. Downloading A1's R18 ZIP: `WPE_CORE2_R18_NEXT_THREE_EXAM_BATCHES_PRIVATE_REVIEW_20261101.zip`.

---

## 3. People and agents

| Name | What it is | Where | Role now |
|---|---|---|---|
| **Owner** | The human | — | Decides everything that is accepted, admitted, released or merged |
| **Oracle** | This Claude Code session (Opus) | `D:\CodeD\grade9v4` | Owns the outcome. Plans, briefs, checks pages itself, reports. Stand-in for the Owner. |
| **Local builder** | Claude subagent (Opus), background | Writes only in its own output folder | Builds reader versions (R2, R3) and runs the browser checks |
| **Source helper** | Claude subagent (Sonnet), background | `WPE_Core2_M39_Source_20261101/` | Finds official papers and keys on the web, read-only |
| **B2-G9v4** | New ChatGPT agent: **independent checker** | https://chatgpt.com/c/6ae689c7-e5ac-83ed-8882-71b8112343d7 | Sealed blind solves; checks the physics and the learner view. Never builds. |
| **A1-G9v4** | Outgoing ChatGPT agent | https://chatgpt.com/c/6ae5c904-9d6c-83ed-b811-466ede6b0763 | Retired after its R19 process check. **Do not give it new work.** |

The ChatGPT agents **cannot see local files**. Paste the text in (method in §6, step D).

---

## 4. Every working file from this session

`workspace/` is private and Git-excluded. **Never `git add` anything under it.**

### 4.1 Oracle files (outside the repo)
| File | Ext | Purpose |
|---|---|---|
| `C:/t/handover/G9V4-STORY.md` | .md | **The project story**: Owner intent with quotes, road map, timeline, decisions. Re-read it first after any compaction. |
| `C:/t/handover/G9V4-RUNBOOK.md` | .md | Draft buddy-runner runbook for checking A1's PR returns. Not agreed; parked now that A1 is retired. |
| `C:/t/handover/G9V35-STORY.md` | .md | The older v3.5 story, which holds the Owner's own words up to 29 Oct |

### 4.2 Repo root
| File | Ext | Purpose |
|---|---|---|
| `ORACLE_HANDOVER_20261101_CLAUDE.md` | .md | This note |
| `ORACLE_CHECKPOINT_20261101.md`, `ORACLE_HANDOVER_20261101.md` | .md | The Codex Oracle's notes (background; heavy on codes) |
| `index.html` | .html | V4 home page. This session added the R3 and R2 links above R1. Backup of the earlier version: `R2/review/V4_HOME_BEFORE.html` |
| `Start_here.md`, `AGENTS.md` | .md | Repo rules: Physics/Maths/Chemistry scope, fail-closed, "No academic approval inferred from software validation" |
| `WPE_Source_to_Core1A_Concept/CONCEPT_REPORT.md` | .md | The concept: two routes (question bank and book) meet at Core1A |

### 4.3 R19 review of the last 5 picks (`workspace/output/WPE_Core2_R19_20261101/`)
| File | Ext | Purpose |
|---|---|---|
| `BRIEF.md` | .md | The brief the Oracle gave the reviewer agent |
| `R19_REVIEW.md` | .md | Full review **with question text** (private) |
| `R19_REGISTER.csv` | .csv | One row per ID: cell, physics vs key, gate |
| `R19_FOR_A1.md` | .md | The same findings **without** question text, safe to paste into a chat |
| `PROCESS.md` | .md | What was read and in what order; solve-before-key evidence |

### 4.4 Reader R2: first exam question (`workspace/output/WPE_Core2_Reader_R2_NSEP_20261101/`)
Kept as history; R3 supersedes it. Same layout as R3 below, plus `prepare_r2.py`, which copied R1 and added the NSEP card.

### 4.5 Reader R3: current learner page (`workspace/output/WPE_Core2_Reader_R3_HintsFirst_20261101/`)
| Path | Ext | Purpose |
|---|---|---|
| `rendered/core2.html` | .html | **The learner page.** Open this. |
| `rendered/index.html`, `rendered/render-receipt.json`, `rendered/css/`, `rendered/js/` | .html/.json/.css/.js | Renderer outputs |
| `native/textbook-bank.json`, `textbook-intake.json` | .json | The 8 textbook cards |
| `native/synthetic-*.json` | .json | The 1 synthetic control card |
| `native/nsep-bank.json`, `nsep-intake.json` | .json | **NSEP Q57 card data (new).** Use it as the template for the next exam card. |
| `native/manifest.json`, `records.json` | .json | Build manifest and records that bind all banks |
| `assets/*.svg` | .svg | Figures. `incline-block-corrected-r2.svg` has the 37° label moved clear. |
| `build_reader.py` | .py | Build wrapper (20 lines) |
| `runtime/` | dir | **Private copy** of the Shared renderer + KaTeX/CSS. `runtime/Shared/tools/render_core.py` is patched. |
| `patch_renderer.py` | .py | Applies the hints-first patch to the renderer **copy** |
| `browser_check.js`, `run_browser_check.js` | .js | 47 headless-Chromium checks; the runner serves `rendered/` on 127.0.0.1 |
| `review/BUILD_COMMAND.json` | .json | Exact build command and renderer hashes (before 0ec1acc7…, after cc236ecf…) |
| `review/BUILD.log`, `BROWSER_CHECKS.log`/`.json` | .log/.json | Proof |
| `review/DELIVERY_REPORT.md` | .md | Benchmark-form report |
| `review/RENDERER_CHANGE.md`, `render_core.diff` | .md/.diff | What changed in the renderer copy, marked "candidate, not installed" |
| `review/REVIEW_RECORDS.json` | .json | Holds, waivers, the Owner's APPLY D2 decision, the 61/611 note. **Keep admin text here, never in learner text.** |
| `review/*.png` | .png | Screenshots: NSEP card before and after the attempt, hints open, full answer open, incline label |

### 4.6 Read-only sources you will need (never edit)
| Path | What |
|---|---|
| `workspace/output/WPE_Core2_Reader_Fix_R1_20261031/` | Reader R1, the Owner's benchmark build. **Never edit.** |
| `workspace/legacy/g9v3.5/qrt/sources/examside-wpe-extract.json` | Extract of 62 exam questions (third-party text and explanations) |
| `workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Candidate_2026-10-30/data/registry.json`, `raw_intake.json` | Registry of the exam candidates (EX-M…, WEP07-03) |
| `workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Academic_Review_R1_20261031/` | Sealed blind review R1; CORRECTION_NOTICE.md; RECONCILIATION_REPORT.md |
| `workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Evidence_Audit_R1_20261030/` | NSEP crop and official solution page |
| `workspace/subjects/physics/blueprints/physics-blueprint.D3-D4.resolved.v0.2.0.json` | Physics Blueprint, D3/D4 cells only |
| `workspace/legacy/g9v3.5/chatgpt/output/WPE_D3_Organized_2026-10-30/packages/` | Per-cell adapter drafts (D3.1–D3.7); none selected by the Owner |
| `chatgpt/*.zip` | Packages A1 delivered (R13–R17); review only |

---

## 5. Methodology: the loop for one exam question

Do **one question at a time**, with **one line of work**. Each pass through the loop ends in the benchmark output.

```text
Pick (Owner) → Source and official key → Sealed blind solve(s) → Cell (QRT)
   → Build card into a NEW reader version → Browser checks → Oracle opens it and tries it
   → Independent page check → ONE repair round max → Report in benchmark form → Owner decides
```

The rules that never bend:
1. **Never edit an earlier reader version.** Copy it to a new dated folder (R4, R5 …).
2. **Never edit the canonical Shared renderer.** Change only the private copy in `runtime/`, and record the diff.
3. **Never put question text, options, keys, figures, Drive links or learner data into Git, a PR or any public place.** ChatGPT chats on the Owner's own account are acceptable for review.
4. **Blind means blind.** Give the solver the question with **no key and no prior answer**. (This session's R19 brief leaked one key, and that solve had to be marked not blind.)
5. **Third-party answers are not keys.** Only NTA's or IAPT's official final key counts as VERIFIED.
6. **The Owner decides:** acceptance, admission, release, merges, renderer installation, scope.
7. **Status words:** HOLD for anything missing; NOT_RUN for anything not run; never APPROVED. Write "No academic approval inferred from software validation." in reports.
8. **One repair round.** If something is still wrong after it, stop and ask the Owner.
9. **Check it yourself.** Open the page and click through it as the learner would before you tell the Owner it is done.

---

## 6. Step-by-step procedures

### A. Find the question's source and official key
1. Look up the ID in `registry.json` and `examside-wpe-extract.json` (search for `"EX-M39"`). Note:
   - exam, date and shift;
   - question type;
   - whether there are figures;
   - `key_kind` (`UNRESOLVED` means there is no key).
2. Search the official site: for JEE Main this is `jeemain.nta.ac.in`, which publishes the **final answer key** as question ID → correct option ID. Then find a copy of the paper showing the **NTA question ID and option IDs** for that shift (coaching sites republish them).
3. Map question ID → official option ID → option text.
   - **VERIFIED** only when that chain is complete.
   - **PARTIAL** when only coaching answers exist, or the IDs can't be mapped.
   - **NOT_FOUND** otherwise.
4. Write `SOURCE_CHECK.md` in a dated folder under `workspace/output/`, with every URL and what each one shows.

### B. Sealed blind solve (checker B2 in ChatGPT)
1. Send B2 the stem and options only, plus:
   - "Reply with: answer and derivation; assumptions and ambiguity; deciding move, kind of thinking, 5 factor scores and level; the two most likely learner wrong routes."
2. Compare its answer with the official key. Record AGREE or DISAGREE.
3. If B2's cell differs from earlier reviews, **do not settle it yourself.** Record both views and ask the Owner (that is how NSEP Q57 became APPLY D2).

### C. Build the card into a new reader version
1. `Copy-Item -Recurse` the current reader folder (R3) to `workspace/output/WPE_Core2_Reader_R4_<Short>_<YYYYMMDD>/`. Update the paths inside `build_reader.py`, `BUILD_COMMAND.json` and `run_browser_check.js`.
2. Make new `native/<name>-bank.json` and `<name>-intake.json` **copied from the `nsep-*` files**, with the same fields:
   - exact stem and options from the source, with maths in KaTeX;
   - answer type (single or multiple correct);
   - the official key;
   - a hint ladder (H0 representation, H1 first move, …);
   - the worked solution steps (Represent / Connect / Calculate, each with Uses / Why valid / Result);
   - a common wrong route, taken from B2's answer;
   - the difficulty sentence;
   - a waiver reason in the review records if there is no figure.
3. Register the new bank in `native/manifest.json` and `records.json`, following how `nsep-bank.json` is registered.
4. Title format: `<Exam> <Year>, <Q-no> (<Body>) · <KIND> · <Level> · candidate, independently unreviewed`. Keep the last part until the Owner changes it.
5. Build: `python -X utf8 -B <R4>/build_reader.py build --manifest <R4>/native/manifest.json --out <R4>/rendered --draft --reference`
   - Use the Python that has `jsonschema` installed: `C:\Users\reall\AppData\Local\Python\pythoncore-3.14-64\python.exe`. The default `python` lacks it, and the first build failed for that reason.
   - Exit code 0 is required. Save the log to `review/BUILD.log`.
   - If it fails, fix the **inputs, never the renderer**. Allow at most 2 rounds.

### D. Browser checks
1. Run `node <R4>/run_browser_check.js`. It uses `playwright-core` 1.52 from `C:/Users/reall/AppData/Local/Temp/pw-1.52.0/node_modules/playwright-core` (or the `PW_CORE` environment variable) and serves `rendered/` on 127.0.0.1.
2. All 47 existing checks must still pass. Add checks for the new card:
   - it renders, and its maths is typeset;
   - hints open one per click;
   - the full answer stays locked before an attempt;
   - a blank attempt is refused;
   - after an attempt, the full answer still needs its own button;
   - state survives a reload;
   - no sideways scroll at 375 px and 1365 px.
3. Save the screenshots to `review/`.

### E. The Oracle's own look (mandatory)
1. Open the page in the built-in browser with `preview_start` and the `file:///…/rendered/core2.html` URL. **Use a fresh tab after every rebuild.** Reusing a tab showed a stale snapshot of the old page.
2. Clear storage, find the new card, open one hint, try the full answer before an attempt (it must refuse), make an attempt, press the full-answer button, and read the working.
3. **Trust what is on screen**, not element-height tests. Text inside closed sections still measures as visible in this pane, which gave a false alarm this session.

### F. Independent page check (B2)
Paste the card's learner-visible text in order: title, chips, stem, options, hints, wrong route, steps. Ask for:
- physics or working errors;
- learner-facing problems, each with its fix;
- whether the teaching order suits a Grade 10 learner;
- a verdict of PASS, PASS WITH FIXES or FAIL.

Send the card-level fixes to the builder in **one** round. Renderer-wide items go to the Owner.

### G. Pasting into ChatGPT (built-in browser)
1. Navigate the tab to the chat URL and wait about 3 seconds.
2. In the javascript tool:
   - focus `document.querySelector('.ProseMirror')`;
   - dispatch a `ClipboardEvent('paste')` whose `DataTransfer` holds the text (typing turns newlines into sends);
   - check that `innerText.length` equals the message length.
3. Send with `[data-testid="send-button"]`. If that button is missing, click the round arrow at the bottom right of the composer.
4. Verify: the composer is empty and the message appears in the chat.
5. Poll for the reply with a loop of up to about 110 s that waits until `[data-testid="stop-button"]` disappears, then read the text after the last "ChatGPT said:".

### H. Link it and report
1. Back up `index.html` into `review/`, then add the new link **above** the older ones. Keep the old links.
2. Report to the Owner in benchmark form (§1.4): link, 3–5 bullets, proof, still open. No codes.
3. Add one line per decision or finished step to `C:/t/handover/G9V4-STORY.md`.

---

## 7. The next steps, in order

1. **The M39 key result is PARTIAL, so ask the Owner first.** The options are:
   - (a) build the card with the coaching key marked HOLD;
   - (b) first rule out the dropped question 533543501, by finding a paper copy with NTA question IDs (try MathonGo or a candidate response sheet) or by having the Owner provide one;
   - (c) pick another question.

   Do not build before the Owner answers.
2. Build **R4** = R3 + the swing question card, following procedures C to E.
   - Use B2's wrong routes for the hints and the wrong-route note: a = g (or g cos θ) at the extreme position; adding g to v²/L at the bottom.
   - Cell: SYNTHESIZE · D3 (7/10). Three independent solves give B.
3. B2 checks the learner view (F). Do one repair round at most.
4. Link R4 on the home page and report to the Owner (H).
5. Then ask the Owner for the next decision. The options are:
   - admit NSEP Q57 and the swing question after the Owner looks at them;
   - fill the 7 vacancies;
   - the renderer-wide wording;
   - installing the hints change in Shared.

## 8. Pitfalls already met (don't repeat them)
- Writing a brief that states the key, which ruins a blind solve.
- Treating "79 collected" or "9 rendered" as questions done.
- Calling "79 reconciled into 78" verified without the ledger.
- Reusing a browser tab after a rebuild, which shows a stale snapshot.
- Using the default `python`, which lacks `jsonschema`.
- Copying default chips from another card, which gave the NSEP card a wrong concept and family at first.
- Locking a behaviour the Owner never asked to lock: R3 first locked hints before an attempt, and the Owner reversed it.
- A1's stacked draft PRs (11–18) sit on the **public** Grade9v4.0 repo. Nobody has checked them for leaked question text; do that before any merge.

No academic approval inferred from software validation.
