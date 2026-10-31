"""Entirely synthetic QRT/WPE fixtures; not authentic PYQs or review receipts."""
import copy
import json
from grade9qa.qrt_binding import inspect_binding

OPS = ["RETRIEVE","EXPLAIN","APPLY","MODEL","REPRESENT","SYNTHESIZE","JUSTIFY"]
PIN = "sha256:" + "a"*64
SCORES = {"concept_model_selection":2,"representation_translation":1,
          "reasoning_chain_length":2,"algebra_computational_load":1,
          "trap_exception_sensitivity":0}

def candidate():
    sl1 = {"schema":"g9v35-smart-labels-1/v1","records":[
        {"question_id":"Q-SYNTH-X1","status":"UNREVIEWED","custody":{"item_digest":PIN},
         "source_verification":{"status":"SOURCE_UNVERIFIED"}}]}
    sl2 = {"schema":"g9v35-smart-labels-2/v1","records":[
        {"question_id":"Q-SYNTH-X1","status":"UNREVIEWED","binding":{"sl1_item_digest":PIN},
         "difficulty_evidence":{"components":{k:{"score":v,"evidence":"synthetic factor"} for k,v in SCORES.items()},
                                "total":6,"band":"D3"},
         "demand_proposal":{"primary":"JUSTIFY","candidate_cell":"QRT-JUSTIFY-D3","status":"PROPOSED"}}]}
    contract = {"schema":"smart-labelling-qrt-contract/v2","records":[
        {"question_id":"Q-SYNTH-X1","sl1_record_digest":PIN,"sl2_record_digest":PIN}]}
    blueprint = {"blueprint_id":"PHYS-QRT-BLUEPRINT","version":"0.2.0",
                 "status":"DRAFT_OWNER_REVIEW","column_order":OPS,
                 "cells":{"D3.7":{"template_ref":"QRT-JUSTIFY-D3"}}}
    adapter = {"adapter_id":"PHYS-TOPIC-WPE","topic_id":"WPE",
               "for_blueprint":"PHYS-QRT-BLUEPRINT 0.2.0",
               "status":"DRAFT_OWNER_REVIEW","cells":{"D3.7":{}}}
    handoff = {"schema":"core1a-source-handoff/v1","status":"CANDIDATE",
               "construction":{"decisive_move":"synthetic example"},"question_links":[]}
    return [sl1,sl2,contract,blueprint,adapter,handoff]

def result(args):
    return inspect_binding(*args)

def codes(args):
    return {i["code"] for i in result(args)["diagnostics"]}

def test_matching_candidate_stays_hold():
    r=result(candidate())
    assert r["mechanical_status"]=="HOLD" and r["qualification_status"]=="HOLD"
    assert r["question_bindings"][0]["blueprint_cell"]=="D3.7"
    assert r["question_bindings"][0]["topic_adapter_cell_present"] is True

def test_independent_qrtreview_absent():
    assert "QRT_INDEPENDENT_DECISION_MISSING" in codes(candidate())

def test_no_question_link_is_preparation_only():
    r=result(candidate())
    assert r["core1a_preparation"]=="SOURCE_PREPARATION_ONLY"
    assert "HANDOFF_NO_REVIEWED_QUESTION_JOIN" in codes(candidate())

def test_sl1_sl2_legacy_digest_mismatch():
    a=candidate();a[1]["records"][0]["binding"]["sl1_item_digest"]="sha256:"+"b"*64
    assert "LEGACY_SL1_SL2_DIGEST_MISMATCH" in codes(a)
    assert result(a)["mechanical_status"]=="FAIL"

def test_sl2_question_set_mismatch():
    a=candidate();a[1]["records"][0]["question_id"]="Q-OTHER"
    assert "SL1_SL2_QUESTION_SET_MISMATCH" in codes(a)

def test_native_sidecar_question_set_mismatch():
    a=candidate();a[2]["records"][0]["question_id"]="Q-OTHER"
    assert "CONTRACT_QUESTION_SET_MISMATCH" in codes(a)

def test_candidate_operation_wrong_cell():
    a=candidate();a[1]["records"][0]["demand_proposal"]["candidate_cell"]="QRT-APPLY-D3"
    assert "SL2_CANDIDATE_CELL_MISMATCH" in codes(a)

def test_total_is_not_rounded_or_guessed():
    a=candidate();a[1]["records"][0]["difficulty_evidence"]["components"]["concept_model_selection"]["score"]=1
    assert "SL2_TOTAL_MISMATCH" in codes(a)

def test_band_score_contradiction():
    a=candidate();e=a[1]["records"][0]["difficulty_evidence"];e["band"]="D4"
    assert "SL2_BAND_SCORE_MISMATCH" in codes(a)

def test_d1_d2_common_blueprint_pending():
    a=candidate();e=a[1]["records"][0]["difficulty_evidence"]
    e["band"]="D2";e["total"]=5;e["components"]["concept_model_selection"]["score"]=1
    assert "D1_D2_BLUEPRINT_SPEC_PENDING" in codes(a)

def test_missing_adapter_cell_holds():
    a=candidate();a[4]["cells"]={"D3.1":{}}
    assert result(a)["mechanical_status"]=="HOLD"
    assert "TOPIC_ADAPTER_CELL_MISSING" in codes(a)

def test_wrong_adapter_blueprint_pin_fails():
    a=candidate();a[4]["for_blueprint"]="PHYS-QRT-BLUEPRINT 0.3.0"
    assert "WPE_ADAPTER_BLUEPRINT_PIN_MISMATCH" in codes(a)

def test_self_declared_approval_never_grants_qualification():
    a=candidate();a[3]["status"]="APPROVED";a[4]["status"]="APPROVED";a[5]["status"]="APPROVED"
    assert result(a)["qualification_status"]=="HOLD"

def test_sl1_verified_claim_not_source_custody():
    a=candidate();a[0]["records"][0]["source_verification"]["status"]="VERIFIED"
    assert "SL1_CLAIM_NOT_INDEPENDENT_CUSTODY" in codes(a)

def test_native_pass_is_not_independently_trusted():
    a=candidate(); native={"schema":"smart-labelling-check-report/v2","selected_gate_status":"PASS"}
    out=inspect_binding(*a,native_sl1=native,native_sl2=native)
    assert out["qualification_status"]=="HOLD"
    assert "NATIVE_REPORT_UNTRUSTED" in {d["code"] for d in out["diagnostics"]}

def test_missing_native_report_is_hold():
    assert "NATIVE_REPORT_ABSENT" in codes(candidate())

def test_native_unknown_schema_fails():
    a=candidate()
    r=inspect_binding(*a,native_sl1={"schema":"unknown","selected_gate_status":"PASS"})
    assert "NATIVE_REPORT_SCHEMA_MISMATCH" in {d["code"] for d in r["diagnostics"]}

def test_optional_handoff_never_fabricated():
    out=inspect_binding(*candidate()[:5])
    assert out["core1a_preparation"]=="NOT_SUPPLIED"
    assert out["qualification_status"]=="HOLD"

def test_do_not_echo_question_stem_or_learner_data():
    a=candidate();a[0]["records"][0]["original_stem"]="private synthetic prompt"
    assert "private synthetic prompt" not in str(result(a))

def test_duplicate_question_id_is_failure():
    a=candidate();a[0]["records"].append(copy.deepcopy(a[0]["records"][0]))
    assert "QUESTION_ID_DUPLICATED" in codes(a)

def test_qrt_bind_cli_still_holds(tmp_path):
    from grade9qa.cli import main
    keys=("sl1","sl2","contract","blueprint","adapter","handoff")
    argv=["qrt-bind"]
    for name, value in zip(keys,candidate()):
        path=tmp_path/(name+".json");path.write_text(json.dumps(value))
        argv+=["--"+name,str(path)]
    out=tmp_path/"out.json"
    assert main(argv+["--out",str(out)])==3
    assert json.loads(out.read_text())["question_count"]==1

def test_qrt_bind_cli_bad_native_source_fails(tmp_path):
    from grade9qa.cli import main
    keys=("sl1","sl2","contract","blueprint","adapter")
    a=candidate();a[4]["for_blueprint"]="PHYS-QRT-BLUEPRINT 99.0"
    argv=["qrt-bind"]
    for name,value in zip(keys,a):
        path=tmp_path/(name+".json");path.write_text(json.dumps(value))
        argv+=["--"+name,str(path)]
    out=tmp_path/"out.json"
    assert main(argv+["--out",str(out)])==1
