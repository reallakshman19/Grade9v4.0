"""Read-only bridge to the REAL Shared/tools/check_subjects.py report.

Shared discovers subjects from <subject>/adapter/CoreContracts.json. This
adapter does not re-implement Shared, execute it, infer directory names, or
authenticate a JSON report. Planned subjects need no fake native adapter.
"""
from __future__ import annotations

import re
from .subjects import audit_subject_intake

SUBJECTS = {"PHYSICS", "MATHEMATICS", "CHEMISTRY"}
NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")


def _problem(code, where, severity="HOLD"):
    return {"code": code, "path": where, "severity": severity}


def inspect_shared_dispatch(candidate: object, native: object, bindings: object) -> dict:
    issues = []
    candidate_result = audit_subject_intake(candidate)
    if candidate_result["mechanical_status"] == "FAIL":
        issues.append(_problem("V2_INTAKE_INVALID", "candidate", "FAIL"))
        return _report(issues, {}, 0)
    if not isinstance(native, dict):
        issues.append(_problem("NATIVE_SHARED_REPORT_MISSING", "native", "HOLD"))
        native = {}
    if not isinstance(bindings, dict):
        issues.append(_problem("EXPLICIT_DIRECTORY_BINDINGS_REQUIRED", "bindings", "FAIL"))
        bindings = {}
    binding_keys = set(bindings)
    if not binding_keys.issubset(SUBJECTS):
        issues.append(_problem("UNKNOWN_SUBJECT_BINDING", "bindings", "FAIL"))
    if any(not isinstance(v, str) or not NAME.fullmatch(v) for v in bindings.values()):
        issues.append(_problem("UNSAFE_SUBJECT_DIRECTORY_BINDING", "bindings", "FAIL"))
    string_names = [x for x in bindings.values() if isinstance(x, str)]
    if len(set(string_names)) != len(string_names) or len(set(x.casefold() for x in string_names)) != len(string_names):
        issues.append(_problem("DUPLICATE_NATIVE_SUBJECT_BINDING", "bindings", "FAIL"))

    reported = native.get("subjects")
    count = native.get("subjects_checked")
    passed = native.get("passed")
    discovered = {}
    if not isinstance(reported, list) or type(count) is not int or count < 0:
        issues.append(_problem("INVALID_NATIVE_DISCOVERY_REPORT", "native", "FAIL"))
        reported = []
    elif count != len(reported):
        issues.append(_problem("NATIVE_COUNT_INCONSISTENT", "native.subjects_checked", "FAIL"))
    elif count == 0:
        issues.append(_problem("NATIVE_NO_SUBJECTS_DISCOVERED", "native", "HOLD"))
    if not isinstance(passed, bool):
        issues.append(_problem("NATIVE_PASSED_STATUS_MISSING", "native.passed", "FAIL"))
    elif passed and not reported:
        issues.append(_problem("VACUOUS_NATIVE_PASS", "native", "FAIL"))
    elif not passed and reported:
        issues.append(_problem("NATIVE_DISCOVERY_NOT_PASSING", "native", "HOLD"))

    for i, row in enumerate(reported):
        if not isinstance(row, dict):
            issues.append(_problem("INVALID_NATIVE_SUBJECT_ROW", f"native.subjects[{i}]", "FAIL"))
            continue
        name, state = row.get("subject"), row.get("state")
        if not isinstance(name, str) or not NAME.fullmatch(name) or name in discovered:
            issues.append(_problem("NATIVE_SUBJECT_NAME_INVALID_OR_REPEATED", f"native.subjects[{i}]", "FAIL"))
            continue
        if state not in ("CONTRACT_ONLY", "IMPLEMENTED"):
            issues.append(_problem("UNKNOWN_NATIVE_SUBJECT_STATE", f"native.subjects[{i}]", "FAIL"))
        if not isinstance(row.get("findings"), list):
            issues.append(_problem("NATIVE_SUBJECT_FINDINGS_MISSING", f"native.subjects[{i}]", "FAIL"))
        elif row["findings"]:
            issues.append(_problem("NATIVE_SUBJECT_FINDINGS_PRESENT", f"native.subjects[{i}]", "FAIL"))
        if type(row.get("gate_registries")) is not int or type(row.get("library_packages")) is not int:
            issues.append(_problem("NATIVE_SUBJECT_COUNTS_INVALID", f"native.subjects[{i}]", "FAIL"))
        elif row["gate_registries"] < 0 or row["library_packages"] < 0:
            issues.append(_problem("NATIVE_SUBJECT_COUNTS_INVALID", f"native.subjects[{i}]", "FAIL"))
        discovered[name] = {"state": state}
    results = {}
    for subject in candidate.get("subjects", []):
        sid = subject["subject_id"]
        desired = subject["stage"] != "PLANNED"
        mapped = bindings.get(sid)
        present = discovered.get(mapped)
        if desired and mapped is None:
            issues.append(_problem("ACTIVE_SUBJECT_NATIVE_BINDING_MISSING", sid, "HOLD"))
        elif desired and present is None:
            issues.append(_problem("ACTIVE_SUBJECT_NOT_NATIVE_DISCOVERED", sid, "HOLD"))
        elif desired and present["state"] != "IMPLEMENTED":
            issues.append(_problem("ACTIVE_SUBJECT_CONTRACT_ONLY", sid, "HOLD"))
        if not desired and mapped is not None:
            issues.append(_problem("PLANNED_SUBJECT_PREMATURE_NATIVE_BINDING", sid, "HOLD"))
        results[sid] = {
            "candidate_stage": subject["stage"],
            "bound_native_directory": mapped,
            "native_state": present["state"] if present else "NOT_DISCOVERED",
            "subject_acceptance": "HOLD",
        }
    issues.append(_problem("NATIVE_JSON_EXECUTION_NOT_ATTESTED", "native", "HOLD"))
    issues.append(_problem("SHARED_CANONICAL_PROMOTION_NOT_ATTEMPTED", "canonical", "HOLD"))
    return _report(issues, results, len(discovered))


def _report(issues, subjects, discovered_count):
    return {
        "schema_version": "1.0.0",
        "audit_type": "SHARED_NATIVE_SUBJECT_DISCOVERY_READ_ONLY",
        "mechanical_status": "FAIL" if any(i["severity"] == "FAIL" for i in issues) else "HOLD",
        "academic_status": "HOLD",
        "canonical_admission": "NOT_PERFORMED",
        "release_status": "HOLD",
        "native_subjects_discovered": discovered_count,
        "subjects": subjects,
        "diagnostics": sorted(issues, key=lambda x: (x["path"], x["code"])),
        "blocked_by": ["TRUSTED_NATIVE_SHARED_EXECUTION_AND_REPORT",
                       "INDEPENDENT_SUBJECT_CANONICAL_REVIEWS",
                       "NATIVE_SOURCE_AND_B1_B7_RECEIPTS",
                       "LEARNER_RUNTIME_PUBLICATION_AUTHORITY"],
        "warning": "NOT_ACADEMIC_APPROVAL: a native discovery JSON claim is not a Shared approval receipt.",
    }
