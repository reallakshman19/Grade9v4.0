import json
from grade9qa.cli import main

def test_validate_not_academic_approval(candidate,tmp_path):
    output=tmp_path/"out.json"
    assert main(["validate","--bundle",str(candidate/"bundle.json"),"--out",str(output)])==0
    result=json.loads(output.read_text())
    assert result["mechanical_status"]=="PASS"
    assert result["qualification_status"]=="HOLD"
    assert result["coverage"]["qualified_constructions"]==0

def test_qualify_holds(candidate,tmp_path):
    output=tmp_path/"out.json"
    assert main(["qualify","--bundle",str(candidate/"bundle.json"),"--out",str(output)])==3
    assert json.loads(output.read_text())["gate_results"][0]["result"]=="HOLD"

def test_report(candidate,tmp_path):
    j,m=tmp_path/"report.json",tmp_path/"report.md"
    assert main(["report","--bundle",str(candidate/"bundle.json"),"--json",str(j),"--md",str(m)])==0
    assert "NOT_ACADEMIC_APPROVAL" in m.read_text()

def test_missing_input(tmp_path):
    assert main(["validate","--bundle",str(tmp_path/"not-found.json"),"--out",str(tmp_path/"out.json")])==2
