"""Local CLI. Exit: 0 successful command, 1 invalid, 2 IO, 3 qualification HOLD."""
import argparse
import sys
from pathlib import Path
from .errors import InputError
from .io import read_json, write_json
from .smart_skills import inspect_native_report
from .shared_audit import audit_shared
from .shared_manifest import inventory_zip
from .shared_authorities import summarize_authorities
from .validate import inspect
from .report import make_report, markdown

def main(argv=None):
    parser = argparse.ArgumentParser(prog="grade9qa", description="Evidence checks, NOT academic approval.")
    subs = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "bridge", "qualify", "report"):
        command = subs.add_parser(name, description="Candidate data only; academic gates remain HOLD.",
                                  epilog="Exit codes: 0=done, 1=invalid, 2=IO, 3=HOLD for qualify.")
        command.add_argument("--bundle", required=True, help="Path to bundle.json")
        if name == "report":
            command.add_argument("--json", required=True)
            command.add_argument("--md", required=True)
        else:
            command.add_argument("--out", required=True)
    smart = subs.add_parser("smart-audit", help="Read-only R2 candidate checker-report inspection; never grants approval.")
    smart.add_argument("--report", required=True, help="Local JSON from original native checker")
    smart.add_argument("--out", required=True, help="Output v4 hold/readiness summary")
    shared = subs.add_parser("shared-audit", help="Read-only external Shared baseline fingerprint and authority audit.")
    shared.add_argument("--shared-root", required=True, help="Path to extracted Shared/ folder")
    shared.add_argument("--baseline", help="Optional owner-supplied fingerprint JSON (default docs/shared-baseline-pins.json)")
    shared.add_argument("--archive", help="Optional original Shared.zip for archive digest/count verification")
    shared.add_argument("--out", required=True, help="Path to audit output JSON")
    manifest = subs.add_parser("shared-manifest", help="Rebuild complete Shared.zip manifest; never grants authority.")
    manifest.add_argument("--archive", required=True, help="Local owner-supplied Shared.zip")
    manifest.add_argument("--shared-root", help="Optional extracted Shared/ directory to compare all files")
    manifest.add_argument("--out", required=True, help="Write complete per-file SHA-256 manifest JSON")
    authority = subs.add_parser("shared-authorities", help="Read native Shared authority reports; never self-approves.")
    authority.add_argument("--review", required=True, help="JSON output of native review_authority.py --audit")
    authority.add_argument("--release", required=True, help="JSON output of native release_authority.py --audit")
    authority.add_argument("--core", required=True, help="JSON output of native core_authority_contract.py")
    authority.add_argument("--out", required=True, help="Output audit summary JSON")
    args = parser.parse_args(argv)
    try:
        if args.command == "shared-manifest":
            baseline_path = Path(__file__).resolve().parents[2] / "docs/shared-baseline-pins.json"
            pin = read_json(baseline_path)["source_archive_sha256"]
            out = inventory_zip(Path(args.archive), root=Path(args.shared_root) if args.shared_root else None,
                                expected_archive_sha256=pin)
            write_json(Path(args.out), out)
            print("SHARED-MANIFEST", out["file_count"], "files; mechanical=" + out["mechanical_status"],
                  "qualification=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if out["mechanical_status"] == "FAIL" else 3
        if args.command == "shared-authorities":
            out = summarize_authorities(read_json(Path(args.review)), read_json(Path(args.release)), read_json(Path(args.core)))
            write_json(Path(args.out), out)
            print("SHARED-AUTHORITIES", out["mechanical_status"], "authority=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if out["mechanical_status"] == "FAIL" else 3
        if args.command == "shared-audit":
            baseline_path = Path(args.baseline) if args.baseline else Path(__file__).resolve().parents[2] / "docs" / "shared-baseline-pins.json"
            baseline = read_json(baseline_path)
            schema = Path(__file__).resolve().parents[2] / "schemas/v1/construction.schema.json"
            summary = audit_shared(Path(args.shared_root), baseline, archive=Path(args.archive) if args.archive else None, construction_schema=schema)
            write_json(Path(args.out), summary)
            print("SHARED-AUDIT mechanical=" + summary["mechanical_status"] + " integration=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if summary["mechanical_status"] == "FAIL" else 3
        if args.command == "smart-audit":
            summary = inspect_native_report(read_json(Path(args.report)))
            write_json(Path(args.out), summary)
            print("SMART-AUDIT native=" + summary["native_check_status"] + " integration=HOLD NOT_ACADEMIC_APPROVAL")
            return 3  # Independent owner/reviewer and Shared/QRT qualification never inferred.
        bundle, data, errors = inspect(args.bundle)
        report = make_report(bundle, data, errors)
        if args.command == "report":
            write_json(Path(args.json), report)
            target = Path(args.md)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(markdown(report), encoding="utf-8")
        else:
            write_json(Path(args.out), report)
        print(args.command.upper(), "structural=" + report["mechanical_status"], "academic=HOLD NOT_ACADEMIC_APPROVAL")
        if errors:
            return 1
        return 3 if args.command == "qualify" else 0
    except (InputError, OSError) as exc:
        print("INPUT_ERROR: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
