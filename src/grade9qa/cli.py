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
from .qrt_binding import inspect_binding, fingerprints
from .bridge_witness import inspect_witness
from .bridge_legacy import inspect_legacy_witness
from .subjects import audit_subject_intake
from .migrate_v1 import preview_v1_to_v2, _load_strict
from .shared_dispatch import inspect_shared_dispatch
from .validate import inspect, schema_errors
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
        if name == "qualify":
            command.add_argument("--witness", help="Optional B1-B7 bridge witness, fail-closed and independently reviewed later")
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
    bind = subs.add_parser("qrt-bind", help="Read-only native Smart R2 → QRT Physics/WPE candidate binding.")
    for option in ("sl1", "sl2", "contract", "blueprint", "adapter"):
        bind.add_argument("--" + option, required=True, help="Local exact upstream " + option + " JSON")
    bind.add_argument("--handoff", help="Optional source-to-Core1A original handoff JSON")
    bind.add_argument("--native-sl1-report", help="Optional native SL1 checker report JSON")
    bind.add_argument("--native-sl2-report", help="Optional native SL2 checker report JSON")
    bind.add_argument("--out", required=True, help="JSON output, no source question text copied")
    bridge_witness = subs.add_parser("bridge-witness", help="B1-B7 teaching/reconstruction evidence audit; no academic self-approval.")
    bridge_witness.add_argument("--witness", required=True, help="Local v1 candidate witness JSON")
    bridge_witness.add_argument("--out", required=True, help="B1-B7 evidence summary JSON output")
    legacy = subs.add_parser("bridge-legacy", help="Sanitized readback of native WPE D3 candidate B1-B7 records.")
    legacy.add_argument("--witness", required=True, help="Original local WPE D3 candidate witness JSON")
    legacy.add_argument("--out", required=True, help="Source status readback without stem/question text")
    subjects = subs.add_parser("subjects-audit", help="Read-only v2 three-subject intake, not academic approval.")
    subjects.add_argument("--manifest", required=True, help="Version 2.0.0 candidate subject intake JSON")
    subjects.add_argument("--out", required=True, help="Candidate validation report, always academic HOLD")
    migration = subs.add_parser("migrate-v1-preview", help="Read-only WEP-01 v1→v2 reference-map preview, never promotes.")
    migration.add_argument("--bundle", required=True, help="Existing original WEP-01 v1 bundle.json")
    migration.add_argument("--manifest", required=True, help="Three-subject v2 candidate intake JSON")
    migration.add_argument("--out", required=True, help="Output preview and full integrity mapping report")
    migration.add_argument("--candidate-out", help="Optional separate candidate v2 manifest output (only if source integrity permits)")
    dispatch = subs.add_parser("shared-dispatch-audit", help="Reconcile explicit subject dirs with native Shared check_subjects report.")
    dispatch.add_argument("--manifest", required=True, help="Three-subject v2 candidate intake JSON")
    dispatch.add_argument("--native-report", required=True, help="Original Shared/tools/check_subjects.py JSON output")
    dispatch.add_argument("--bindings", required=True, help="Explicit subject_id→native directory JSON map")
    dispatch.add_argument("--out", required=True, help="No academic authority asserted")
    args = parser.parse_args(argv)
    try:
        if args.command == "migrate-v1-preview":
            original_root = Path(args.bundle).resolve().parent
            manifest_in = Path(args.manifest).resolve()
            report_out = Path(args.out).resolve()
            preview_out = Path(args.candidate_out).resolve() if args.candidate_out else None
            for output in (report_out, preview_out):
                if output is not None and (output.is_relative_to(original_root) or output == manifest_in):
                    raise InputError("OUTPUT_WOULD_OVERWRITE_HISTORIC_V1_OR_V2_INPUT")
            if preview_out is not None and preview_out == report_out:
                raise InputError("PREVIEW_AND_REPORT_OUTPUTS_MUST_BE_DISTINCT")
            result = preview_v1_to_v2(Path(args.bundle), Path(args.manifest))
            # Preview is portable only after original bundle/source bytes were checked.
            write_json(report_out, result)
            if preview_out is not None and result["candidate_manifest"] is not None:
                write_json(preview_out, result["candidate_manifest"])
            print("V1-MIGRATION-PREVIEW mechanical=" + result["mechanical_status"] +
                  " SharedAdmission=NOT_PERFORMED academic=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if result["mechanical_status"] == "FAIL" else 3
        if args.command == "shared-dispatch-audit":
            output = Path(args.out).resolve()
            originals = {Path(args.manifest).resolve(), Path(args.native_report).resolve(),
                         Path(args.bindings).resolve()}
            if output in originals:
                raise InputError("OUTPUT_WOULD_OVERWRITE_NATIVE_INPUT")
            report = inspect_shared_dispatch(
                _load_strict(Path(args.manifest)),
                _load_strict(Path(args.native_report)),
                _load_strict(Path(args.bindings)),
            )
            write_json(output, report)
            print("SHARED-DISPATCH mechanical=" + report["mechanical_status"] +
                  " canonicalAdmission=NOT_PERFORMED academic=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if report["mechanical_status"] == "FAIL" else 3
        if args.command == "subjects-audit":
            report = audit_subject_intake(read_json(Path(args.manifest)))
            write_json(Path(args.out), report)
            print("SUBJECTS-AUDIT mechanical=" + report["mechanical_status"] +
                  " academic=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if report["mechanical_status"] == "FAIL" else 3
        if args.command == "bridge-legacy":
            summary = inspect_legacy_witness(read_json(Path(args.witness)))
            write_json(Path(args.out), summary)
            print("BRIDGE-LEGACY status=" + summary["mechanical_status"] +
                  " qualification=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if summary["mechanical_status"] == "FAIL" else 3
        if args.command == "bridge-witness":
            data = read_json(Path(args.witness))
            report = inspect_witness(data)
            schema_findings = schema_errors(data, "bridge-witness", str(args.witness))
            if schema_findings:
                report["mechanical_status"] = "FAIL"
                report["diagnostics"].extend(
                    {"gate": "CONTRACT", "code": item.code, "severity": "FAIL",
                     "detail": item.message, "path": item.path} for item in schema_findings
                )
                report["diagnostics"].sort(key=lambda row: (row["gate"], row["code"], row["detail"]))
            write_json(Path(args.out), report)
            print("BRIDGE-WITNESS mechanical=" + report["mechanical_status"] +
                  " qualification=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if report["mechanical_status"] == "FAIL" else 3
        if args.command == "qrt-bind":
            sources = {key: Path(getattr(args, key)) for key in ("sl1", "sl2", "contract", "blueprint", "adapter")}
            if args.handoff:
                sources["handoff"] = Path(args.handoff)
            if args.native_sl1_report:
                sources["native_sl1"] = Path(args.native_sl1_report)
            if args.native_sl2_report:
                sources["native_sl2"] = Path(args.native_sl2_report)
            evidence = {key: read_json(path) for key, path in sources.items()}
            output = inspect_binding(evidence["sl1"], evidence["sl2"], evidence["contract"],
                                     evidence["blueprint"], evidence["adapter"],
                                     handoff=evidence.get("handoff"),
                                     native_sl1=evidence.get("native_sl1"),
                                     native_sl2=evidence.get("native_sl2"),
                                     input_fingerprints=fingerprints(sources))
            write_json(Path(args.out), output)
            print("QRT-BIND mechanical=" + output["mechanical_status"] +
                  " integration=HOLD NOT_ACADEMIC_APPROVAL")
            return 1 if output["mechanical_status"] == "FAIL" else 3
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
            if args.command == "qualify" and args.witness and not errors:
                evidence = read_json(Path(args.witness))
                shape = schema_errors(evidence, "bridge-witness", str(args.witness))
                if shape:
                    report["mechanical_status"] = "FAIL"
                    report["diagnostics"].extend(
                        {"code":d.code, "severity":"ERROR", "object_id":"",
                         "path":d.path, "message":d.message,
                         "remediation":"Correct the v1 bridge-witness JSON shape."} for d in shape
                    )
                    write_json(Path(args.out), report)
                    print("QUALIFY structural=FAIL (invalid bridge contract) NOT_ACADEMIC_APPROVAL")
                    return 1
                bridge = inspect_witness(evidence)
                expected = {c["id"] for c in data.get("constructions", [])}
                if bridge["construction_id"] not in expected:
                    report["qualification_status"] = "FAIL"
                    report["diagnostics"].append({
                        "code":"WITNESS_CONSTRUCTION_NOT_IN_BUNDLE",
                        "severity":"ERROR","object_id":bridge["construction_id"],
                        "path":"bridge_witness.construction.construction_id",
                        "message":"Witness refers to a different bound construction.",
                        "remediation":"Provide the correctly scoped witness for this bundle."
                    })
                elif bridge["mechanical_status"] == "FAIL":
                    report["qualification_status"] = "FAIL"
                report["bridge_results"] = bridge["gate_results"]
                report["diagnostics"].extend({
                    "code":d["code"], "severity":d["severity"],
                    "object_id":bridge["construction_id"], "path":d["gate"],
                    "message":d["detail"],"remediation":"Resolve and independently review this gate."
                } for d in bridge["diagnostics"])
                report["coverage"]["qualified_constructions"] = 0
            write_json(Path(args.out), report)
        print(args.command.upper(), "structural=" + report["mechanical_status"],
              "academic=" + report["qualification_status"] + " NOT_ACADEMIC_APPROVAL")
        if errors:
            return 1
        if args.command == "qualify":
            return 4 if report["qualification_status"] == "FAIL" else 3
        return 0
    except (InputError, OSError, ValueError, UnicodeError) as exc:
        print("INPUT_ERROR: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
