import json
from grade9qa.validate import inspect

def mutate(root, filename, fn):
    path = root / filename
    data = json.loads(path.read_text())
    fn(data)
    path.write_text(json.dumps(data))

def codes(root):
    return [item.code for item in inspect(root / "bundle.json")[2]]

def test_missing_warrant_reference(candidate):
    mutate(candidate,"constructions.json",lambda d:d[0]["warrant_ids"].append("WARR-MISSING"))
    assert "INVALID_REFERENCE" in codes(candidate)

def test_duplicate_id(candidate):
    mutate(candidate,"warrants.json",lambda d:d[0].update(id="SOURCE-N01"))
    assert "DUPLICATE_ID" in codes(candidate)

def test_cyclic_prerequisite(candidate):
    mutate(candidate,"constructions.json",lambda d:d[0]["prerequisite_ids"].append("WEP-C01"))
    assert "PREREQUISITE_CYCLE" in codes(candidate)

def test_traversal(candidate):
    mutate(candidate,"bundle.json",lambda d:d["files"].update(sources="../secret.json"))
    assert "SCHEMA_ERROR" in codes(candidate)
