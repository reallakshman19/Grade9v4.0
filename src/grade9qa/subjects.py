"""Subject-neutral v2 candidate intake checks for Physics, Mathematics, Chemistry.

This is not Shared's canonical schema or a subject Blueprint. The existing
WPE-only v1 bundle remains valid and unchanged. Candidate validity NEVER
implies an academic or publication approval.
"""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

SUBJECTS = ("PHYSICS", "MATHEMATICS", "CHEMISTRY")
KINDS = ("sources", "warrants", "constructions")
TYPES = {"sources": "source", "warrants": "warrant", "constructions": "construction"}
REF_FIELDS = {
    "warrants": {"source_refs": "source"},
    "constructions": {
        "source_refs": "source", "warrant_refs": "warrant",
        "prerequisite_refs": "construction",
    },
}
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas/v2/subject-intake.schema.json"


def _error(code: str, path: str, message: str) -> dict:
    return {"code": code, "path": path, "message": message, "severity": "ERROR"}


def _fq(subject: str, topic: str, name: str) -> str:
    return f"{subject}/{topic}/{name}"


def audit_subject_intake(data: object) -> dict:
    """Return mechanically checked, per-subject candidate evidence with HOLD.

    References are fully qualified subject/topic/record identities. Cross-topic
    dependencies within a subject are allowed when the target is present;
    cross-subject links are rejected even when their targets exist.
    """
    problems: list[dict] = []
    if not isinstance(data, dict):
        data = {}
        problems.append(_error("INPUT_NOT_OBJECT", "$", "Expected JSON object."))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data),
                    key=lambda e: (tuple(str(x) for x in e.absolute_path), str(e.validator)))
    for err in errors:
        path = "$" + "".join(
            f"[{p}]" if isinstance(p, int) else f".{p}" for p in err.absolute_path)
        # Do not repeat original source contents, titles or learner answers.
        problems.append(_error("V2_SCHEMA_ERROR", path, "Constraint violation: " + str(err.validator)))
    if errors:
        return _result(data, problems, {})

    index: dict[str, dict[str, tuple]] = {k: {} for k in TYPES.values()}
    summary = {}
    seen_subjects = set()
    for sidx, subject in enumerate(data["subjects"]):
        sid = subject["subject_id"]
        if sid in seen_subjects:
            problems.append(_error("DUPLICATE_SUBJECT", f"subjects[{sidx}]", "Subject entry repeated."))
            continue
        seen_subjects.add(sid)
        topics = subject["topics"]
        blueprint = subject["blueprint_ref"]
        stage = subject["stage"]
        if stage == "PLANNED" and (topics or blueprint is not None):
            problems.append(_error("PLANNED_SUBJECT_HAS_CONTENT", f"subjects[{sidx}]",
                                   "PLANNED cannot claim an active Blueprint or topic."))
        if stage != "PLANNED" and (not topics or blueprint is None):
            problems.append(_error("ACTIVE_SUBJECT_MISSING_CONTENT", f"subjects[{sidx}]",
                                   "Active subject must have a pinned Blueprint and topic."))
        if blueprint is not None and blueprint["subject_id"] != sid:
            problems.append(_error("BLUEPRINT_SUBJECT_MISMATCH", f"subjects[{sidx}].blueprint_ref",
                                   "Blueprint belongs to a different subject."))
        seen_topics = set()
        for tidx, topic in enumerate(topics):
            path = f"subjects[{sidx}].topics[{tidx}]"
            tid = topic["topic_id"]
            if tid in seen_topics:
                problems.append(_error("DUPLICATE_TOPIC", path, "Topic repeated within subject."))
            seen_topics.add(tid)
            adapter = topic["adapter_ref"]
            if adapter["subject_id"] != sid or adapter["topic_id"] != tid:
                problems.append(_error("ADAPTER_SCOPE_MISMATCH", path,
                                       "Adapter does not belong to selected subject/topic."))
            if blueprint is not None and adapter["blueprint_sha256"] != blueprint["sha256"]:
                problems.append(_error("ADAPTER_BLUEPRINT_PIN_MISMATCH", path,
                                       "Adapter Blueprint hash differs from subject pin."))
            for collection in KINDS:
                for ridx, record in enumerate(topic[collection]):
                    record_path = f"{path}.{collection}[{ridx}]"
                    key = _fq(sid, tid, record["id"])
                    if any(key in records for records in index.values()):
                        problems.append(_error("DUPLICATE_SCOPED_RECORD", record_path,
                                               "Duplicate record ID in this subject/topic."))
                    index[TYPES[collection]][key] = (record, record_path, sid)
                    if collection == "warrants" and record["discipline"] != sid:
                        problems.append(_error("WARRANT_DISCIPLINE_MISMATCH", record_path,
                                               "Warrant must match subject discipline."))
        summary[sid] = {
            "stage": stage, "topic_count": len(topics),
            "candidate_source_count": sum(len(t["sources"]) for t in topics),
            "candidate_warrant_count": sum(len(t["warrants"]) for t in topics),
            "candidate_construction_count": sum(len(t["constructions"]) for t in topics),
            "qualified_construction_count": 0,
            "subject_blueprint_status": "OWNER_SOURCE_PIN_UNTRUSTED" if blueprint else "NOT_SUPPLIED",
            "academic_status": "HOLD",
        }

    for collection in KINDS:
        for record, path, sid in index[TYPES[collection]].values():
            for field, target_type in REF_FIELDS.get(collection, {}).items():
                for value in record[field]:
                    target_subject, _, _ = value.split("/", 2)
                    if target_subject != sid:
                        problems.append(_error("CROSS_SUBJECT_REFERENCE", path + "." + field,
                                               "Cross-subject references need a separate reviewed transfer contract."))
                    elif value not in index[target_type]:
                        wrong_type = any(value in records for kind, records in index.items()
                                         if kind != target_type)
                        problems.append(_error("REFERENCE_TYPE_MISMATCH" if wrong_type else "UNKNOWN_SCOPED_REFERENCE",
                                               path + "." + field, "Referenced type/ID not found in the same subject."))

    graph = {key: record["prerequisite_refs"]
             for key, (record, _, _) in index["construction"].items()}
    visited, active = set(), set()
    def walk(key):
        if key in active:
            problems.append(_error("PREREQUISITE_CYCLE", "constructions",
                                   "Prerequisite dependency graph contains a cycle."))
            return
        if key in visited:
            return
        active.add(key)
        for next_key in graph.get(key, ()):
            if next_key in graph:
                walk(next_key)
        active.remove(key)
        visited.add(key)
    for key in graph:
        walk(key)
    return _result(data, problems, summary)


def _result(data: dict, problems: list, summary: dict) -> dict:
    return {
        "schema_version": "2.0.0",
        "audit_type": "THREE_SUBJECT_CANDIDATE_INTAKE",
        "programme_id": data.get("programme_id"),
        "mechanical_status": "FAIL" if problems else "PASS",
        "qualification_status": "HOLD",
        "release_status": "HOLD",
        "subjects": summary,
        "diagnostics": sorted(problems, key=lambda d: (d["path"], d["code"])),
        "blocked_by": [
            "NATIVE_SHARED_SUBJECT_AUTHORITY",
            "INDEPENDENT_SUBJECT_BLUEPRINT_AND_WARRANTS",
            "TRUSTED_SMART_QRT_AND_SOURCE_CUSTODY",
            "REVIEWED_B1_B7_AND_LEARNER_RUNTIME",
            "SHARED_PUBLICATION_RELEASE_RECEIPTS",
        ],
        "warning": "NOT_ACADEMIC_APPROVAL: candidate schema and hash pins do not qualify any subject.",
    }
