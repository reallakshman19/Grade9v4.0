"""Compare actual Owner-supplied WEP-01 Core1A/B drafts without emitting content.

Two original WEP-01 teaching/reconstruction records from Input sources(4).zip
are candidates. Their version differences require human pedagogic selection.
No source file or exam question is republished; no answer exposure is tested.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

ARCHIVE_SHA256 = "ed0880d9ff314853c084834f2a8ac4ced69d2b8f5b019612ca999a1222b20565"
FILES = {
    "candidate_1": "wpe-pilot/tiles/wep01/wep01-core1ab-9e95dde5.json",
    "candidate_2": "wpe-pilot/tiles/wep01/wep01-core1ab-a886c004.json",
}
EXPECTED = {
    "candidate_1": "9e95dde53a83f15e25e9a4ff47b3830ec4e43453181b8d927b925fe52d82fe0b",
    "candidate_2": "a886c004bbbd26b6e525d8461ad935f7894e27ba01424e15b8a49c176bdb5c83",
}
SAFE_REF = re.compile(r"^[A-Z][A-Z0-9_-]{1,80}$")


def _hash(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def _decode(raw):
    def reject_dupes(pairs):
        o={}
        for k,v in pairs:
            if k in o: raise ValueError("DUPLICATE_JSON_KEY")
            o[k]=v
        return o
    return json.loads(raw.decode("utf-8"), object_pairs_hook=reject_dupes,
                      parse_constant=lambda k: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")))


def compare_wep01_drafts(archive: Path, *, sha: str = ARCHIVE_SHA256,
                         member_pins: dict | None = None) -> dict:
    """The CLI requires the exact owner-supplied archive; tests override pins."""
    pins = member_pins if member_pins is not None else EXPECTED
    errors=[]
    versions={}
    try:
        archive_sha=_hash(archive)
        if archive_sha != sha:
            errors.append("INPUT_ARCHIVE_HASH_MISMATCH")
            return _report(errors, versions, None)
        with zipfile.ZipFile(archive) as z:
            for key, name in FILES.items():
                info=z.getinfo(name)
                if info.is_dir() or info.file_size <= 0 or info.file_size > 250000:
                    raise ValueError("REVIEW_MEMBER_TOO_LARGE_OR_INVALID")
                raw=z.read(info)
                digest=hashlib.sha256(raw).hexdigest()
                if digest != pins[key]:
                    errors.append("CANDIDATE_MEMBER_HASH_MISMATCH")
                    continue
                row=_decode(raw)
                if not isinstance(row,dict):
                    errors.append("CANDIDATE_JSON_NOT_OBJECT")
                    continue
                ca,cb=row.get("core1a"),row.get("core1b")
                status=row.get("writer_status")
                if (status!="WRITER_DRAFT_FOR_INDEPENDENT_CHECK_NOT_APPROVED"
                        or row.get("writer_does_not_approve") is not True):
                    errors.append("WRITER_SELF_APPROVAL_OR_STATUS_CHANGED")
                if not isinstance(ca,dict) or not isinstance(cb,dict) or ca.get("id")!="CORE1A-WEP01" or cb.get("id")!="CORE1B-WEP01":
                    errors.append("WEP01_CORE_ROLE_IDENTITY_MISMATCH")
                    continue
                if row.get("source_custody_visibility") != "NO_EXAM_QUESTIONS_PRESENT; ALL_EXAMPLES_AUTHORED; CORE2_NOT_AUTHORED":
                    errors.append("WEP01_ORIGINAL_AUTHORING_CUSTODY_CHANGED")
                controls=row.get("answer_visibility_contract") or {}
                if (controls.get("rendering_must_enforce") != "NOT_TESTED"
                        or controls.get("core1b_predict_answers") != "AFTER_ATTEMPT_ONLY"
                        or controls.get("core1b_rubrics_model_answers") != "AFTER_ATTEMPT_ONLY"):
                    errors.append("WEP01_ANSWER_EXPOSURE_CONTRACT_CHANGED")
                cycles=cb.get("concept_cycles")
                if not isinstance(cycles,list):
                    errors.append("WEP01_CYCLES_NOT_ARRAY")
                    continue
                ids=[c.get("id") for c in cycles if isinstance(c,dict)]
                if (len(ids)!=len(cycles) or len(set(ids))!=len(ids)
                        or not all(isinstance(x,str) and SAFE_REF.fullmatch(x) for x in ids)):
                    errors.append("WEP01_CYCLE_IDENTITY_INVALID")
                    ids=[]
                visible=cb.get("visible_convention_refs")
                deferred=cb.get("deferred_convention_refs")
                if not all(isinstance(v,list) and all(isinstance(x,str) and SAFE_REF.fullmatch(x) for x in v)
                           for v in (visible,deferred)):
                    errors.append("WEP01_CONVENTION_SCOPE_INVALID")
                    visible,deferred=[],[]
                if set(visible)&set(deferred):
                    errors.append("WEP01_PREATTEMPT_CONVENTION_OVERLAP")
                versions[key]={
                    "source_member_sha256":digest,
                    "authoring_state":"WRITER_DRAFT_NOT_APPROVED",
                    "core1a_id":"CORE1A-WEP01","core1b_id":"CORE1B-WEP01",
                    "core1a_block_count":len(ca.get("ordered_blocks",[])) if isinstance(ca.get("ordered_blocks"),list) else None,
                    "core1b_cycle_count":len(cycles),
                    "core1b_cycle_ids":ids,
                    "pre_attempt_convention_refs":visible,
                    "post_attempt_convention_refs":deferred,
                    "answer_visibility_implementation":"NOT_TESTED",
                    "original_exam_question_content":"NONE_AUTHORED_EXAMPLES",
                    "qualification_status":"HOLD",
                }
    except (OSError,ValueError,KeyError,UnicodeError,zipfile.BadZipFile):
        errors.append("OWNER_INPUTS_ARCHIVE_INVALID")
    return _report(errors,versions,archive_sha if "archive_sha" in locals() else None)


def _report(errors,versions,archive_sha):
    compare={}
    if len(versions)==2:
        a,b=versions["candidate_1"],versions["candidate_2"]
        compare={
            "added_cycle_ids_in_candidate_2":sorted(set(b["core1b_cycle_ids"])-set(a["core1b_cycle_ids"])),
            "removed_cycle_ids_in_candidate_2":sorted(set(a["core1b_cycle_ids"])-set(b["core1b_cycle_ids"])),
            "pre_attempt_conventions_only_candidate_1":sorted(set(a["pre_attempt_convention_refs"])-set(b["pre_attempt_convention_refs"])),
            "pre_attempt_conventions_only_candidate_2":sorted(set(b["pre_attempt_convention_refs"])-set(a["pre_attempt_convention_refs"])),
            "version_selection":"UNREVIEWED_NEITHER_AUTO_PREFERRED",
        }
    return {
        "schema_version":"1.0.0","audit_type":"OWNER_WEP01_CORE1A_CORE1B_DRAFT_COMPARISON",
        "archive_sha256":archive_sha,
        "versions":versions,"comparison":compare,
        "mechanical_status":"FAIL" if errors else "HOLD",
        "academic_status":"HOLD","release_status":"HOLD",
        "diagnostic_codes":sorted(set(errors + [
            "INDEPENDENT_WEP01_DRAFT_SELECTION_MISSING",
            "CORE1B_FIRST_ATTEMPT_RUNTIME_NOT_TESTED",
            "PHYSICS_LIBRARY_AND_TEACHING_SUFFICIENCY_UNAPPROVED",
            "NO_AUTHENTIC_EXAM_EVIDENCE_IN_AUTHOR_DRAFT",
            "D311_TO_WEP01_CONSTRUCTION_BINDING_UNREVIEWED",
        ])),
        "warning":"NOT_ACADEMIC_APPROVAL: two authored draft pairs, no verified first-try/runtime or independent subject review.",
    }
