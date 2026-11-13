"""Read-only report adapter for native Smart Labelling R2 CANDIDATE.

This does NOT execute, install, replace, sign, or independently authenticate
the SL1/SL2 skills. It only summarizes a report produced elsewhere, and
can never issue approval based on that report alone.
"""
import re

R2_SCHEMA = "smart-labelling-check-report/v2"
R2_VERSION = "2.0.0-candidate"
GATES = (
    "integrity", "answer", "practice", "official_source", "official_key",
    "observations", "qrt", "canonical", "construction", "release",
)
ALLOWED_STATUSES = {"PASS", "HOLD", "NOT_APPLICABLE"}
SHA = re.compile(r"^sha256:[0-9a-f]{64}$")


def inspect_native_report(report: object) -> dict:
    """Summarize untrusted native report facts with a non-bypassable HOLD."""
    problems = []
    if not isinstance(report, dict):
        report = {}
        problems.append("REPORT_NOT_OBJECT")
    if report.get("schema") != R2_SCHEMA:
        problems.append("NATIVE_SCHEMA_MISMATCH")
    if report.get("checker_version") != R2_VERSION:
        problems.append("NATIVE_VERSION_UNRECOGNIZED")
    if report.get("mode") != "DETERMINISTIC_CONTRACT":
        problems.append("NOT_NATIVE_CONTRACT_CHECK")
    if report.get("legacy_checks") in (None, "NOT_RUN"):
        problems.append("LEGACY_CHECKS_NOT_EVIDENCED")
    if not isinstance(report.get("inputs"), dict) or not report["inputs"]:
        problems.append("INPUT_HASHES_NOT_EVIDENCED")
    elif any(not isinstance(h, str) or not SHA.fullmatch(h) for h in report["inputs"].values()):
        problems.append("INPUT_HASH_FORMAT_UNSUPPORTED")
    checker = report.get("checker_artifact")
    if not isinstance(checker, dict) or not SHA.fullmatch(str(checker.get("sha256", ""))):
        problems.append("CHECKER_HASH_NOT_EVIDENCED")
    records = report.get("records")
    if not isinstance(records, list) or not records:
        problems.append("NO_NATIVE_RECORDS")
        records = []
    summary = report.get("gate_summary")
    if not isinstance(summary, dict):
        summary = {}
        problems.append("MISSING_GATE_SUMMARY")
    states = {}
    for gate in GATES:
        value = summary.get(gate)
        if value not in ALLOWED_STATUSES:
            problems.append("MISSING_OR_INVALID_GATE:" + gate)
            states[gate] = "HOLD"
        else:
            states[gate] = value
    observed_ids = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            problems.append("INVALID_RECORD:" + str(index))
            continue
        record_id = record.get("question_id")
        if not isinstance(record_id, str) or not record_id:
            problems.append("MISSING_QUESTION_ID:" + str(index))
            continue
        if record_id in observed_ids:
            problems.append("DUPLICATE_QUESTION_ID:" + record_id)
        observed_ids.append(record_id)
        gates = record.get("gates")
        if not isinstance(gates, dict):
            problems.append("MISSING_RECORD_GATES:" + record_id)
            continue
        for gate in GATES:
            state = gates.get(gate)
            if state not in ALLOWED_STATUSES | {"NOT_RUN"}:
                problems.append("INVALID_RECORD_GATE:" + record_id + ":" + gate)
            if states[gate] == "PASS" and state != "PASS":
                # The native aggregate can be PASS with NOT_APPLICABLE in
                # some records; only HOLD/NOT_RUN is a contradictory claim.
                if state in ("HOLD", "NOT_RUN", None):
                    problems.append("CONTRADICTORY_AGGREGATE:" + record_id + ":" + gate)
    selected = report.get("selected_gate")
    if selected not in GATES or report.get("selected_gate_status") != states.get(selected):
        problems.append("SELECTED_GATE_MISMATCH")
    if not isinstance(report.get("issues"), list):
        problems.append("ISSUES_NOT_EVIDENCED")
    elif report["issues"] and states.get(selected) == "PASS":
        problems.append("ISSUES_CONTRADICT_PASS")
    return {
        "schema_version": "1.0.0",
        "integration": "SMART_LABELLING_R2_CANDIDATE",
        "native_report_schema": report.get("schema"),
        "native_checker_version": report.get("checker_version"),
        "native_selected_gate": selected,
        "native_check_status": "HOLD" if problems or states.get(selected) == "HOLD" else states.get(selected),
        "native_gate_summary": states,
        "question_count": len(observed_ids),
        "optional_p1_not_applicable": states["observations"] == "NOT_APPLICABLE",
        "diagnostic_codes": sorted(set(problems)),
        "integration_status": "HOLD",
        "qualification_status": "HOLD",
        "blocked_by": [
            "INDEPENDENT_R2_SKILL_ACCEPTANCE",
            "TRUSTED_NATIVE_ARTIFACT_PIN",
            "SHARED_QRT_PHYSICS_GOVERNANCE_BINDING",
            "INDEPENDENT_ACADEMIC_RELEASE_RECEIPTS",
        ],
        "warning": "NOT_ACADEMIC_APPROVAL: this is an untrusted read-only native report summary.",
    }
