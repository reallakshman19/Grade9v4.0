# P0.5b — Immutable WPE v1 → three-subject v2 migration and Shared subject dispatch

**Status:** Engineering preview implemented in [draft PR #9](https://github.com/reallakshman19/Grade9v4.0/pull/9). **Actual Shared canonical subject integration:** NOT IMPLEMENTED. **Subject qualification and learner release:** HOLD.

This work follows [Issue #8](https://github.com/reallakshman19/Grade9v4.0/issues/8). Grade9 v4.0 is for **Physics, Mathematics and Chemistry**. WPE is the first Physics pilot. Neither this preview nor a successful v2 schema check establishes a Maths/Chemistry Blueprint or licensed content.

## 1. Immutable v1 reference-map preview

```bash
python -m pip install -e ".[dev]"
grade9qa migrate-v1-preview \
  --bundle examples/wpe-n01-candidate/bundle.json \
  --manifest examples/three-subjects-candidate/manifest.json \
  --out out/wpe-v1-v2-migration-report.json \
  --candidate-out out/wpe-v2-preview.json
```

The CLI reads the ORIGINAL v1 bundle and all six referenced record collections, validates v1 typed records with existing v1 code, strictly rejects ambiguous duplicate JSON keys and nonfinite JSON numbers, and checks the exact file and original source-asset bytes. It does **not mutate or overwrite** any original v1 asset or the v2 input manifest.

- The report preserves **original IDs/statuses**, per-file byte SHA-256, v1 original-record canonical JSON digests as derived observations (not native reviewer signatures), and the explicit proposed `PHYSICS/WEP-01/<original-id>` mapping.
- The optional `--candidate-out` file contains the *candidate* v2 intake manifest with mapped **sources/warrants/constructions only**. It does **not** contain the full original textbook/exam text or teaching content.
- Original `lessons`, `assessments` and `approvals` retain v1 custody. Their reference mapping is listed as **NOT_MIGRATED**; no original authority is promoted.
- Existing v1 `APPROVED` claims, absent or changed original source bytes, bad references and invalid v1/v2 schemas prevent an installable candidate preview. No status is silently downgraded or upgraded.
- The original v1 `PHYSICS-D3D4@0.2.0-CANDIDATE` and `WPE-PILOT@0.1.0-CANDIDATE` identities **do not match** the later `PHYS-QRT-BLUEPRINT` and `PHYS-TOPIC-WPE` candidate pins. Both aliases remain explicit HOLD for independent Owner review, not auto-mapped equivalence.

The fixture's original `synthetic-note.txt` is an **authored synthetic test source**, not an authenticated Physics textbook or exam. Successful byte validation only proves consistency with the local v1 claim.

The preview never calls `Shared/library/intake.py`, `Shared/library/promote.py`, or `Shared/tools/release_authority.py`; it explicitly reports `shared_canonical_admission: NOT_PERFORMED`.

## 2. Native Shared subject discovery is a separate authority boundary

The original source `Shared/tools/check_subjects.py` discovers subjects by finding `<subject>/adapter/CoreContracts.json` in the **full repository root**. It checks that subject's Core contract, native gates/library, and existing Shared semantics. It has no hardcoded Physics/Mathematics/Chemistry list.

Run in a trusted local workspace containing the *original* Shared platform **and actual subject directories**:

```bash
python -B Shared/tools/check_subjects.py > /local/native-subject-check.json
grade9qa shared-dispatch-audit \
  --manifest out/wpe-v2-preview.json \
  --native-report /local/native-subject-check.json \
  --bindings /local/subject-directory-bindings.json \
  --out out/shared-subject-dispatch.json
```

Bindings are **explicit** and source-grounded, such as `{"PHYSICS":"<actual-subject-directory>"}`; the application does **not guess** that Mathematics is `Maths`, `Math`, etc. Use a real directory from Shared's actual report, not the angle-bracket placeholder.

**Observed on the standalone Owner-supplied `Shared.zip` on 2026-10-31:** `{"subjects_checked":0,"subjects":[],"passed":false}` and native exit code 1. The archive does **not** include the complete subject workspaces. This is an honest HOLD, not evidence of deployed subjects or a subject-level failure in a complete repository.

The read-only adapter rejects contradictory native subject counts/rows, invalid directory bindings, native findings, and cross-subject alias collisions. A native `CONTRACT_ONLY` subject is not promoted to `IMPLEMENTED`. Missing subject workspaces or independent binding stay HOLD. Even a `passed:true` input is an **untrusted JSON execution claim**, not independently authenticated reviewer or Shared canonical promotion evidence.

## 3. Candidate and authority outcomes

| Condition | Migration/dispatch disposition |
|---|---|
| Verified local v1 bytes and matching scoped candidate references | mechanically compatible candidate; **qualification HOLD** |
| Historical v1 status `APPROVED` | migration preview withheld until independently reviewed authority mapping |
| Missing original source file | HOLD, no preview output |
| Mutated source hash or invalid old/new reference | FAIL, no preview output |
| Unresolved old/new Physics Blueprint or adapter alias | HOLD; cannot certify semantic identity |
| No installed subject discovered in standalone Shared archive | HOLD, not fabricated |
| Native subject report with adverse findings or inconsistent rows | FAIL |
| Apparently complete native report or claim of an approved subject | **still HOLD without trustworthy original receipts** |

Exit codes: **1** structural or provenance contradiction; **2** IO/invalid JSON/unsafe overwrite attempt; **3** compatible or incomplete **HOLD**. There is **no automatic 0/PASS** for migration or release.

## 4. What remains before subject-level readiness

1. Confirm complete and independently trusted Shared baseline, distribution rights, and pinned original source/canonical records.
2. Install **actual subject workspaces** with `adapter/CoreContracts.json` for approved Physics, Mathematics, Chemistry scoped sources, rather than inventing them from the Shared ZIP alone.
3. Run Shared's native subject checks on those full workspaces and separately review all findings.
4. Independently approve legacy WPE QRT/Blueprint/adapter identity aliasing, then bind exact reviewed native Physics source/warrant and Smart R2 records.
5. Create separate Mathematics and Chemistry subject-specific Blueprint and source adapters from Owner-authorized material; select topics rather than fabricate examples.
6. Preserve all v1 external examination rights/figure/key custody, QRT adjudication, genuine Core1A/Core1B teaching/assessment evidence, B1–B7 and native Shared review/promotion receipts.
7. Run real learner/runtime tests with protected answer state and subject-authorized release.

**Do not label a candidate v2 manifest as an accepted Shared library package. No academic approval inferred from software validation.**
