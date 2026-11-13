import json
from grade9qa.validate import inspect

def test_mismatched_band(candidate):
    p=candidate/"constructions.json"
    content=json.loads(p.read_text())
    content[0]["demand_scores"]["conceptual"]=0
    p.write_text(json.dumps(content))
    assert "BAND_MISMATCH" in [x.code for x in inspect(candidate/"bundle.json")[2]]

def test_empty_demand_evidence(candidate):
    p=candidate/"constructions.json"
    content=json.loads(p.read_text())
    content[0]["demand_evidence"]["conceptual"]=""
    p.write_text(json.dumps(content))
    assert "SCHEMA_ERROR" in [x.code for x in inspect(candidate/"bundle.json")[2]]
