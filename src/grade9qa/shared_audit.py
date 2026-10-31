"""Read-only compatibility inspection for Owner-supplied Shared.zip snapshots.

Does not execute imported Shared code or grant any academic authority.
A successful mechanical audit remains integration HOLD until Owner and
independent-review requirements are satisfied.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

REQUIRED_OPERATIONS = frozenset((
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY",
))
CORE_ROLES = ("CORE1", "CORE2", "CORE1A", "CORE1B", "CORE2A", "CORE2B")
REQUIRED_AUTHORITIES = {
    "CORE1": {"CANONICAL_ACADEMIC_TRUTH"},
    "CORE1A": {"CANONICAL_ACADEMIC_TRUTH"},
    "CORE1B": {"CANONICAL_ACADEMIC_TRUTH"},
    "CORE2": {"AUTHORIZED_SOURCE_CUSTODY"},
    "CORE2A": {"CANONICAL_ACADEMIC_TRUTH"},
    "CORE2B": {"CANONICAL_ACADEMIC_TRUTH", "PRIOR_EXPOSURE"},
}
CONTRACT_BLOCK = re.compile(r"^" + "\x60"*3 + r"core-authority\s*$\n(.*?)^" + "\x60"*3 + r"\s*$",
                             re.MULTILINE | re.DOTALL)
EXPECTED_G9_SCOPE = "PREREQUISITE"


def _finding(code: str, severity: str, path: str, detail: str) -> dict:
    return {"code": code, "severity": severity, "path": path, "detail": detail}


def _hash_bytes(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as reader:
        while block := reader.read(1048576):
            digest.update(block)
    return digest.hexdigest()


def _under(root: Path, name: str) -> Path | None:
    """Reject absolute, parent traversal, and symlinks escaping the source root."""
    raw = Path(name)
    if raw.is_absolute() or ".." in raw.parts or not name.startswith("Shared/"):
        return None
    path = (root / raw.relative_to("Shared")).resolve()
    if not path.is_relative_to(root.resolve()):
        return None
    return path


def audit_shared(shared_root: Path, baseline: dict, *, archive: Path | None = None,
                 construction_schema: Path | None = None) -> dict:
    root = Path(shared_root).resolve()
    issues: list[dict] = []
    checked = 0
    expected = baseline.get("files")
    if not isinstance(expected, list) or not expected:
        issues.append(_finding("BASELINE_PINS_MISSING", "FAIL", "baseline.files",
                               "Expected at least one explicitly pinned file."))
        expected = []
    if baseline.get("schema_version") != "1.0.0":
        issues.append(_finding("BASELINE_VERSION_INVALID", "FAIL", "baseline.schema_version",
                               "Unrecognized baseline schema."))
    if baseline.get("trust") != "OWNER_SUPPLIED_UNVERIFIED":
        issues.append(_finding("BASELINE_TRUST_MISMATCH", "FAIL", "baseline.trust",
                               "Baseline must not claim independent verification."))
    if not root.is_dir():
        issues.append(_finding("SHARED_ROOT_MISSING", "HOLD", str(root),
                               "Provide extracted Shared/ folder; do not auto-download or execute it."))
    for record in expected:
        if not isinstance(record, dict):
            issues.append(_finding("BASELINE_ENTRY_INVALID", "FAIL", "baseline.files", "Object required."))
            continue
        name = record.get("path", "")
        path = _under(root, name) if isinstance(name, str) else None
        if path is None:
            issues.append(_finding("PATH_ESCAPE", "FAIL", str(name), "Disallowed path in upstream pin."))
            continue
        if not path.is_file():
            issues.append(_finding("PINNED_FILE_MISSING", "HOLD", str(name), "Missing required upstream file."))
            continue
        try:
            actual_sha = _hash_bytes(path)
            actual_size = path.stat().st_size
        except OSError as exc:
            issues.append(_finding("PINNED_FILE_UNREADABLE", "HOLD", str(name), str(exc)))
            continue
        if actual_sha != record.get("sha256") or actual_size != record.get("size"):
            issues.append(_finding("PINNED_FILE_CHANGED", "FAIL", str(name),
                                   "Hash/size differs from supplied external baseline."))
        else:
            checked += 1

    if root.is_dir() and isinstance(baseline.get("file_count"), int):
        count = sum(1 for p in root.rglob("*") if p.is_file())
        if count != baseline["file_count"]:
            issues.append(_finding("SHARED_FILE_COUNT_DRIFT", "HOLD", "Shared/",
                                   f"Found {count}; archive baseline records {baseline['file_count']} files."))
    else:
        count = 0

    archive_status = "NOT_SUPPLIED"
    if archive is not None:
        archive_path = Path(archive)
        try:
            valid_digest = _hash_bytes(archive_path) == baseline.get("source_archive_sha256")
            with zipfile.ZipFile(archive_path) as zf:
                archive_count = sum(not item.is_dir() for item in zf.infolist())
            if not valid_digest or archive_count != baseline.get("file_count"):
                archive_status = "FAIL"
                issues.append(_finding("SHARED_ARCHIVE_MISMATCH", "FAIL", str(archive_path),
                                       "Archive digest or contained file count differs from baseline."))
            else:
                archive_status = "PASS_OWNER_SUPPLIED_PIN"
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            archive_status = "HOLD"
            issues.append(_finding("SHARED_ARCHIVE_UNREADABLE", "HOLD", str(archive_path), str(exc)))

    roles = {}
    order_is_not_authority = False
    source = _under(root, "Shared/roles/CORE-AUTHORITY-CONTRACT.md")
    if source is not None and source.is_file():
        try:
            content = source.read_text(encoding="utf-8")
            blocks = CONTRACT_BLOCK.findall(content)
            if len(blocks) != 1:
                raise ValueError(f"Expected one core-authority block, found {len(blocks)}")
            contract = json.loads(blocks[0])
            role_records = contract.get("roles")
            if not isinstance(role_records, dict):
                raise ValueError("roles must be a JSON object")
            order_is_not_authority = contract.get("invariants", {}).get("execution_order_is_not_authority_order") is True
            if not order_is_not_authority:
                issues.append(_finding("AUTHORITY_ORDER_INVERSION", "FAIL",
                                       "Shared/roles/CORE-AUTHORITY-CONTRACT.md",
                                       "Operational order must not become academic authority."))
            for role in CORE_ROLES:
                row = role_records.get(role)
                if not isinstance(row, dict):
                    issues.append(_finding("CORE_ROLE_MISSING", "FAIL", role, "Six-Core role definition absent."))
                    continue
                required = set(row.get("required_authority") or [])
                roles[role] = sorted(required)
                if not REQUIRED_AUTHORITIES[role].issubset(required):
                    issues.append(_finding("CORE_ROLE_AUTHORITY_CONFLICT", "FAIL", role,
                                           f"Expected authority {sorted(REQUIRED_AUTHORITIES[role])}."))
                if role in ("CORE1", "CORE1A", "CORE1B"):
                    if "AUTHORIZED_SOURCE_CUSTODY" in required or "AUTHORIZED_SOURCE_CUSTODY" not in set(row.get("forbidden_authority_substitution") or []):
                        issues.append(_finding("CORE1_SOURCE_AUTHORITY_CONFLICT", "FAIL", role,
                                               "Core1-family academic authority must remain canonical."))
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
            issues.append(_finding("CORE_AUTHORITY_CONTRACT_INVALID", "FAIL", "roles/CORE-AUTHORITY-CONTRACT.md", str(exc)))
    else:
        issues.append(_finding("CORE_AUTHORITY_CONTRACT_MISSING", "HOLD",
                               "roles/CORE-AUTHORITY-CONTRACT.md", "Cannot inspect six-Core authority."))

    operations: list[str] = []
    policy_value = None
    def load_object(name: str) -> dict | None:
        path = _under(root, "Shared/" + name)
        if path is None or not path.is_file():
            issues.append(_finding("SHARED_POLICY_FILE_MISSING", "HOLD", name, "File absent."))
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError("Expected a JSON object")
            return value
        except (OSError, ValueError, UnicodeError) as exc:
            issues.append(_finding("SHARED_POLICY_FILE_INVALID", "FAIL", name, str(exc)))
            return None

    vocab = load_object("vocabularies/cognitive-demand.v1.json")
    if vocab is not None:
        declared = vocab.get("demands")
        if not isinstance(declared, dict) or set(declared) != REQUIRED_OPERATIONS:
            issues.append(_finding("COGNITIVE_VOCABULARY_CONFLICT", "FAIL",
                                   "vocabularies/cognitive-demand.v1.json",
                                   "Seven canonical operations differ from Grade9QA enum."))
        else:
            operations = sorted(declared)
    if construction_schema is not None and vocab is not None:
        try:
            schema = json.loads(Path(construction_schema).read_text(encoding="utf-8"))
            mapped = set(schema["properties"]["operation"]["enum"])
            if mapped != set(vocab["demands"]):
                issues.append(_finding("GRADE9QA_VOCABULARY_DRIFT", "FAIL", str(construction_schema),
                                       "Grade9QA schema operation enum diverges from Shared's vocabulary."))
        except (OSError, ValueError, KeyError, TypeError) as exc:
            issues.append(_finding("GRADE9QA_SCHEMA_UNREADABLE", "FAIL", str(construction_schema), str(exc)))

    policy = load_object("policy/grade9-physics.v1.json")
    if policy is not None:
        entries = [x for x in policy.get("concept_policies", [])
                   if isinstance(x, dict) and x.get("concept_id") == "WORK_ENERGY"]
        if len(entries) != 1:
            issues.append(_finding("WORK_ENERGY_SCOPE_MISSING", "FAIL",
                                   "policy/grade9-physics.v1.json", "Expected exactly one WORK_ENERGY record."))
        else:
            policy_value = entries[0].get("scope_class")
            if policy_value != EXPECTED_G9_SCOPE:
                issues.append(_finding("WORK_ENERGY_SCOPE_CHANGED", "FAIL",
                                       "policy/grade9-physics.v1.json",
                                       "Grade9 policy must remain PREREQUISITE until separately authorized."))

    failures = any(x["severity"] == "FAIL" for x in issues)
    mechanical = "FAIL" if failures else ("HOLD" if issues else "PASS")
    return {
        "schema_version": "1.0.0",
        "audit_type": "EXTERNAL_SHARED_BASELINE",
        "source_archive_sha256_from_untrusted_baseline": baseline.get("source_archive_sha256"),
        "archive_integrity": archive_status,
        "pinned_files_checked": checked,
        "pinned_files_expected": len(expected),
        "files_seen": count,
        "files_expected": baseline.get("file_count"),
        "mechanical_status": mechanical,
        "authority_contract": {"roles": roles, "execution_order_is_not_authority_order": order_is_not_authority},
        "cognitive_operations": operations,
        "grade9_work_energy_scope": policy_value,
        "diagnostics": sorted(issues, key=lambda f: (f["path"], f["code"])),
        "integration_status": "HOLD",
        "qualification_status": "HOLD",
        "blocked_by": [
            "OWNER_SHARED_REDISTRIBUTION_DECISION",
            "INDEPENDENT_BASELINE_AND_FULL_SOURCE_REVIEW",
            "SHARED_RUNTIME_INTEGRATION_TESTS",
            "SMART_SKILLS_R2_REVIEW",
            "OWNER_AUTHORITY_WORKFLOW_CONFIRMATION",
        ],
        "warning": "NOT_ACADEMIC_APPROVAL: archive/role compatibility does not certify Physics, QRT, or release.",
    }
