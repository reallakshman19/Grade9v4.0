# Candidate evidence contract v2

This is a derived validation sidecar, not a replacement Physics Blueprint, a new Smart Labelling stage, or an academic certificate. Keep the existing v1 overlays and digest algorithm unchanged. Read the original [record shape](record-shape.md) for their fields. The two skills vendor identical standard-library helpers so either folder can run independently; maintain and test those copies together.

## Prepare, review, check

Prepare a **new** sidecar with current byte and per-item payload pins:

```powershell
python -B -X utf8 -I <skill>/scripts/prepare_contract.py <sl1.json> --sl2 <sl2.json> --library <library.json> --vocab <vocabulary.json> --adapter examside-json/v1 --out <new-contract.json>
```

Add `--attempts <actual-saved-attempts.json>` only when those observations exist. Preparation never edits inputs, fills a cognitive seed, invents save/exposure history, issues reviews, or qualifies a record. Existing absolute legacy paths are required; relative v2 artifact paths resolve from the sidecar directory. Unsupported source shapes and missing key extraction stay open. Do not use re-snapshotting to conceal changed source content: retained legacy digest/binding checks still run, and semantic review subjects must be regenerated and independently reviewed when their dependencies change.

For a mixed bank, use `--adapter-map <map.json>` with an exact question-ID-to-adapter object. `--adapter` can remain a default for other IDs. The map selects maintained adapters, not arbitrary source/key field names. WPE M84/N11 use `examside-json/v1`; AN1/AN5 use `anchors-json/v1`. The preparer never guesses an adapter from whichever fields happen to make a check green.

SL1 validation:

```powershell
python -B -X utf8 -I <skill>/scripts/check_sl1.py <sl1.json> --library <library.json> --vocab <vocabulary.json> --contract <contract.json> --gate practice
```

SL2 validation:

```powershell
python -B -X utf8 -I <skill>/scripts/check_sl2.py <sl2.json> --sl1 <sl1.json> --vocab <vocabulary.json> --contract <contract.json> --gate qrt --review-registry <owner-trusted-registry.json> --registry-sha256 <independently-known-sha256>
```

`--json-output <new-report.json>` saves the report without overwriting a checked input. An exit of zero qualifies **only the named deterministic gate**. The default is `integrity`. A QUESTION observation gate returns NOT_APPLICABLE, never independent learner evidence. `--legacy-only` is an explicit migration inspection with `qualification: NOT_RUN`; omitting the sidecar never silently falls back. SL2's original `--binding <sl1.json> <question_id>` helper still prints a legacy binding and grants no qualification.

Use `--allow-partial-practice` only under the actual Owner's policy. It permits honestly labelled, source-partial practice after the other practice checks; it does not authenticate examination coverage. An incomplete semantic draft can be kept separate from the SL1-only contract prepared without `--sl2`. Missing optional P1 never blocks QUESTION-mode analysis or learning.

## Sidecar and digest meanings

```json
{
  "schema": "smart-labelling-qrt-contract/v2",
  "inputs": {
    "sl1": {"path": "sl1.json", "sha256": "sha256:<64 lowercase hex>"},
    "sl2": {"path": "sl2.json", "sha256": "sha256:<64 lowercase hex>"},
    "library": {"path": "library.json", "sha256": "sha256:<64 lowercase hex>"},
    "vocabulary": {"path": "vocab.json", "sha256": "sha256:<64 lowercase hex>"}
  },
  "records": [{
    "question_id": "Q-...",
    "sl1_record_digest": "sha256:...",
    "sl2_record_digest": "sha256:...",
    "source": {
      "adapter": "examside-json/v1", "path": "source.json", "sha256": "sha256:...",
      "item_id": "M101", "question_digest": "sha256:...", "answer_digest": "sha256:...",
      "figure_assets": []
    },
    "answer_reference": {"kind": "UNRESOLVED"},
    "cognitive_seed": null
  }]
}
```

`sl2` and its record digest are optional for SL1-only work. Contract records cover the selected overlay exactly once; complete paired contracts require matching SL1/SL2 question sets. All referenced bytes are rehashed. Declared overlay library/vocabulary/SL1/rubric paths, available versions and supplied hashes must agree with the sidecar. Duplicate JSON keys, record/source/attempt/library IDs, non-finite JSON numbers and malformed types are rejected.

Raw hashes are SHA-256 of exact bytes. `digest(value)` is SHA-256 of UTF-8 JSON with sorted keys, no insignificant whitespace, Unicode retained, no NaN, and the `sha256:` prefix. It performs no Unicode/text normalization. It is a **new v2 meaning**, never a replacement for legacy `item_digest` or the legacy SL2 key digest. Use `source_payloads()`/`digest()` from the helpers rather than hand-building hashes.

The question payload binds adapter, item ID, stem, options, actual figure references and source format. The separate answer payload binds the existing `key` and `explanation` fields. Figure assets each add `source_ref`, saved `path` and exact `sha256`. Every actual `figs` locator must resolve to one bound asset. A changed asset or reference cannot inherit old qualification.

Adapters:

| Adapter | Supported source | Explicit limitation |
| --- | --- | --- |
| `examside-json/v1` | `items` array or root array, unique string `id`, `stem`, `options`, actual `figs`; optional `key`, `explanation`, `paper`, `type` | Explanation prose is not automatically a key; source paper must agree with SL1 |
| `anchors-json/v1` | Unique `id`, `text`, options object, optional explicit `answer`/`answer_basis`, source `format` | Declared aliases normalize text/answer; rejects separate actual figure fields rather than ignoring them |
| `explicit-key-json/v1` | Same JSON containers, `id`, `stem`, `options`, `figure_note`; optional explicit `key` | Rejects a source containing actual `figs`, so it cannot hide that field |
| `text-file/v1` | Entire UTF-8 saved text file | No automatic key extraction; essential non-text figures need a further supported adapter, not a green assertion |

For the actual WPE M84/M101 layout, use the first adapter. M101 is the AIEEE 2012 source question, not the separately authored cut-spring MAIN. A family ID never merges their task identities or demand.

Answer explanations, lure descriptions and saved `score_proposed`/`score_evidence` in anchor sources are reviewer material. Extract only the normalized question payload for a first independent cognitive assessment; do not expose those fields and then declare the assessment blind. Previously exposed authors cannot provide an unexposed independent review merely by saving a new receipt.

Answer references are `PUBLISHER_FIELD` plus `value`, `NO_KEY` with no copied key, or `REVIEWED_EXTRACTION` plus `value`, extraction `artifact` and `review_ref`. An unresolved/unsupported answer is HOLD at answer-dependent gates. Extraction artifacts contain `schema: smart-labelling-answer-extraction/v2`, `source_item_id`, current `source_answer_digest`, `answer` and `author`; their independent review must affirm that answer. Publisher answer consistency and official-key custody are separate gates.

## Local review trust

A reviewer-name string is insufficient. A caller supplies an already Owner-trusted registry and an **independently known pin**. A registry copied from an untrusted candidate is not made trustworthy by hashing it yourself. The helper does not install trust or establish the real-world identity behind a registry entry.

Registry shape:

```json
{"schema":"smart-labelling-review-registry/v2","reviewers":[
  {"id":"<actual-reviewer>","status":"ACTIVE","roles":["qrt"]}
]}
```

Recognized review purposes used by the contract are `sl1`, `sl2`, `source_custody`, `key_custody`, `answer_extraction`, `learner_interpretation`, `qrt`, `canonical`, `construction`, `runtime`, `acceptance`. Author and reviewer must differ; current role/status must permit that purpose. Review files are immutable inputs with exact path/hash references:

```json
{
  "schema":"smart-labelling-review/v2", "role":"qrt", "status":"APPROVED",
  "reviewer":"<actual-reviewer>", "author":"<actual-labeller>",
  "subject_digest":"sha256:<current reviewed subject>",
  "findings":"<actual independent findings>",
  "evidence_refs":[{"path":"...","sha256":"sha256:...","locator":"<exact item/page/span>"}],
  "decision":{}
}
```

The subject construction and purpose-specific decision fields are implemented in `qrt_contract.py`; synthetic, non-exam builders in the package's `tests/fixtures.py` demonstrate their complete shapes. They are test receipts, never actual approvals. No real registry or academic approvals are supplied with this candidate.

SL1 REVIEWED requires `sl1_review_ref`; SL2 REVIEWED requires `sl2_review_ref`. Their subjects bind record, full question and source-answer digests and current library/vocabulary pins. Official `official_source` and `official_key` groups each carry their own artifact `evidence_refs` and `review_ref`. Paper review maps exact source item, paper, question digest and official locator. Key review maps the key row, source item and answer plus typed `option_mapping`: `kind`, `source_options_digest`, `source_answer`, `official_answer`, and for MCQ `official_to_source`. A reviewed paper alone cannot verify a key.

## Truthful optional observations

EVIDENCE entries add `observation` with actual `attempts_ref`, `attempt_id`, `snapshot_digest`, `stage`, `task_id` and, for derived interpretation, `interpretation_review_ref`. The actual saved attempt must have unique ID and bind question ID, question version, legacy item digest, full v2 question digest, task and actual P1 stage. Preserve `answer`, `reasoning`, `confidence`, `committed_before_feedback` exactly; no cleaned-up explanation may replace her saved reasoning.

Successful persistence and ordering require actual saved fields: `saved: true`, integer `save_sequence`, explicit integer-or-null `feedback_sequence`, `exposures_before_save`, and `help_before_commit`. These fields may come from an inspected event-log adapter or genuinely captured save protocol; never add invented events to an old attempt. The current adapter supports the normalized saved JSON fields only. Unsupported legacy history stays HOLD/UNKNOWN, not retrospectively independent.

The selected attempt must be the unique first saved observation for this task, question version, digest and P1 stage. Missing/null/false help never means NONE. An honestly UNKNOWN observation can be retained without capability/correctness inference. Explicit assistance remains ASSISTED. Core1B is a different observation stage and cannot be passed off as P1. The candidate extends the legacy help enum only with UNKNOWN; all other legacy checks are retained.

Correctness, prerequisite-state and failure hypotheses are derived interpretation, not raw observation. Their review subject binds the saved attempt, current resolved answer binding and complete interpretation. A changed reference answer invalidates that review. Byte hashes verify present consistency; a mutable file and self-declared sequence do not prove historical immutability or absence of undisclosed help.

## Compact cognitive seed and QRT review

`cognitive_seed.schema` is `smart-labelling-cognitive-seed/v2`. Required parts are:

- `inputs`/`outputs`: role and a resolvable source JSON pointer.
- `decisive_roles`: unique ID, intellectual work, one or more actual SL2 route move refs. Multiple linked decisive roles are allowed.
- `conditions`: explicit condition text; `dependencies`: role and REQUIRED/UNQUALIFIED/NOT_APPLICABLE authority status. SL2 does not self-qualify Physics.
- `boundary_checks`: route ref and check; `wrong_move_hypotheses`: route ref, existing SL2 hypothesis index and HYPOTHESIS status.
- `competing_operations`: a different existing operation and reason.
- `operation_structure`: the operation-specific requirement below.
- `independent_demand`: assessor, TASK_INTRINSIC basis, `prior_score_seen: false`, operation, five scores, factor-to-route refs and optional exact prior comparison.

| Existing operation | Structure |
| --- | --- |
| RETRIEVE | RECALL with cue/target, or CLASSIFY with criteria/exclusions |
| EXPLAIN | mechanism |
| APPLY | rule/conditions |
| MODEL | variables/assumptions |
| REPRESENT | correspondences/invariants |
| SYNTHESIZE | dependency roles/traversal |
| JUSTIFY | claim/warrant/scope |

RETRIEVE and REPRESENT may display as Recall/Classify and Translate; they keep their existing IDs. Every demand factor remains 0..2; bands remain D1 0–2, D2 3–5, D3 6–7, D4 8–10. Compare complete vectors. Where the SL2 prior proposal exists, `prior_comparison` must bind its digest, exact scores and actual differences; equal-total disagreements cannot disappear.

The candidate explicitly checks these boundaries against the pinned vocabulary. A changed rubric is unsupported and held until a versioned implementation update; a new hash alone cannot silently authorize a new demand policy.

`qrt_review_ref` reviews the exact source question/answer, SL1/SL2 records, seed, semantic library digest and rubric. Its decision records operation, scores, source role, target operation/band, one primary coverage home and distinct secondary references. A separate `first_assessment_ref` points to `smart-labelling-independent-demand/v2`: question ID/digest, rubric pin, authorized independent assessor, operation, scores, factor evidence, `prior_score_seen: false`, and saved sequence before the decision's comparison sequence. This preserves the reported first assessment; it cannot independently prove the person's actual exposure history.

Source roles: DIRECT_EXAM_EVIDENCE requires authenticated paper/key custody and matching source/target operation and demand. PREREQUISITE_BRIDGE can differ from its target; the bound target needs its own qualification. AUTHORED_TRANSFER needs a separately authored source identity. Unresolved roles cannot acquire coverage placement. A source with no final QRT disposition can still be honestly inspected locally.

## Optional downstream binder validation

The binder supplies `canonical` warrants and `construction`; SL2 does not author or complete them. Qualification binds actual authority artifact bytes, an exact warrant pointer, version, conditions and independent review. Availability of CANDIDATE canonical bytes alone does not qualify a warrant.

Construction binds shared `blueprint_refs`, `topic_adapter_ref`, distinct source question/bound task/family IDs, reviewed source relationship, different Core1A/Core1B task IDs and artifacts, and role correspondences. Core1A declares `source_kind: AUTHORED_NON_EXAM` and cannot reuse the source examination task ID; independent review must establish the actual different-example origin, not merely accept the declaration. Every Core1B-required role must be taught and elicited. Every Core1A role claimed assessed must be elicited, or explicitly marked prerequisite/support. Passage spans bind artifact, one-based line range and exact selected UTF-8 text hash. `bridge_evidence` includes actual evidence for B1 through B7. Independent construction review must qualify those criteria, sufficient teaching, freshness and the bound task's own target operation/demand.

These are derived witness checks. They do not alter the Blueprint, infer a physical proof from matching labels, or certify semantic sufficiency by counting spans. Plain HTML/text spans are supported; PDF/DOM passage extraction and browser execution are not implemented by this helper.

Release additionally needs pinned compiled and baseline artifacts, trusted runtime review of protected work/save ordering/content preservation, and actual authorized learner-acceptance evidence. The runtime/compiler owner produces those checks. This candidate does not grant release permission.

## Gate meanings and invalidation

| Gate | What a successful check establishes |
| --- | --- |
| integrity | Current references, hashes, declared dependencies, identifiers and supported source/record bindings; unsupported VERIFIED claims cannot pass |
| answer | Current publisher field or independently reviewed extraction agrees with copied key; NO_KEY is NOT_APPLICABLE |
| practice | Integrity, checked answer and legacy readiness rules; partial provenance needs explicit caller policy |
| official_source / official_key | Separate current artifact mappings and trusted review receipts; authenticity still rests on custody review |
| observations | Exact saved P1 binding and truthful copied fields; derived interpretations independently reviewed if claimed |
| qrt | Typed seed, independent first-score evidence, current adjudication and source relationship |
| canonical | Selected warrant qualification, independent of mere library availability |
| construction | Current Blueprint/adapter/authority bindings, actual passage correspondence and trusted B1–B7 decision |
| release | Construction plus reviewed compiled preservation/protection/save behavior and actual acceptance evidence |

Each run reports actual input hashes, versions, attempted checks, per-record/aggregate gates, reasons and unsupported capabilities. Missing work is NOT_RUN/HOLD or NOT_APPLICABLE, never VERIFIED by silence. Changes are recomputed into stale/unresolved state and block affected promotions; the checker does not edit original overlays. Formatting-only source changes require byte-pin readback but need not change an unchanged semantic payload or its existing per-item review subject. Coverage reconciliation rejects orphaned/missing/duplicate records. On legacy structural failure the wrapper holds qualification and retains full diagnostics; use an SL1-only contract to continue upstream practice checks while an SL2 draft is incomplete.

All candidate checks are author-side. Independent academic/behavioral review and Owner acceptance remain separate.
