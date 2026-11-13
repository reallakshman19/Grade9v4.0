"""CLI shared by the two self-contained candidate skills."""
import argparse
import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path

from qrt_contract import Checker, GATES, Invalid, VERSION, file_digest, gate_passed, read_json


def legacy(stage, overlay, library=None, vocab=None, sl1=None, attempts=None):
    path = Path(__file__).with_name(f"legacy_check_sl{stage}.py")
    spec = importlib.util.spec_from_file_location(f"sl_legacy_{stage}", path)
    module = importlib.util.module_from_spec(spec)
    old_argv = sys.argv
    output = io.StringIO()
    try:
        spec.loader.exec_module(module)
        # v2 preserves UNKNOWN exposure. No other legacy rule is weakened.
        if stage == 2:
            module.ENUMS["help"].add("UNKNOWN")
        sys.argv = [str(path), str(overlay), "--vocab", str(vocab)]
        if stage == 1:
            sys.argv += ["--library", str(library)]
        else:
            sys.argv += ["--sl1", str(sl1)]
            if attempts:
                sys.argv += ["--attempts", str(attempts)]
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = module.main()
        return {"stage": stage, "script": str(path), "script_sha256": file_digest(path),
                "compatibility_extension": "UNKNOWN help enum only" if stage == 2 else None,
                "exit_code": code, "output": output.getvalue().splitlines()}
    except (Exception, SystemExit) as exc:
        return {"stage": stage, "exit_code": 1, "output": [f"LEGACY_CHECK_ERROR: {type(exc).__name__}: {exc}"]}
    finally:
        sys.argv = old_argv


def main(stage):
    parser = argparse.ArgumentParser(description="Candidate SL checks; zero exit qualifies only the selected deterministic gate")
    parser.add_argument("overlay", nargs="?")
    parser.add_argument("--library")
    parser.add_argument("--sl1")
    parser.add_argument("--vocab")
    parser.add_argument("--attempts")
    parser.add_argument("--binding", nargs=2, metavar=("SL1", "QUESTION_ID"))
    parser.add_argument("--contract")
    parser.add_argument("--gate", choices=GATES, default="integrity")
    parser.add_argument("--review-registry")
    parser.add_argument("--registry-sha256")
    parser.add_argument("--allow-partial-practice", action="store_true")
    parser.add_argument("--legacy-only", action="store_true")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    if args.binding:
        if stage != 2 or args.overlay or args.contract:
            parser.error("--binding is an SL2 migration helper, separate from validation")
        try:
            rows = read_json(args.binding[0])["records"]
            matches = [r for r in rows if r.get("question_id") == args.binding[1]]
            if len(matches) != 1:
                raise Invalid("AMBIGUOUS_QUESTION", args.binding[1])
            spec = importlib.util.spec_from_file_location("binding_legacy", Path(__file__).with_name("legacy_check_sl2.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(json.dumps(module.binding_for(matches[0]), indent=2))
            return 0
        except (Invalid, KeyError, TypeError) as exc:
            print(json.dumps({"status": "HOLD", "error": str(exc)}))
            return 1
    if not args.overlay or not args.vocab or (stage == 1 and not args.library) or (stage == 2 and not args.sl1):
        parser.error("overlay and --vocab plus --library (SL1) or --sl1 (SL2) are required")
    if args.legacy_only:
        if args.contract:
            parser.error("--legacy-only cannot be combined with --contract")
        result = legacy(stage, args.overlay, args.library, args.vocab, args.sl1, args.attempts)
        print(json.dumps({"mode": "LEGACY_STRUCTURE_ONLY", "qualification": "NOT_RUN", "legacy_check": result}, indent=2))
        return result["exit_code"]
    if not args.contract:
        print(json.dumps({"schema": "smart-labelling-check-report/v2", "checker_version": VERSION,
                          "status": "HOLD", "issues": [{"code": "CONTRACT_REQUIRED", "detail": "Use a v2 contract, or explicit --legacy-only for migration inspection"}]}, indent=2))
        return 1
    checker = Checker(args.contract, args.review_registry, args.registry_sha256)
    report = checker.check(args.allow_partial_practice)
    report["cli_artifact"] = {"path": str(Path(__file__).resolve()), "sha256": file_digest(__file__)}
    try:
        if not checker.inputs:
            raise Invalid("INPUTS_NOT_RESOLVED", "Contract inputs were not loaded")
        refs = checker.contract["inputs"]
        expected = "sl1" if stage == 1 else "sl2"
        if Path(args.overlay).resolve() != checker.resolve(refs[expected]["path"]):
            raise Invalid("CLI_INPUT_MISMATCH", "Overlay differs from the contract input")
        if Path(args.vocab).resolve() != checker.resolve(refs["vocabulary"]["path"]):
            raise Invalid("CLI_INPUT_MISMATCH", "Vocabulary differs from the contract input")
        if stage == 1 and Path(args.library).resolve() != checker.resolve(refs["library"]["path"]):
            raise Invalid("CLI_INPUT_MISMATCH", "Library differs from the contract input")
        if stage == 2 and Path(args.sl1).resolve() != checker.resolve(refs["sl1"]["path"]):
            raise Invalid("CLI_INPUT_MISMATCH", "SL1 differs from the contract input")
        if args.attempts:
            for entry in checker.contract["records"]:
                observation = entry.get("observation")
                if observation and checker.resolve(observation["attempts_ref"]["path"]) != Path(args.attempts).resolve():
                    raise Invalid("CLI_INPUT_MISMATCH", "Attempt file differs from the contract")
        checks = [legacy(1, checker.resolve(refs["sl1"]["path"]), checker.resolve(refs["library"]["path"]), args.vocab)]
        if "sl2" in refs:
            checks.append(legacy(2, checker.resolve(refs["sl2"]["path"]), vocab=args.vocab,
                                 sl1=checker.resolve(refs["sl1"]["path"]), attempts=args.attempts))
        report["legacy_checks"] = checks
        if any(check["exit_code"] != 0 for check in checks):
            raise Invalid("LEGACY_RULES_FAILED", "See legacy_checks for the preserved content/record rules")
    except (Invalid, KeyError, TypeError) as exc:
        report["issues"].append({"code": getattr(exc, "code", "INVALID_CONTRACT_SHAPE"), "detail": str(exc)})
    if report["issues"]:
        report["gate_summary"] = {gate: "HOLD" for gate in GATES}
    passed = gate_passed(report, args.gate)
    report.update(selected_gate=args.gate, selected_gate_status=report["gate_summary"][args.gate],
                  exit_meaning="Only the selected deterministic gate; no automatic academic or release acceptance",
                  status="SELECTED_GATE_PASSED" if passed else "HOLD")
    if report["issues"]:
        report["selected_gate_status"] = "HOLD"
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json_output:
        destination = Path(args.json_output).resolve()
        code_files = {str(p.resolve()) for p in Path(__file__).parent.glob("*.py")}
        if str(destination) in checker.artifacts or str(destination) in code_files:
            parser.error("A report must not overwrite any input/evidence artifact")
        destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if passed else 1
