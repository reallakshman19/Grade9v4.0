"""P0.1 structural checks only. Source-hash and academic gates remain HOLD."""
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from .errors import InputError
from .io import confined_path, read_json
from .models import Diagnostic
from .traceability import COLLECTIONS, check_references
from .demand import check_demand

SCHEMAS = Path(__file__).resolve().parents[2] / "schemas" / "v1"

def schema_errors(item, name, path):
    validator = Draft202012Validator(read_json(SCHEMAS / (name + ".schema.json")), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(item), key=lambda e: (str(list(e.absolute_path)), e.message))
    return [Diagnostic("SCHEMA_ERROR", path + "/" + "/".join(str(p) for p in e.absolute_path),
                       e.message, "Conform to schemas/v1.") for e in errors]

def inspect(bundle_file):
    bundle_file = Path(bundle_file)
    bundle = read_json(bundle_file)
    problems = schema_errors(bundle, "bundle", str(bundle_file))
    if problems:
        return bundle, {key: [] for key in COLLECTIONS}, problems
    data = {}
    for name in COLLECTIONS:
        relative = bundle["files"][name]
        try:
            records = read_json(confined_path(bundle_file.resolve().parent, relative))
        except InputError as exc:
            problems.append(Diagnostic("INPUT_ERROR", relative, str(exc), "Supply the referenced JSON file."))
            data[name] = []
            continue
        if not isinstance(records, list):
            problems.append(Diagnostic("SCHEMA_ERROR", relative, "Expected array.", "Use a JSON array."))
            records = []
        data[name] = records
        for index, record in enumerate(records):
            problems.extend(schema_errors(record, name[:-1] if name != "sources" else "source", f"{relative}[{index}]"))
    if not problems:
        problems.extend(check_references(data))
        problems.extend(check_demand(data))
    problems.sort(key=lambda x: (x.path, x.code, x.message))
    return bundle, data, problems
