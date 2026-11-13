# Smart Labelling 2: overlay and record shape

One overlay file per topic: `qrt/labels/smart-labels-2.<topic>.v1.json`.

## File

```json
{
  "schema": "g9v35-smart-labels-2/v1",
  "derivation_version": "SL2 1.0.0",
  "topic": {"subject": "Physics", "topic_code": "WPE", "title": "Work, Power and Energy"},
  "sl1_ref": {"path": "D:/CodeD/g9v3.5/qrt/labels/smart-labels-1.wpe.v1.json"},
  "rubric_ref": {"path": "C:/CodeC/Grade9v3.5/Shared/vocabularies/learner-question-metadata.v1.json", "version": "1.1.0"},
  "labeller": "<who labelled>",
  "date": "YYYY-MM-DD",
  "records": []
}
```

## Record (all groups required)

```json
{
  "question_id": "Q-PHY-WPE-JEEM-M84",
  "mode": "QUESTION",
  "status": "UNREVIEWED",
  "derivation_version": "SL2 1.0.0",
  "binding": {"sl1_item_digest": "sha256:...", "answer_ref_status": "KEY_FROM_PUBLISHER", "answer_ref_digest": "sha256:..."},
  "route": {
    "moves": [{"id": "m1", "text": "..."}, {"id": "m2", "text": "..."}],
    "crux_move_ref": "m2",
    "crux": "<the decisive move in one sentence>"
  },
  "difficulty_evidence": {
    "components": {
      "concept_model_selection": {"score": 2, "evidence": "<sentence about this question>"},
      "representation_translation": {"score": 1, "evidence": "..."},
      "reasoning_chain_length": {"score": 2, "evidence": "..."},
      "algebra_computational_load": {"score": 1, "evidence": "..."},
      "trap_exception_sensitivity": {"score": 2, "evidence": "..."}
    },
    "total": 8,
    "band": "D4",
    "prior_proposal": {"source": "<map or adapter anchor>", "scores": "2/1/2/1/2", "total": 8},
    "differences": "none"
  },
  "demand_proposal": {"primary": "MODEL", "secondary": ["APPLY"], "rationale": "...", "candidate_cell": "QRT-MODEL-D4", "status": "PROPOSED"},
  "representation_requirement": [{"kind": "VECTOR", "transformation": "..."}],
  "independent_checks": [{"kind": "UNITS", "check": "..."}],
  "wrong_route_hypotheses": [{"route": "...", "confirming_evidence": "...", "alternative": "...", "status": "HYPOTHESIS", "misconception_ref": null}],
  "learner": {
    "attempt_ref": null,
    "committed_before_feedback": null,
    "original_answer": null,
    "result": "NOT_EVALUATED",
    "confidence": "MISSING",
    "reasoning": null,
    "help_exposure": "NOT_APPLICABLE",
    "prerequisite_state": {"CAP-WEP-POWER-RATES": "UNKNOWN"},
    "failure_hypothesis": null
  },
  "learning_route": {"value": "PREREQUISITE_BRIDGE", "reason": "..."}
}
```

`prior_proposal` is null when no earlier score exists. In EVIDENCE mode `learner` is filled from the attempt record named by `attempt_ref`.

## Allowed values

| Field | Values |
|---|---|
| `mode` | QUESTION, EVIDENCE |
| `status` | UNREVIEWED, REVIEWED, STALE |
| `binding.answer_ref_status` | KEY_VERIFIED, KEY_FROM_PUBLISHER, KEY_DOUBTFUL, NO_KEY |
| component `score` | 0, 1, 2 (rubric anchors) |
| `band` | D1 (0–2), D2 (3–5), D3 (6–7), D4 (8–10) |
| `demand_proposal.primary` / `secondary` | RETRIEVE, EXPLAIN, APPLY, MODEL, REPRESENT, SYNTHESIZE, JUSTIFY |
| `demand_proposal.status` | PROPOSED (QRT alone resolves) |
| `representation_requirement[].kind` | DIAGRAM, FREE_BODY_DIAGRAM, VECTOR, GRAPH, EQUATION, TABLE, ENERGY_BARS, WORDS |
| `independent_checks[].kind` | UNITS, LIMITING_CASE, SIGN, ROUND_TRIP, ENERGY_LEDGER, COUNTEREXAMPLE, ALTERNATE_DERIVATION |
| `wrong_route_hypotheses[].status` | HYPOTHESIS |
| `learner.result` | CORRECT, INCORRECT, NO_ANSWER, NOT_EVALUATED |
| `learner.confidence` | SURE, UNSURE, GUESSING, MISSING |
| `learner.help_exposure` | INDEPENDENT, HINT, SCAFFOLD, EXPLANATION, WORKED_EXAMPLE, FULL_SOLUTION, NOT_APPLICABLE |
| `learner.prerequisite_state` values | DEMONSTRATED, UNCERTAIN, MISSING, UNKNOWN |
| `learning_route.value` | PREREQUISITE_BRIDGE, CORE1A_CONSTRUCTION, CORE1B_RECONSTRUCTION, FRESH_RECHECK |

## Attempt record (EVIDENCE mode input, written when she really tries a question)

`qrt/labels/p1-attempts.<topic>.v1.json`: `{"schema": "g9v35-p1-attempts/v1", "attempts": [{"attempt_id", "question_id", "item_digest", "date", "answer", "reasoning", "confidence", "help_before_commit", "committed_before_feedback", "time_taken_s"}]}`. Records are never edited after they are written; a correction is a new record.
