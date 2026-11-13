"""WEP01 pair tests: synthetic author files, no copyrighted question text."""
import copy
import hashlib
import json
import zipfile

from grade9qa.pilot_pair_review import FILES, compare_wep01_drafts
from grade9qa.cli import main


def candidate(index, *, six=False):
    ids=["CYCLE-ANGLE","CYCLE-OWNERSHIP","CYCLE-ZERO","CYCLE-SUM","CYCLE-FRAME"]
    if six: ids.insert(3,"CYCLE-ZERO-DISPLACEMENT")
    return {
        "writer_status":"WRITER_DRAFT_FOR_INDEPENDENT_CHECK_NOT_APPROVED",
        "writer_does_not_approve":True,
        "source_custody_visibility":"NO_EXAM_QUESTIONS_PRESENT; ALL_EXAMPLES_AUTHORED; CORE2_NOT_AUTHORED",
        "core1a":{"id":"CORE1A-WEP01","role":"CORE1A","ordered_blocks":[{"id":"SYNTH-1"}]},
        "core1b":{"id":"CORE1B-WEP01","role":"CORE1B",
                  "concept_cycles":[{"id":k} for k in ids],
                  "visible_convention_refs":["WEP01-C2","WEP01-C4","WEP01-C10"] if six else ["WEP01-C1","WEP01-C2","WEP01-C3","WEP01-C4"],
                  "deferred_convention_refs":["WEP01-C1","WEP01-C3","WEP01-C5"] if six else ["WEP01-C5","WEP01-C6"]},
        "answer_visibility_contract":{
            "rendering_must_enforce":"NOT_TESTED",
            "core1b_predict_answers":"AFTER_ATTEMPT_ONLY",
            "core1b_rubrics_model_answers":"AFTER_ATTEMPT_ONLY",
        },
    }


def make(tmp_path, a=None, b=None, missing=None):
    values={"candidate_1":candidate(1),"candidate_2":candidate(2,six=True)}
    if a is not None: values["candidate_1"]=a
    if b is not None: values["candidate_2"]=b
    path=tmp_path/"input-sources.zip"
    pins={}
    with zipfile.ZipFile(path,"w") as z:
        for key, member in FILES.items():
            if key==missing:continue
            raw=json.dumps(values[key]).encode()
            pins[key]=hashlib.sha256(raw).hexdigest()
            z.writestr(member,raw)
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    return path,sha,pins


def run(tmp_path,a=None,b=None,missing=None):
    path,sha,pins=make(tmp_path,a,b,missing)
    return compare_wep01_drafts(path,sha=sha,member_pins=pins)


def codes(r):
    return set(r["diagnostic_codes"])


def test_pair_is_candidate_hold(tmp_path):
    r=run(tmp_path)
    assert r["mechanical_status"]=="HOLD"
    assert r["academic_status"]==r["release_status"]=="HOLD"
    assert r["comparison"]["version_selection"]=="UNREVIEWED_NEITHER_AUTO_PREFERRED"


def test_zero_displacement_cycle_is_added(tmp_path):
    r=run(tmp_path)
    assert r["versions"]["candidate_1"]["core1b_cycle_count"]==5
    assert r["versions"]["candidate_2"]["core1b_cycle_count"]==6
    assert r["comparison"]["added_cycle_ids_in_candidate_2"]==["CYCLE-ZERO-DISPLACEMENT"]


def test_visible_convention_changes_are_recorded_without_content(tmp_path):
    r=run(tmp_path)
    assert r["comparison"]["pre_attempt_conventions_only_candidate_1"]==["WEP01-C1","WEP01-C3"]
    assert r["comparison"]["pre_attempt_conventions_only_candidate_2"]==["WEP01-C10"]


def test_writer_cannot_self_approve(tmp_path):
    a=candidate(1);a["writer_status"]="APPROVED";a["writer_does_not_approve"]=False
    r=run(tmp_path,a)
    assert r["mechanical_status"]=="FAIL"
    assert "WRITER_SELF_APPROVAL_OR_STATUS_CHANGED" in codes(r)


def test_answer_leak_contract_changed_fails(tmp_path):
    a=candidate(1)
    a["answer_visibility_contract"]["core1b_predict_answers"]="BEFORE_ATTEMPT"
    assert "WEP01_ANSWER_EXPOSURE_CONTRACT_CHANGED" in codes(run(tmp_path,a))


def test_custody_cannot_be_rewritten_to_exam_approved(tmp_path):
    a=candidate(1);a["source_custody_visibility"]="EXAM_VERIFIED"
    assert "WEP01_ORIGINAL_AUTHORING_CUSTODY_CHANGED" in codes(run(tmp_path,a))


def test_overlapping_pre_and_post_attempt_conventions_fail(tmp_path):
    a=candidate(1)
    a["core1b"]["deferred_convention_refs"].append("WEP01-C1")
    assert "WEP01_PREATTEMPT_CONVENTION_OVERLAP" in codes(run(tmp_path,a))


def test_duplicate_core1b_cycle_id_fails(tmp_path):
    a=candidate(1)
    a["core1b"]["concept_cycles"].append({"id":"CYCLE-ANGLE"})
    assert "WEP01_CYCLE_IDENTITY_INVALID" in codes(run(tmp_path,a))


def test_missing_second_candidate_fails(tmp_path):
    assert "OWNER_INPUTS_ARCHIVE_INVALID" in codes(run(tmp_path,missing="candidate_2"))


def test_archive_pin_mismatch_fails(tmp_path):
    p,_,pins=make(tmp_path)
    r=compare_wep01_drafts(p,sha="0"*64,member_pins=pins)
    assert r["mechanical_status"]=="FAIL"
    assert "INPUT_ARCHIVE_HASH_MISMATCH" in codes(r)


def test_member_pin_mismatch_fails(tmp_path):
    p,sha,pins=make(tmp_path)
    pins["candidate_2"]="0"*64
    assert "CANDIDATE_MEMBER_HASH_MISMATCH" in codes(compare_wep01_drafts(p,sha=sha,member_pins=pins))


def test_private_exam_stem_or_student_answer_not_echoed(tmp_path):
    a=candidate(1)
    a["exam_stem"]="PRIVATE EXAM STEM"
    a["core1b"]["private_response"]="PRIVATE STUDENT RESPONSE"
    r=run(tmp_path,a)
    assert "PRIVATE EXAM" not in json.dumps(r)
    assert "PRIVATE STUDENT" not in json.dumps(r)


def test_matcher_is_deterministic(tmp_path):
    p,sha,pins=make(tmp_path)
    assert compare_wep01_drafts(p,sha=sha,member_pins=pins)==compare_wep01_drafts(p,sha=sha,member_pins=pins)


def test_tiny_synthetic_payload_is_not_qualification(tmp_path):
    r=run(tmp_path)
    assert "CORE1B_FIRST_ATTEMPT_RUNTIME_NOT_TESTED" in codes(r)
    assert r["versions"]["candidate_2"]["answer_visibility_implementation"]=="NOT_TESTED"
