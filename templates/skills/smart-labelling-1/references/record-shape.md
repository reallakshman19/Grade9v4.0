# Smart Labelling 1: overlay and record shape

One overlay file per topic: `qrt/labels/smart-labels-1.<topic>.v1.json`.

## File

```json
{
  "schema": "g9v35-smart-labels-1/v1",
  "derivation_version": "SL1 1.0.0",
  "topic": {"subject": "Physics", "topic_code": "WPE", "title": "Work, Power and Energy"},
  "library_ref": {"path": "C:/CodeC/Grade9v3.5/Physics/library/phy-work-energy-power.v1.json", "version": "<library version>"},
  "vocabulary_ref": {"path": "C:/CodeC/Grade9v3.5/Shared/vocabularies/learner-question-metadata.v1.json", "version": "1.1.0"},
  "labeller": "<who labelled>",
  "date": "YYYY-MM-DD",
  "records": []
}
```

## Record (all groups required)

```json
{
  "question_id": "Q-PHY-WPE-JEEM-M84",
  "version": 1,
  "status": "UNREVIEWED",
  "flags": [],
  "custody": {
    "source_file": "D:/CodeD/g9v3.5/qrt/sources/examside-wpe-extract.json",
    "source_item_id": "M84",
    "digest_fields": ["stem", "options", "figure_note"],
    "item_digest": "sha256:<from scripts/digest.py>"
  },
  "source_identity": {"authority": "JEE_MAIN", "discovered_via": "EXAMSIDE", "paper": "<paper, date, shift>", "locator": "<url or page/number>", "note": "<optional>"},
  "source_verification": {"status": "PARTIAL", "basis": "<what was and was not seen>", "provenance": "SOURCE_UNVERIFIED"},
  "canonical_identity": {"original_id": "<source's own id>", "variant_parent_id": null, "duplicate_of": null},
  "subject_classification": {"subject": "Physics", "topic": "Work, Power and Energy", "microtopic_refs": ["MIC-PHY-WEP-POWER-RATES"], "primary_capability_ref": "CAP-WEP-POWER-RATES"},
  "curriculum_stage": {"value": "JEE_MAIN_TARGET", "reason": "<one line>"},
  "concept_difficulty": {"value": "MEDIUM", "from": "MIC-PHY-WEP-POWER-RATES.intrinsic_badge"},
  "prerequisites": {"edges": [{"capability_ref": "CAP-WEP-WORK-DIRECTION", "kind": "ESSENTIAL"}], "missing_links": ["<idea the library lacks>"]},
  "question_family": {"ref": null, "proposed": "<family name>"},
  "format": {"question_type": "single_correct_mcq", "figure": "NONE"},
  "assessment_fitness": {"first_try_ok": true, "answer_exposure": "<text>", "ambiguity_found": false, "ambiguity": "none found", "cue_risk": "<text>", "notes": "<text>"},
  "content_integrity": {
    "answer_check": {"status": "AGREES", "key": "A", "worked_answer": "<your answer>", "basis": "<short working>"},
    "option_cue_checked": true,
    "figure_validated": "NOT_APPLICABLE",
    "rights": "OWNER_LOCAL_ONLY",
    "duplicate_status": "UNIQUE"
  },
  "workflow_action": {"value": "READY_FOR_FIRST_TRY", "reason": "<one line>"},
  "learner_card": {"title": "...", "subject": "Physics", "topic": "...", "concept": "...", "stage": "...", "concept_badge": "Medium concept", "format": "Single-correct MCQ", "required": "<what the question asks for>", "hints": "No hints"}
}
```

## Allowed values

| Field | Values |
|---|---|
| `status` | UNREVIEWED, REVIEWED, STALE |
| `source_identity.authority` | JEE_MAIN, NCERT, CBSE, TEXTBOOK, ALLEN, BYJUS, AUTHORED, OTHER |
| `source_identity.discovered_via` | OFFICIAL, EXAMSIDE, TEXTBOOK_EXTRACT, OWNER, AGENT_RESEARCH, OTHER |
| `source_verification.status` | VERIFIED, PARTIAL, UNVERIFIED |
| `source_verification.provenance` | the vocabulary's `provenance` keys (PYQ_VERIFIED and PYQ_ADAPTED need VERIFIED) |
| `curriculum_stage.value` | GRADE9_CORE, GRADE9_EXTENSION, BRIDGE_10_12, JEE_MAIN_TARGET |
| `concept_difficulty.value` | EASY, MEDIUM, HARD (= the library badge of the first microtopic) |
| `prerequisites.edges[].kind` | ESSENTIAL, SUPPORTING |
| `format.question_type` | the vocabulary's `question_types` keys |
| `format.figure` | NONE, HELPFUL, ESSENTIAL |
| `content_integrity.answer_check.status` | AGREES, DISAGREES, NOT_CHECKED |
| `content_integrity.figure_validated` | VALIDATED, NOT_VALIDATED, NOT_APPLICABLE |
| `content_integrity.rights` | OWNER_LOCAL_ONLY, OPEN, UNKNOWN |
| `content_integrity.duplicate_status` | UNIQUE, DUPLICATE, VARIANT |
| `workflow_action.value` | READY_FOR_FIRST_TRY, RESEARCH_SOURCE, REPAIR_QUESTION, QUALIFY_PREREQUISITE, EXCLUDE_FROM_ASSESSMENT |
| `learner_card` keys | title, subject, topic, concept, stage, concept_badge, format, required, hints (nothing else) |

`flags` copies any flag the source file carries (e.g. AMBIGUOUS, KEY DOUBTFUL); a flagged record cannot be READY.
