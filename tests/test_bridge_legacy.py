"""Synthetic representations of archived candidate formats, no private PYQ data."""
from grade9qa.bridge_legacy import inspect_legacy_witness


def test_d31_candidate_preserves_native_partial_gates():
    r=inspect_legacy_witness({"construction_id":"SYNTH-D31","B1_B7_status":{
        "B1":"HOLD","B2":"PARTIAL_STRUCTURAL_ONLY","B3":"NOT_RUN",
        "B4":"NOT_RUN","B5":"LOCAL_PREVIEW_CHECKS_ONLY","B6":"NOT_RUN","B7":"HOLD"}})
    assert r["mechanical_status"]=="HOLD"
    assert r["records"][0]["source_native_gate_status"]["B2"]=="PARTIAL_STRUCTURAL_ONLY"
    assert r["records"][0]["qualification_status"]=="HOLD"


def test_d36_aggregated_children_are_independent():
    source={"witnesses":{"SYNTH-A":{"witness_gates":{"B1":{"status":"PARTIAL"},"B5":{"status":"HOLD"}}},
                          "SYNTH-B":{"witness_gates":{"B1":{"status":"HOLD"},"B5":{"status":"HOLD"}}}}}
    r=inspect_legacy_witness(source)
    assert len(r["records"])==2
    assert r["qualification_status"]=="HOLD"
    assert r["records"][0]["source_native_gate_status"]["B1"]=="PARTIAL"
    assert r["records"][1]["source_native_gate_status"]["B1"]=="HOLD"


def test_self_claimed_native_pass_does_not_certify():
    r=inspect_legacy_witness({"construction_id":"SYNTH","B1_B7_status":{x:"PASS" for x in
                                ("B1","B2","B3","B4","B5","B6","B7")}})
    assert r["qualification_status"]=="HOLD"
    assert r["records"][0]["result"]=="HOLD"


def test_archived_explicit_fail_is_not_downgraded():
    r=inspect_legacy_witness({"construction_id":"SYNTH","B1_B7_status":{"B7":"REJECTED"}})
    assert r["mechanical_status"]=="FAIL"


def test_d36_unstructured_candidate_not_assumed_complete():
    r=inspect_legacy_witness({"instance_id":"SYNTH-D36","B1_source_target":"AUTHORED_TRANSFER"})
    assert "ARCHIVED_GATE_FORMAT_UNMAPPED" in r["diagnostic_codes"]
    assert r["records"][0]["source_native_gate_status"]["B1"]=="NOT_RUN"


def test_no_private_stem_or_excerpts_echoed():
    r=inspect_legacy_witness({"construction_id":"SYNTH","B1_B7_status":{"B1":"HOLD"},
                              "original_exam_stem":"PRIVATE_STEM","core1a":{"excerpt":"PRIVATE_EXCERPT"}})
    assert "PRIVATE_STEM" not in str(r) and "PRIVATE_EXCERPT" not in str(r)


def test_archived_bad_format_fails_closed():
    assert inspect_legacy_witness([])["mechanical_status"]=="FAIL"
