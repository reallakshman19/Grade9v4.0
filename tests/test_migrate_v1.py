"""P0.5b migration tests use ONLY the existing synthetic WEP-01 v1 fixture."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from grade9qa.cli import main
from grade9qa.migrate_v1 import preview_v1_to_v2
from grade9qa.subjects import audit_subject_intake

BASE = Path(__file__).resolve().parents[1] / "examples/three-subjects-candidate/manifest.json"


def base_v2(tmp_path):
    dest = tmp_path / "v2-input.json"
    dest.write_bytes(BASE.read_bytes())
    return dest


def report(candidate, tmp_path):
    return preview_v1_to_v2(candidate / "bundle.json", base_v2(tmp_path))


def diag_codes(output):
    return {x["code"] for x in output["diagnostics"]}


def mutate(candidate, name, fn):
    p = candidate / name
    data = json.loads(p.read_text())
    fn(data)
    p.write_text(json.dumps(data))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v1_preview_keeps_original_ids_and_statuses(candidate, tmp_path):
    r = report(candidate, tmp_path)
    assert r["mechanical_status"] == "HOLD"
    assert r["qualification_status"] == "HOLD"
    expected = {"SOURCE-N01", "WARR-N01", "WEP-C01", "LESSON-A01", "TEST-Q01"}
    assert {x["original_id"] for x in r["reference_mappings"]} == expected
    assert all(x["original_status"] == "CANDIDATE" for x in r["reference_mappings"])
    assert all(x["proposed_ref"].startswith("PHYSICS/WEP-01/") for x in r["reference_mappings"])


def test_v1_preview_sources_are_original_bytes(candidate, tmp_path):
    r = report(candidate, tmp_path)
    assert r["source_file_pins"]["bundle.json"] == sha(candidate / "bundle.json")
    for name in ("sources", "warrants", "constructions", "lessons", "assessments", "approvals"):
        assert r["source_file_pins"]["v1/" + name] == sha(candidate / (name + ".json"))
    assert r["source_file_pins"]["original-source/SOURCE-N01"] == sha(candidate / "synthetic-note.txt")


def test_no_historical_data_written(candidate, tmp_path):
    inputs = list(candidate.glob("*"))
    before = {p.name: p.read_bytes() for p in inputs if p.is_file()}
    report(candidate, tmp_path)
    assert before == {p.name: p.read_bytes() for p in inputs if p.is_file()}


def test_v2_candidate_has_subject_scoped_typed_refs(candidate, tmp_path):
    r = report(candidate, tmp_path)
    v2 = r["candidate_manifest"]
    assert v2 is not None
    assert audit_subject_intake(v2)["mechanical_status"] == "PASS"
    physics = next(s for s in v2["subjects"] if s["subject_id"] == "PHYSICS")
    topic = physics["topics"][0]
    assert [x["id"] for x in topic["constructions"]] == ["WEP-C01"]
    assert topic["constructions"][0]["warrant_refs"] == ["PHYSICS/WEP-01/WARR-N01"]
    assert topic["constructions"][0]["source_refs"] == ["PHYSICS/WEP-01/SOURCE-N01"]
    assert topic["warrants"][0]["source_refs"] == ["PHYSICS/WEP-01/SOURCE-N01"]


def test_legacy_blueprint_and_adapter_aliases_are_not_invented(candidate, tmp_path):
    r = report(candidate, tmp_path)
    assert "LEGACY_BLUEPRINT_ALIAS_REVIEW_REQUIRED" in diag_codes(r)
    assert "LEGACY_ADAPTER_ALIAS_REVIEW_REQUIRED" in diag_codes(r)
    assert "PHYSICS_BLUEPRINT_ID_VERSION_ALIAS" in r["unresolved_fields"]
    assert r["shared_canonical_admission"] == "NOT_PERFORMED"


def test_no_lessons_or_approvals_silently_migrated(candidate, tmp_path):
    r = report(candidate, tmp_path)
    table = {x["collection"]: x["migration"] for x in r["reference_mappings"]}
    assert table["lessons"] == "NOT_MIGRATED"
    assert table["assessments"] == "NOT_MIGRATED"
    assert "NATIVE_LESSONS_MIGRATION_NOT_IMPLEMENTED" in r["unresolved_fields"]


def test_maths_and_chem_stay_planned(candidate, tmp_path):
    r = report(candidate, tmp_path)
    for s in r["candidate_manifest"]["subjects"]:
        if s["subject_id"] in ("MATHEMATICS", "CHEMISTRY"):
            assert s["stage"] == "PLANNED"
            assert s["blueprint_ref"] is None and s["topics"] == []


def test_modified_source_asset_produces_fail(candidate, tmp_path):
    (candidate / "synthetic-note.txt").write_text("changed source bytes")
    r = report(candidate, tmp_path)
    assert r["mechanical_status"] == "FAIL"
    assert r["candidate_manifest"] is None
    assert "SOURCE_CONTENT_DIGEST_CHANGED" in diag_codes(r)


def test_missing_source_asset_blocks_preview(candidate, tmp_path):
    (candidate / "synthetic-note.txt").unlink()
    r = report(candidate, tmp_path)
    assert r["mechanical_status"] == "HOLD"
    assert r["candidate_manifest"] is None
    assert "SOURCE_ORIGINAL_BYTES_UNAVAILABLE" in diag_codes(r)


def test_old_source_path_escape_is_rejected(candidate, tmp_path):
    mutate(candidate,"sources.json",lambda d:d[0].update(path="../private-note.txt"))
    r=report(candidate,tmp_path)
    assert r["mechanical_status"] == "FAIL"
    assert r["candidate_manifest"] is None


def test_approved_record_status_not_downgraded(candidate, tmp_path):
    mutate(candidate,"warrants.json",lambda d:d[0].update(status="APPROVED"))
    r=report(candidate,tmp_path)
    assert r["candidate_manifest"] is None
    assert "HISTORIC_APPROVAL_NOT_PORTABLE" in diag_codes(r)


def test_approved_bundle_requires_independent_promotion_review(candidate, tmp_path):
    mutate(candidate,"bundle.json",lambda d:d.update(status="APPROVED"))
    r=report(candidate,tmp_path)
    assert r["candidate_manifest"] is None
    assert "HISTORIC_BUNDLE_APPROVAL_REQUIRES_REVIEW" in diag_codes(r)


def test_contradictory_topic_not_auto_migrated(candidate, tmp_path):
    mutate(candidate,"bundle.json",lambda d:d.update(topic_id="WEP-03"))
    r=report(candidate,tmp_path)
    assert r["candidate_manifest"] is None
    assert "PILOT_TOPIC_NOT_WEP01" in diag_codes(r)


def test_invalid_v1_bundle_record_ref_fails(candidate, tmp_path):
    mutate(candidate,"constructions.json",lambda d:d[0].update(warrant_ids=["NONEXISTENT"]))
    r=report(candidate,tmp_path)
    assert r["mechanical_status"] == "FAIL"
    assert r["candidate_manifest"] is None


def test_invalid_v2_schema_fails(candidate, tmp_path):
    p=base_v2(tmp_path)
    obj=json.loads(p.read_text())
    obj["subjects"][2]["subject_id"]="BIOLOGY"
    p.write_text(json.dumps(obj))
    r=preview_v1_to_v2(candidate/"bundle.json",p)
    assert "V2_BASE_MANIFEST_INVALID" in diag_codes(r)
    assert r["candidate_manifest"] is None


def test_target_with_existing_records_fails(candidate, tmp_path):
    p=base_v2(tmp_path)
    obj=json.loads(p.read_text())
    obj["subjects"][0]["topics"][0]["sources"]=[{"id":"EXIST","status":"CANDIDATE","origin_ref":"old"}]
    p.write_text(json.dumps(obj))
    r=preview_v1_to_v2(candidate/"bundle.json",p)
    assert "NONEMPTY_MIGRATION_TARGET" in diag_codes(r)
    assert r["candidate_manifest"] is None


def test_wrong_wpe_unit_fails(candidate, tmp_path):
    p=base_v2(tmp_path)
    obj=json.loads(p.read_text())
    obj["subjects"][0]["topics"][0]["unit_id"]="NOT-WPE"
    p.write_text(json.dumps(obj))
    r=preview_v1_to_v2(candidate/"bundle.json",p)
    assert "WPE_UNIT_MISMATCH" in diag_codes(r)


def test_duplicate_keys_in_v1_bundle_fail(candidate, tmp_path):
    p=candidate/"bundle.json"
    raw=p.read_text().replace('"topic_id": "WEP-01",','"topic_id": "WEP-01", "topic_id": "WEP-01",')
    p.write_text(raw)
    r=report(candidate,tmp_path)
    assert r["mechanical_status"]=="FAIL"


def test_duplicate_keys_in_original_v1_collection_fail(candidate, tmp_path):
    p=candidate/"sources.json"
    p.write_text(p.read_text().replace('"id": "SOURCE-N01",','"id": "SOURCE-N01", "id":"SOURCE-N01",'))
    r=report(candidate,tmp_path)
    assert "V1_COLLECTION_NOT_STABLE" in diag_codes(r)


def test_migration_report_does_not_echo_source_text(candidate, tmp_path):
    r=report(candidate,tmp_path)
    dump=json.dumps(r)
    assert "Fixture only; not a textbook source" not in dump
    assert "Magnitude alone does not determine sign" not in dump


def test_deterministic_preview(candidate, tmp_path):
    a=report(candidate,tmp_path)
    b=report(candidate,tmp_path)
    assert a==b


def test_cli_report_and_candidate_out(candidate, tmp_path):
    p=base_v2(tmp_path)
    out=tmp_path/"report.json"
    target=tmp_path/"candidate.json"
    code=main(["migrate-v1-preview","--bundle",str(candidate/"bundle.json"),
               "--manifest",str(p),"--out",str(out),"--candidate-out",str(target)])
    assert code==3
    report=json.loads(out.read_text())
    assert report["qualification_status"]=="HOLD"
    assert audit_subject_intake(json.loads(target.read_text()))["mechanical_status"]=="PASS"


def test_cli_never_overwrites_historical_v1_bundle(candidate, tmp_path):
    p=base_v2(tmp_path)
    original=(candidate/"bundle.json").read_bytes()
    code=main(["migrate-v1-preview","--bundle",str(candidate/"bundle.json"),
               "--manifest",str(p),"--out",str(candidate/"bundle.json")])
    assert code==2
    assert (candidate/"bundle.json").read_bytes()==original


def test_cli_never_overwrites_input_v2_manifest(candidate, tmp_path):
    p=base_v2(tmp_path)
    original=p.read_bytes()
    rc=main(["migrate-v1-preview","--bundle",str(candidate/"bundle.json"),
             "--manifest",str(p),"--out",str(p)])
    assert rc==2
    assert p.read_bytes()==original


def test_cli_never_writes_candidate_into_original_folder(candidate, tmp_path):
    p=base_v2(tmp_path)
    rc=main(["migrate-v1-preview","--bundle",str(candidate/"bundle.json"),
             "--manifest",str(p),"--out",str(tmp_path/"out.json"),
             "--candidate-out",str(candidate/"new.json")])
    assert rc==2
    assert not (candidate/"new.json").exists()


def test_cli_does_not_export_candidate_if_source_is_missing(candidate, tmp_path):
    p=base_v2(tmp_path)
    (candidate/"synthetic-note.txt").unlink()
    target=tmp_path/"out-candidate.json"
    rc=main(["migrate-v1-preview","--bundle",str(candidate/"bundle.json"),
             "--manifest",str(p),"--out",str(tmp_path/"audit.json"),
             "--candidate-out",str(target)])
    assert rc==3
    assert not target.exists()
