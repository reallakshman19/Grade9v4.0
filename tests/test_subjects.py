"""Synthetic three-subject intake tests. No Maths/Chemistry curriculum is approved."""
import copy
import json
from pathlib import Path

import pytest

from grade9qa.subjects import audit_subject_intake, SCHEMA_PATH
from grade9qa.cli import main
from grade9qa.validate import inspect as inspect_v1

FIXTURE = Path(__file__).resolve().parents[1] / "examples/three-subjects-candidate/manifest.json"
H = "f"*64

@pytest.fixture
def manifest():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))

def codes(m):
    return {i["code"] for i in audit_subject_intake(m)["diagnostics"]}

def subject(m, sid):
    return next(s for s in m["subjects"] if s["subject_id"] == sid)

def add_synthetic_topic(m, sid, tid="SYNTH-T1"):
    s = subject(m, sid)
    s["stage"] = "PILOT_CANDIDATE"
    s["blueprint_ref"] = {"subject_id":sid,"id":"SYNTH-BLUEPRINT","version":"0.0-synthetic","sha256":H}
    t = {"topic_id":tid,
         "adapter_ref":{"subject_id":sid,"topic_id":tid,"id":"SYNTH-ADAPTER",
                        "version":"0.0-synthetic","sha256":"e"*64,"blueprint_sha256":H},
         "sources":[{"id":"SRC-001","status":"CANDIDATE","origin_ref":"synthetic-test-only"}],
         "warrants":[{"id":"WAR-001","status":"CANDIDATE","discipline":sid,
                      "source_refs":[f"{sid}/{tid}/SRC-001"],"claim_ref":"synthetic-claim"}],
         "constructions":[{"id":"CON-001","status":"CANDIDATE","operation":"JUSTIFY",
                           "band":"D3","grade_track":"G9_FOUNDATION",
                           "direction":"EXPLICIT_SYNTHETIC_PROOF_DIRECTION",
                           "source_refs":[f"{sid}/{tid}/SRC-001"],
                           "warrant_refs":[f"{sid}/{tid}/WAR-001"],"prerequisite_refs":[]}]}
    s["topics"].append(t)
    return t

def test_all_three_subjects_registered(manifest):
    r = audit_subject_intake(manifest)
    assert r["mechanical_status"] == "PASS"
    assert r["qualification_status"] == r["release_status"] == "HOLD"
    assert set(r["subjects"]) == {"PHYSICS","MATHEMATICS","CHEMISTRY"}

def test_math_chem_are_planned_not_qualified(manifest):
    r = audit_subject_intake(manifest)
    for sid in ("MATHEMATICS","CHEMISTRY"):
        assert r["subjects"][sid]["stage"] == "PLANNED"
        assert r["subjects"][sid]["subject_blueprint_status"] == "NOT_SUPPLIED"
        assert r["subjects"][sid]["qualified_construction_count"] == 0

def test_wpe_is_a_physics_topic_not_platform(manifest):
    s = subject(manifest,"PHYSICS")
    assert s["topics"][0]["unit_id"] == "WPE"
    assert s["topics"][0]["topic_id"] == "WEP-01"
    assert audit_subject_intake(manifest)["qualification_status"] == "HOLD"

def test_subject_specific_synthetic_math_candidate_is_allowed_but_hold(manifest):
    add_synthetic_topic(manifest,"MATHEMATICS")
    r = audit_subject_intake(manifest)
    assert r["mechanical_status"] == "PASS"
    assert r["subjects"]["MATHEMATICS"]["candidate_construction_count"] == 1
    assert r["subjects"]["MATHEMATICS"]["qualified_construction_count"] == 0

def test_synthetic_chem_topic_allowed_but_not_reused_physics(manifest):
    add_synthetic_topic(manifest,"CHEMISTRY","SYNTH-CHEM")
    r = audit_subject_intake(manifest)
    assert r["mechanical_status"] == "PASS"
    assert r["qualification_status"] == "HOLD"

def test_synthetic_both_subjects_can_share_local_raw_id(manifest):
    add_synthetic_topic(manifest,"MATHEMATICS")
    add_synthetic_topic(manifest,"CHEMISTRY")
    assert "DUPLICATE_SCOPED_RECORD" not in codes(manifest)
    assert audit_subject_intake(manifest)["mechanical_status"] == "PASS"

def test_wrong_subject_blueprint_is_blocked(manifest):
    add_synthetic_topic(manifest,"MATHEMATICS")
    subject(manifest,"MATHEMATICS")["blueprint_ref"]["subject_id"] = "PHYSICS"
    assert "BLUEPRINT_SUBJECT_MISMATCH" in codes(manifest)

def test_wrong_subject_adapter_is_blocked(manifest):
    t = add_synthetic_topic(manifest,"CHEMISTRY")
    t["adapter_ref"]["subject_id"] = "PHYSICS"
    assert "ADAPTER_SCOPE_MISMATCH" in codes(manifest)

def test_wrong_adapter_topic_is_blocked(manifest):
    t=add_synthetic_topic(manifest,"MATHEMATICS")
    t["adapter_ref"]["topic_id"]="WRONG-TOPIC"
    assert "ADAPTER_SCOPE_MISMATCH" in codes(manifest)

def test_adapter_wrong_blueprint_digest_is_blocked(manifest):
    t=add_synthetic_topic(manifest,"MATHEMATICS")
    t["adapter_ref"]["blueprint_sha256"]="0"*64
    assert "ADAPTER_BLUEPRINT_PIN_MISMATCH" in codes(manifest)

def test_cross_subject_source_reference_blocked(manifest):
    add_synthetic_topic(manifest,"PHYSICS","SYNTH-PHYS")
    m=add_synthetic_topic(manifest,"MATHEMATICS","SYNTH-MATH")
    m["constructions"][0]["source_refs"]=["PHYSICS/SYNTH-PHYS/SRC-001"]
    assert "CROSS_SUBJECT_REFERENCE" in codes(manifest)

def test_cross_subject_warrant_reference_blocked(manifest):
    add_synthetic_topic(manifest,"CHEMISTRY","SYNTH-CHEM")
    m=add_synthetic_topic(manifest,"MATHEMATICS","SYNTH-MATH")
    m["constructions"][0]["warrant_refs"]=["CHEMISTRY/SYNTH-CHEM/WAR-001"]
    assert "CROSS_SUBJECT_REFERENCE" in codes(manifest)

def test_cross_subject_prerequisite_blocked(manifest):
    add_synthetic_topic(manifest,"CHEMISTRY","SYNTH-CHEM")
    m=add_synthetic_topic(manifest,"MATHEMATICS","SYNTH-MATH")
    m["constructions"][0]["prerequisite_refs"]=["CHEMISTRY/SYNTH-CHEM/CON-001"]
    assert "CROSS_SUBJECT_REFERENCE" in codes(manifest)

def test_valid_same_subject_cross_topic_prerequisite(manifest):
    a=add_synthetic_topic(manifest,"MATHEMATICS","SYNTH-A")
    b=add_synthetic_topic(manifest,"MATHEMATICS","SYNTH-B")
    b["constructions"][0]["prerequisite_refs"]=["MATHEMATICS/SYNTH-A/CON-001"]
    assert audit_subject_intake(manifest)["mechanical_status"] == "PASS"

def test_unknown_scoped_ref_blocked(manifest):
    a=add_synthetic_topic(manifest,"MATHEMATICS")
    a["constructions"][0]["warrant_refs"]=["MATHEMATICS/SYNTH-T1/UNKNOWN"]
    assert "UNKNOWN_SCOPED_REFERENCE" in codes(manifest)

def test_wrong_reference_type_blocked(manifest):
    a=add_synthetic_topic(manifest,"MATHEMATICS")
    a["constructions"][0]["warrant_refs"]=["MATHEMATICS/SYNTH-T1/SRC-001"]
    assert "REFERENCE_TYPE_MISMATCH" in codes(manifest)

def test_prerequisite_cycle_blocked(manifest):
    a=add_synthetic_topic(manifest,"MATHEMATICS")
    c=a["constructions"][0]
    c["prerequisite_refs"]=["MATHEMATICS/SYNTH-T1/CON-001"]
    assert "PREREQUISITE_CYCLE" in codes(manifest)

def test_cross_kind_duplicate_scoped_record_blocked(manifest):
    a=add_synthetic_topic(manifest,"MATHEMATICS")
    a["warrants"][0]["id"] = a["sources"][0]["id"]
    assert "DUPLICATE_SCOPED_RECORD" in codes(manifest)

def test_warrant_subject_discipline_mismatch_blocked(manifest):
    a=add_synthetic_topic(manifest,"CHEMISTRY")
    a["warrants"][0]["discipline"]="PHYSICS"
    assert "WARRANT_DISCIPLINE_MISMATCH" in codes(manifest)

def test_planned_subject_cannot_fake_active_topic(manifest):
    add_synthetic_topic(manifest,"MATHEMATICS")
    subject(manifest,"MATHEMATICS")["stage"]="PLANNED"
    assert "PLANNED_SUBJECT_HAS_CONTENT" in codes(manifest)

def test_active_subject_needs_blueprint(manifest):
    s=subject(manifest,"MATHEMATICS")
    s["stage"]="PILOT_CANDIDATE"
    assert "ACTIVE_SUBJECT_MISSING_CONTENT" in codes(manifest)

def test_missing_subject_fails_schema(manifest):
    manifest["subjects"].pop()
    assert "V2_SCHEMA_ERROR" in codes(manifest)

def test_duplicate_subject_fails(manifest):
    manifest["subjects"][2] = copy.deepcopy(manifest["subjects"][1])
    assert audit_subject_intake(manifest)["mechanical_status"] == "FAIL"

def test_unknown_subject_fails_schema(manifest):
    subject(manifest,"CHEMISTRY")["subject_id"]="BIOLOGY"
    assert "V2_SCHEMA_ERROR" in codes(manifest)

def test_self_declared_approval_fails_schema(manifest):
    manifest["status"]="APPROVED"
    assert "V2_SCHEMA_ERROR" in codes(manifest)

def test_v1_not_accidentally_accepted_as_v2(candidate):
    old=json.loads((candidate/"bundle.json").read_text())
    assert "V2_SCHEMA_ERROR" in codes(old)

def test_v1_wpe_remains_unchanged(candidate):
    bundle, data, errors = inspect_v1(candidate/"bundle.json")
    assert not errors
    assert bundle["topic_id"] == "WEP-01"

def test_report_does_not_echo_input_payload(manifest):
    manifest["private_student_answer"]="MY SECRET"
    report=json.dumps(audit_subject_intake(manifest))
    assert "MY SECRET" not in report

def test_cli_candidate_exits_hold(tmp_path,manifest):
    p=tmp_path/"manifest.json";p.write_text(json.dumps(manifest))
    out=tmp_path/"audit.json"
    assert main(["subjects-audit","--manifest",str(p),"--out",str(out)]) == 3
    assert json.loads(out.read_text())["qualification_status"] == "HOLD"

def test_cli_cross_subject_failure_exits_one(tmp_path,manifest):
    add_synthetic_topic(manifest,"MATHEMATICS")["constructions"][0]["source_refs"]=["CHEMISTRY/SYNTH/SRC-001"]
    p=tmp_path/"manifest.json";p.write_text(json.dumps(manifest))
    out=tmp_path/"audit.json"
    assert main(["subjects-audit","--manifest",str(p),"--out",str(out)]) == 1
    assert json.loads(out.read_text())["mechanical_status"] == "FAIL"

def test_schema_conforms_to_draft_202012():
    from jsonschema import Draft202012Validator
    Draft202012Validator.check_schema(json.loads(SCHEMA_PATH.read_text()))
