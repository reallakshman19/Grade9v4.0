"""Native Shared subject-discovery adapter negative controls, not approvals."""
import copy
import json
from pathlib import Path

import pytest

from grade9qa.cli import main
from grade9qa.shared_dispatch import inspect_shared_dispatch

MANIFEST=Path(__file__).resolve().parents[1]/"examples/three-subjects-candidate/manifest.json"


@pytest.fixture
def candidate():
    return json.loads(MANIFEST.read_text())


@pytest.fixture
def native():
    return {"passed": True, "subjects_checked": 1,
            "subjects":[{"subject":"Physics","state":"IMPLEMENTED",
                         "gate_registries":1,"library_packages":1,"findings":[]}]}


def problems(report):
    return {d["code"] for d in report["diagnostics"]}


def test_native_subject_with_explicit_mapping_is_not_canonical_approval(candidate,native):
    r=inspect_shared_dispatch(candidate,native,{"PHYSICS":"Physics"})
    assert r["subjects"]["PHYSICS"]["native_state"]=="IMPLEMENTED"
    assert r["mechanical_status"]=="HOLD"
    assert r["academic_status"]==r["release_status"]=="HOLD"
    assert r["canonical_admission"]=="NOT_PERFORMED"


def test_standalone_shared_archive_has_no_native_subjects(candidate):
    native={"passed":False,"subjects_checked":0,"subjects":[]}
    r=inspect_shared_dispatch(candidate,native,{})
    assert r["mechanical_status"]=="HOLD"
    assert "NATIVE_NO_SUBJECTS_DISCOVERED" in problems(r)
    assert "ACTIVE_SUBJECT_NATIVE_BINDING_MISSING" in problems(r)


def test_missing_explicit_native_directory_binding_holds(candidate,native):
    assert "ACTIVE_SUBJECT_NATIVE_BINDING_MISSING" in problems(
        inspect_shared_dispatch(candidate,native,{}))


def test_guessed_math_and_chem_native_subject_bindings_not_accepted(candidate,native):
    r=inspect_shared_dispatch(candidate,native,{"PHYSICS":"Physics","MATHEMATICS":"Math","CHEMISTRY":"Chem"})
    assert "PLANNED_SUBJECT_PREMATURE_NATIVE_BINDING" in problems(r)
    assert r["academic_status"]=="HOLD"


def test_untrusted_native_pass_with_zero_subjects_fails(candidate):
    r=inspect_shared_dispatch(candidate,{"passed":True,"subjects_checked":0,"subjects":[]},{})
    assert "VACUOUS_NATIVE_PASS" in problems(r)


def test_native_findings_fail(candidate,native):
    native["subjects"][0]["findings"]=["COMPAT_FAILURE"]
    r=inspect_shared_dispatch(candidate,native,{"PHYSICS":"Physics"})
    assert r["mechanical_status"]=="FAIL"
    assert "NATIVE_SUBJECT_FINDINGS_PRESENT" in problems(r)


def test_native_mismatch_count_fails(candidate,native):
    native["subjects_checked"]=2
    assert "NATIVE_COUNT_INCONSISTENT" in problems(
        inspect_shared_dispatch(candidate,native,{"PHYSICS":"Physics"}))


def test_native_contract_only_is_not_implemented(candidate,native):
    native["subjects"][0]["state"]="CONTRACT_ONLY"
    assert "ACTIVE_SUBJECT_CONTRACT_ONLY" in problems(
        inspect_shared_dispatch(candidate,native,{"PHYSICS":"Physics"}))


def test_binding_to_unknown_native_subject_holds(candidate,native):
    assert "ACTIVE_SUBJECT_NOT_NATIVE_DISCOVERED" in problems(
        inspect_shared_dispatch(candidate,native,{"PHYSICS":"UnknownPhysics"}))


def test_mapping_path_escape_rejected(candidate,native):
    r=inspect_shared_dispatch(candidate,native,{"PHYSICS":"../../Physics"})
    assert "UNSAFE_SUBJECT_DIRECTORY_BINDING" in problems(r)
    assert r["mechanical_status"]=="FAIL"


def test_directory_casefold_collision_rejected(candidate,native):
    r=inspect_shared_dispatch(candidate,native,
                              {"PHYSICS":"Physics","MATHEMATICS":"physics"})
    assert "DUPLICATE_NATIVE_SUBJECT_BINDING" in problems(r)


def test_unknown_subject_mapping_rejected(candidate,native):
    assert "UNKNOWN_SUBJECT_BINDING" in problems(
        inspect_shared_dispatch(candidate,native,{"BIOLOGY":"Biology"}))


def test_forged_native_pass_does_not_authorize(candidate,native):
    native["published"]="RELEASE_ALLOWED"
    r=inspect_shared_dispatch(candidate,native,{"PHYSICS":"Physics"})
    assert r["release_status"]=="HOLD"
    assert r["academic_status"]=="HOLD"
    assert "published" not in json.dumps(r)


def test_invalid_candidate_will_not_be_dispatched(candidate,native):
    candidate["subjects"][0]["topic_id"]="INVALID"
    assert "V2_INTAKE_INVALID" in problems(
        inspect_shared_dispatch(candidate,native,{"PHYSICS":"Physics"}))


def test_shared_dispatch_cli_remains_hold(candidate,native,tmp_path):
    paths={}
    for name,data in (("manifest",candidate),("native",native),("bindings",{"PHYSICS":"Physics"})):
        p=tmp_path/(name+".json")
        p.write_text(json.dumps(data))
        paths[name]=p
    out=tmp_path/"dispatch.json"
    rc=main(["shared-dispatch-audit","--manifest",str(paths["manifest"]),
             "--native-report",str(paths["native"]),
             "--bindings",str(paths["bindings"]),"--out",str(out)])
    assert rc==3
    assert json.loads(out.read_text())["canonical_admission"]=="NOT_PERFORMED"


def test_shared_dispatch_cli_prevents_source_overwrite(candidate,native,tmp_path):
    paths={}
    for name,data in (("manifest",candidate),("native",native),("bindings",{"PHYSICS":"Physics"})):
        p=tmp_path/(name+".json")
        p.write_text(json.dumps(data))
        paths[name]=p
    original=paths["native"].read_bytes()
    rc=main(["shared-dispatch-audit","--manifest",str(paths["manifest"]),
             "--native-report",str(paths["native"]),
             "--bindings",str(paths["bindings"]),"--out",str(paths["native"])])
    assert rc==2
    assert paths["native"].read_bytes()==original


def test_shared_dispatch_cli_invalid_duplicate_json_key_is_input_error(candidate,native,tmp_path):
    a=tmp_path/"manifest.json"; a.write_text(json.dumps(candidate))
    b=tmp_path/"native.json"; b.write_text('{"passed":true,"passed":true}')
    c=tmp_path/"map.json"; c.write_text('{"PHYSICS":"Physics"}')
    assert main(["shared-dispatch-audit","--manifest",str(a),"--native-report",str(b),
                 "--bindings",str(c),"--out",str(tmp_path/"result.json")])==2
