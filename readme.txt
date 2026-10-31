Grade9 v4.0 — Academic workflow and Smart Skills integration
Version: 2026-10-31 / candidate integration design
Master issue: https://github.com/reallakshman19/Grade9v4.0/issues/1
Draft PR: https://github.com/reallakshman19/Grade9v4.0/pull/2

PRODUCT SCOPE — 2026-10-31 CORRECTION
===================================
Grade9 v4.0 is a planned Physics + Mathematics + Chemistry learning platform.
WPE is ONLY the Physics pilot topic. The Physics Blueprint is not a generic
Blueprint for Mathematics/Chemistry, and WEP-01 cannot certify the whole app.
Shared, Smart Skills, QRT governance, the six Core roles, B1–B7 and release
evidence should be reusable; subject Blueprints, warrants, demand calibration,
topic adapters, exams and academic approvals are separately qualified.
The workflow below illustrates the WPE Physics PILOT, not the only product flow.
See docs/product-scope.md for planned v2 schemas and subject adapters.

1. Correct workflow placement
=============================

Shared platform + canonical source library
    |
    v
Smart Labelling 1 (SL1) — original question identity, source/figure/key
custody, prerequisites, source fitness, learner-safe first-try card
    |
    +---- Optional P1: actual independently saved first attempt (never required
    |     to read instruction or to perform QUESTION-mode labelling)
    v
Smart Labelling 2 (SL2) — independently proposed decisive reasoning route,
competing cognitive operations, five-factor demand evidence, optional real
learner observation; still UNREVIEWED/PROPOSED
    |
    v
QRT independent adjudication — independently judge operation, D1–D4 task
demand, direct-exam vs prerequisite-bridge vs authored-transfer role
    |
    v
Qualified Physics warrant + WPE topic adapter + construction binder —
pin scientific assumptions, current Blueprint/adapter, task/family identity,
actual teaching/reconstruction spans and independent B1–B7 bridge review
    |
    v
Core1A complete teaching -> Core1B fresh independent reconstruction

Core2 question admission is a separately governed source/key/question
promotion process; teaching sequence does not redefine academic authority.
Grade9QA checks consistency and approval evidence ACROSS these stages;
it is NOT an SL1/SL2/QRT replacement and cannot self-issue approval.

2. Authority and separation of duties
=====================================

- Shared owns common platform contracts, role policies and runtime foundation.
- SL1 owns source/question identity and first-try/source fitness, NOT final
  cognitive difficulty certification.
- SL2 owns a CANDIDATE cognitive proposal and optional truthful observation,
  NOT independent QRT adjudication or mastery certification.
- QRT owns independent cognitive adjudication and question coverage role.
- Physics warrants and WPE adapter own the scoped physical truth and lesson
  construction requirements, subject to independent scientific acceptance.
- Core1A teaches; Core1B independently tests a fresh but equivalent operation.
- Grade9QA is a read-only integration/qualification visibility layer.
- Core2, Core2A, Core2B and Core1 retain their Shared-defined role contracts
  even when a particular WPE pilot implements a narrower sequence.

3. Current source baseline and readiness
========================================

- Provided source: SMART_LABELLING_QRT_HARDENING_R2_CANDIDATE(2).zip.
- Two native candidate skill directories exist under archive skills/:
  smart-labelling-1 and smart-labelling-2, both v2.0.0-candidate.
- Archive holds source, standard-library checkers, contract helpers,
  fixtures, 90-case regression suite, manifest and historical review data.
- Its author-side report records 90/90 passing tests. The archive was also
  independently executed locally in this review environment: 90/90 passed.
- Archive manifest: 35/35 listed internal payload hashes matched on extraction.
  This checks payload identity under the supplied manifest; it is not an
  independently trusted publisher signature.
- Independent reviewer acceptance has NOT occurred here. Installation, actual
  learner acceptance, official PYQ certification and release remain HOLD.
- The complete native R2 skill source is staged locally from the uploaded ZIP
  and has NOT been committed to GitHub or enabled as an installed skill.
- The Shared ZIP, canonical Physics Blueprint and full WPE source collections
  are likewise not yet fully imported to GitHub.

4. Implementation dependency: P0.2 BLOCKED until Smart Skills review
======================================================================

Do NOT construct duplicate SL1/SL2 validators in src/grade9qa.
Before P0.2 source-custody/Physics qualification is called integrated:
[ ] Preserve versioned native R2 candidate and its exact hash manifest.
[ ] Review candidate source/privacy, license and redistribution boundaries.
[ ] Distinct reviewer independently checks source adapters, answer/figure
    custody, receipt trust and 90 regression results.
[ ] Bind Shared's existing authority contracts and pinned QRT vocabulary.
[ ] Introduce a read-only adapter for R2 check reports, preserving gate
    status (PASS/HOLD/NOT_APPLICABLE), source IDs and review identity.
[ ] Test that absent P1 is allowed, SL2 PROPOSED is not QRT approved, and
    native PASS never becomes student RELEASE_ALLOWED without separate gates.
[ ] Require B1–B7 and qualified Physics/teacher review downstream.

IMPORTANT: no hash, green CI check, proposed D3 label or candidate SL2
report authorizes academic approval or student release.

5. Upstream source pointers
===========================

SMART_LABELLING_QRT_HARDENING_R2_CANDIDATE(2).zip:
  STATUS.md
  R2_SHA256_MANIFEST.json
  skills/smart-labelling-1/SKILL.md
  skills/smart-labelling-2/SKILL.md
  skills/*/references/hardening-contract.md
  review/R2_IMPLEMENTATION_AND_REVIEW.md
  review/R2_AUTHORITY_AND_PROGRESS.json
  tests/test_hardening.py

Further detail: docs/smart-skills-integration.md

MULTI-SUBJECT ENGINEERING UPDATE — P0.5a
======================================
The version 2.0.0 three-subject candidate intake is added in draft PR #7:
  schemas/v2/subject-intake.schema.json
  examples/three-subjects-candidate/manifest.json
  grade9qa subjects-audit --manifest ... --out ...
Existing WPE v1 contracts remain unchanged. Maths/Chemistry are PLANNED with
no fabricated Blueprints or content. Scoped references cannot silently cross
subjects. Mechanical PASS is still academic HOLD; canonical migration and
independent subject-specific academic review remain pending.
