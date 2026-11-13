"""Reproducible all-file Shared.zip inventory, without extracting or executing code.

The archive is an Owner-supplied CANDIDATE source. A complete hash match never
establishes a trusted signature or approval.
"""
from __future__ import annotations

import hashlib
import stat
import zipfile
from pathlib import Path, PurePosixPath

MAX_FILES = 20000
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024


def _finding(code, detail, path=""):
    return {"code": code, "path": path, "detail": detail}


def _sha_stream(handle) -> str:
    h = hashlib.sha256()
    while chunk := handle.read(1024 * 1024):
        h.update(chunk)
    return h.hexdigest()


def inventory_zip(archive: Path, root: Path | None = None,
                  expected_archive_sha256: str | None = None) -> dict:
    """Build inventory for ALL files; optionally compare exact extracted snapshot.

    Does not unzip. ZIP members must use POSIX names under Shared/ and must be
    regular files. Reject duplicate/casefold entries, symlinks, traversal, bombs,
    size/hash drift, missing files and extra extracted files.
    """
    archive = Path(archive)
    problems = []
    entries = []
    try:
        with archive.open("rb") as source:
            archive_hash = _sha_stream(source)
        if expected_archive_sha256 and archive_hash != expected_archive_sha256:
            problems.append(_finding("UNEXPECTED_ARCHIVE_SHA256", "Supplied archive is not the pinned candidate."))
        with zipfile.ZipFile(archive) as z:
            members = [i for i in z.infolist() if not i.is_dir()]
            if len(members) > MAX_FILES:
                problems.append(_finding("ZIP_ENTRY_LIMIT", "Archive contains too many files."))
                members = []
            total = 0
            names = set()
            casefold_names = set()
            for info in sorted(members, key=lambda i: i.filename):
                name = info.filename
                pp = PurePosixPath(name)
                file_mode = info.external_attr >> 16
                filetype = stat.S_IFMT(file_mode)
                unsafe = (
                    not name.startswith("Shared/") or name.startswith("/")
                    or "\\" in name or ".." in pp.parts
                    or any(p in ("", ".") for p in pp.parts)
                    or pp.as_posix() != name
                    or filetype not in (0, stat.S_IFREG)
                    or info.flag_bits & 0x1
                    or name in names or name.casefold() in casefold_names
                )
                if unsafe:
                    problems.append(_finding("UNSAFE_ZIP_MEMBER", "Bad path, duplicate, symlink, encrypted or nonregular entry.", name))
                    continue
                names.add(name)
                casefold_names.add(name.casefold())
                total += info.file_size
                if info.file_size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                    problems.append(_finding("ZIP_SIZE_LIMIT", "Archive exceeds conservative file/total size limits.", name))
                    continue
                try:
                    with z.open(info) as source:
                        h = _sha_stream(source)
                except (OSError, RuntimeError, ValueError, zipfile.BadZipFile) as exc:
                    problems.append(_finding("ZIP_MEMBER_UNREADABLE", str(exc), name))
                    continue
                entries.append({"path": name, "size": info.file_size, "sha256": h})
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        return {"schema_version": "1.0.0", "mechanical_status": "FAIL",
                "qualification_status": "HOLD", "file_count": 0, "files": [],
                "diagnostics": [_finding("ARCHIVE_UNREADABLE", str(exc), str(archive))],
                "warning": "NOT_ACADEMIC_APPROVAL"}
    actual_extra = []
    checked = 0
    if root is not None:
        root = Path(root).resolve()
        if not root.is_dir():
            problems.append(_finding("SHARED_ROOT_MISSING", "Expected extracted Shared directory.", str(root)))
        else:
            expected = {e["path"] for e in entries}
            for e in entries:
                target = (root / PurePosixPath(e["path"]).relative_to("Shared")).resolve()
                if not target.is_relative_to(root):
                    problems.append(_finding("PATH_ESCAPE", "Symlink escapes supplied Shared root.", e["path"]))
                elif not target.is_file():
                    problems.append(_finding("EXTRACTED_FILE_MISSING", "Expected file absent.", e["path"]))
                elif target.stat().st_size != e["size"]:
                    problems.append(_finding("EXTRACTED_SIZE_MISMATCH", "Extracted file size differs.", e["path"]))
                else:
                    try:
                        with target.open("rb") as source:
                            digest = _sha_stream(source)
                        if digest != e["sha256"]:
                            problems.append(_finding("EXTRACTED_HASH_MISMATCH", "Extracted file bytes differ.", e["path"]))
                        else:
                            checked += 1
                    except OSError as exc:
                        problems.append(_finding("EXTRACTED_FILE_UNREADABLE", str(exc), e["path"]))
            for p in sorted(root.rglob("*")):
                if p.is_file() or p.is_symlink():
                    path = "Shared/" + p.relative_to(root).as_posix()
                    if path not in expected:
                        actual_extra.append(path)
            for p in actual_extra:
                problems.append(_finding("UNEXPECTED_EXTRACTED_FILE", "Extra file not present in pinned archive.", p))
    return {
        "schema_version": "1.0.0",
        "archive_sha256": archive_hash,
        "archive_trust": "OWNER_SUPPLIED_UNVERIFIED",
        "file_count": len(entries),
        "files": entries,
        "extracted_files_verified": checked,
        "mechanical_status": "FAIL" if problems else "PASS",
        "qualification_status": "HOLD",
        "blocked_by": ["TRUSTED_OWNER_SIGNATURE", "INDEPENDENT_FULL_BASELINE_REVIEW",
                       "SHARED_INTEGRATION_REVIEW", "PUBLIC_REDISTRIBUTION_PERMISSION"],
        "diagnostics": sorted(problems, key=lambda x: (x["path"], x["code"])),
        "warning": "NOT_ACADEMIC_APPROVAL: full file hashes do not certify academic content or release.",
    }
