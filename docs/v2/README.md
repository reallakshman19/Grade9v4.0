# Versioned three-subject candidate intake — PR #7

**Grade9 v4.0 product scope:** Physics, Mathematics and Chemistry. **WPE is only the Physics pilot**, with WEP-01 the first target construction/topic inside WPE.

## Status and authority

This PR implements **P0.5a, mechanical intake validation only**. The native Shared canonical platform, native SL1/SL2 Smart Skills, independent QRT adjudication, specialist subject Blueprints, per-construction B1–B7 reviews, reviewer authorization and release decisions remain separately governed.

- `schemas/v2/subject-intake.schema.json` is **not** a replacement for `Shared/library/package.schema.json` and does not authenticate its digest strings.
- `schemas/v1/*` are unchanged; v1 WEP-only schema and existing synthetic Physics/WPE fixtures continue working.
- `examples/three-subjects-candidate/manifest.json` registers PHYSICS (WPE/WEP-01 candidate), MATHEMATICS (PLANNED, no Blueprint or topics), CHEMISTRY (PLANNED, no Blueprint or topics). The Physics pins refer to owner-supplied candidate artifacts, not independent trusted signatures.
- `grade9qa subjects-audit` is a structural/namespace check. A mechanically PASS output is **always** academic HOLD and release HOLD.

## Run

```bash
python -m pip install -e ".[dev]"
grade9qa subjects-audit --manifest examples/three-subjects-candidate/manifest.json --out out/subjects.json
python -m pytest -q
```

Expected candidate: mechanical PASS, academic HOLD, exit **3**. Invalid schema, subject/adapter conflicts, cross-subject links, incorrect typed references or construction prerequisite cycles: mechanical FAIL, exit **1**. IO error: exit **2**.

## Contract boundaries

| Field / rule | What the candidate intake checks |
|---|---|
| `subjects[*].subject_id` | PHYSICS, MATHEMATICS, CHEMISTRY — explicitly all registered |
| `stage` | PLANNED subjects cannot claim active Blueprint or topics; active subjects require both |
| `blueprint_ref` | Separate subject-id, artifact-id, version and 64-digit SHA256 pin |
| `adapter_ref` | Correct subject/topic identity and exact same Blueprint SHA256 |
| `topic_id` | Subject-local namespace (e.g. Physics WEP-01); **not** a universal WEP-only regex |
| `sources`, `warrants`, `constructions` | Subject/topic-local raw stable IDs; typed records, candidate statuses |
| `<subject>/<topic>/<record-id>` references | Cross-subject dependency **rejected**, missing/wrong-type refs rejected, same-subject cross-topic prerequisites allowed |
| `prerequisite_refs` | Typed reference resolution and cycle detection |
| `operation`, `band` | Seven shared operation labels and D1–D4 bands; **not** independent academic calibration |
| `grade_track` | G9_FOUNDATION, G10_STRENGTHENING, JEE_BRIDGE; separate from operation/demand |
| `status` | No self-declared APPROVED record can authorize a release; this candidate contract excludes it |

All example source/warrant/lesson counts are **candidate** counts. No Mathematics or Chemistry topic is nominated, and no subject may inherit Physics correctness/approval.

## v1 → v2 migration: unimplemented, requires a separate reviewed plan

1. **Preserve** every v1 WEP-`NN` stable ID, file SHA, status and source locator as historical evidence; never rewrite existing records in place or regenerate original native digests.
2. Record the subject mapping `PHYSICS` and the WPE unit separately from `WEP-01` scoped topic IDs. Maintain explicit old-ID/new-qualified-reference mapping, e.g. `PHYSICS/WEP-01/<legacy-id>`.
3. Map v1 `blueprint_ref`, `adapter_ref`, sources and warrants to independently verified subject-scoped pins. Do not copy Physics-specific `physics_claim`, `sign_convention` or force/potential direction enumerations into generic Maths/Chemistry schema fields.
4. Bind the v2 intake to **actual** native Shared canonical subject records/receipts; establish source authenticity and subject reviewer scopes independently.
5. Migrate historical B1–B7 witnesses only with an explicit version and approved transformation mapping; schema validation alone does not certify teaching equivalence.
6. Add first Mathematics and Chemistry native subject Blueprint, topic adapter, warrants and qualified examples **only once the owner supplies/selects them**.
7. Run subject-specific Physics, Mathematics, Chemistry tests and real learner/runtime validation before claiming three-subject readiness.

**Cross-subject links:** v2 candidate intake rejects them; a future explicit, reviewed cross-subject prerequisite mechanism is required rather than silently allowing them.

**Exit policy:** 0 is not returned by this candidate command. Successful mechanical checks still return HOLD/3.

No academic approval inferred from software validation.
