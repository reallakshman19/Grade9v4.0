import json
from grade9qa.validate import inspect

def _modify(root, name, fn):
    p = root / name
    obj = json.loads(p.read_text())
    fn(obj)
    p.write_text(json.dumps(obj))

def test_valid_candidate(candidate):
    bundle, data, errors = inspect(candidate / "bundle.json")
    assert not errors
    assert bundle["id"] == "BUNDLE-WEP01"
    assert len(data["constructions"]) == 1

def test_missing_signature_field(candidate):
    _modify(candidate, "constructions.json", lambda d: d[0]["signature"].pop("obstacle"))
    assert "SCHEMA_ERROR" in [e.code for e in inspect(candidate / "bundle.json")[2]]

def test_bad_schema_version(candidate):
    _modify(candidate, "bundle.json", lambda d: d.update(schema_version="4.0.0"))
    assert "SCHEMA_ERROR" in [e.code for e in inspect(candidate / "bundle.json")[2]]

def test_invalid_demand_band(candidate):
    _modify(candidate, "constructions.json", lambda d: d[0].update(band="D5"))
    assert "SCHEMA_ERROR" in [e.code for e in inspect(candidate / "bundle.json")[2]]
