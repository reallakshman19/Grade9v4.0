# P0.5c — Native Shared subject workspace preflight

**Status:** Read-only engineering checks implemented; **actual installed subject workspaces not supplied**. Mathematics and Chemistry still PLANNED; WPE remains the **Physics** pilot.

## Native ownership and rules

The existing `Shared/tools/check_subjects.py` discovers subjects via `<subject>/adapter/CoreContracts.json` in the complete repository root. The original check includes `check_contract`, `capability_audit`, gate-registry validation and library intake/promotion. **Do not replace it with Grade9QA**.

The preflight `src/grade9qa/subject_workspaces.py` independently inspects the *on-disk* directory layout and compares the results to Shared's own native discovery report. It is not an academic verifier. It never imports subject adapters, executes code or installs source material.

Run only against an Owner-authorized subject workspace:

```bash
# In a trusted full subject repository root:
python -B Shared/tools/check_subjects.py > /local/native-subjects.json

# Explicit mapping with the directory names actually returned by Shared:
# /local/subject-directory-map.json might contain {"PHYSICS":"Physics"}
grade9qa subject-workspace-audit \
  --manifest examples/three-subjects-candidate/manifest.json \
  --root /path/to/full-subject-repository \
  --bindings /local/subject-directory-map.json \
  --native-report /local/native-subjects.json \
  --out out/native-workspaces.json
```

`--native-report` is optional, but leaving it out is a review HOLD. Outputs may not overwrite original subject workspace files or supplied manifest/binding/native report. Exit **3** is candidate/HOLD, **1** indicates contradictory evidence, **2** invalid file/IO or unsafe overwrite. There is deliberately no automatic PASS/release.

## What is checked

- Exact explicit subject-directory mapping for the three subject IDs; rejects unknown binding subjects, path traversal, casefold collisions and subject-contract symlink escapes.
- Six named Core products exist in each active subject's `adapter/CoreContracts.json`. Examines `production` declarations and documented `NOT_COMPILED` reasons; tests validator-catalogue `result.comparison` and `does_not_prove` limitations.
- Reads native subject contract JSON with strict duplicate-key and nonfinite-number rejection; returns only its byte SHA-256 and sanitized evidence codes.
- Detects native subject `CONTRACT_ONLY` state, absent adapter module, empty gate registries and library packages, local/native count disagreements, claimed IMPLEMENTED without file evidence and native subject reports containing adverse findings.
- **PLANNED Mathematics/Chemistry require no native directories**. Existing unbound native directories are reported for explicit owner resolution, not silently mapped to `Math`, `Maths`, or other guessed names.
- Candidate native report `passed:true` remains an untrusted execution claim, not independently attested original Shared checks or publication authority.
- No source PYQ stems, chemical recipes, teaching passages, learner responses or contract internals are copied into audit outputs.

## Evidence from source-backed local smoke on 2026-10-31

The user-provided `Shared.zip` includes **292 Shared platform files but no actual subject directories**. The original `Shared/tools/check_subjects.py` on the standalone archive previously returned **0 discovered, exit 1**.

To test the original *native discovery mechanism*, I also ran the **unchanged native Shared checker** in an ephemeral **isolated, synthetic workspace**, containing a copy of that Owner-supplied Shared platform plus three minimal synthetic `adapter/CoreContracts.json` directories (`Physics`, `Mathematics`, `Chemistry`). Their adapter files had no `load()` and contained no curriculum, gates or library packages. The native result was:

```json
{
  "subjects_checked": 3,
  "subjects": [
    {"subject": "Chemistry", "state": "CONTRACT_ONLY", "gate_registries": 0, "library_packages": 0, "findings": []},
    {"subject": "Mathematics", "state": "CONTRACT_ONLY", "gate_registries": 0, "library_packages": 0, "findings": []},
    {"subject": "Physics", "state": "CONTRACT_ONLY", "gate_registries": 0, "library_packages": 0, "findings": []}
  ],
  "passed": true
}
```

The native program exited 0. **This proves discovery handles three synthetic subject contract directories, NOT that any subject is implemented or academically qualified.** The preflight correctly retains HOLD for such empty workspaces. None of these temporary synthetic subject directories is committed as a real platform subject.

## Tests and remaining acceptance

`tests/test_subject_workspaces.py` covers missing/forged contracts, native reporting contradictions, hollow IMPLEMENTED claims, unexpected subject directories, untrusted passing claims, zero curriculum, unsafe paths, symlinks, blank reasons, missing rights and no-source output leaks.

- [ ] Owner supplies actual **complete subject repositories**; currently only Shared platform archives and Physics/WPE candidate material are present.
- [ ] Independently approved source licences/custody and trusted Shared original baseline.
- [ ] Original native subject `check_subjects.py` runs in complete context and each relevant findings/registries/libraries undergo independent review.
- [ ] Truthfully implemented Mathematics and Chemistry source/topic adapters, blueprints, proof/chemical warrants, teaching and assessment.
- [ ] Correct native Shared canonical promotion and release authority receipts, not `APPROVED` metadata.
- [ ] Learner runtime protected-attempt checks and independent B1–B7 teaching equivalence before subject/course release.

**No academic approval inferred from software validation.**
