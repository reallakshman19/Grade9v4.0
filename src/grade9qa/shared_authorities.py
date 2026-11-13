"""Read-only adapter for native Shared review/release authority audit results.

A native Passed audit with zero receipts is not a review receipt.
An arbitrary JSON object claiming 'verified' is not a trusted native invocation.
The adapter always returns integration HOLD.
"""
from __future__ import annotations


def _issue(code, detail):
    return {"code": code, "detail": detail}


def summarize_authorities(review: object, release: object, core: object) -> dict:
    issues = []
    counts = {}
    def inspect_report(name, data, list_key):
        if not isinstance(data, dict):
            issues.append(_issue(name + "_REPORT_INVALID", "Report must be a JSON object."))
            return 0
        rows = data.get(list_key)
        findings = data.get("findings")
        if not isinstance(rows, list) or not isinstance(findings, list):
            issues.append(_issue(name + "_SHAPE_INVALID", "Expected list of rows and findings."))
            return 0
        if data.get("passed") is not True or findings:
            issues.append(_issue(name + "_NATIVE_FAILURE", "Native report contains failed checks or findings."))
        for i, row in enumerate(rows):
            if not isinstance(row, dict) or not row.get("path"):
                issues.append(_issue(name + "_RECEIPT_INVALID", f"Invalid receipt row {i}."))
            elif name == "REVIEW":
                if row.get("verified") is not True or row.get("findings"):
                    issues.append(_issue("REVIEW_RECEIPT_NOT_VERIFIED", f"Review receipt row {i} is unverified."))
            elif name == "RELEASE":
                if row.get("verified") is not True or row.get("findings"):
                    issues.append(_issue("RELEASE_RECEIPT_NOT_VERIFIED", f"Release receipt row {i} is unverified."))
        counts[name.lower() + "_receipts_reported"] = len(rows)
        if not rows:
            issues.append(_issue(name + "_NO_RECEIPTS", "Native audit passed vacuously; no reviewed receipt is present."))
        return len(rows)

    inspect_report("REVIEW", review, "receipts")
    inspect_report("RELEASE", release, "receipts")
    if isinstance(release, dict):
        self_auth = release.get("self_authorized_manifests")
        if not isinstance(self_auth, list) or self_auth:
            issues.append(_issue("RELEASE_SELF_AUTHORIZATION", "A publication cannot self-authorize, or evidence is missing."))
    if not isinstance(core, dict) or core.get("passed") is not True or core.get("roles_checked") != 6:
        issues.append(_issue("CORE_AUTHORITY_UNVERIFIED", "Expected passing six-Core native authority audit."))
    elif not isinstance(core.get("findings"), list) or core["findings"]:
        issues.append(_issue("CORE_AUTHORITY_FINDINGS", "Six-Core authority report is incomplete or has findings."))

    structural_failure = any(
        i["code"].endswith(("_REPORT_INVALID", "_SHAPE_INVALID", "_NATIVE_FAILURE", "_RECEIPT_INVALID",
                            "_NOT_VERIFIED", "_SELF_AUTHORIZATION", "_UNVERIFIED", "_FINDINGS"))
        for i in issues
    )
    return {
        "schema_version": "1.0.0",
        "source": "EXTERNAL_UNTRUSTED_NATIVE_SHARED_REPORTS",
        "receipt_counts": counts,
        "mechanical_status": "FAIL" if structural_failure else "HOLD",
        "authority_status": "HOLD",
        "qualification_status": "HOLD",
        "integration_status": "HOLD",
        "diagnostics": issues,
        "blocked_by": ["NATIVE_RUN_ATTESTATION", "CURRENT_SUBJECT_RECEIPT_DIGEST_BINDING",
                       "TRUSTED_SHARED_BASELINE", "INDEPENDENT_GOVERNANCE_REVIEW"],
        "warning": "NOT_ACADEMIC_APPROVAL: native report JSON is not a trusted execution receipt.",
    }
