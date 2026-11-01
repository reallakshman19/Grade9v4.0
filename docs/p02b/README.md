# P0.2b: Shared full baseline and native authority receipts — engineering implementation

**Status:** implemented read-only candidate verification; Owner/independent acceptance **HOLD**.

**Source:** `Shared.zip` supplied by the Owner. SHA-256 pinned by prior PR #3:
`16b6fba6c349923d1744badf0c53f5debdbbe4e25eae7f02413a7baeee76667b`.
The uploaded ZIP has 292 regular files and 18 directory entries. A local full-byte comparison of the extracted snapshot matched 292/292 and found no extra extracted files.

## What this PR implements

`grade9qa shared-manifest` is a safe read-only command that inspects **every** ZIP file, fingerprints its contents, rejects duplicate names/case collisions, traversal, symlinks, encrypted/non-file entries and excessive sizes, compares the archive against the candidate SHA-256, and optionally compares all extracted files against their archive bytes. Results contain the entire deterministic manifest and remain `qualification_status:HOLD`.

`grade9qa shared-authorities` ingests **three native reports**, without replacing Shared's validators, executing untrusted code, or claiming the reports were actually produced by a trusted run. It checks whether six roles were verified and whether review/release receipts and findings are consistent. A vacuous native `passed:true` with `receipts:[]` becomes **HOLD with `REVIEW_NO_RECEIPTS` and `RELEASE_NO_RECEIPTS`**. A failed or contradictory receipt produces a mechanical FAIL. Native `verified:true` still does not grant Grade9QA authority.

## Reproduce locally (do not publish original source files)

1. Start from the exact Owner-supplied `Shared.zip`, and extract it to a local workspace to create `<workspace>/Shared/`. Check copyright, confidentiality and local execution trust before running any native script.
2. Install Grade9QA from its feature branch: `python -m pip install -e ".[dev]"`.
3. `grade9qa shared-manifest --archive <workspace>/Shared.zip --shared-root <workspace>/Shared --out out/shared-full-manifest.json`. A consistent **candidate** returns exit 3 (HOLD), not 0/release.
4. Only in an approved local environment, invoke the **original** validators from the extracted project root:
   ```bash
   python -B Shared/tools/core_authority_contract.py > core-authority.json
   python -B Shared/tools/review_authority.py --audit --enforce > review-audit.json
   python -B Shared/tools/release_authority.py --audit --enforce > release-audit.json
   ```
5. `grade9qa shared-authorities --core core-authority.json --review review-audit.json --release release-audit.json --out out/native-authorities.json`.
6. **Do not** treat zero receipts as readiness. Native JSON is a report **claim**, not an authenticated execution record. Bind exact subject-root paths, input artifact digests, trusted runtime and independently reviewed receipts in a subsequent phase before attempting release.

## Observed on Owner-provided local ZIP (2026-10-31)

- ZIP digest matches the pinned candidate value; full manifest: **292/292** source hashes matched against extracted files, 0 extra files.
- Native `core_authority_contract.py`: `passed:true`, six Core roles, zero findings.
- Native `review_authority.py --audit --enforce`: `passed:true`, **zero receipts**, zero findings.
- Native `release_authority.py --audit --enforce`: `passed:true`, **zero receipts**, zero findings, zero self-authorized manifests.
- QRT pipeline guard loaded via `--help`; **no actual QRT run record was supplied** for verification.
- Grade9QA new negative controls cover archive modification, unsafe ZIP paths, missing/extra files, valid-but-empty native reports, stale/failed receipts and self-authorization.

## Pending mandatory acceptance gates

- [ ] Independently signed/trusted Owner pin of original Shared snapshot and complete extraction evidence.
- [ ] Owner confirms redistribution/licensing and confidentiality; original 292-file Shared code remains external.
- [ ] Run and independently qualify the full native Shared suite in a complete Grade9 subject root; source ZIP alone lacks subject-specific runtime records.
- [ ] Bind Shared review/release receipts to their exact current canonical artifact digests and Owner-authorized reviewers, using Shared's **existing native verifiers**.
- [ ] Verify native SL1/SL2 R2 to QRT/Physics integration with scope-preserving IDs, no SL2 auto-promotion.
- [ ] Confirm that WEP-01 is `PREREQUISITE` under Grade 9 policy and scope any special JEE bridge authoring workflow independently.
- [ ] Add real learner browser tests and independently approved B1–B7 witnesses.

**No academic approval inferred from software validation.**
