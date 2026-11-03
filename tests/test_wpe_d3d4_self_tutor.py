"""Static integrity and independent calculations for the C01/C02 practice preview.

This is software QA, not a learner performance score or academic admission.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "physics/wpe/d3d4-self-tutor.html"
SCRIPT = ROOT / "physics/wpe/d3d4-self-tutor.js"
STYLE = ROOT / "physics/wpe/d3d4-self-tutor.css"
META = ROOT / "physics/wpe/d3d4-self-tutor.review.json"
HUB = ROOT / "physics/wpe/index.html"
CURRENT_MAP = ROOT / "physics/wpe/learn-challenge-source-map.json"
BASE = ROOT / "WPE_Source_to_Core1A_Concept/learning-bridge"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-11), (a, b)


def test_two_source_grounded_guided_and_fresh_pairs():
    data = load(META)
    assert data["schema"] == "wpe-c01-c02-six-stage-self-tutor/v1"
    assert data["publication_role"] == "STUDENT_PRACTICE_PREVIEW_ONLY"
    assert data["academic"] == {
        "native_core1a": "NOT_ACCEPTED", "native_core1b": "NOT_ACCEPTED",
        "qrt": "NOT_RUN", "owner": "PENDING", "qualified_learner_routes": 0,
    }
    assert [row["id"] for row in data["lessons"]] == ["C01", "C02"]
    html = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    assert 'href="d3d4-self-tutor.css"' in html
    assert 'src="d3d4-self-tutor.js"' in html
    assert 'href="d3d4-self-tutor.html"' in HUB.read_text(encoding="utf-8")
    assert html.count('class="stage-root"') == 2
    for row in data["lessons"]:
        source = ROOT / row["author_pack"]
        assert source.is_file()
        assert git_blob(source) == row["author_pack_blob_sha"], row["id"]
        assert row["revision"] == 1
        assert row["source_join_status"] == "PROPOSED_UNQUALIFIED"
        assert all(x.startswith(("EX-", "TB-")) for x in row["proposed_source_themes"])
        assert f'id="{row["id"]}"' in html
        assert f'data-stage-root="{row["id"]}"' in html
    assert "starts from rest at the bottom" in html
    assert "not attached" in html
    assert "Six thinking" not in html  # no inflated master-level claims
    assert "source-question" in json.dumps(data).lower()


def test_six_distinct_phases_and_first_attempt_separation():
    meta = load(META)
    assert meta["six_stage_contract"] == [
        "PREDICT", "ATTEMPT", "RECONSTRUCT", "DIAGNOSE", "REPAIR", "BOUNDARY_TEST",
    ]
    p = meta["first_attempt_policy"]
    assert p["recorded_first_model"] == "browser_local_storage"
    assert p["immutable_after_commit_until_explicit_reset"] is True
    assert p["separate_repair_record"] is True
    assert p["answer_revealed_in_dom_only_after_first_attempt"] is True
    assert p["secure_answer_secrecy"] is False
    assert p["graded_reasoning"] is False
    assert p["independent_student_observation"] is False
    script = SCRIPT.read_text(encoding="utf-8")
    assert script.count('if(!values.reason)') == 1
    assert "state.first=values;state.stage=2" in script
    assert "state.repair=repaired;state.stage=5" in script
    assert "state.boundary=answer" in script
    assert "value.first &&" in script
    assert "window.confirm" in script
    assert "localStorage.setItem" in script and "localStorage.removeItem" in script
    assert "innerHTML" not in script  # user text can never become executable markup
    assert "state.boundary===null" in script
    assert "workedList(card,config.worked" in script


def test_work_ledger_guided_and_fresh_expected_answer():
    guide_pull = 10*3
    guide_friction = -4*3
    guide_gravity = guide_normal = 0
    delta_k = sum((guide_pull, guide_friction, guide_gravity, guide_normal))
    close(delta_k, 18)
    initial_k = 0.5*2*1**2
    close(initial_k, 1)
    close(math.sqrt(2*(initial_k+delta_k)/2), math.sqrt(19))

    motor, friction, gravity, normal = 15*2, -3*2, -(3*10*.5), 0
    net = sum((motor, friction, gravity, normal))
    close(net, 9)
    close(math.sqrt(2*net/3), math.sqrt(6))
    lower_motor_net = 10*2 + friction + gravity
    close(lower_motor_net, -1)
    assert lower_motor_net < 0  # from rest, full ramp would require negative K
    assert 10 < (3*10*.5/2 + 3)  # uphill motor < gravity component + friction


def test_spring_contact_and_rough_strip_expected_answer():
    guide_energy = .5*100*(.20**2)
    close(guide_energy, 2)
    close(math.sqrt(2*guide_energy/1), 2)
    spring_energy = .5*200*(.10**2)
    release_speed = math.sqrt(2*spring_energy/2)
    friction_work = -1*.50
    final_k = spring_energy+friction_work
    close(spring_energy, 1)
    close(release_speed, 1)
    close(friction_work, -.5)
    close(final_k, .5)
    close(math.sqrt(2*final_k/2), math.sqrt(.5))
    boundary_k = spring_energy-1*1.00
    close(boundary_k, 0)
    close(boundary_k, 0)


def test_no_upgrade_to_native_status_or_exam_original_delivery():
    meta = load(META)
    source_map = load(CURRENT_MAP)
    assert source_map["auth"]["native_core1a"] == "NOT_ACCEPTED"
    assert source_map["auth"]["native_core1b"] == "NOT_ACCEPTED"
    assert source_map["auth"]["qrt"] == "NOT_RUN"
    assert source_map["auth"]["owner"] == "PENDING"
    assert all(row["source_join_status"] == "PROPOSED_UNQUALIFIED" for row in meta["lessons"])
    html = PAGE.read_text(encoding="utf-8")
    assert "These are newly authored" in html
    assert "does not" in html and "securely hide" in html
