"""Qualify must make B1–B7 violations noncompensatory without self-approval."""
import json
from pathlib import Path

from grade9qa.cli import main

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/wpe-b1b7-candidate/witness.json"


def wpe_bundle_match(candidate, tmp_path):
    c = candidate / "constructions.json"
    values = json.loads(c.read_text())
    values[0]["id"] = "WPE-C-SYNTH-01"
    c.write_text(json.dumps(values))
    # Update the single Core1A and exam references to the renamed construction.
    for filename in ("lessons.json", "assessments.json"):
        p = candidate / filename
        rows = json.loads(p.read_text())
        rows[0]["construction_id"] = "WPE-C-SYNTH-01"
        p.write_text(json.dumps(rows))
    witness = tmp_path / "witness.json"
    witness.write_text(EXAMPLE.read_text())
    return witness


def test_valid_witness_still_qualification_hold(candidate, tmp_path):
    witness = wpe_bundle_match(candidate, tmp_path)
    output = tmp_path / "qualify.json"
    rc = main(["qualify","--bundle",str(candidate / "bundle.json"),
               "--witness",str(witness),"--out",str(output)])
    assert rc == 3
    report = json.loads(output.read_text())
    assert report["qualification_status"] == "HOLD"
    assert len(report["bridge_results"]) == 7
    assert report["coverage"]["qualified_constructions"] == 0


def test_known_physics_contradiction_forces_qualify_four(candidate, tmp_path):
    witness = wpe_bundle_match(candidate, tmp_path)
    obj = json.loads(witness.read_text())
    obj["source_and_physics"]["known_physics_contradiction"] = True
    witness.write_text(json.dumps(obj))
    output = tmp_path / "qualify.json"
    rc = main(["qualify","--bundle",str(candidate / "bundle.json"),
               "--witness",str(witness),"--out",str(output)])
    assert rc == 4
    assert json.loads(output.read_text())["qualification_status"] == "FAIL"


def test_misbound_witness_never_qualifies(candidate, tmp_path):
    witness = tmp_path / "witness.json"
    witness.write_text(EXAMPLE.read_text())
    output = tmp_path / "qualify.json"
    assert main(["qualify","--bundle",str(candidate / "bundle.json"),
                 "--witness",str(witness),"--out",str(output)]) == 4
    assert any(x["code"] == "WITNESS_CONSTRUCTION_NOT_IN_BUNDLE"
               for x in json.loads(output.read_text())["diagnostics"])


def test_invalid_witness_contract_is_input_error(candidate, tmp_path):
    witness = wpe_bundle_match(candidate, tmp_path)
    obj = json.loads(witness.read_text())
    obj["status"] = "APPROVED"
    witness.write_text(json.dumps(obj))
    output = tmp_path / "qualify.json"
    assert main(["qualify","--bundle",str(candidate / "bundle.json"),
                 "--witness",str(witness),"--out",str(output)]) == 1
    assert json.loads(output.read_text())["mechanical_status"] == "FAIL"
