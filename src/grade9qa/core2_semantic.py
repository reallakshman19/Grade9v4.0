"""Physics/WPE Blueprint x topic-adapter *structural* cell resolution.

Original QRT drafts are passed by the caller with exact byte pins.
The Owner must independently select an adapter and approve the Blueprint.
No QRT, source, Physics or release authority can be inferred from a match.
Do not apply this Physics resolver to Mathematics or Chemistry.
"""
from __future__ import annotations

import re

OPERATIONS = ("RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY")
HEX = re.compile(r"^[0-9a-f]{64}$")
FAMILY = re.compile(r"^WEP-(0[1-9]|10)$")
CELL = re.compile(r"^D[34]\.[1-7]$")


def _problem(code, identity="GENERAL", severity="HOLD"):
    return {"code": code, "subject": identity, "severity": severity}


def resolve_wpe_cells(blueprint: object, adapter: object, entries: object,
                      *, blueprint_digest: str | None = None,
                      adapter_digest: str | None = None,
                      selected_adapter_digest: str | None = None) -> dict:
    """Read-only resolution of a subset of source candidates to native QRT cells.

    Each input entry: source_id, operation, band, topic_family (nullable),
    optionally subtile_id and capability_refs. No original question content.
    Unsupported or unreviewed input is held; contradictions fail.
    """
    issues, resolutions = [], []
    if not isinstance(blueprint, dict) or not isinstance(adapter, dict):
        return _report([_problem("NATIVE_BLUEPRINT_OR_ADAPTER_NOT_OBJECT", severity="FAIL")], [])
    if not isinstance(entries, list) or len(entries) > 1000:
        return _report([_problem("QUESTION_CANDIDATE_LIST_INVALID", severity="FAIL")], [])
    if blueprint.get("blueprint_id") != "PHYS-QRT-BLUEPRINT" or blueprint.get("subject") != "Physics":
        issues.append(_problem("PHYSICS_BLUEPRINT_ID_OR_DISCIPLINE_MISMATCH", severity="FAIL"))
    if blueprint.get("column_order") != list(OPERATIONS):
        issues.append(_problem("BLUEPRINT_OPERATION_ORDER_MISMATCH", severity="FAIL"))
    bc = blueprint.get("cells")
    if not isinstance(bc, dict) or set(bc) != {
        f"D{band}.{index}" for band in (3, 4) for index in range(1, 8)
    }:
        issues.append(_problem("BLUEPRINT_14_CELL_COVERAGE_MISMATCH", severity="FAIL"))
        bc = bc if isinstance(bc, dict) else {}
    else:
        for key, body in bc.items():
            band, number = key.split(".")
            if not isinstance(body, dict) or body.get("template_ref") != (
                f"QRT-{OPERATIONS[int(number)-1]}-{band}"
            ):
                issues.append(_problem("BLUEPRINT_CELL_TEMPLATE_CHANGED", key, "FAIL"))
    if blueprint.get("status") != "APPROVED":
        issues.append(_problem("BLUEPRINT_OWNER_APPROVAL_MISSING"))
    if adapter.get("adapter_id") != "PHYS-TOPIC-WPE" or adapter.get("topic_id") != "WPE":
        issues.append(_problem("WRONG_SUBJECT_OR_WPE_ADAPTER", severity="FAIL"))
    if adapter.get("subject", "Physics") != "Physics":
        issues.append(_problem("ADAPTER_DISCIPLINE_MISMATCH", severity="FAIL"))
    version = blueprint.get("version")
    expected = f"{blueprint.get('blueprint_id')} {version}"
    pointer = adapter.get("for_blueprint")
    if isinstance(pointer, dict):
        matched = pointer.get("id") == blueprint.get("blueprint_id") and pointer.get("version") == version
    else:
        matched = pointer == expected
    if not matched:
        issues.append(_problem("BLUEPRINT_ADAPTER_VERSION_INCOMPATIBLE", severity="FAIL"))
    if adapter.get("status") != "APPROVED":
        issues.append(_problem("WPE_ADAPTER_APPROVAL_MISSING"))
    for name, digest in (("BLUEPRINT", blueprint_digest), ("ADAPTER", adapter_digest)):
        if not isinstance(digest, str) or not HEX.fullmatch(digest):
            issues.append(_problem(name + "_BYTE_PIN_REQUIRED", severity="FAIL"))
    if selected_adapter_digest is None:
        issues.append(_problem("OWNER_ADAPTER_SELECTION_NOT_SUPPLIED"))
    elif not HEX.fullmatch(selected_adapter_digest) or selected_adapter_digest != adapter_digest:
        issues.append(_problem("OWNER_SELECTION_ADAPTER_BYTE_MISMATCH", severity="FAIL"))
    else:
        # A matching self-declared pin is only a candidate. It is not a signed Owner receipt.
        issues.append(_problem("OWNER_ADAPTER_SELECTION_NOT_INDEPENDENTLY_ATTESTED"))
    families = adapter.get("families")
    family_ids = {x.get("id") for x in families if isinstance(x, dict)} if isinstance(families, list) else set()
    a_cells = adapter.get("cells")
    subtiles = adapter.get("subtiles")
    if not isinstance(a_cells, dict) and not isinstance(subtiles, dict):
        issues.append(_problem("TOPIC_ADAPTER_NO_KNOWN_NATIVE_CELL_MAP", severity="FAIL"))
        a_cells, subtiles = {}, {}
    seen = set()
    for idx, item in enumerate(entries):
        if not isinstance(item, dict):
            issues.append(_problem("ENTRY_NOT_OBJECT", str(idx), "FAIL"))
            continue
        sid, op, band = item.get("source_id"), item.get("operation"), item.get("band")
        if not isinstance(sid, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{1,127}", sid):
            issues.append(_problem("SOURCE_ID_INVALID", str(idx), "FAIL"))
            continue
        if sid in seen:
            issues.append(_problem("DUPLICATE_EXAM_IDENTITY_IN_SCOPE", sid, "FAIL"))
        seen.add(sid)
        result = {"source_id": sid, "operation": op if op in OPERATIONS else None,
                  "band": band if band in ("D1","D2","D3","D4") else None,
                  "blueprint_cell": None, "adapter_cell": None,
                  "family": None, "capabilities_structurally_present": False,
                  "resolution": "HOLD", "academic_status": "HOLD"}
        resolutions.append(result)
        if op not in OPERATIONS:
            issues.append(_problem("QRT_OPERATION_UNSUPPORTED", sid, "FAIL"))
            continue
        if band in ("D1", "D2"):
            issues.append(_problem("D1_D2_BLUEPRINT_NOT_AUTHORED", sid))
            continue
        if band not in ("D3", "D4"):
            issues.append(_problem("DEMAND_BAND_INVALID", sid, "FAIL"))
            continue
        key = f"{band}.{OPERATIONS.index(op)+1}"
        result["blueprint_cell"] = key
        cell = bc.get(key)
        if not isinstance(cell, dict) or cell.get("template_ref") != f"QRT-{op}-{band}":
            issues.append(_problem("REQUIRED_BLUEPRINT_CELL_UNAVAILABLE", sid, "FAIL"))
            continue
        family = item.get("topic_family")
        if family is None:
            issues.append(_problem("WPE_TOPIC_FAMILY_NOT_ADJUDICATED", sid))
        elif not isinstance(family, str) or not FAMILY.fullmatch(family):
            issues.append(_problem("WPE_TOPIC_FAMILY_INVALID", sid, "FAIL"))
        else:
            result["family"] = family
        matched_family = False
        if isinstance(a_cells, dict):
            native = a_cells.get(key)
            if not isinstance(native, dict):
                issues.append(_problem("ADAPTER_CELL_UNWRITTEN", sid))
                continue
            result["adapter_cell"] = key
            if native.get("tile_id") != f"PHY-WPE-{key}" or not str(native.get("blueprint_cell","")).startswith(key+" "):
                issues.append(_problem("ADAPTER_CELL_IDENTITY_MISMATCH", sid, "FAIL"))
                continue
            subs = native.get("subtopics")
            if not isinstance(subs, list) or not subs:
                issues.append(_problem("ADAPTER_CELL_EMPTY", sid, "FAIL"))
                continue
            all_caps = set()
            for sub in subs:
                if not isinstance(sub, dict):
                    issues.append(_problem("ADAPTER_SUBTOPIC_INVALID", sid, "FAIL"))
                    continue
                families_here = sub.get("family_refs")
                caps = sub.get("canonical_refs")
                if not isinstance(families_here, list) or not isinstance(caps, list) or not caps:
                    issues.append(_problem("ADAPTER_SUBTOPIC_FOREIGN_KEYS_MISSING", sid, "FAIL"))
                    continue
                if any(not isinstance(ref,str) or not FAMILY.fullmatch(ref) or ref not in family_ids
                       for ref in families_here):
                    issues.append(_problem("ADAPTER_SUBTOPIC_FAMILY_REF_UNRESOLVED", sid, "FAIL"))
                if family in families_here:
                    matched_family = True
                    all_caps.update(x for x in caps if isinstance(x,str))
            if family is not None and not matched_family:
                issues.append(_problem("ADAPTER_CELL_WRONG_TOPIC_FAMILY", sid, "FAIL"))
                continue
            requested = item.get("capability_refs")
            if not isinstance(requested, list) or not requested:
                issues.append(_problem("QRT_CAPABILITY_REVIEW_MISSING", sid))
            elif any(not isinstance(x,str) or x not in all_caps for x in requested):
                issues.append(_problem("ADAPTER_CAPABILITY_FOREIGN_KEY_UNRESOLVED", sid, "FAIL"))
            else:
                result["capabilities_structurally_present"] = True
        else:
            # Subtile adapters (v0.2.x) contain only specific D3.1.x instances,
            # not all fourteen operation cells and not generic WEP family mapping.
            subtile = item.get("subtile_id")
            if not isinstance(subtile, str) or not re.fullmatch(re.escape(key)+r"\.\d+", subtile):
                issues.append(_problem("SPECIFIC_SUBTILE_ID_REQUIRED", sid))
                continue
            native = subtiles.get(subtile)
            if not isinstance(native, dict):
                issues.append(_problem("SUBTILE_NOT_IN_SELECTED_ADAPTER", sid))
                continue
            result["adapter_cell"] = subtile
            # Native v0.2.x subtiles do not declare an independently adjudicated
            # WEP family. A matching unit ID alone never proves topic meaning.
            issues.append(_problem("SUBTILE_WEP_FAMILY_BINDING_UNSUPPORTED", sid))
            units = native.get("units")
            if not isinstance(units, list) or not units or not all(isinstance(x,str) and x for x in units):
                issues.append(_problem("SUBTILE_UNIT_REFS_INVALID", sid,"FAIL"))
                continue
            requested=item.get("capability_refs")
            if not isinstance(requested,list) or not requested:
                issues.append(_problem("QRT_CAPABILITY_REVIEW_MISSING", sid))
            elif any(x not in units for x in requested):
                issues.append(_problem("SUBTILE_UNIT_REFERENCE_MISSING", sid,"FAIL"))
            else:
                result["capabilities_structurally_present"] = True
        if result["family"] and matched_family and result["capabilities_structurally_present"]:
            result["resolution"] = "STRUCTURAL_MATCH_CANDIDATE_ONLY"
            issues.append(_problem("INDEPENDENT_QRT_SOURCE_PHYSICS_REVIEW_MISSING", sid))
    return _report(issues, resolutions)


def _report(issues, bindings):
    return {
        "schema_version": "1.0.0", "audit_type": "PHYSICS_WPE_NATIVE_BLUEPRINT_TOPIC_ADAPTER_RESOLUTION",
        "mechanical_status": "FAIL" if any(x["severity"]=="FAIL" for x in issues) else "HOLD",
        "academic_status": "HOLD", "core2_admission": "NOT_PERFORMED",
        "native_render": "NOT_PERFORMED", "release_status": "HOLD",
        "question_bindings": bindings,
        "diagnostics": sorted(issues, key=lambda x:(x["subject"],x["code"])),
        "blocked_by": ["OWNER_SELECTED_PINNED_WPE_ADAPTER",
                        "INDEPENDENT_SL1_SL2_QRT_ADJUDICATION",
                        "AUTHENTIC_PAPER_FIGURE_AND_OFFICIAL_KEY",
                        "SCOPED_PHYSICS_WARRANTS",
                        "NATIVE_SHARED_ACADEMIC_APPROVALS"],
        "warning": "NOT_ACADEMIC_APPROVAL: Physics WPE candidate-only contract; never use as Maths/Chemistry resolver.",
    }
