# Product scope — Physics, Mathematics and Chemistry

**Decision, 2026-10-31:** Grade9 v4.0 is a **three-subject learning platform** for **Physics, Mathematics and Chemistry**. **Work, Power and Energy (WPE)** is an initial **Physics-only pilot**, not the platform's content scope, generic schema, or final product.

This file supersedes any description of the whole application as a "WPE app" or "Physics app" in older planning text. It does **not** declare any Mathematics or Chemistry teaching content, source archive, or subject-specific QRT Blueprint to be present, qualified, or approved.

## Platform architecture (ownership boundaries)

```text
Grade9 v4.0 — multi-subject educational application
  Shared / canonical source and authority contracts / six Core roles
  Native Smart Labelling SL1 + optional P1 + SL2 / candidate source reasoning
  QRT cognitive vocabulary and adjudication workflow (common interface)
  Grade9QA evidence checks, B1–B7, provenance and noncompensatory HOLD/FAIL
  Learner runtime / protected attempts / publication and review authorities
          |
          +-- PHYSICS
          |     Physics subject Blueprint + Physics warrant library
          |     Topic adapters -> WPE (PILOT), then other Physics topics
          |     First reference qualification: WEP-01, within WPE
          |
          +-- MATHEMATICS
          |     Mathematics subject Blueprint + reviewed mathematical warrants
          |     Topic adapters -> first topic NOT YET SELECTED
          |     No approved mathematics Blueprint or content claimed
          |
          +-- CHEMISTRY
                Chemistry subject Blueprint + reviewed chemical warrants
                Topic adapters -> first topic NOT YET SELECTED
                No approved chemistry Blueprint or content claimed
```

**QRT distinction:** seven current operation labels are the proposed common interface, but the existing `PHYS-QRT-BLUEPRINT 0.2.0` is **Physics-specific** and draft. Never reuse its examples, rubric calibration, scientific assumptions or D3/D4 cells as if they automatically qualify Mathematics or Chemistry. Subject-specific operation interpretation, demand calibration, lesson witnesses and scientific/mathematical correctness need independent review.

**Smart Skills distinction:** SL1/SL2 roles and native source-review boundaries are reusable by contract; format adapters, source custody, answer keys and problem structures may vary by subject. No claim that the Physics native exam adapter already handles Mathematics or Chemistry.

**Scientific warrants:** Physics laws, mathematical definitions/proofs, and Chemistry laws/models require subject-appropriate expert checks. Treat `source_authenticity`, `content_correctness`, `cognitive_qualification`, `teaching_sufficiency`, `assessment_validity`, `implementation`, and `release_authority` as distinct noncompensatory evidence.

## Canonical namespace requirements for the next schema revision

The current `schemas/v1/bundle.schema.json` and `construction.schema.json` hardcode `topic_id` to `^WEP-(0[1-9]|10)$`. They are **WPE pilot contracts**. Do not simply change their regex in place and call the platform multi-subject; version and test a migration.

Proposed **v2 subject-neutral intake fields** (not yet implemented/approved):

| Field | Rule |
|---|---|
| `subject_id` | Required, one of `PHYSICS`, `MATHEMATICS`, `CHEMISTRY` |
| `topic_id` | Nonempty stable topic identifier qualified by `subject_id`, not a WEP-only pattern |
| `subject_blueprint_ref` | Version-pinned subject Blueprint; no shared Physics Blueprint assumption |
| `topic_adapter_ref` | Pinned adapter inside the selected subject |
| `construction_id` | Unique scoped construction; no accidental cross-subject ID collisions |
| `academic_track` | Instructional track separated from operation and D1–D4 task demand |
| `source_roles` and `review_scopes` | Subject-specific authorities using Shared's canonical governance; not invented by Grade9QA |

**Implementation update (2026-10-31):** [Draft PR #7](https://github.com/reallakshman19/Grade9v4.0/pull/7) introduces `schemas/v2/subject-intake.schema.json`, `grade9qa subjects-audit`, and an intentionally unqualified three-subject candidate manifest. This is an **intake envelope**, not a replacement for Shared's canonical schemas or a completed v1-to-v2 migration. The subject-specific Blueprints for Mathematics and Chemistry remain unknown/unapproved.

**Migration conditions:** maintain v1 support and its existing tests, add exact v2 schema validation/migration fixtures, reject unknown subjects and cross-subject references, preserve immutable source IDs and historical digests, and never silently widen `WEP` schema semantics.

Existing `grade9qa qrt-bind` is a **Physics/WPE-specific candidate binding CLI**. It is not the generic binding for all three subjects. The cross-subject interface must dispatch to subject adapters without modifying or weakening native QRT/Shared authority.

## Delivery plan and gates

1. **Platform hardening:** preserve Shared, SL1/SL2, QRT governance and generic B1–B7 semantics; document which currently committed validators are WPE-coupled.
2. **Physics/WPE pilot:** independently qualify one WEP-01 construction with actual Core1A and fresh Core1B tasks, scientific warrants, real browser protection and trusted reviewer receipts; hold until evidence exists.
3. **Subject-neutral v2 contracts:** implement subject identity and topic namespaces with positive Physics and synthetic Mathematics/Chemistry fixtures; no science claims inferred from synthetic fixtures.
4. **Mathematics subject adapter:** owner selects first topic and supplies sources; independently calibrate Blueprint/operations, proof correctness and teaching/reconstruction.
5. **Chemistry subject adapter:** owner selects first topic and supplies sources; independently calibrate Blueprint/operations, chemical models/conditions and teaching/reconstruction.
6. **Scale subject content:** expand qualified Physics topics and independently selected Mathematics/Chemistry topics; separately count qualified constructions, syllabus coverage and authenticated examination questions.
7. **Release:** per subject, per topic and per construction, require all applicable independent academic, provenance, learner-state and governance gates. No subject inherits another subject's approvals.

**Do not count WPE pilot completeness as product completeness.** No mathematics or chemistry curriculum coverage or academic approval is established by the current code.

## Suggested repository structure (design target; not all directories exist)

```text
Shared/                         upstream platform after rights/ownership clearance
skills/                         native owner-authorized SL1/SL2
schemas/v2/                     future subject-neutral contracts
src/grade9qa/                   shared evidence engine + subject dispatch
subjects/
  physics/
    blueprints/
    warrants/
    topics/wpe/                 pilot adapter and reviewed construction records
  mathematics/
    blueprints/
    warrants/
    topics/                     first topic not selected
  chemistry/
    blueprints/
    warrants/
    topics/                     first topic not selected
reference/                      source receipts and permitted public references
tests/
  platform/
  subjects/physics/
  subjects/mathematics/
  subjects/chemistry/
```

These are **planned** paths. The existing pilot contracts and tools remain in place until a versioned migration is implemented and tested.
