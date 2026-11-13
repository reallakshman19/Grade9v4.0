import json
from grade9qa.smart_skills import GATES, inspect_native_report
from grade9qa.cli import main

HASH = "sha256:" + "a" * 64

def sample(obs="NOT_APPLICABLE"):
    states = {k: "PASS" for k in GATES}
    states["observations"] = obs
    return {
        "schema": "smart-labelling-check-report/v2",
        "checker_version": "2.0.0-candidate",
        "mode": "DETERMINISTIC_CONTRACT",
        "legacy_checks": [{"stage": 1, "exit_code": 0}],
        "inputs": {"contract.json": HASH},
        "checker_artifact": {"path": "scripts/qrt_contract.py", "sha256": HASH},
        "gate_summary": states,
        "records": [{"question_id": "Q-CANDIDATE", "gates": states.copy()}],
        "issues": [],
        "selected_gate": "integrity",
        "selected_gate_status": "PASS",
    }

def test_native_pass_does_not_grant_release():
    r = inspect_native_report(sample())
    assert r["native_check_status"] == "PASS"
    assert r["integration_status"] == "HOLD"
    assert r["qualification_status"] == "HOLD"
    assert "INDEPENDENT_ACADEMIC_RELEASE_RECEIPTS" in r["blocked_by"]

def test_p1_not_applicable_is_not_an_error():
    r = inspect_native_report(sample())
    assert r["optional_p1_not_applicable"] is True
    assert "MISSING_OR_INVALID_GATE:observations" not in r["diagnostic_codes"]

def test_bad_schema_holds():
    src = sample()
    src["schema"] = "legacy-report/v1"
    r = inspect_native_report(src)
    assert r["native_check_status"] == "HOLD"
    assert "NATIVE_SCHEMA_MISMATCH" in r["diagnostic_codes"]

def test_unverifiable_hash_holds():
    src = sample()
    src["checker_artifact"]["sha256"] = "forged"
    assert inspect_native_report(src)["native_check_status"] == "HOLD"

def test_selected_gate_mismatch_holds():
    src = sample()
    src["selected_gate_status"] = "HOLD"
    assert "SELECTED_GATE_MISMATCH" in inspect_native_report(src)["diagnostic_codes"]

def test_aggregate_record_mismatch_holds():
    src = sample()
    src["records"][0]["gates"]["qrt"] = "HOLD"
    assert "CONTRADICTORY_AGGREGATE:Q-CANDIDATE:qrt" in inspect_native_report(src)["diagnostic_codes"]

def test_missing_observations_is_diagnostic_not_fake_p1():
    src = sample()
    del src["gate_summary"]["observations"]
    assert not inspect_native_report(src)["optional_p1_not_applicable"]
    assert "MISSING_OR_INVALID_GATE:observations" in inspect_native_report(src)["diagnostic_codes"]

def test_no_records_cannot_qualify():
    src = sample()
    src["records"] = []
    assert inspect_native_report(src)["native_check_status"] == "HOLD"

def test_smart_audit_cli_returns_hold(tmp_path):
    inp = tmp_path / "native.json"
    out = tmp_path / "summary.json"
    inp.write_text(json.dumps(sample()))
    assert main(["smart-audit", "--report", str(inp), "--out", str(out)]) == 3
    assert json.loads(out.read_text())["qualification_status"] == "HOLD"

def test_report_never_echoes_learner_data():
    src = sample()
    src["records"][0]["original_learner_reasoning"] = "sensitive-response"
    result = inspect_native_report(src)
    assert "sensitive-response" not in json.dumps(result)
