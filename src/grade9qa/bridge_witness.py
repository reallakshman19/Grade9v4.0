"""Bidirectional B1–B7 witness inspection; mechanical evidence only.

This module is deliberately NOT an academic reviewer, Shared release authority,
QRT adjudicator, semantic equivalence judge or physics validator.
No input, including a forged APPROVED receipt, can cause a PASS/release result.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GATES = {
    "B1": "Correct cognitive target and assessed demand",
    "B2": "Construction signature and decisive reasoning bridge",
    "B3": "Core1A explicit teaching sufficiency",
    "B4": "Fresh, directionally equivalent Core1B reconstruction",
    "B5": "Protected attempt, durable save and fail-closed reveal",
    "B6": "Evidence-based diagnosis and changed-condition transfer",
    "B7": "Separate qualified Physics and source custody",
}
TEACHING_SLOTS = (
    "physical_demo", "qualitative_prediction", "law_and_conditions",
    "worked_original_example", "guided_practice", "misconception_repair",
    "verification_check",
)
EXPOSURE_SURFACES = ("HINT", "PICTURE_STAGE", "ALT_TEXT", "MODEL_RESPONSE", "RUBRIC", "EXAM_RETURN")
EVENT_TYPES = {
    "ANSWER_ENTERED", "FIRST_ANSWER_SAVED", "SAVE_FAILED",
    "HINT_SHOWN", "ANSWER_REVEALED",
}
REVIEW_DISCIPLINES = {
    "B1": ("COGNITIVE", "QRT"),
    "B2": ("COGNITIVE",),
    "B3": ("PEDAGOGY", "COGNITIVE"),
    "B4": ("COGNITIVE", "PEDAGOGY"),
    "B5": ("TECHNICAL",),
    "B6": ("PEDAGOGY", "COGNITIVE"),
    "B7": ("PHYSICS", "SOURCE_CUSTODY"),
}


def _digest(value: Any) -> str:
    """Canonical JSON bytes; not human approval or an upstream hash format."""
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def inspect_witness(witness: dict, *, trusted_shared_receipts: bool = False) -> dict:
    """Return B1–B7 evidence disposition; never academic PASS.

    trusted_shared_receipts is reserved for later native integration and
    intentionally has no acceptance effect. A caller cannot set this flag to
    bypass independent human verification.
    """
    diagnostics: list[dict] = []
    gate_problems: dict[str, list[dict]] = {gate: [] for gate in GATES}

    def mark(gate: str, code: str, detail: str, severity: str = "HOLD") -> None:
        item = {"gate": gate, "code": code, "severity": severity, "detail": detail}
        gate_problems[gate].append(item)
        diagnostics.append(item)

    if not isinstance(witness, dict):
        witness = {}
        mark("B2", "WITNESS_NOT_OBJECT", "Expected a v1 witness object.", "FAIL")
    construction = witness.get("construction") or {}
    teaching = witness.get("core1a") or {}
    learner = witness.get("core1b") or {}
    assessment = witness.get("assessment") or {}
    science = witness.get("source_and_physics") or {}
    reviewers = witness.get("review_receipts") or []
    if witness.get("schema_version") != "grade9qa-b1b7-witness/v1":
        mark("B2", "WITNESS_SCHEMA_UNKNOWN", "Exact v1 witness schema required.", "FAIL")
    if not isinstance(construction, dict) or not isinstance(teaching, dict) or not isinstance(learner, dict):
        mark("B2", "WITNESS_RECORD_SHAPE_INVALID", "Construction and roles must be objects.", "FAIL")
        construction, teaching, learner = {}, {}, {}
    if not isinstance(assessment, dict) or not isinstance(science, dict) or not isinstance(reviewers, list):
        mark("B7", "EVIDENCE_RECORD_SHAPE_INVALID", "Assessment, science and receipts must have correct shapes.", "FAIL")
        assessment, science, reviewers = {}, {}, []

    subject_id = construction.get("construction_id", "")
    c_op, c_band, c_dir = (construction.get(k) for k in ("operation", "band", "direction"))
    c_roles = construction.get("decisive_roles")
    if not _nonempty(subject_id):
        mark("B1", "CONSTRUCTION_ID_MISSING", "Stable bound construction ID required.")
    for label, entry in (("Core1A", teaching), ("Core1B", learner)):
        if entry.get("construction_id") != subject_id:
            mark("B1", "CONSTRUCTION_BINDING_MISMATCH",
                 f"{label} references different construction identity.", "FAIL")
        if entry.get("operation") != c_op or entry.get("band") != c_band:
            mark("B1", "COGNITIVE_TARGET_MISMATCH",
                 f"{label} operation or demand differs from construction.", "FAIL")
    if assessment.get("operation") != c_op or assessment.get("band") != c_band:
        mark("B1", "ASSESSMENT_TARGET_MISMATCH",
             "Assessment's operation/band must match the claimed construction.", "FAIL")
    if not _nonempty(assessment.get("qrt_decision_ref")):
        mark("B1", "QRT_DECISION_ABSENT", "SL2 PROPOSED is not independently reviewed QRT.")
    vector = assessment.get("demand_vector")
    allowed = {"D1": (0, 2), "D2": (3, 5), "D3": (6, 7), "D4": (8, 10)}
    if (not isinstance(vector, list) or len(vector) != 5
            or any(type(k) is not int or k < 0 or k > 2 for k in vector)):
        mark("B1", "DEMAND_VECTOR_MISSING", "Five evidence-supported 0..2 factors required.")
    elif c_band in allowed and not allowed[c_band][0] <= sum(vector) <= allowed[c_band][1]:
        mark("B1", "DEMAND_BAND_CONTRADICTION", "Five-factor sum contradicts claimed band.", "FAIL")
    if not _nonempty(assessment.get("demand_evidence_ref")):
        mark("B1", "INDEPENDENT_DEMAND_EVIDENCE_MISSING",
             "Numerical score alone is not cognitive difficulty adjudication.")
    if assessment.get("source_role") not in (
        "DIRECT_EXAM_EVIDENCE", "PREREQUISITE_BRIDGE", "AUTHORED_TRANSFER"
    ):
        mark("B1", "SOURCE_ROLE_UNRESOLVED",
             "Authenticate direct exam evidence separately from bridge or authored transfer.")

    signature = construction.get("signature") or {}
    if not isinstance(signature, dict):
        signature = {}
    for field in ("inputs", "obstacle", "decisive_move", "output",
                  "independent_check", "validity_boundary"):
        value = signature.get(field)
        if field == "inputs":
            if not isinstance(value, list) or not value or not all(map(_nonempty, value)):
                mark("B2", "SIGNATURE_INPUTS_MISSING", "Explicit nonempty inputs needed.")
        elif not _nonempty(value):
            mark("B2", "SIGNATURE_" + field.upper() + "_MISSING",
                 "Explicit construction signature " + field + " needed.")
    if not isinstance(c_roles, list) or not c_roles or not all(map(_nonempty, c_roles)):
        mark("B2", "DECISIVE_ROLES_MISSING", "Declared protected cognitive roles needed.")
        c_roles = []
    for field in ("conditions", "dependency_refs"):
        value = signature.get(field)
        if not isinstance(value, list) or not value or not all(map(_nonempty, value)):
            mark("B2", "SIGNATURE_" + field.upper() + "_MISSING",
                 "Explicit nonempty governing conditions and dependency stages required.")
    if len(set(c_roles)) != len(c_roles):
        mark("B2", "DUPLICATE_DECISIVE_ROLE", "Roles must have distinct stable IDs.", "FAIL")

    slots = teaching.get("teaching_slots") or {}
    if not isinstance(slots, dict):
        slots = {}
    for field in TEACHING_SLOTS:
        if not _nonempty(slots.get(field)):
            mark("B3", "TEACHING_SLOT_MISSING", f"Core1A {field} evidence missing.")
    teaching_roles = teaching.get("taught_roles")
    if not isinstance(teaching_roles, dict):
        teaching_roles = {}
    for role in c_roles:
        item = teaching_roles.get(role)
        if not isinstance(item, dict) or not _nonempty(item.get("teaching_span_ref")) or not _nonempty(item.get("demonstration_ref")):
            mark("B3", "DECISIVE_ROLE_NOT_DEMONSTRATED",
                 f"Role {role} needs both teaching span and demonstrated working.")
    if teaching.get("direction") != c_dir:
        mark("B3", "TEACHING_DIRECTION_MISMATCH",
             "Core1A does not teach the exact protected direction.", "FAIL")
    if not _nonempty(teaching.get("content_sha256")):
        mark("B3", "CORE1A_CONTENT_HASH_ABSENT", "Pin actual teaching content bytes.")
    if not _nonempty(teaching.get("worked_example_sha256")):
        mark("B3", "WORKED_EXAMPLE_HASH_ABSENT", "Worked example identity must be pinned.")

    assessed_roles = learner.get("assessed_roles")
    if not isinstance(assessed_roles, dict):
        assessed_roles = {}
    for role in c_roles:
        item = assessed_roles.get(role)
        if not isinstance(item, dict) or not _nonempty(item.get("attempt_field")) or not _nonempty(item.get("observable")):
            mark("B4", "ASSESSMENT_ROLE_UNOBSERVED",
                 f"Role {role} needs an independently observable attempt field.")
    extra = sorted(set(assessed_roles) - set(c_roles))
    if extra:
        mark("B4", "UNTAGGED_ASSESSED_ROLES", "Core1B requires undeclared roles: " + ", ".join(extra), "FAIL")
    if learner.get("direction") != c_dir:
        mark("B4", "RECONSTRUCTION_DIRECTION_MISMATCH",
             "Core1B direction differs; reverse U→F / F→U is a new construction unless explicitly taught.", "FAIL")
    if not _nonempty(learner.get("fresh_context_ref")):
        mark("B4", "FRESH_CONTEXT_UNPINNED", "Document different Core1B situation.")
    ta = teaching.get("worked_example_sha256")
    tb = learner.get("task_sha256")
    if not _nonempty(tb):
        mark("B4", "CORE1B_TASK_HASH_ABSENT", "Pin actual fresh assessment bytes.")
    elif _nonempty(ta) and tb == ta:
        mark("B4", "SAME_WORKED_AND_TESTED_TASK", "Core1B duplicates Core1A solved task.", "FAIL")
    if not _nonempty(learner.get("freshness_review_ref")):
        mark("B4", "FRESHNESS_SEMANTIC_REVIEW_ABSENT",
             "Different hashes are not proof of a fresh cognitive task.")

    state = learner.get("attempt_contract") or {}
    if not isinstance(state, dict):
        state = {}
    for k in ("p1_optional", "first_answer_before_hint", "reveal_requires_saved_attempt",
              "fail_closed_on_save_error"):
        if state.get(k) is not True:
            mark("B5", "ATTEMPT_PROTECTION_CONTRACT_INVALID",
                 f"{k} must be true; optional P1 must not gate teaching.", "FAIL")
    events = learner.get("attempt_events")
    if not isinstance(events, list):
        events = []
    last_time = None
    saved = False
    attempted = False
    for idx, event in enumerate(events):
        if not isinstance(event, dict) or event.get("type") not in EVENT_TYPES:
            mark("B5", "ATTEMPT_EVENT_INVALID", f"Event {idx} invalid.", "FAIL")
            continue
        at = event.get("at")
        try:
            when = datetime.fromisoformat(at.replace("Z", "+00:00")) if isinstance(at, str) else None
            if when is None or when.tzinfo is None:
                raise ValueError("timezone required")
            when = when.astimezone(timezone.utc)
        except (ValueError, TypeError, AttributeError):
            mark("B5", "ATTEMPT_EVENT_TIME_INVALID", f"Event {idx} needs offset-aware timestamp.", "FAIL")
            continue
        if last_time is not None and when < last_time:
            mark("B5", "ATTEMPT_EVENT_ORDER_INVALID", "Timestamps must be monotone.", "FAIL")
        last_time = when
        kind = event["type"]
        if kind == "ANSWER_ENTERED":
            attempted = True
        if kind == "SAVE_FAILED":
            saved = False
        if kind == "FIRST_ANSWER_SAVED":
            if not attempted or event.get("durable") is not True:
                mark("B5", "FALSE_SAVED_ATTEMPT", "Require entered answer and durable success.", "FAIL")
            else:
                saved = True
        if kind in ("HINT_SHOWN", "ANSWER_REVEALED") and not saved:
            mark("B5", "PREMATURE_HINT_OR_REVEAL",
                 f"{kind} before successful durable first-answer save.", "FAIL")
    if not events:
        mark("B5", "ATTEMPT_TRACE_NOT_PROVIDED", "Need synthetic/native runtime state trace for an actual check.")
    surfaces = learner.get("exposure_audit")
    if not isinstance(surfaces, list):
        surfaces = []
    index = {}
    for row in surfaces:
        if not isinstance(row, dict) or row.get("surface") not in EXPOSURE_SURFACES:
            mark("B5", "EXPOSURE_SURFACE_INVALID", "Unknown protected-answer exposure surface.", "FAIL")
            continue
        name = row["surface"]
        if name in index:
            mark("B5", "EXPOSURE_SURFACE_DUPLICATE", "Exposure surface audited more than once.", "FAIL")
        index[name] = row
        if not _nonempty(row.get("audit_ref")):
            mark("B5", "EXPOSURE_AUDIT_EVIDENCE_MISSING", f"Missing source-native {name} trace.")
        if row.get("decisive_route_visible_before_save") is True:
            mark("B5", "PROTECTED_ROUTE_LEAK", f"{name} reveals decisive work before durable first save.", "FAIL")
        if row.get("decisive_route_visible_before_save") not in (True, False):
            mark("B5", "EXPOSURE_OUTCOME_UNKNOWN", f"{name} exposure state was not audited.")
    for name in EXPOSURE_SURFACES:
        if name not in index:
            mark("B5", "EXPOSURE_SURFACE_NOT_AUDITED", f"Protected-answer surface {name} untested.")
    if not _nonempty(learner.get("native_runtime_receipt_ref")):
        mark("B5", "NATIVE_RUNTIME_EVIDENCE_MISSING",
             "Synthetic state log is not a verified deployed-browser/runtime test.")

    diagnoses = learner.get("diagnostic_rules")
    if not isinstance(diagnoses, list) or not diagnoses:
        mark("B6", "DIAGNOSIS_NOT_DEFINED", "Map observed failed roles to actionable repair.")
        diagnoses = []
    role_diagnosed = set()
    for item in diagnoses:
        if not isinstance(item, dict):
            mark("B6", "DIAGNOSIS_ROW_INVALID", "Expected role-linked diagnostic object.", "FAIL")
            continue
        role = item.get("role_id")
        if role not in c_roles:
            mark("B6", "DIAGNOSIS_UNKNOWN_ROLE", "Diagnosis references non-bound role.", "FAIL")
        elif (_nonempty(item.get("observable")) and _nonempty(item.get("repair_ref"))
              and _nonempty(item.get("failed_node_ref"))):
            role_diagnosed.add(role)
        else:
            mark("B6", "DIAGNOSIS_EVIDENCE_MISSING",
                 "Diagnosis needs observed error, erroneous construction node and Core1A repair span.")
    for role in set(c_roles)-role_diagnosed:
        mark("B6", "DECISIVE_ROLE_UNDIAGNOSED", f"No diagnosis/repair bound to {role}.")
    if not _nonempty(learner.get("changed_condition_transfer_ref")):
        mark("B6", "TRANSFER_NOT_DEFINED", "Changed-condition follow-up needed.")
    if not _nonempty(learner.get("transfer_success_criterion")):
        mark("B6", "TRANSFER_SUCCESS_CRITERION_MISSING",
             "Specify observable changed-condition success, not only changed numbers.")
    if not _nonempty(learner.get("saved_answer_evidence_ref")):
        mark("B6", "INSUFFICIENT_EVIDENCE",
             "No actual saved response; do not claim a misconception was observed.")

    if not _nonempty(science.get("physics_warrant_ref")):
        mark("B7", "PHYSICS_WARRANT_NOT_PINNED", "Exact Physics law and validity claim required.")
    if not _nonempty(science.get("physics_review_ref")):
        mark("B7", "PHYSICS_REVIEW_MISSING", "Separate independently reviewed Physics warrant required.")
    if not _nonempty(science.get("source_custody_ref")):
        mark("B7", "SOURCE_CUSTODY_REVIEW_MISSING",
             "Source custody is not scientific correctness.")
    if assessment.get("source_role") == "DIRECT_EXAM_EVIDENCE":
        for field in ("paper_ref", "official_key_ref", "solution_review_ref"):
            if not _nonempty(science.get(field)):
                mark("B7", "EXAM_" + field.upper() + "_MISSING",
                     "Authenticated exam evidence requires independently verified " + field)
    links = science.get("warrant_links")
    if not isinstance(links, list):
        links = []
    secured_roles = set()
    for row in links:
        if not isinstance(row, dict) or row.get("role_id") not in c_roles:
            mark("B7", "WARRANT_ROLE_INVALID", "Physics warrant must map to a bound decisive step.", "FAIL")
            continue
        if not _nonempty(row.get("warrant_ref")) or not _nonempty(row.get("library_sha256")):
            mark("B7", "WARRANT_UNPINNED", "Each consequential step requires an exact version-pinned warrant.")
        else:
            secured_roles.add(row["role_id"])
    for role in set(c_roles) - secured_roles:
        mark("B7", "CONSEQUENTIAL_STEP_WARRANT_MISSING",
             f"No scoped canonical Physics warrant pin for role {role}.")
    if science.get("known_physics_contradiction") is True:
        mark("B7", "KNOWN_PHYSICS_CONTRADICTION", "Known physics contradiction blocks qualification.", "FAIL")
    if not isinstance(reviewers, list):
        reviewers = []
    declared = set()
    raw_subject = {k: v for k, v in witness.items() if k != "review_receipts"}
    try:
        subject_digest = _digest(raw_subject)
    except (TypeError, ValueError, UnicodeError):
        subject_digest = None
        mark("B2", "WITNESS_DIGEST_UNAVAILABLE", "Non-canonical/nonfinite JSON cannot be pinned.", "FAIL")
    for i, item in enumerate(reviewers):
        if not isinstance(item, dict):
            mark("B7", "REVIEW_RECORD_INVALID", f"Receipt {i} not an object.", "FAIL")
            continue
        gate, discipline = item.get("gate"), item.get("discipline")
        if gate not in GATES or discipline not in REVIEW_DISCIPLINES.get(gate, ()):
            mark("B7", "REVIEW_SCOPE_INVALID", f"Receipt {i} has invalid gate/discipline.", "FAIL")
            continue
        declared.add((gate,discipline))
        if item.get("reviewer_id") == item.get("author_id") or item.get("independent_of_author") is not True:
            mark(gate, "SELF_REVIEW_NOT_ACCEPTABLE", "Review must be independently performed.", "FAIL")
        if item.get("construction_id") != subject_id:
            mark(gate, "REVIEW_SUBJECT_MISMATCH", "Receipt scoped to different construction.", "FAIL")
        if not subject_digest or item.get("subject_sha256") != subject_digest:
            mark(gate, "STALE_OR_UNBOUND_REVIEW", "Review not bound to current witness digest.")
        if item.get("decision") == "REJECTED":
            mark(gate, "REVIEW_REJECTED", "Independent reviewer rejected this obligation.", "FAIL")
        elif item.get("decision") != "APPROVED":
            mark(gate, "REVIEW_DECISION_MISSING", "Explicit reviewed decision required.")
        # Even seemingly valid receipts are untrusted user-supplied data;
        # Shared must verify artifact hashes, identity and owner authorization.
        mark(gate, "REVIEW_RECEIPT_NOT_NATIVE_TRUSTED",
             "Metadata is not Shared-native authenticated reviewer authority.")
    for gate, disciplines in REVIEW_DISCIPLINES.items():
        for discipline in disciplines:
            if (gate, discipline) not in declared:
                mark(gate, "INDEPENDENT_" + discipline + "_REVIEW_MISSING",
                     "Missing scoped independent " + discipline + " review.")

    gate_results = []
    for gate, desc in GATES.items():
        entries = gate_problems[gate]
        inconsistent = any(e["severity"] == "FAIL" for e in entries)
        gate_results.append({
            "gate": gate, "requirement": desc,
            "mechanical_state": "CONTRADICTORY" if inconsistent else (
                "EVIDENCE_GAPS" if entries else "STRUCTURALLY_COMPLETE"),
            "result": "FAIL" if inconsistent else "HOLD",
            "review_authority": "UNVERIFIED",
            "diagnostic_codes": sorted({e["code"] for e in entries}),
        })

    return {
        "schema_version": "1.0.0",
        "witness_schema": witness.get("schema_version"),
        "construction_id": subject_id,
        "mechanical_status": "FAIL" if any(g["result"] == "FAIL" for g in gate_results) else "HOLD",
        "qualification_status": "HOLD",
        "release_status": "HOLD",
        "gate_results": gate_results,
        "diagnostics": sorted(diagnostics, key=lambda x: (x["gate"], x["code"], x["detail"])),
        "witness_subject_sha256": subject_digest,
        "coverage": {"candidate_constructions": 1 if _nonempty(subject_id) else 0,
                     "academically_qualified_constructions": 0},
        "blocked_by": ["SHARED_NATIVE_REVIEW_AUTHORITY", "INDEPENDENT_SEMANTIC_B1_B7",
                       "SCOPED_PHYSICS_AND_SOURCE_CUSTODY", "NATIVE_LEARNER_RUNTIME",
                       "SHARED_RELEASE_AUTHORITY"],
        "warning": "NOT_ACADEMIC_APPROVAL: no reviewed semantic equivalence or release from structure, supplied receipts, or hashes.",
    }
