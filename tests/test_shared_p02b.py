import hashlib
import json
import zipfile

from grade9qa.cli import main
from grade9qa.shared_manifest import inventory_zip
from grade9qa.shared_authorities import summarize_authorities


def sample_zip(tmp_path, files=None):
    files = files or {"Shared/contracts.py": b"original", "Shared/roles/CORE1.md": b"roles"}
    archive = tmp_path / "Shared.zip"
    with zipfile.ZipFile(archive, "w") as writer:
        for name, data in files.items():
            writer.writestr(name, data)
    root = tmp_path / "Shared"
    for name, data in files.items():
        p = root / name.removeprefix("Shared/")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    pin = hashlib.sha256(archive.read_bytes()).hexdigest()
    return archive, root, pin


def codes(result):
    return [x["code"] for x in result["diagnostics"]]


def test_full_inventory_counts_and_verifies_bytes(tmp_path):
    a, root, pin = sample_zip(tmp_path)
    report = inventory_zip(a, root=root, expected_archive_sha256=pin)
    assert report["file_count"] == 2
    assert report["extracted_files_verified"] == 2
    assert report["mechanical_status"] == "PASS"
    assert report["qualification_status"] == "HOLD"
    assert all(len(e["sha256"]) == 64 for e in report["files"])


def test_full_inventory_repeatable(tmp_path):
    a, root, pin = sample_zip(tmp_path)
    assert inventory_zip(a, root=root, expected_archive_sha256=pin) == inventory_zip(a, root=root, expected_archive_sha256=pin)


def test_archive_pin_mismatch(tmp_path):
    a, root, _ = sample_zip(tmp_path)
    assert "UNEXPECTED_ARCHIVE_SHA256" in codes(inventory_zip(a, root=root, expected_archive_sha256="0" * 64))


def test_extracted_file_changed(tmp_path):
    a, root, pin = sample_zip(tmp_path)
    (root / "contracts.py").write_bytes(b"changed-length")
    assert "EXTRACTED_SIZE_MISMATCH" in codes(inventory_zip(a, root=root, expected_archive_sha256=pin))


def test_extracted_same_size_changed(tmp_path):
    a, root, pin = sample_zip(tmp_path)
    (root / "contracts.py").write_bytes(b"ORIGINAL")
    assert "EXTRACTED_HASH_MISMATCH" in codes(inventory_zip(a, root=root, expected_archive_sha256=pin))


def test_extra_extracted_file(tmp_path):
    a, root, pin = sample_zip(tmp_path)
    (root / "extra.txt").write_text("oops")
    assert "UNEXPECTED_EXTRACTED_FILE" in codes(inventory_zip(a, root=root, expected_archive_sha256=pin))


def test_missing_extracted_file(tmp_path):
    a, root, pin = sample_zip(tmp_path)
    (root / "contracts.py").unlink()
    assert "EXTRACTED_FILE_MISSING" in codes(inventory_zip(a, root=root, expected_archive_sha256=pin))


def test_zip_path_traversal(tmp_path):
    a, _, _ = sample_zip(tmp_path, {"Shared/../other.txt": b"bad"})
    assert "UNSAFE_ZIP_MEMBER" in codes(inventory_zip(a))


def test_zip_duplicate_entry(tmp_path):
    archive = tmp_path / "duplicate.zip"
    with zipfile.ZipFile(archive, "w") as writer:
        writer.writestr("Shared/a.txt", b"a")
        writer.writestr("Shared/a.txt", b"b")
    assert "UNSAFE_ZIP_MEMBER" in codes(inventory_zip(archive))


def test_zip_case_collision(tmp_path):
    a, _, _ = sample_zip(tmp_path, {"Shared/Alpha.txt": b"a", "Shared/alpha.txt": b"b"})
    assert "UNSAFE_ZIP_MEMBER" in codes(inventory_zip(a))


def test_no_zip(tmp_path):
    report = inventory_zip(tmp_path / "absent.zip")
    assert report["mechanical_status"] == "FAIL"
    assert "ARCHIVE_UNREADABLE" in codes(report)


def native(core=True, reviews=None, releases=None):
    return ({"passed": True, "roles_checked": 6, "findings": []} if core else
            {"passed": False, "roles_checked": 5, "findings": ["bad"]},
            {"passed": True, "receipts": [] if reviews is None else reviews, "findings": []},
            {"passed": True, "receipts": [] if releases is None else releases,
             "self_authorized_manifests": [], "findings": []})


def test_empty_successful_native_reports_are_hold():
    core, review, release = native()
    report = summarize_authorities(review, release, core)
    assert report["mechanical_status"] == "HOLD"
    assert report["qualification_status"] == "HOLD"
    assert {"REVIEW_NO_RECEIPTS", "RELEASE_NO_RECEIPTS"} <= set(codes(report))


def test_native_claimed_approvals_never_self_authorize():
    core, review, release = native(
        reviews=[{"path": "Reviews/receipts/r.json", "verified": True, "findings": []}],
        releases=[{"path": "Releases/receipts/x.json", "verified": True, "findings": []}],
    )
    report = summarize_authorities(review, release, core)
    assert report["integration_status"] == "HOLD"
    assert report["qualification_status"] == "HOLD"
    assert report["mechanical_status"] == "HOLD"


def test_failed_native_receipt_is_failure():
    core, review, release = native(reviews=[{"path": "review.json", "verified": False, "findings": ["stale"]}])
    result = summarize_authorities(review, release, core)
    assert result["mechanical_status"] == "FAIL"
    assert "REVIEW_RECEIPT_NOT_VERIFIED" in codes(result)


def test_forged_self_authorization_fails():
    core, review, release = native()
    release["self_authorized_manifests"] = ["subject/content/publication/manifest.json"]
    assert "RELEASE_SELF_AUTHORIZATION" in codes(summarize_authorities(review, release, core))


def test_core_authority_mismatch_fails():
    core, review, release = native(core=False)
    assert "CORE_AUTHORITY_UNVERIFIED" in codes(summarize_authorities(review, release, core))


def test_native_findings_override_pass():
    core, review, release = native()
    review["findings"] = [{"point": "REVIEW_STALE"}]
    result = summarize_authorities(review, release, core)
    assert result["mechanical_status"] == "FAIL"


def test_cli_native_authorities_hold(tmp_path):
    core, review, release = native()
    for path, obj in ((tmp_path / "c.json", core),
                      (tmp_path / "r.json", review),
                      (tmp_path / "l.json", release)):
        path.write_text(json.dumps(obj))
    out = tmp_path / "out.json"
    assert main(["shared-authorities", "--core", str(tmp_path / "c.json"),
                 "--review", str(tmp_path / "r.json"),
                 "--release", str(tmp_path / "l.json"),
                 "--out", str(out)]) == 3
    assert json.loads(out.read_text())["qualification_status"] == "HOLD"


def test_cli_native_failure(tmp_path):
    core, review, release = native(core=False)
    for path, obj in ((tmp_path / "c.json", core),
                      (tmp_path / "r.json", review),
                      (tmp_path / "l.json", release)):
        path.write_text(json.dumps(obj))
    out = tmp_path / "out.json"
    assert main(["shared-authorities", "--core", str(tmp_path / "c.json"),
                 "--review", str(tmp_path / "r.json"),
                 "--release", str(tmp_path / "l.json"),
                 "--out", str(out)]) == 1


def test_manifest_cli_rejects_non_pinned_archive(tmp_path):
    archive, root, _ = sample_zip(tmp_path)
    out = tmp_path / "manifest.json"
    result = main(["shared-manifest", "--archive", str(archive),
                   "--shared-root", str(root), "--out", str(out)])
    assert result == 1
    assert "UNEXPECTED_ARCHIVE_SHA256" in codes(json.loads(out.read_text()))
