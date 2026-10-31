"""Local CLI. Exit: 0 successful command, 1 invalid, 2 IO, 3 qualification HOLD."""
import argparse
import sys
from pathlib import Path
from .errors import InputError
from .io import write_json
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
    args = parser.parse_args(argv)
    try:
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
