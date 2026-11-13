# Smart Labelling 1 / 2 → QRT → WPE integration (R2 candidate)

> **Status: candidate, review-required; NOT installed.** This document is a mapping and adoption gate, not an independent acceptance receipt.

## 1. Version and evidence baseline

Received: `SMART_LABELLING_QRT_HARDENING_R2_CANDIDATE(2).zip`.
Native IDs: `smart-labelling-1`, `smart-labelling-2`; native version `2.0.0-candidate`.
Native schema: `smart-labelling-qrt-contract/v2`; native reports: `smart-labelling-check-report/v2`.

The archive contains **36 entries** with 35 files in the internal SHA-256 manifest (the manifest itself is the 36th). Locally checked against the supplied manifest: 35 matches, 0 mismatches. Replayed `python -B -X utf8 tests/test_hardening.py` against the extracted candidate: `tests_run: 90, passed: true, failures: 0, errors: 0`.

**Bounded claim:** These are technical/author-side candidate checks. Trust in the supplied manifest is not an independent immutable owner pin; no real academic, examiner, browser, learner, or student-release acceptance was executed.

## 2. Responsibilities and workflow

1. Shared's canonical library/authority owns common records and permissions.
2. **SL1** validates source question/figure/key/paper identities, local hashes, version dependencies and optional practice fitness. `integrity` and `official_key` are separate deterministic gates. No final D3/D4 classification.
3. **P1** is OPTIONAL. QUESTION mode must not claim evidence; EVIDENCE mode requires original saved first attempt and exposure/sequence history. Missing help exposure stays UNKNOWN rather than inferred INDEPENDENT.
4. **SL2** records proposed decisive route, competing operations, five rubric factors and optional observed reasoning. Proposal remains `PROPOSED`/`UNREVIEWED`.
5. **QRT** independently adjudicates operation, task demand and coverage role. `DIRECT_EXAM_EVIDENCE`, `PREREQUISITE_BRIDGE`, `AUTHORED_TRANSFER` are distinct roles; bridge ≠ authenticated exam coverage.
6. **Physics library + WPE adapter + binder** carry qualified scientific warrants, Blueprint/adapter pins, separate source/task/family IDs and independently assessed B1–B7 correspondence.
7. **Core1A/Core1B** produce instruction and fresh protected reconstruction. Grade9QA reports evidence and blockers but does not certify these from matching strings.
8. **Core2 admission** and learner publication/release require separate Shared governance and exact current receipts.

## 3. Native R2 report mapping (read-only)

| Native `gate_summary` key | Integration label | Grade9QA interpretation |
|---|---|---|
| `integrity` | SL1_SOURCE_INTEGRITY | Source/figure binding is machine-checked only |
| `answer` | SL1_ANSWER | Published/extracted answer binding, not necessarily official |
| `practice` | SL1_PRACTICE | Partial practice requires explicit Owner authorization |
| `official_source` | EXAM_PAPER_CUSTODY | Independent paper identity review needed |
| `official_key` | EXAM_KEY_CUSTODY | Separate verified key review needed |
| `observations` | OPTIONAL_P1 | NOT_APPLICABLE in QUESTION mode is valid, not missing mandatory evidence |
| `qrt` | QRT_ADJUDICATION | Requires trusted external reviewer receipt |
| `canonical` | CANONICAL_RECORD | Approved canonical connection distinct from source bytes |
| `construction` | BINDER_B1_B7 | Requires independently approved actual teaching/reconstruction |
| `release` | LEARNER_RELEASE | Requires runtime, owner/learner and publication approvals |

The R2 checker returns `PASS`, `HOLD` or `NOT_APPLICABLE` per gate. Its CLI exit 0 applies **only** to the selected deterministic gate. Do not convert `PASS` to `ACADEMICALLY_APPROVED` and do not mistake a `NOT_APPLICABLE` optional P1 for a failure.

A future adapter must bind native report `schema`, `checker_version`, exact input hashes, checker artifact hash, selected gate, issues, per-record gate results, and independently trusted reviewer-registry pin. Do not accept a standalone JSON report as proof that the native binary was executed or that human approval was independent.

## 4. Safe use of native scripts

From extracted, separately reviewed R2 candidate:

```bash
python -B -X utf8 tests/test_hardening.py
python -B -X utf8 -I skills/smart-labelling-1/scripts/check_sl1.py --help
python -B -X utf8 -I skills/smart-labelling-2/scripts/check_sl2.py --help
```

Example native syntax (only if all referenced inputs exist, and **without claiming qualification**):

```bash
python -B -X utf8 -I skills/smart-labelling-1/scripts/prepare_contract.py sl1.json --sl2 sl2.json --library library.json --vocab vocab.json --adapter examside-json/v1 --out contract.json
python -B -X utf8 -I skills/smart-labelling-1/scripts/check_sl1.py sl1.json --library library.json --vocab vocab.json --contract contract.json --gate integrity --json-output sl1-check.json
python -B -X utf8 -I skills/smart-labelling-2/scripts/check_sl2.py sl2.json --sl1 sl1.json --vocab vocab.json --contract contract.json --gate qrt --review-registry owner-registry.json --registry-sha256 independently-known-sha256 --json-output sl2-check.json
```

A trusted registry and independently known digest are mandatory for qualification of external reviewer receipts. The above file names are placeholders, not repo-provided exam evidence.

## 5. Required implementation order

- **S0** Inventory native skill source and frozen manifest; verify checksums; review licensing/privacy. **Keep candidate uninstalled.**
- **S1** Distinct independent code/semantic reviewer verifies the 90-regression baseline and recognizes protected native source hashes and version; currently HOLD.
- **S2** Bind Shared/QRT vocabulary and source identities. Do not edit shared Blueprint or rewrite native candidate to fit new v4 schemas.
- **S3** Implement a read-only R2 report adapter to v4's report/diagnostic layer. No native skill reimplementation.
- **S4** Add negative controls for forged `REVIEWED`, optional P1, stale inputs, incorrect paper/key equivalence, and QRT vs SL2 proposal.
- **S5** Only after independent receipts and Owner authorization, start P0.2 cross-stage custody/Physics qualification; never infer release.

## 6. Failing and incomplete evidence in real WPE trial

The included real WPE read-only trial remains HOLD: M84's answer extraction unresolved; N11's figure assets unbound; AN5 lacks copied key; AN1 needs reviewed answer normalization. This is **not** a claim the historical answers are wrong. No official NTA verification, qualified Physics, QRT cognitive adjudication or learner browser testing was performed.

Do not conflate the R2 author-tested state with installation or production acceptance.

See root `readme.txt` for the exact **“1. Correct workflow placement”** section.
