import hashlib
import json
from pathlib import Path
from grade9qa.cli import main
from grade9qa.shared_audit import audit_shared

CANON = "CANONICAL_ACADEMIC_TRUTH"
CUSTODY = "AUTHORIZED_SOURCE_CUSTODY"

def make_fixture(tmp_path):
    shared = tmp_path / "Shared"
    files = {
        "roles/CORE-AUTHORITY-CONTRACT.md": """# Synthetic authority for parser tests
""" + "\x60"*3 + """core-authority
""" + json.dumps({
            "roles": {role: {
                "required_authority": ([CUSTODY] if role == "CORE2" else
                                       [CANON, "PRIOR_EXPOSURE"] if role == "CORE2B" else [CANON]),
                "forbidden_authority_substitution": [CUSTODY],
            } for role in ("CORE1","CORE2","CORE1A","CORE1B","CORE2A","CORE2B")},
            "invariants": {"execution_order_is_not_authority_order": True}
        }) + "\n" + "\x60"*3 + "\n",
        "vocabularies/cognitive-demand.v1.json": json.dumps({
            "demands": {k: {} for k in ("RETRIEVE","EXPLAIN","APPLY","MODEL","REPRESENT","SYNTHESIZE","JUSTIFY")}
        }),
        "policy/grade9-physics.v1.json": json.dumps({
            "concept_policies": [{"concept_id":"WORK_ENERGY", "scope_class":"PREREQUISITE"}]
        }),
    }
    baseline = {"schema_version":"1.0.0", "trust":"OWNER_SUPPLIED_UNVERIFIED",
                "source_archive_sha256": "0"*64, "file_count":len(files), "files":[]}
    for relative, text in files.items():
        path = shared / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        baseline["files"].append({"path":"Shared/"+relative, "sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                                  "size":path.stat().st_size})
    return shared, baseline

def codes(output):
    return [d["code"] for d in output["diagnostics"]]

def test_valid_fingerprint_is_still_hold(tmp_path):
    root, baseline = make_fixture(tmp_path)
    report = audit_shared(root, baseline)
    assert report["mechanical_status"] == "PASS"
    assert report["qualification_status"] == "HOLD"
    assert report["pinned_files_checked"] == 3
    assert report["grade9_work_energy_scope"] == "PREREQUISITE"

def test_changed_byte_fails(tmp_path):
    root, baseline = make_fixture(tmp_path)
    (root/"policy/grade9-physics.v1.json").write_text('{"concept_policies":[]}')
    result = audit_shared(root, baseline)
    assert result["mechanical_status"] == "FAIL"
    assert "PINNED_FILE_CHANGED" in codes(result)

def test_missing_pinned_file_holds(tmp_path):
    root, baseline = make_fixture(tmp_path)
    (root/"vocabularies/cognitive-demand.v1.json").unlink()
    result = audit_shared(root, baseline)
    assert result["mechanical_status"] == "HOLD"
    assert "PINNED_FILE_MISSING" in codes(result)

def test_path_escape_fails(tmp_path):
    root, baseline = make_fixture(tmp_path)
    baseline["files"][0]["path"] = "Shared/../SECRET"
    assert "PATH_ESCAPE" in codes(audit_shared(root, baseline))

def test_missing_role_is_detected(tmp_path):
    root, baseline = make_fixture(tmp_path)
    file = root/"roles/CORE-AUTHORITY-CONTRACT.md"
    file.write_text(file.read_text().replace('"CORE1B"', '"REMOVED"'))
    output = audit_shared(root, baseline)
    assert "CORE_ROLE_MISSING" in codes(output)

def test_order_is_not_authority(tmp_path):
    root, baseline = make_fixture(tmp_path)
    f = root/"roles/CORE-AUTHORITY-CONTRACT.md"
    f.write_text(f.read_text().replace('"execution_order_is_not_authority_order": true',
                                       '"execution_order_is_not_authority_order": false'))
    assert "AUTHORITY_ORDER_INVERSION" in codes(audit_shared(root, baseline))

def test_vocabulary_drift_fails(tmp_path):
    root, baseline = make_fixture(tmp_path)
    file = root/"vocabularies/cognitive-demand.v1.json"
    file.write_text(file.read_text().replace('"RETRIEVE"', '"MEMORIZE"'))
    assert "COGNITIVE_VOCABULARY_CONFLICT" in codes(audit_shared(root, baseline))

def test_work_energy_not_silently_promoted(tmp_path):
    root, baseline = make_fixture(tmp_path)
    file = root/"policy/grade9-physics.v1.json"
    file.write_text(file.read_text().replace("PREREQUISITE", "CORE"))
    assert "WORK_ENERGY_SCOPE_CHANGED" in codes(audit_shared(root, baseline))

def test_bad_baseline_trust_fails(tmp_path):
    root, baseline = make_fixture(tmp_path)
    baseline["trust"] = "VERIFIED"
    assert "BASELINE_TRUST_MISMATCH" in codes(audit_shared(root, baseline))

def test_external_schema_operation_drift(tmp_path):
    root, baseline = make_fixture(tmp_path)
    schema = tmp_path/"schema.json"
    schema.write_text(json.dumps({"properties":{"operation":{"enum":["MODEL"]}}}))
    assert "GRADE9QA_VOCABULARY_DRIFT" in codes(audit_shared(root, baseline,construction_schema=schema))

def test_cli_exit_hold_on_compatible_snapshot(tmp_path):
    root, baseline = make_fixture(tmp_path)
    pins = tmp_path/"pins.json"
    pins.write_text(json.dumps(baseline))
    out = tmp_path/"report.json"
    code = main(["shared-audit","--shared-root",str(root),"--baseline",str(pins),"--out",str(out)])
    assert code == 3
    assert json.loads(out.read_text())["integration_status"] == "HOLD"

def test_cli_exit_fail_on_modified_snapshot(tmp_path):
    root, baseline = make_fixture(tmp_path)
    (root/"roles/CORE-AUTHORITY-CONTRACT.md").write_text("changed")
    pins = tmp_path/"pins.json"
    pins.write_text(json.dumps(baseline))
    out = tmp_path/"report.json"
    assert main(["shared-audit","--shared-root",str(root),"--baseline",str(pins),"--out",str(out)]) == 1

def test_archive_digest_mismatch(tmp_path):
    root, baseline = make_fixture(tmp_path)
    archive = tmp_path/"wrong.zip"
    archive.write_bytes(b"not a zip")
    assert "SHARED_ARCHIVE_UNREADABLE" in codes(audit_shared(root, baseline,archive=archive))

def test_no_user_data_in_report(tmp_path):
    root, baseline = make_fixture(tmp_path)
    baseline["private_user_note"] = "do-not-publish-this"
    assert "do-not-publish-this" not in json.dumps(audit_shared(root, baseline))
