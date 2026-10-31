"""P0.4 bridge tests use synthetic records ONLY, never authentic examination evidence."""
import copy
import hashlib
import json
from pathlib import Path

import pytest
from grade9qa.bridge_witness import inspect_witness
from grade9qa.cli import main
from grade9qa.validate import schema_errors

SOURCE = Path(__file__).resolve().parents[1] / "examples/wpe-b1b7-candidate/witness.json"


@pytest.fixture
def base():
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def codes(output, gate=None):
    return {r["code"] for r in output["diagnostics"] if gate is None or r["gate"] == gate}


def gate(output, key):
    return next(row for row in output["gate_results"] if row["gate"] == key)


def test_v1_fixture_schema_is_valid(base):
    assert schema_errors(base, "bridge-witness", str(SOURCE)) == []


def test_schema_rejects_unknown_top_level_and_status(base):
    base["claimed_success"] = True
    assert schema_errors(base, "bridge-witness", str(SOURCE))


def test_complete_candidate_is_still_academic_hold(base):
    result = inspect_witness(base)
    assert result["mechanical_status"] == "HOLD"
    assert result["qualification_status"] == result["release_status"] == "HOLD"
    assert result["coverage"]["academically_qualified_constructions"] == 0
    assert len(result["gate_results"]) == 7
    assert all(g["result"] == "HOLD" for g in result["gate_results"])


def test_wrong_operation_is_critical_b1_contradiction(base):
    base["core1b"]["operation"] = "APPLY"
    r = inspect_witness(base)
    assert "COGNITIVE_TARGET_MISMATCH" in codes(r, "B1")
    assert gate(r,"B1")["result"] == "FAIL"


def test_wrong_banding_not_accepted(base):
    base["assessment"]["band"] = "D2"
    assert "ASSESSMENT_TARGET_MISMATCH" in codes(inspect_witness(base), "B1")


def test_misbound_construction_fails(base):
    base["core1a"]["construction_id"] = "NOT-THE-CONSTRUCTION"
    assert "CONSTRUCTION_BINDING_MISMATCH" in codes(inspect_witness(base), "B1")


def test_missing_independent_qrt_stays_hold(base):
    base["assessment"]["qrt_decision_ref"] = ""
    out = inspect_witness(base)
    assert "QRT_DECISION_ABSENT" in codes(out, "B1")
    assert gate(out,"B1")["result"] == "HOLD"


def test_signature_missing_decisive_move_holds(base):
    base["construction"]["signature"]["decisive_move"] = ""
    assert "SIGNATURE_DECISIVE_MOVE_MISSING" in codes(inspect_witness(base), "B2")


def test_duplicate_role_fails(base):
    base["construction"]["decisive_roles"].append("CONDITION")
    assert "DUPLICATE_DECISIVE_ROLE" in codes(inspect_witness(base), "B2")


def test_teacher_missing_worked_demonstration_holds(base):
    base["core1a"]["taught_roles"]["CONDITION"]["demonstration_ref"] = ""
    assert "DECISIVE_ROLE_NOT_DEMONSTRATED" in codes(inspect_witness(base), "B3")


def test_teacher_unwarranted_reverse_direction_fails(base):
    base["core1a"]["direction"] = "POTENTIAL_TO_FORCE"
    assert "TEACHING_DIRECTION_MISMATCH" in codes(inspect_witness(base), "B3")


def test_exact_directionality_does_not_reverse_silently(base):
    base["core1b"]["direction"] = "FORCE_TO_POTENTIAL"
    out = inspect_witness(base)
    assert "RECONSTRUCTION_DIRECTION_MISMATCH" in codes(out, "B4")
    assert gate(out, "B4")["result"] == "FAIL"


def test_missing_assessed_decisive_role_is_held(base):
    base["core1b"]["assessed_roles"].pop("CONDITION")
    assert "ASSESSMENT_ROLE_UNOBSERVED" in codes(inspect_witness(base), "B4")


def test_untaught_assessment_role_fails(base):
    base["core1b"]["assessed_roles"]["NEW_UNTAUGHT"] = {"attempt_field":"x","observable":"reason"}
    assert "UNTAGGED_ASSESSED_ROLES" in codes(inspect_witness(base), "B4")


def test_same_content_hash_means_not_fresh(base):
    base["core1b"]["task_sha256"] = base["core1a"]["worked_example_sha256"]
    out = inspect_witness(base)
    assert gate(out,"B4")["result"] == "FAIL"
    assert "SAME_WORKED_AND_TESTED_TASK" in codes(out,"B4")


def test_distinct_hashes_not_semantic_freshness_proof(base):
    out = inspect_witness(base)
    assert gate(out, "B4")["result"] == "HOLD"


def test_missing_freshness_review_holds(base):
    base["core1b"]["freshness_review_ref"] = ""
    assert "FRESHNESS_SEMANTIC_REVIEW_ABSENT" in codes(inspect_witness(base),"B4")


def test_attempt_p1_must_be_optional(base):
    base["core1b"]["attempt_contract"]["p1_optional"] = False
    assert "ATTEMPT_PROTECTION_CONTRACT_INVALID" in codes(inspect_witness(base), "B5")


def test_protection_cannot_unlock_on_save_failure(base):
    events = base["core1b"]["attempt_events"]
    events[1] = {"type":"SAVE_FAILED","at":"2026-10-31T10:00:01Z"}
    out=inspect_witness(base)
    assert "PREMATURE_HINT_OR_REVEAL" in codes(out, "B5")
    assert gate(out,"B5")["result"]=="FAIL"


def test_premature_reveal_without_save_fails(base):
    base["core1b"]["attempt_events"] = [{"type":"ANSWER_ENTERED","at":"2026-10-31T10:00:00Z"},
                                          {"type":"ANSWER_REVEALED","at":"2026-10-31T10:00:02Z"}]
    assert "PREMATURE_HINT_OR_REVEAL" in codes(inspect_witness(base),"B5")


def test_false_durable_save_fails(base):
    base["core1b"]["attempt_events"][1]["durable"]=False
    assert "FALSE_SAVED_ATTEMPT" in codes(inspect_witness(base),"B5")


def test_unordered_events_fail(base):
    base["core1b"]["attempt_events"][2]["at"]="2026-10-31T09:59:59Z"
    assert "ATTEMPT_EVENT_ORDER_INVALID" in codes(inspect_witness(base), "B5")


def test_missing_runtime_evidence_stays_hold(base):
    base["core1b"]["native_runtime_receipt_ref"] = ""
    assert "NATIVE_RUNTIME_EVIDENCE_MISSING" in codes(inspect_witness(base),"B5")


def test_no_response_means_insufficient_evidence_not_misconception(base):
    base["core1b"]["saved_answer_evidence_ref"] = ""
    out=inspect_witness(base)
    assert "INSUFFICIENT_EVIDENCE" in codes(out, "B6")
    assert "MISCONCEPTION_DETECTED" not in codes(out)


def test_missing_repair_mapping_holds(base):
    base["core1b"]["diagnostic_rules"].pop()
    assert "DECISIVE_ROLE_UNDIAGNOSED" in codes(inspect_witness(base),"B6")


def test_unknown_diagnosis_role_fails(base):
    base["core1b"]["diagnostic_rules"][0]["role_id"]="SOMETHING_ELSE"
    assert "DIAGNOSIS_UNKNOWN_ROLE" in codes(inspect_witness(base), "B6")


def test_distinct_physics_and_source_reviews_needed(base):
    base["source_and_physics"]["physics_review_ref"]=""
    base["source_and_physics"]["source_custody_ref"]=""
    out=inspect_witness(base)
    assert "PHYSICS_REVIEW_MISSING" in codes(out,"B7")
    assert "SOURCE_CUSTODY_REVIEW_MISSING" in codes(out,"B7")


def test_direct_exam_paper_key_solution_needed(base):
    base["assessment"]["source_role"]="DIRECT_EXAM_EVIDENCE"
    out=inspect_witness(base)
    assert "EXAM_PAPER_REF_MISSING" in codes(out,"B7")
    assert "EXAM_OFFICIAL_KEY_REF_MISSING" in codes(out,"B7")
    assert "EXAM_SOLUTION_REVIEW_REF_MISSING" in codes(out,"B7")


def test_known_physics_contradiction_fails(base):
    base["source_and_physics"]["known_physics_contradiction"]=True
    out=inspect_witness(base)
    assert gate(out,"B7")["result"]=="FAIL"


def test_self_review_fails_even_with_approved_flag(base):
    base["review_receipts"]=[{"gate":"B3","discipline":"PEDAGOGY","reviewer_id":"AUTH","author_id":"AUTH","independent_of_author":True,
                             "construction_id":"WPE-C-SYNTH-01","subject_sha256":"sha256:"+"a"*64,"decision":"APPROVED"}]
    assert "SELF_REVIEW_NOT_ACCEPTABLE" in codes(inspect_witness(base),"B3")


def test_stale_receipt_is_never_accepted(base):
    base["review_receipts"]=[{"gate":"B7","discipline":"PHYSICS","reviewer_id":"REVIEWER","author_id":"AUTH",
                             "independent_of_author":True,"construction_id":"WPE-C-SYNTH-01",
                             "subject_sha256":"sha256:"+"0"*64,"decision":"APPROVED"}]
    assert "STALE_OR_UNBOUND_REVIEW" in codes(inspect_witness(base),"B7")


def test_forged_complete_receipt_set_never_self_approves(base):
    # Even scoped hash-matching user-provided receipt metadata does not establish
    # native Shared identity, trust, correct scientific judgement or release.
    pairs={"B1":["COGNITIVE","QRT"],"B2":["COGNITIVE"],"B3":["PEDAGOGY","COGNITIVE"],
           "B4":["COGNITIVE","PEDAGOGY"],"B5":["TECHNICAL"],
           "B6":["PEDAGOGY","COGNITIVE"],"B7":["PHYSICS","SOURCE_CUSTODY"]}
    d=inspect_witness(base)["witness_subject_sha256"]
    base["review_receipts"]=[{"gate":gate,"discipline":discipline,"reviewer_id":"EXTERNAL", "author_id":"AUTH",
                              "independent_of_author":True,"construction_id":base["construction"]["construction_id"],
                              "subject_sha256":d,"decision":"APPROVED"}
                             for gate, ds in pairs.items() for discipline in ds]
    out=inspect_witness(base, trusted_shared_receipts=True)
    assert out["qualification_status"]=="HOLD"
    assert all(g["result"]=="HOLD" for g in out["gate_results"])
    assert "REVIEW_RECEIPT_NOT_NATIVE_TRUSTED" in codes(out)


def test_review_rejection_fails(base):
    base["review_receipts"]=[{"gate":"B4","discipline":"PEDAGOGY","reviewer_id":"DIFFERENT","author_id":"AUTH",
                             "independent_of_author":True,"construction_id":"WPE-C-SYNTH-01",
                             "subject_sha256":"sha256:"+"a"*64,"decision":"REJECTED"}]
    assert "REVIEW_REJECTED" in codes(inspect_witness(base), "B4")


def test_no_question_text_or_answer_echoed(base):
    base["private_original_question"]="DO NOT ECHO"
    base["core1b"]["saved_answer_evidence_ref"]="DO NOT ECHO RESPONSE"
    output=json.dumps(inspect_witness(base))
    assert "DO NOT ECHO" not in output


def test_cli_candidate_returns_three(base,tmp_path):
    witness=tmp_path/"witness.json"
    output=tmp_path/"report.json"
    witness.write_text(json.dumps(base))
    assert main(["bridge-witness","--witness",str(witness),"--out",str(output)]) == 3
    report=json.loads(output.read_text())
    assert report["qualification_status"]=="HOLD"


def test_cli_known_physics_contradiction_returns_one(base,tmp_path):
    base["source_and_physics"]["known_physics_contradiction"]=True
    witness=tmp_path/"witness.json"
    output=tmp_path/"report.json"
    witness.write_text(json.dumps(base))
    assert main(["bridge-witness","--witness",str(witness),"--out",str(output)]) == 1


def test_report_deterministic(base):
    assert inspect_witness(base)==inspect_witness(copy.deepcopy(base))
