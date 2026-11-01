"""Owner-source WPE D3.1.1 pilot evidence readback, not an academic reviewer.

Reads only five fixed, small JSON/Markdown members of the three original
Owner-supplied ZIPs. Never extracts files, executes source scripts, embeds
exam text, promotes old source/role IDs, or issues approval. All states HOLD.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

SOURCES = {
    "d3": {
        "archive_sha256": "b664284944de4eb76775a089ecdf795a86cd99d250081625aca700dc90f2356c",
        "members": {
            "witness": "WPE_D3_Organized_2026-10-30/packages/WPE_D31_RECALL_FULL_PACKAGE/05_constructions/D3.1.1/bridge_witness.json",
            "source_register": "WPE_D3_Organized_2026-10-30/packages/WPE_D31_RECALL_FULL_PACKAGE/01_sources/source_register.json",
            "physics_authority": "WPE_D3_Organized_2026-10-30/packages/WPE_D31_RECALL_FULL_PACKAGE/03_canonical/physics_authority_review.md",
        },
    },
    "handoff": {
        "archive_sha256": "c14de8a538c2276855a5f911dc9685adbebd159f5c631ff870daba87a05ab681",
        "members": {
            "handoff": "skill/source-to-core1a/examples/wpe-work-direction/handoff.json",
        },
    },
    "hub": {
        "archive_sha256": "50fb7c1e5cba1a9fba4efea360452ed06cb97efc2f370ab382e6598b13583705",
        "members": {
            "browser_checks": "BROWSER_CHECKS.json",
        },
    },
}
GATES = ("B1", "B2", "B3", "B4", "B5", "B6", "B7")
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
MAX_MEMBER_SIZE = 250_000
# Preserve only known native status tokens. Never output arbitrary strings.
ALLOWED = frozenset((
    "HOLD", "PARTIAL", "PARTIAL_STRUCTURAL_ONLY", "NOT_RUN",
    "LOCAL_PREVIEW_CHECKS_ONLY", "PASS", "APPROVED", "FAIL", "REJECTED",
))


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1048576):
            h.update(chunk)
    return h.hexdigest()


def _read_selected(path: Path, members: dict[str, str]) -> tuple[dict, dict]:
    objects, hashes = {}, {}
    with zipfile.ZipFile(path) as archive:
        for label, member in members.items():
            info = archive.getinfo(member)
            if info.is_dir() or info.file_size > MAX_MEMBER_SIZE or info.file_size <= 0:
                raise ValueError("UNSAFE_OR_OVERSIZED_EVIDENCE_MEMBER")
            with archive.open(info) as reader:
                content = reader.read(MAX_MEMBER_SIZE + 1)
            if len(content) != info.file_size or len(content) > MAX_MEMBER_SIZE:
                raise ValueError("EVIDENCE_MEMBER_LENGTH_MISMATCH")
            hashes[label] = hashlib.sha256(content).hexdigest()
            if member.endswith(".json"):
                def unique(pairs):
                    out = {}
                    for key, value in pairs:
                        if key in out:
                            raise ValueError("DUPLICATE_EVIDENCE_JSON_KEY")
                        out[key] = value
                    return out
                objects[label] = json.loads(
                    content.decode("utf-8"), object_pairs_hook=unique,
                    parse_constant=lambda value: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")),
                )
            else:
                objects[label] = content.decode("utf-8")
    return objects, hashes


def _issue(code, status="HOLD"):
    return {"code": code, "severity": status}


def readback_pilot(d3_archive: Path, handoff_archive: Path, hub_archive: Path,
                   *, source_contract: dict | None = None) -> dict:
    """Read the exact three Owner-supplied archive versions.

    source_contract is optional only for isolated synthetic unit fixtures;
    the CLI uses immutable SOURCES above. No external signer trust is implied.
    """
    spec = source_contract if source_contract is not None else SOURCES
    sources, pins, diagnostics = {}, {}, []
    archives = {"d3": Path(d3_archive), "handoff": Path(handoff_archive), "hub": Path(hub_archive)}
    for label, path in archives.items():
        try:
            sha = _digest(path)
            if sha != spec[label]["archive_sha256"]:
                diagnostics.append(_issue("ARCHIVE_PIN_MISMATCH_" + label.upper(), "FAIL"))
                continue
            values, member_pins = _read_selected(path, spec[label]["members"])
            sources.update(values)
            pins[label] = {"archive_sha256": sha, "members_sha256": member_pins}
        except (OSError, zipfile.BadZipFile, KeyError, ValueError, UnicodeError) :
            diagnostics.append(_issue("ARCHIVE_OR_MEMBER_INVALID_" + label.upper(), "FAIL"))
    if len(pins) != 3:
        return _finish(pins, diagnostics, {}, {})

    witness = sources["witness"]
    register = sources["source_register"]
    handoff = sources["handoff"]
    hub = sources["browser_checks"]
    if not all(isinstance(x, dict) for x in (witness, register, handoff, hub)):
        diagnostics.append(_issue("EVIDENCE_RECORD_NOT_OBJECT", "FAIL"))
        return _finish(pins, diagnostics, {}, {})

    cid = witness.get("construction_id")
    if not isinstance(cid, str) or not SAFE_ID.fullmatch(cid):
        diagnostics.append(_issue("CONSTRUCTION_ID_INVALID", "FAIL"))
        cid = None
    if witness.get("witness_version") != "0.1.DERIVED_NONCANONICAL" or witness.get("subset") != "D3.1.1":
        diagnostics.append(_issue("D31_WITNESS_IDENTITY_MISMATCH", "FAIL"))
    states = witness.get("B1_B7_status")
    states = states if isinstance(states, dict) else {}
    statuses = {}
    for gate in GATES:
        native = states.get(gate)
        if not isinstance(native, str) or native not in ALLOWED:
            diagnostics.append(_issue("B_GATE_STATUS_INVALID_" + gate, "FAIL"))
            statuses[gate] = "UNRECOGNIZED"
        else:
            statuses[gate] = native
            if native in ("FAIL", "REJECTED"):
                diagnostics.append(_issue("NATIVE_B_GATE_REJECTION_" + gate, "FAIL"))
            else:
                diagnostics.append(_issue("INDEPENDENT_B_GATE_NOT_VERIFIED_" + gate))
    if witness.get("operation") != "RECALL_CLASSIFY_PROPOSED" or witness.get("demand_level") != "D3_PROPOSED":
        diagnostics.append(_issue("D31_COGNITIVE_PROPOSAL_CHANGED", "FAIL"))

    source = witness.get("source_alignment") or {}
    if not isinstance(source, dict):
        source = {}
    if source.get("original_evidence_qualification") != "HOLD":
        diagnostics.append(_issue("SOURCE_ADJUDICATION_UNKNOWN_OR_CHANGED", "FAIL"))
    else:
        diagnostics.append(_issue("ORIGINAL_EXAM_EVIDENCE_NOT_QUALIFIED"))
    requested = register.get("requested_input_sources_zip") or {}
    if not isinstance(requested, dict) or requested.get("status") != "NOT_RECEIVED":
        diagnostics.append(_issue("REQUESTED_SOURCE_ARCHIVE_STATUS_UNREVIEWED", "FAIL"))
    else:
        diagnostics.append(_issue("REQUIRED_ORIGINAL_SOURCE_ARCHIVE_NOT_RECEIVED"))
    if register.get("source_custody") != "OWNER_LOCAL_PRIVATE_NOT_FOR_PUBLIC_DEPLOYMENT":
        diagnostics.append(_issue("OWNER_LOCAL_CUSTODY_SCOPE_UNKNOWN", "FAIL"))
    else:
        diagnostics.append(_issue("OWNER_LOCAL_PRIVATE_CUSTODY_NOT_FOR_PUBLIC_DEPLOYMENT"))

    authority = sources["physics_authority"]
    if not isinstance(authority, str) or "Physics authority review — HOLD" not in authority[:200]:
        diagnostics.append(_issue("PHYSICS_AUTHORITY_HOLD_RECORD_UNKNOWN", "FAIL"))
    else:
        diagnostics.append(_issue("PHYSICS_WARRANT_REVIEW_NOT_QUALIFIED"))

    if handoff.get("schema") != "core1a-source-handoff/v1" or handoff.get("status") != "CANDIDATE":
        diagnostics.append(_issue("CORE1A_HANDOFF_SHAPE_OR_STATUS_CHANGED", "FAIL"))
    links = handoff.get("question_links")
    if not isinstance(links, list):
        diagnostics.append(_issue("HANDOFF_QUESTION_LINKS_INVALID", "FAIL"))
        links = []
    elif links:
        diagnostics.append(_issue("HANDOFF_NEW_QUESTION_LINKS_NEED_REVIEW"))
    else:
        diagnostics.append(_issue("CORE1A_HANDOFF_HAS_ZERO_REVIEWED_QUESTION_LINKS"))
    diagnostics.append(_issue("D31_VS_WEP01_CONSTRUCTION_JOIN_NOT_ESTABLISHED"))

    bscope = hub.get("scope")
    if bscope != "AUTHOR_HUB_BROWSER_CHECKS_ONLY" or hub.get("independent_QA") is not False:
        diagnostics.append(_issue("HUB_AUDIT_SCOPE_INVALID", "FAIL"))
    tests = hub.get("results")
    if (not isinstance(tests, list)
            or type(hub.get("passed")) is not int or hub["passed"] != len(tests)
            or not all(isinstance(t, dict) and t.get("pass") is True for t in tests)):
        diagnostics.append(_issue("HUB_CHECKS_NOT_VERIFIABLE", "FAIL"))
    diagnostics.append(_issue("HUB_BROWSER_CHECKS_NOT_LEARNER_ATTEMPT_VALIDATION"))

    c1a = witness.get("core1a") or {}
    c1b = witness.get("core1b") or {}
    teaching = c1a.get("construction_ids") if isinstance(c1a, dict) else None
    testing = c1b.get("cycle_ids") if isinstance(c1b, dict) else None
    if (not isinstance(teaching, list) or not teaching
            or not all(isinstance(x, str) and SAFE_ID.fullmatch(x) for x in teaching)
            or not isinstance(testing, list) or not testing
            or not all(isinstance(x, str) and SAFE_ID.fullmatch(x) for x in testing)):
        diagnostics.append(_issue("TEACHING_OR_TESTING_REFERENCES_MISSING", "FAIL"))
        teaching, testing = [], []
    diagnostics.append(_issue("CORE1A_TO_CORE1B_SEMANTIC_FRESHNESS_NOT_REVIEWED"))
    summary = {
        "construction_id": cid, "source_subset": "D3.1.1", "subject_id": "PHYSICS",
        "unit_id": "WPE", "native_operation": "RECALL_CLASSIFY_PROPOSED",
        "native_demand": "D3_PROPOSED", "b1_b7_native_status": statuses,
        "teaching_reference_ids": teaching, "assessment_cycle_ids": testing,
        "handoff_question_link_count": len(links), "handoff_status": "CANDIDATE",
        "hub_browser_checks_passed": hub.get("passed") if isinstance(hub.get("passed"), int) else None,
        "learner_runtime_verified": False, "independent_academic_review": False,
        "wep01_fixture_is_same_construction": "UNDETERMINED_NOT_JOINED",
    }
    return _finish(pins, diagnostics, summary, {"candidate_constructions": 1, "qualified_constructions": 0})


def _finish(pins, diagnostics, summary, coverage):
    return {
        "schema_version": "1.0.0",
        "audit_type": "OWNER_LOCAL_WPE_D311_EVIDENCE_READBACK",
        "mechanical_status": "FAIL" if any(d["severity"] == "FAIL" for d in diagnostics) else "HOLD",
        "academic_status": "HOLD", "release_status": "HOLD",
        "review_subject": summary, "coverage": coverage,
        "source_fingerprints": pins,
        "diagnostic_codes": sorted({d["code"] for d in diagnostics}),
        "blocked_by": [
            "INDEPENDENT_D311_QRT_DEMAND_AND_SOURCE_ROLE",
            "PHYSICS_WARRANT_REVIEW_AND_CANONICAL_BYTE_PIN",
            "CORE1A_TEACHING_TO_FRESH_CORE1B_B1_B7",
            "ACTUAL_FIRST_ATTEMPT_PROTECTED_RUNTIME_TEST",
            "TRUSTED_SHARED_NATIVE_REVIEWS_AND_RELEASE",
            "CROSS_NAMESPACE_WEP01_MAPPING_REVIEW",
        ],
        "warning": "NOT_ACADEMIC_APPROVAL: original WPE owner-local evidence is candidate, not qualified.",
    }
