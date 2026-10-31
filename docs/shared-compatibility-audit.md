# P0.2 Shared compatibility audit — independent external baseline

> **Scope:** read-only compatibility audit for the supplied `Shared.zip` (292 files). It is NOT imported into this public repository.

## Evidence checked

- SHA-256 of the uploaded `Shared.zip`: `16b6fba6c349923d1744badf0c53f5debdbbe4e25eae7f02413a7baeee76667b`.
- The archive has **310 ZIP entries** (18 directories, 292 files). `docs/shared-baseline-pins.json` records **16 critical files** with exact byte hashes and sizes; **this is not a complete 292-file signature manifest**.
- A direct local run of the supplied `Shared/tools/core_authority_contract.py` returned `passed: true, roles_checked: 6, findings: []`. This execution is a source-archive smoke test, **not** an independent audit or publisher signature.
- No top-level `LICENSE` or `COPYING` file was found in `Shared.zip`. Do not republish the 292 files until the Owner confirms rights, confidentiality and dependency safety.

## Audit CLI (read-only)

```bash
grade9qa shared-audit --shared-root /path/to/extracted/Shared --out out/shared-audit.json
```

The command checks selected file pins, the role/authority JSON embedded in the existing Shared contract, Shared cognitive vocabulary, and Grade 9 Physics policy. It **does not import, mutate, execute, or replace Shared code**. A mechanically consistent snapshot returns exit code **3 (HOLD)** because independent baseline acceptance and actual integration are outstanding. Missing files give HOLD; changed pinned bytes or contradictory authority declarations give FAIL/exit 1.

To override the baseline for fixture tests, pass `--baseline /path/to/fixture-pins.json`. Do not treat an arbitrary override as Owner approval.

## Shared vs. Grade9QA overlap matrix

| Grade9QA / initial #1 | Existing Shared authority/function | Decision | Risk / follow-up |
|---|---|---|---|
| `io.py`, `sha256.py` | `Shared/contracts.py`: digest, canonical, path/refs | **Adapter** | Match digest encoding and exact JSON canonicalization; don't produce two scientific proofs |
| `schemas/v1/*.json` | `Shared/library/package.schema.json`, role-specific and source schemas | **Temporary intake DTOs** | Avoid parallel canonical records; add explicit shape mapping and version pin |
| `traceability.py` | `Shared/library/intake.py`, `Shared/library/compile_inputs.py`, `Shared/contracts.py` | **Reuse canonical checks** | Do not double-authorize canonical identity |
| `demand.py` and QRT fields | `Shared/vocabularies/cognitive-demand.v1.json`, `Shared/quality/question-demand-matrix.v1.json`, `Shared/tools/qrt_pipeline_guard.py` | **Read/translate only** | A five-factor total checks rubric arithmetic, not adjudication |
| `gates.py` | `Shared/tools/review_authority.py`, `Shared/tools/release_authority.py`, `Shared/assurance/` | **Do not duplicate** | Independent digest-scoped review receipts remain authoritative |
| `bridge.py` | `Shared/library/core1a_construction.py`, `core1b_reconstruction.py`, `Shared/roles/CORE1A.md`, `CORE1B.md` | **New extension** | B1–B7 directional teaching/transfer *witness*; needs academic review |
| `smart_skills.py` | R2 native skills + Shared QRT guard | **Read-only adapter** | R2 native PASS or SL2 PROPOSED is not QRT/learner release |
| `report.py` | `Shared/assurance/aggregate.py`, `Shared/tools/academic_readiness.py` | **Adapter** | No competing issue of review/release authority |

## Authority graph vs. operational order

`Shared/roles/CORE-AUTHORITY-CONTRACT.md` states: **execution order is not derivation order**. Specifically:
- `CORE1`, `CORE1A`, `CORE1B`: `CANONICAL_ACADEMIC_TRUTH`.
- `CORE2`: `AUTHORIZED_SOURCE_CUSTODY`.
- `CORE2A`: canonical truth **plus** eligible reviewed demand or truthfully authored practice.
- `CORE2B`: canonical truth + prior exposure + reviewed demand or authored practice.

The earlier master Issue #1 described a **Core2 approval prerequisite for Core1A authoring**. Keep it as a *scoped WPE pilot workflow proposal* pending Owner confirmation, **not** an unconditional platform rule. Shared explicitly permits source-custody research to continue without blocking canonical Core1-family work.

**Policy reconciliation:** `Shared/policy/grade9-physics.v1.json` classifies `WORK_ENERGY` as `PREREQUISITE`. The WPE/JEE bridge must be an additive programme-level route; do not rewrite Shared's Grade 9 scope policy.

## Preconditions for importing Shared source into GitHub

- [ ] Owner supplies explicit licence/redistribution decision for the 292-file baseline.
- [ ] Run security/privacy/source-path/dependency checks before public import.
- [ ] Independently verify the **complete** upstream archive signature or trusted owner pin.
- [ ] Run *all* applicable native Shared smoke tests against a complete project root, not only the authority-contract checker.
- [ ] Obtain Owner sign-off on authority/workflow graph and WPE/JEE bridge classification.
- [ ] Replace redundant Grade9QA functions only through versioned adapters and regression tests.
- [ ] Validate native Smart Skills R2 integration separately; don't conflate this with Shared acceptance.

**Outcome:** P0.2 audit implemented as a reproducible local evidence check; **platform integration and academic approval remain HOLD**.
