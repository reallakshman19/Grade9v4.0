"""Read-only native Shared subject-workspace preflight.

Uses the *actual* Shared/tools/check_subjects.py discovery contract:
  <workspace>/<subject-directory>/adapter/CoreContracts.json
Never installs/executes subject adapters, copies curricula, or elevates
contract presence / native 'passed' claims into academic qualification.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .shared_dispatch import inspect_shared_dispatch
from .subjects import audit_subject_intake

ROLES = frozenset({"CORE1", "CORE2", "CORE1A", "CORE1B", "CORE2A", "CORE2B"})
SAFE_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")
NATIVE_BINDINGS = "gates/curriculum-bindings.v1.json"


def _issue(code, subject, severity="HOLD"):
    return {"code": code, "subject": subject, "severity": severity}


def _strict_json(path: Path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("duplicate-key")
            obj[key] = value
        return obj
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite")))


def _hash(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1048576):
            h.update(block)
    return h.hexdigest()


def _contained(root: Path, relative: Path):
    candidate = root / relative
    # Shared's checker uses Python file access. The preflight must not trust
    # symlinks that leave the supplied subject repository's root.
    if any(part in ("..", "") for part in relative.parts) or relative.is_absolute():
        return None
    target = candidate.resolve()
    if not target.is_relative_to(root):
        return None
    return target


def inspect_workspaces(manifest, root, bindings, native=None):
    """Inspect actual declared subject workspaces; ALWAYS academic HOLD.

    The output is a *preflight*, not a clone of native check_subjects.py. For
    contract interpretation and execution, run the original Shared checker
    in the real subject repository and supply its report separately.
    """
    issues, subjects = [], {}
    candidate = audit_subject_intake(manifest)
    if candidate["mechanical_status"] == "FAIL":
        issues.append(_issue("V2_MANIFEST_INVALID", "manifest", "FAIL"))
        return _output(issues, subjects, None)
    root = Path(root).resolve()
    if not root.is_dir():
        issues.append(_issue("SUBJECT_REPOSITORY_MISSING", "workspace"))
        return _output(issues, subjects, None)
    if not isinstance(bindings, dict):
        issues.append(_issue("EXPLICIT_SUBJECT_BINDINGS_REQUIRED", "bindings", "FAIL"))
        return _output(issues, subjects, None)
    recognized = {s["subject_id"] for s in manifest["subjects"]}
    if any(k not in recognized for k in bindings):
        issues.append(_issue("UNKNOWN_BINDING_SUBJECT", "bindings", "FAIL"))
    values = []
    for k, v in bindings.items():
        if not isinstance(v, str) or not SAFE_NAME.fullmatch(v):
            issues.append(_issue("UNSAFE_SUBJECT_DIR", str(k), "FAIL"))
        else:
            values.append(v)
    if len({v.casefold() for v in values}) != len(values):
        issues.append(_issue("COLLIDING_SUBJECT_DIRECTORIES", "bindings", "FAIL"))
    if any(i["severity"] == "FAIL" for i in issues):
        return _output(issues, subjects, None)

    shared_checker = _contained(root, Path("Shared/tools/check_subjects.py"))
    if shared_checker is None:
        issues.append(_issue("SHARED_TOOL_PATH_ESCAPE", "Shared", "FAIL"))
    elif not shared_checker.is_file():
        issues.append(_issue("ORIGINAL_SHARED_CHECKER_NOT_IN_ROOT", "Shared"))
    # Exact native checker provenance must still be externally pinned and
    # authenticated; source presence and SHA-256 alone never imply trust.
    native_contract_path = "adapter/CoreContracts.json"
    contract_digests = {}
    for sub in manifest["subjects"]:
        sid, stage = sub["subject_id"], sub["stage"]
        directory = bindings.get(sid)
        row = {
            "candidate_stage": stage, "subject_directory": directory,
            "contract_sha256": None, "six_core_contract": "NOT_CHECKED",
            "adapter_file_present": False,
            "gate_registry_files": 0, "library_package_files": 0,
            "native_discovery_status": "UNVERIFIED",
            "academic_status": "HOLD",
        }
        subjects[sid] = row
        if stage == "PLANNED":
            if directory is not None:
                issues.append(_issue("PLANNED_SUBJECT_WORKSPACE_PREMATURE", sid))
            continue
        if directory is None:
            issues.append(_issue("ACTIVE_SUBJECT_WORKSPACE_NOT_BOUND", sid))
            continue
        subroot = _contained(root, Path(directory))
        if subroot is None:
            issues.append(_issue("SUBJECT_ROOT_PATH_ESCAPE", sid, "FAIL"))
            continue
        contract_path = _contained(root, Path(directory) / native_contract_path)
        if contract_path is None:
            issues.append(_issue("CONTRACT_PATH_ESCAPE", sid, "FAIL"))
            continue
        if not contract_path.is_file():
            issues.append(_issue("CORE_CONTRACT_FILE_MISSING", sid))
            continue
        try:
            contract = _strict_json(contract_path)
            row["contract_sha256"] = _hash(contract_path)
        except (ValueError, UnicodeError, OSError):
            issues.append(_issue("CORE_CONTRACT_INVALID_JSON", sid, "FAIL"))
            continue
        if not isinstance(contract, dict):
            issues.append(_issue("CORE_CONTRACT_NOT_OBJECT", sid, "FAIL"))
            continue
        roles = contract.get("learner_products")
        if not isinstance(roles, dict) or set(roles) != ROLES:
            issues.append(_issue("SIX_CORE_ROLE_CONTRACT_MISMATCH", sid, "FAIL"))
            continue
        row["six_core_contract"] = "SIX_DECLARED_UNTRUSTED"
        for name, definition in roles.items():
            if not isinstance(definition, dict):
                issues.append(_issue("CORE_PRODUCT_STATE_INVALID", sid, "FAIL"))
                continue
            state = definition.get("production")
            if state not in ("COMPILED", "NOT_COMPILED"):
                issues.append(_issue("CORE_PRODUCT_PRODUCTION_UNKNOWN", sid, "FAIL"))
            if state == "NOT_COMPILED" and not str(definition.get("reason", "")).strip():
                issues.append(_issue("CORE_PRODUCT_MISSING_REASON", sid, "FAIL"))
        catalogue = contract.get("validator_catalogue", [])
        if not isinstance(catalogue, list):
            issues.append(_issue("NATIVE_VALIDATOR_CATALOGUE_INVALID", sid, "FAIL"))
        else:
            for entry in catalogue:
                if not isinstance(entry, dict) or not isinstance(entry.get("result"), dict):
                    issues.append(_issue("NATIVE_VALIDATOR_CONTRACT_INVALID", sid, "FAIL"))
                elif "comparison" not in entry["result"] or not str(entry.get("does_not_prove", "")).strip():
                    issues.append(_issue("NATIVE_VALIDATOR_LIMIT_MISSING", sid, "FAIL"))
        adapter_py = _contained(root, Path(directory) / "adapter/__init__.py")
        if adapter_py is None:
            issues.append(_issue("ADAPTER_PATH_ESCAPE", sid, "FAIL"))
        else:
            row["adapter_file_present"] = adapter_py.is_file()
            if not row["adapter_file_present"]:
                issues.append(_issue("SUBJECT_ADAPTER_NOT_SUPPLIED", sid))
        gates = _contained(root, Path(directory) / "gates")
        library = _contained(root, Path(directory) / "library")
        if gates is None or library is None:
            issues.append(_issue("SUBJECT_EVIDENCE_PATH_ESCAPE", sid, "FAIL"))
            continue
        gate_paths = [p for p in gates.glob("*.v1.json") if p.is_file() and p.name != Path(NATIVE_BINDINGS).name] if gates.is_dir() else []
        library_paths = [p for p in library.glob("*.json") if p.is_file()] if library.is_dir() else []
        for artifact in gate_paths + library_paths:
            if not artifact.resolve().is_relative_to(root):
                issues.append(_issue("SUBJECT_ARTIFACT_SYMLINK_ESCAPE", sid, "FAIL"))
        row["gate_registry_files"] = len(gate_paths)
        row["library_package_files"] = len(library_paths)
        if not gate_paths:
            issues.append(_issue("SUBJECT_GATE_REGISTRY_EMPTY", sid))
        if not library_paths:
            issues.append(_issue("SUBJECT_LIBRARY_PACKAGES_EMPTY", sid))
        if row["adapter_file_present"] and gate_paths and library_paths:
            issues.append(_issue("SUBJECT_CONTENT_REQUIRES_NATIVE_REVIEW", sid))
        contract_digests[sid] = row["contract_sha256"]

    if native is None:
        issues.append(_issue("NATIVE_SUBJECT_RUN_NOT_SUPPLIED", "Shared"))
    else:
        native_summary = inspect_shared_dispatch(manifest, native, bindings)
        for problem in native_summary["diagnostics"]:
            if problem["severity"] == "FAIL":
                issues.append(_issue("NATIVE_" + problem["code"], problem["path"], "FAIL"))
            elif problem["code"] != "NATIVE_JSON_EXECUTION_NOT_ATTESTED":
                issues.append(_issue("NATIVE_" + problem["code"], problem["path"]))
        raw_rows = native.get("subjects", []) if isinstance(native, dict) else []
        found = {r.get("subject"): r for r in raw_rows
                 if isinstance(r, dict) and isinstance(r.get("subject"), str)}
        unbound = set(found) - set(bindings.values())
        for name in sorted(unbound):
            issues.append(_issue("NATIVE_UNBOUND_SUBJECT_DIRECTORY", "Shared"))
        for sid, row in subjects.items():
            name = bindings.get(sid)
            if name in found:
                native_row = found[name]
                row["native_discovery_status"] = native_row.get("state", "UNKNOWN")
                if row["contract_sha256"] is None:
                    issues.append(_issue("NATIVE_SUBJECT_WITHOUT_LOCAL_CONTRACT", sid, "FAIL"))
                if row["native_discovery_status"] == "IMPLEMENTED":
                    if not row["adapter_file_present"]:
                        issues.append(_issue("NATIVE_IMPLEMENTED_WITHOUT_ADAPTER_FILE", sid, "FAIL"))
                    if (native_row.get("gate_registries") != row["gate_registry_files"]
                            or native_row.get("library_packages") != row["library_package_files"]):
                        issues.append(_issue("NATIVE_LOCAL_ARTIFACT_COUNT_DISAGREEMENT", sid, "FAIL"))
                    if row["gate_registry_files"] == 0 or row["library_package_files"] == 0:
                        issues.append(_issue("HOLLOW_IMPLEMENTED_SUBJECT", sid))
    return _output(issues, subjects, contract_digests)


def _output(issues, subjects, digests):
    failed = any(i["severity"] == "FAIL" for i in issues)
    return {
        "schema_version": "1.0.0",
        "audit_type": "NATIVE_SHARED_SUBJECT_WORKSPACE_PREFLIGHT",
        "mechanical_status": "FAIL" if failed else "HOLD",
        "academic_status": "HOLD",
        "canonical_promotion": "NOT_PERFORMED",
        "release_status": "HOLD",
        "subjects": subjects,
        "contract_digests_untrusted": digests or {},
        "diagnostics": sorted(issues, key=lambda x: (x["subject"], x["code"])),
        "blocked_by": [
            "TRUSTED_NATIVE_SHARED_SOURCE_AND_EXECUTION",
            "SUBJECT_BLUEPRINTS_AND_CUSTODY",
            "FULL_NATIVE_CHECK_SUBJECTS_ACCEPTANCE",
            "QUALIFIED_SUBJECT_LIBRARY_AND_REVIEW_RECEIPTS",
            "LEARNER_RUNTIME_AND_RELEASE_AUTHORITY",
        ],
        "warning": "NOT_ACADEMIC_APPROVAL: contract and directory presence cannot authorize a subject.",
    }
