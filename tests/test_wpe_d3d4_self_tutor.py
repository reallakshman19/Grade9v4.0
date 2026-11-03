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
    assert data["schema"] == "wpe-c01-c04-six-stage-self-tutor/v2"
    assert data["publication_role"] == "STUDENT_PRACTICE_PREVIEW_ONLY"
    assert data["academic"] == {
        "native_core1a": "NOT_ACCEPTED", "native_core1b": "NOT_ACCEPTED",
        "qrt": "NOT_RUN", "owner": "PENDING", "qualified_learner_routes": 0,
    }
    assert [row["id"] for row in data["lessons"]] == ["C01", "C02", "C03", "C04"]
    html = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    assert 'href="d3d4-self-tutor.css"' in html
    assert 'src="d3d4-self-tutor.js"' in html
    assert 'href="d3d4-self-tutor.html"' in HUB.read_text(encoding="utf-8")
    assert html.count('class="stage-root"') == 4
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
    assert "Four thinking skills" in html
    assert "source-question" in json.dumps(data).lower()
    batch=data["implementation_batch"]
    assert batch["new_topics"] == ["C03","C04"]
    assert batch["retained_topics"] == ["C01","C02"]
    assert batch["real_student_usability_observed"] is False
    assert batch["software_browser_simulations_only"] is True
    assert batch["academic_admissions_changed"] is False


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



def test_constant_power_c03_guided_and_fresh_with_graph_operations():
    # C03 guide: 2 kg sled already at 2 m/s, 12 W useful motor power.
    initial=0.5*2*2**2
    close(initial,4)
    for elapsed,expected_k,expected_v in [(1,16,4),(4,52,math.sqrt(52))]:
        k=initial+12*elapsed
        close(k,expected_k)
        close(math.sqrt(2*k/2),expected_v)
    # Fresh trolley: 3 kg, 2 m/s initial, 18 W, 2 s and 6 s.
    fresh_initial=0.5*3*2**2
    close(fresh_initial,6)
    for elapsed,expected_k,expected_v in [(2,42,math.sqrt(28)),(6,114,math.sqrt(76))]:
        k=fresh_initial+18*elapsed
        close(k,expected_k)
        close(math.sqrt(2*k/3),expected_v)
    boundary_k=fresh_initial+9*2
    close(boundary_k,24)
    close(math.sqrt(2*boundary_k/3),4)
    # Constant power gives linear K(t), increasing concave-down v(t).
    v0=2
    v2=math.sqrt(28)
    v6=math.sqrt(76)
    assert (v2-v0)/2 > (v6-v2)/4
    html=PAGE.read_text(encoding="utf-8")
    script=SCRIPT.read_text(encoding="utf-8")
    assert "C03" in html and "C03:" in script
    assert "displacement–time" in html
    assert "calculus" in html.lower()


def test_distributed_mass_c04_two_hanging_states_and_full_lift():
    # C04 guide: only 2 m of a 4 m, 2 kg chain hangs.
    lambd=2/4
    initial_mass=lambd*2
    close(initial_mass,1)
    close(initial_mass*10*(2/2),10)
    # Fresh: uniform 8 m, 4 kg, hanging length falls 4 m -> 2 m.
    mass_per_m=4/8
    def potential(hanging_length):
        hanging_mass=mass_per_m*hanging_length
        middle_depth=hanging_length/2
        return -hanging_mass*10*middle_depth
    close(potential(4),-40)
    close(potential(2),-10)
    close(potential(2)-potential(4),30)
    close(potential(0)-potential(4),40)
    assert potential(2) < 0 < 40
    html=PAGE.read_text(encoding="utf-8")
    script=SCRIPT.read_text(encoding="utf-8")
    assert "C04" in html and "C04:" in script
    assert "middle of the hanging piece" in html.lower()
    assert "endMass" in script and "endDepth" in script


def test_all_four_preserve_existing_local_attempt_keys_and_ungraded_status():
    script=SCRIPT.read_text(encoding="utf-8")
    meta=load(META)
    assert 'return "g9:wpe:d3d4:self-tutor:v1:"+lesson;' in script
    assert 'Object.keys(lessons).length+" challenges completed"' in script
    assert len(meta["lessons"])==4
    assert meta["academic"]["qualified_learner_routes"]==0
    assert meta["first_attempt_policy"]["graded_reasoning"] is False
    assert meta["first_attempt_policy"]["independent_student_observation"] is False

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
