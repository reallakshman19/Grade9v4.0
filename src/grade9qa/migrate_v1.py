"""Read-only, non-authorizing preview: historic Physics/WPE v1 -> subject v2.

Never modifies a v1 file, claims native Shared promotion or transmutes v1
APPROVED records into new candidate approval. Source bytes and status are
evidence, not proof of authority.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .errors import InputError
from .io import confined_path
from .subjects import audit_subject_intake
from .traceability import COLLECTIONS
from .validate import inspect


def _issue(code: str, path: str, category: str = "HOLD") -> dict:
    return {"code": code, "path": path, "severity": category}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_digest(data: object) -> str:
    """Native Shared canonical JSON encoding; output is NOT native attestation."""
    return _sha(json.dumps(data, sort_keys=True, ensure_ascii=False,
                           allow_nan=False, separators=(",", ":")).encode("utf-8"))


def _strict_object_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("DUPLICATE_JSON_KEY")
        obj[key] = value
    return obj


def _reject_constant(value):
    raise ValueError("NONFINITE_JSON_CONSTANT")


def _load_strict(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object_pairs,
                      parse_constant=_reject_constant)


def _fq(topic: str, identity: str) -> str:
    return f"PHYSICS/{topic}/{identity}"


def _finish(problems, candidate, digest_map, mappings, unresolved):
    if candidate is not None:
        audit = audit_subject_intake(candidate)
        for issue in audit["diagnostics"]:
            problems.append(_issue("V2_" + issue["code"], issue["path"], "FAIL"))
    failures = any(x["severity"] == "FAIL" for x in problems)
    return {
        "schema_version": "1.0.0",
        "audit_type": "V1_WPE_TO_V2_READ_ONLY_PREVIEW",
        "mechanical_status": "FAIL" if failures else ("HOLD" if problems else "PASS"),
        "qualification_status": "HOLD",
        "shared_canonical_admission": "NOT_PERFORMED",
        "source_file_pins": digest_map,
        "reference_mappings": mappings,
        "unresolved_fields": sorted(set(unresolved)),
        "diagnostics": sorted(problems, key=lambda d: (d["path"], d["code"])),
        "candidate_manifest": candidate if not failures and candidate is not None else None,
        "blocked_by": [
            "INDEPENDENT_V1_SOURCE_AND_NATIVE_DIGEST_ACCEPTANCE",
            "OWNER_LEGACY_BLUEPRINT_ADAPTER_ALIAS_REVIEW",
            "SHARED_NATIVE_CANONICAL_INTAKE",
            "SUBJECT_SCOPED_REVIEW_AUTHORITY_AND_RELEASE",
        ],
        "warning": "NOT_ACADEMIC_APPROVAL: proposed mapping never certifies subject truth or changes historic status.",
    }


def preview_v1_to_v2(bundle_path: Path, manifest_path: Path) -> dict:
    """Build a lossless *reference-map preview*, not a canonical conversion.

    Only sources, warrants and constructions are represented in v2 candidate
    intake. Lessons, assessments and approvals remain immutable v1 evidence
    with explicit NOT_MIGRATED mappings until their native contracts exist.
    """
    issues = []
    pins, mappings, unresolved = {}, [], []
    bundle_path, manifest_path = Path(bundle_path).resolve(), Path(manifest_path).resolve()
    try:
        if bundle_path == manifest_path:
            raise InputError("Bundle and v2 manifest must be distinct.")
        raw_bundle = bundle_path.read_bytes()
        bundle = _load_strict(bundle_path)
        base = _load_strict(manifest_path)
        pins["bundle.json"] = _sha(raw_bundle)
        pins["v2-base-manifest.json"] = _sha(manifest_path.read_bytes())
        # Reuse existing WPE v1 schemas and typed references; do not rewrite.
        _, original, structural_errors = inspect(bundle_path)
    except (OSError, ValueError, UnicodeError, InputError, TypeError) as exc:
        issues.append(_issue("INVALID_OR_UNREADABLE_INPUT", "inputs", "FAIL"))
        return _finish(issues, None, pins, mappings, unresolved)
    if structural_errors:
        for item in structural_errors:
            issues.append(_issue("V1_" + item.code, item.path, "FAIL"))
        return _finish(issues, None, pins, mappings, unresolved)
    base_audit = audit_subject_intake(base)
    if base_audit["mechanical_status"] != "PASS":
        issues.append(_issue("V2_BASE_MANIFEST_INVALID", "v2-base-manifest", "FAIL"))
        return _finish(issues, None, pins, mappings, unresolved)
    if bundle["topic_id"] != "WEP-01":
        # The first pilot conversion is explicitly scoped and separately tested.
        issues.append(_issue("PILOT_TOPIC_NOT_WEP01", "bundle.topic_id", "FAIL"))
        return _finish(issues, None, pins, mappings, unresolved)
    if bundle["status"] == "APPROVED":
        issues.append(_issue("HISTORIC_BUNDLE_APPROVAL_REQUIRES_REVIEW",
                             "bundle.status", "HOLD"))
        return _finish(issues, None, pins, mappings, unresolved)
    if base.get("status") != "CANDIDATE":
        issues.append(_issue("V2_BASE_PROMOTION_UNTRUSTED", "v2.status", "FAIL"))
        return _finish(issues, None, pins, mappings, unresolved)

    subjects = [s for s in base["subjects"] if s["subject_id"] == "PHYSICS"]
    if len(subjects) != 1:
        issues.append(_issue("PHYSICS_SUBJECT_NOT_UNIQUE", "v2.subjects", "FAIL"))
        return _finish(issues, None, pins, mappings, unresolved)
    topics = [t for t in subjects[0]["topics"] if t["topic_id"] == bundle["topic_id"]]
    if len(topics) != 1:
        issues.append(_issue("WPE_PILOT_TOPIC_NOT_UNIQUE", "v2.subjects.PHYSICS", "FAIL"))
        return _finish(issues, None, pins, mappings, unresolved)
    topic = topics[0]
    if topic.get("unit_id") != "WPE":
        issues.append(_issue("WPE_UNIT_MISMATCH", "v2.subjects.PHYSICS.WEP-01", "FAIL"))
    if any(topic[name] for name in ("sources", "warrants", "constructions")):
        issues.append(_issue("NONEMPTY_MIGRATION_TARGET", "v2.subjects.PHYSICS.WEP-01", "FAIL"))
    if issues:
        return _finish(issues, None, pins, mappings, unresolved)

    # Read all six original collections byte-for-byte and strictly reject
    # ambiguous duplicate keys. Keep paths relative to bundle root.
    strict_rows = {}
    for collection in COLLECTIONS:
        path = bundle["files"][collection]
        try:
            resolved = confined_path(bundle_path.parent, path)
            raw = resolved.read_bytes()
            data = _load_strict(resolved)
            if not isinstance(data, list) or data != original[collection]:
                raise ValueError("Original records differ from validated typed data")
            pins["v1/" + collection] = _sha(raw)
            strict_rows[collection] = data
        except (OSError, UnicodeError, ValueError, InputError):
            issues.append(_issue("V1_COLLECTION_NOT_STABLE", "v1/" + collection, "FAIL"))
    if issues:
        return _finish(issues, None, pins, mappings, unresolved)

    for collection in COLLECTIONS:
        for index, row in enumerate(strict_rows[collection]):
            rid = row["id"]
            state = row.get("status", "")
            old = f"v1/{collection}/{rid}"
            proposed = _fq(bundle["topic_id"], rid)
            converted = collection in ("sources", "warrants", "constructions")
            pinned = _canonical_digest(row)
            mappings.append({
                "old_ref": old, "proposed_ref": proposed,
                "collection": collection, "original_id": rid,
                "original_status": state, "original_record_json_sha256": pinned,
                "migration": "CANDIDATE_INTAKE_ONLY" if converted else "NOT_MIGRATED",
            })
            if state == "APPROVED":
                issues.append(_issue("HISTORIC_APPROVAL_NOT_PORTABLE", old, "HOLD"))
            elif converted and state not in ("CANDIDATE", "UNDER_REVIEW", "BLOCKED", "REJECTED"):
                issues.append(_issue("UNSUPPORTED_V1_RECORD_STATUS", old, "FAIL"))
            if not converted:
                unresolved.append("NATIVE_" + collection.upper() + "_MIGRATION_NOT_IMPLEMENTED")

    # The Physics pilot IDs disagree with the later original QRT artifact
    # identity/version. No alias is guessed or silently promoted.
    if bundle["blueprint_ref"] != (
        subjects[0]["blueprint_ref"]["id"] + "@" + subjects[0]["blueprint_ref"]["version"]
    ):
        issues.append(_issue("LEGACY_BLUEPRINT_ALIAS_REVIEW_REQUIRED", "bundle.blueprint_ref", "HOLD"))
        unresolved.append("PHYSICS_BLUEPRINT_ID_VERSION_ALIAS")
    if bundle["adapter_ref"] != (
        topic["adapter_ref"]["id"] + "@" + topic["adapter_ref"]["version"]
    ):
        issues.append(_issue("LEGACY_ADAPTER_ALIAS_REVIEW_REQUIRED", "bundle.adapter_ref", "HOLD"))
        unresolved.append("PHYSICS_WPE_ADAPTER_ID_VERSION_ALIAS")

    for idx, src in enumerate(strict_rows["sources"]):
        path = src.get("path", "")
        try:
            actual = confined_path(bundle_path.parent, path)
            raw = actual.read_bytes()
            recorded = src["sha256"]
            if _sha(raw) != recorded:
                issues.append(_issue("SOURCE_CONTENT_DIGEST_CHANGED", f"sources[{idx}]", "FAIL"))
            else:
                pins[f"original-source/{src['id']}"] = recorded
        except (OSError, UnicodeError, InputError):
            issues.append(_issue("SOURCE_ORIGINAL_BYTES_UNAVAILABLE", f"sources[{idx}]", "HOLD"))
    if any(i["severity"] == "FAIL" or i["code"] == "SOURCE_ORIGINAL_BYTES_UNAVAILABLE"
           for i in issues):
        # A missing original asset blocks even a mechanically portable preview:
        # an unverifiable source must not be wrapped into a new intake record.
        return _finish(issues, None, pins, mappings, unresolved)

    # Never silently downgrade an archived APPROVED status. Refuse the v2
    # preview unless an independent governance migration decides how to map it.
    if any(i["code"] == "HISTORIC_APPROVAL_NOT_PORTABLE" for i in issues):
        unresolved.append("OWNER_APPROVAL_MIGRATION_REVIEW")
        return _finish(issues, None, pins, mappings, unresolved)

    # Deep copy via strict JSON round-trip; neither input path is written.
    candidate = json.loads(json.dumps(base))
    chosen = [s for s in candidate["subjects"] if s["subject_id"] == "PHYSICS"][0]
    topic = [t for t in chosen["topics"] if t["topic_id"] == bundle["topic_id"]][0]
    prefix = lambda name: _fq(bundle["topic_id"], name)
    for src in strict_rows["sources"]:
        topic["sources"].append({
            "id": src["id"], "status": src["status"],
            "origin_ref": f"v1/{bundle['files']['sources']}#{src['id']}",
        })
    for w in strict_rows["warrants"]:
        topic["warrants"].append({
            "id": w["id"], "status": w["status"],
            "discipline": "PHYSICS",
            "source_refs": [prefix(rid) for rid in w["source_ids"]],
            "claim_ref": f"v1/{bundle['files']['warrants']}#{w['id']}.physics_claim",
        })
    for c in strict_rows["constructions"]:
        topic["constructions"].append({
            "id": c["id"], "status": c["status"],
            "operation": c["operation"], "band": c["band"],
            "grade_track": c["grade_track"],
            "direction": c["signature"]["direction"],
            "source_refs": [prefix(rid) for rid in c["source_ids"]],
            "warrant_refs": [prefix(rid) for rid in c["warrant_ids"]],
            "prerequisite_refs": [prefix(rid) for rid in c["prerequisite_ids"]],
        })
    return _finish(issues, candidate, pins, mappings, unresolved)
