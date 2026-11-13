"""Private WPE readback uses tiny synthetic ZIPs, not actual copyrighted source."""
import copy
import hashlib
import json
import zipfile

import pytest

from grade9qa.pilot_evidence import SOURCES, readback_pilot


def fixture_data():
    return {
        "witness": {
            "witness_version": "0.1.DERIVED_NONCANONICAL",
            "construction_id": "SYNTH-D311-REVIEW",
            "subset": "D3.1.1",
            "operation": "RECALL_CLASSIFY_PROPOSED",
            "demand_level": "D3_PROPOSED",
            "B1_B7_status": {
                "B1":"HOLD", "B2":"PARTIAL_STRUCTURAL_ONLY", "B3":"NOT_RUN",
                "B4":"NOT_RUN", "B5":"LOCAL_PREVIEW_CHECKS_ONLY", "B6":"NOT_RUN", "B7":"HOLD",
            },
            "source_alignment": {"original_evidence_qualification":"HOLD"},
            "core1a": {"construction_ids":["SYNTH-TEACH-1","SYNTH-TEACH-2"]},
            "core1b": {"cycle_ids":["SYNTH-CYCLE-1"]},
        },
        "source_register": {
            "source_custody":"OWNER_LOCAL_PRIVATE_NOT_FOR_PUBLIC_DEPLOYMENT",
            "requested_input_sources_zip":{"status":"NOT_RECEIVED"},
        },
        "physics_authority": "# D3.1 Physics authority review — HOLD\nSynthetic, unreviewed.",
        "handoff": {
            "schema":"core1a-source-handoff/v1",
            "status":"CANDIDATE",
            "question_links":[],
        },
        "browser_checks": {
            "scope":"AUTHOR_HUB_BROWSER_CHECKS_ONLY",
            "passed":2,
            "results":[{"name":"synthetic desktop","pass":True},
                       {"name":"synthetic mobile","pass":True}],
            "independent_QA":False,
        },
    }


def build_archives(tmp_path, overrides=None, discard=None):
    data = fixture_data()
    for key, value in (overrides or {}).items():
        data[key] = value
    contract = copy.deepcopy(SOURCES)
    paths = {}
    for group in ("d3", "handoff", "hub"):
        path = tmp_path / (group + ".zip")
        with zipfile.ZipFile(path,"w",compression=zipfile.ZIP_DEFLATED) as z:
            for key, member in contract[group]["members"].items():
                if (group,key) == discard:
                    continue
                payload = data[key]
                payload = payload if isinstance(payload, str) else json.dumps(payload)
                z.writestr(member, payload.encode("utf8"))
        paths[group] = path
        contract[group]["archive_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    return paths, contract


def run(paths,contract):
    return readback_pilot(paths["d3"], paths["handoff"], paths["hub"], source_contract=contract)


def codes(x):
    return set(x["diagnostic_codes"])


def test_candidate_state_stays_hold(tmp_path):
    paths,pin=build_archives(tmp_path)
    report=run(paths,pin)
    assert report["mechanical_status"]=="HOLD"
    assert report["academic_status"]==report["release_status"]=="HOLD"
    assert report["review_subject"]["subject_id"]=="PHYSICS"
    assert report["review_subject"]["native_demand"]=="D3_PROPOSED"
    assert report["review_subject"]["wep01_fixture_is_same_construction"]=="UNDETERMINED_NOT_JOINED"
    assert report["coverage"]["qualified_constructions"]==0


def test_all_seven_native_gate_states_preserved(tmp_path):
    paths,pin=build_archives(tmp_path)
    report=run(paths,pin)
    expected=fixture_data()["witness"]["B1_B7_status"]
    assert report["review_subject"]["b1_b7_native_status"]==expected


def test_native_pass_is_not_promoted(tmp_path):
    w=fixture_data()["witness"]
    w["B1_B7_status"]={key:"PASS" for key in w["B1_B7_status"]}
    paths,pin=build_archives(tmp_path,{"witness":w})
    report=run(paths,pin)
    assert report["academic_status"]=="HOLD"
    assert report["release_status"]=="HOLD"
    assert report["coverage"]["qualified_constructions"]==0


def test_native_fail_is_not_ignored(tmp_path):
    w=fixture_data()["witness"]
    w["B1_B7_status"]["B7"]="REJECTED"
    paths,pin=build_archives(tmp_path,{"witness":w})
    report=run(paths,pin)
    assert report["mechanical_status"]=="FAIL"
    assert "NATIVE_B_GATE_REJECTION_B7" in codes(report)


def test_missing_member_fails(tmp_path):
    paths,pin=build_archives(tmp_path,discard=("d3","witness"))
    report=run(paths,pin)
    assert report["mechanical_status"]=="FAIL"
    assert "ARCHIVE_OR_MEMBER_INVALID_D3" in codes(report)


def test_original_archive_integrity_mismatch_fails(tmp_path):
    paths,pin=build_archives(tmp_path)
    pin["d3"]["archive_sha256"]="0"*64
    assert "ARCHIVE_PIN_MISMATCH_D3" in codes(run(paths,pin))


def test_unreviewed_physics_authority_hard_boundary(tmp_path):
    paths,pin=build_archives(tmp_path,{"physics_authority":"# NOT AN AUTHORITY RECEIPT"})
    report=run(paths,pin)
    assert report["mechanical_status"]=="FAIL"
    assert "PHYSICS_AUTHORITY_HOLD_RECORD_UNKNOWN" in codes(report)


def test_original_exam_source_missing_stays_hold(tmp_path):
    paths,pin=build_archives(tmp_path)
    r=run(paths,pin)
    assert "REQUIRED_ORIGINAL_SOURCE_ARCHIVE_NOT_RECEIVED" in codes(r)
    assert r["academic_status"]=="HOLD"


def test_handoff_has_no_question_join(tmp_path):
    paths,pin=build_archives(tmp_path)
    r=run(paths,pin)
    assert "CORE1A_HANDOFF_HAS_ZERO_REVIEWED_QUESTION_LINKS" in codes(r)
    assert r["review_subject"]["handoff_question_link_count"]==0


def test_handoff_with_links_still_unreviewed(tmp_path):
    handoff=fixture_data()["handoff"]
    handoff["question_links"]=["SYNTH-UNVERIFIED-Q"]
    paths,pin=build_archives(tmp_path,{"handoff":handoff})
    r=run(paths,pin)
    assert "HANDOFF_NEW_QUESTION_LINKS_NEED_REVIEW" in codes(r)
    assert r["academic_status"]=="HOLD"


def test_browser_hub_not_learner_runtime(tmp_path):
    paths,pin=build_archives(tmp_path)
    r=run(paths,pin)
    assert "HUB_BROWSER_CHECKS_NOT_LEARNER_ATTEMPT_VALIDATION" in codes(r)
    assert r["review_subject"]["learner_runtime_verified"] is False


def test_hub_claimed_independent_qa_causes_mismatch(tmp_path):
    hub=fixture_data()["browser_checks"]
    hub["independent_QA"]=True
    paths,pin=build_archives(tmp_path,{"browser_checks":hub})
    assert "HUB_AUDIT_SCOPE_INVALID" in codes(run(paths,pin))


def test_failed_hub_browser_check_fails(tmp_path):
    hub=fixture_data()["browser_checks"]
    hub["results"][0]["pass"]=False
    paths,pin=build_archives(tmp_path,{"browser_checks":hub})
    assert "HUB_CHECKS_NOT_VERIFIABLE" in codes(run(paths,pin))


def test_unknown_gate_status_fails(tmp_path):
    w=fixture_data()["witness"]
    w["B1_B7_status"]["B1"]="TOTALLY_APPROVED_BY_ME"
    paths,pin=build_archives(tmp_path,{"witness":w})
    assert "B_GATE_STATUS_INVALID_B1" in codes(run(paths,pin))


def test_no_exam_or_learner_text_echo(tmp_path):
    w=fixture_data()["witness"]
    w["original_private_exam_stem"]="PRIVATE EXAM TEXT"
    w["core1a"]["illustrative_exact_excerpts"]=["PRIVATE TEACHING EXCERPT"]
    w["core1b"]["student_response"]="PRIVATE STUDENT ANSWER"
    paths,pin=build_archives(tmp_path,{"witness":w})
    output=json.dumps(run(paths,pin))
    assert "PRIVATE EXAM" not in output
    assert "PRIVATE TEACHING" not in output
    assert "PRIVATE STUDENT" not in output


def test_repeated_run_deterministic(tmp_path):
    paths,pin=build_archives(tmp_path)
    assert run(paths,pin)==run(paths,pin)
