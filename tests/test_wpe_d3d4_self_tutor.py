"""Static integrity and independent calculations for C01–C08 plus E01–E05 student practice.

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


def test_thirteen_source_grounded_guided_and_fresh_pairs():
    data = load(META)
    assert data["schema"] == "wpe-c01-c08-e01-e05-six-stage-self-tutor/v5"
    assert data["publication_role"] == "STUDENT_PRACTICE_PREVIEW_ONLY"
    assert data["academic"] == {
        "native_core1a": "NOT_ACCEPTED", "native_core1b": "NOT_ACCEPTED",
        "qrt": "NOT_RUN", "owner": "PENDING", "qualified_learner_routes": 0,
    }
    assert [row["id"] for row in data["lessons"]] == ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "E01", "E02", "E03", "E04", "E05"]
    html = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    assert 'href="d3d4-self-tutor.css"' in html
    assert 'src="d3d4-self-tutor.js"' in html
    assert 'href="d3d4-self-tutor.html"' in HUB.read_text(encoding="utf-8")
    assert html.count('class="stage-root"') == 13
    for row in data["lessons"]:
        source = ROOT / row["author_pack"]
        assert source.is_file()
        assert git_blob(source) == row["author_pack_blob_sha"], row["id"]
        assert row["revision"] == 1
        assert row["source_join_status"] == "PROPOSED_UNQUALIFIED"
        assert all(x.startswith(("EX-", "TB-", "WEP07-")) for x in row["proposed_source_themes"])
        assert f'id="{row["id"]}"' in html
        assert f'data-stage-root="{row["id"]}"' in html
    assert "starts from rest at the bottom" in html
    assert "not attached" in html
    assert "Thirteen thinking skills" in html
    assert "grade written reasoning" in html  # practice is not a mastery claim
    assert "source-question" in json.dumps(data).lower()
    batch=data["implementation_batch"]
    assert batch["new_topics"] == ["C07","C08"]
    assert batch["retained_topics"] == ["C01","C02","C03","C04","C05","C06"]
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
    assert len(meta["lessons"])==13
    assert meta["academic"]["qualified_learner_routes"]==0
    assert meta["first_attempt_policy"]["graded_reasoning"] is False
    assert meta["first_attempt_policy"]["independent_student_observation"] is False


def test_axis_first_c05_guide_and_three_fresh_graph_operations():
    # Guide: area under a horizontal F–x line, negative slope of U–x, and s–t slope.
    close(3*2, 6)
    close(-(3-9)/(2-0), 3)
    close((6-0)/(3-0), 2)
    # Fresh card R, a triangle from 0 N to +8 N across a 4 m displacement.
    work_r = 0.5*(4-0)*8
    close(work_r, 16)
    # Fresh card S, potential increases by 6 J across 2 m: force is negative slope.
    force_s = -(8-2)/(2-0)
    close(force_s, -3)
    # Fresh card T asks for interval 2 to 5 s, not average over the whole 0–5.
    velocity_t = (16-4)/(5-2)
    close(velocity_t, 4)
    assert velocity_t != (16-0)/(5-0)
    # Changed graph axis: F–time area gives impulse in N s, not work in J.
    impulse_ft = 0.5*(4)*8
    close(impulse_ft, 16)
    html=PAGE.read_text(encoding="utf-8")
    script=SCRIPT.read_text(encoding="utf-8")
    assert 'id="C05"' in html and 'data-stage-root="C05"' in html
    assert "0 N" in html and "16 m" in html
    assert "C05:" in script
    assert "impulse" in script.lower()
    assert "negative slope" in script.lower()


def test_vertical_circular_c06_energy_then_tension_and_boundary():
    g = 10
    # Guided top-speed known: 0.5 kg, r=2, v_top=6.
    mass_guide, r_guide, top_speed = 0.5, 2, 6
    t_top=mass_guide*top_speed**2/r_guide-mass_guide*g
    close(t_top, 4)
    v_bottom_squared=top_speed**2+4*g*r_guide
    close(v_bottom_squared, 116)
    close(mass_guide*v_bottom_squared/r_guide+mass_guide*g, 34)
    # Fresh: known bottom speed 7 m/s, r=1, m=1.
    mass, r, bottom_speed = 1, 1, 7
    v_top_squared=bottom_speed**2-4*g*r
    close(v_top_squared, 9)
    assert v_top_squared > 0  # enough mechanical energy to reach top HEIGHT
    theoretical_tension=mass*v_top_squared/r-mass*g
    close(theoretical_tension, -1)
    assert theoretical_tension < 0  # a taut string cannot push: assumption invalid
    # Changed bottom speed 8 m/s: tension becomes positive.
    v_top_boundary=8**2-4*g*r
    close(v_top_boundary, 24)
    close(mass*v_top_boundary/r-mass*g, 14)
    close(math.sqrt(5*g*r), math.sqrt(50))
    assert 7 < math.sqrt(50) < 8
    html=PAGE.read_text(encoding="utf-8")
    script=SCRIPT.read_text(encoding="utf-8")
    assert 'id="C06"' in html and 'data-stage-root="C06"' in html
    assert "radial" in html.lower()
    assert "string can pull" in html.lower()
    assert "C06:" in script
    assert "−1 N" in script and "+14 N" in script


def test_existing_four_local_storage_keys_not_versioned_away():
    data=load(META)
    script=SCRIPT.read_text(encoding="utf-8")
    assert [lesson["revision"] for lesson in data["lessons"]] == [1]*13
    assert "g9:wpe:d3d4:self-tutor:v1:" in script
    batch=data["implementation_batch"]
    assert batch["existing_storage_keys_preserved"] is True
    assert batch["real_student_usability_observed"] is False
    assert data["first_attempt_policy"]["secure_answer_secrecy"] is False
    assert data["academic"]["qualified_learner_routes"] == 0
    assert next(x for x in data["lessons"] if x["id"]=="C05")["original_source_graphs_verified"] is False
    assert len(next(x for x in data["lessons"] if x["id"]=="C06")["required_prerequisites"]) == 4


def test_conveyor_c07_steady_momentum_flow_and_heat_ledger():
    """Two separate mechanical rates must balance without equating them."""
    # Guided: 1 kg/s arrives at u=0, leaves with 2 m/s belt.
    m_dot, u, v = 1, 0, 2
    force=m_dot*(v-u)
    motor=force*v
    gain=0.5*m_dot*(v*v-u*u)
    heat=0.5*m_dot*(v-u)**2
    close(force, 2)
    close(motor, 4)
    close(gain, 2)
    close(heat, 2)
    close(motor, gain+heat)

    # Fresh: 4 m/s belt, 1 m/s rightward arrivals, flow rate is v/2.
    belt, incoming = 4, 1
    rate=belt/2
    F=rate*(belt-incoming)
    P=F*belt
    K_dot=0.5*rate*(belt*belt-incoming*incoming)
    Q_dot=0.5*rate*(belt-incoming)**2
    close(rate, 2)
    close(F, 6)
    close(P, 24)
    close(K_dot, 15)
    close(Q_dot, 9)
    close(P, K_dot+Q_dot)
    # Boundary: the feed rate, belt speed, and speed gap all change.
    belt=2
    rate=belt/2
    force=rate*(belt-incoming)
    motor=force*belt
    gain=0.5*rate*(belt*belt-incoming*incoming)
    heat=0.5*rate*(belt-incoming)**2
    for actual, expected in [(rate,1),(force,1),(motor,2),(gain,1.5),(heat,0.5)]:
        close(actual,expected)
    close(motor,gain+heat)
    html=PAGE.read_text(encoding="utf-8")
    script=SCRIPT.read_text(encoding="utf-8")
    assert 'id="C07"' in html and 'data-stage-root="C07"' in html
    assert "zero horizontal speed" in html
    assert "1 m/s" in html and "4 m/s" in html
    assert "C07:" in script
    assert "24 W" in script and "15 W" in script and "9 W" in script
    assert "0.5 W" in script


def test_spring_c08_fixed_compression_versus_final_force_reversal():
    """Compare both lab conditions with separately inferred stiffnesses."""
    # Guided: given spring constants, x=0.10 m or F_final=10 N.
    stiffness_guide=[100,200]
    for k, expected_x, expected_f in zip(stiffness_guide,[0.5,1],[0.5,0.25]):
        close(0.5*k*0.10**2,expected_x)
        close(10**2/(2*k),expected_f)

    # Fresh: measured forces 8 N/16 N at the same x=4 cm.
    measured_forces=[8,16]
    stiffness=[force/0.04 for force in measured_forces]
    close(stiffness[0],200)
    close(stiffness[1],400)
    fixed_x=[0.5*k*0.05**2 for k in stiffness]
    fixed_force_extensions=[12/k for k in stiffness]
    fixed_force=[12**2/(2*k) for k in stiffness]
    for actual,expected in zip(fixed_x,[0.25,0.5]):close(actual,expected)
    for actual,expected in zip(fixed_force_extensions,[0.06,0.03]):close(actual,expected)
    for actual,expected in zip(fixed_force,[0.36,0.18]):close(actual,expected)
    assert fixed_x[1]>fixed_x[0] and fixed_force[0]>fixed_force[1]

    # Doubling the final equilibrium force quadruples energy for each fixed k.
    doubled=[24**2/(2*k) for k in stiffness]
    close(doubled[0],1.44)
    close(doubled[1],0.72)
    for i in range(2):close(doubled[i]/fixed_force[i],4)
    html=PAGE.read_text(encoding="utf-8")
    script=SCRIPT.read_text(encoding="utf-8")
    assert 'id="C08"' in html and 'data-stage-root="C08"' in html
    assert "<caption>Measured final equilibrium force at 4 cm compression</caption>" in html
    assert "C08:" in script
    assert "0.36 J" in script and "0.18 J" in script
    assert "1.44 J" in script and "0.72 J" in script


def test_six_prior_local_saved_tries_keep_same_storage_keys():
    data=load(META)
    batch=data["implementation_batch"]
    assert batch["new_topics"]==["C07","C08"]
    assert batch["retained_topics"]==["C01","C02","C03","C04","C05","C06"]
    assert batch["existing_storage_keys_preserved"] is True
    assert batch["real_student_usability_observed"] is False
    assert batch["academic_admissions_changed"] is False
    assert data["academic"]["qualified_learner_routes"]==0
    script=SCRIPT.read_text(encoding="utf-8")
    assert 'return "g9:wpe:d3d4:self-tutor:v1:"+lesson;' in script
    assert 'Object.keys(lessons).length+" challenges completed"' in script
    assert "state.first=values;state.stage=2" in script
    c07=next(x for x in data["lessons"] if x["id"]=="C07")
    c08=next(x for x in data["lessons"] if x["id"]=="C08")
    assert c07["source_join_status"]==c08["source_join_status"]=="PROPOSED_UNQUALIFIED"
    assert c08["source_selection_reader_conflict_unresolved"] is True
    assert len(c07["required_prerequisites"])==4


def test_learner_readiness_supports_eight_lessons_and_no_real_observations():
    """Code review and physics contracts are not evidence of student mastery."""
    meta = load(META)
    batch = meta["learner_readiness_batch"]
    assert batch["real_student_sessions_conducted"] == 0
    assert batch["actual_child_observations"] is False
    assert batch["automated_browser_regression_only"] is True
    assert batch["academic_admissions_changed"] is False
    assert batch["first_attempt_key_changed"] is False
    assert batch["first_attempt_unlock_changed"] is False
    assert meta["academic"]["qualified_learner_routes"] == 0
    protocol = ROOT / batch["observational_protocol"]
    assert protocol.is_file()
    guide = protocol.read_text(encoding="utf-8")
    assert "observations NOT RUN" in guide
    assert "do not" in guide.lower()
    assert "Boundary" in guide
    script = SCRIPT.read_text(encoding="utf-8")
    for topic in [f"C0{i}" for i in range(5, 9)]:
        start = script.index("    "+topic+": {")
        end = script.find("\n    C0", start+8)
        if end == -1:
            end = script.index("\n  };\n\n  function initState",start)
        section = script[start:end]
        assert "hints: [" in section, topic
        assert "diagnosisFeedback: [" in section, topic
        assert "Which" in section or "which" in section

    assert "state.predictionDraft" in script
    assert "state.draft=formValues(root)" in script
    assert "state.first=values;state.stage=2;state.draft=null;" in script
    assert "g9:wpe:d3d4:self-tutor:v1:" in script
    assert 'el("details","review-model")' in script
    assert "stage===3 || stage===4" in script
    assert "saveUnfinishedInput" in script
    assert "innerHTML" not in script
    assert "real_student_sessions_conducted" not in script  # no invented learner telemetry



def test_e01_potential_well_connected_accessible_regions_and_crossing():
    """E01 must test connected reachability, not merely low U at each endpoint."""
    # Guide U=(x-2)^2, E=4 J, m=2 kg.
    for x,u in [(0,4),(1,1),(2,0),(3,1),(4,4)]:
        close((x-2)**2,u)
        assert 4-u>=0
    close(math.sqrt(2*(4-0)/2),2)
    # Fresh U=(q²-4)², E=9 J, two separated intervals.
    U=lambda q:(q*q-4)**2
    close(U(0),16)
    close(U(-2),0)
    close(U(2),0)
    assert U(0)>9 and U(1)==9
    assert math.sqrt(7)>2
    assert 1<=2<=math.sqrt(7)
    close(math.sqrt(2*(9-U(2))/2),3)
    # E=17 J has K=1 at the old barrier and v=1 m/s.
    assert 17>U(0)
    close(math.sqrt(2*(17-U(0))/2),1)
    html=PAGE.read_text(encoding="utf-8")
    js=SCRIPT.read_text(encoding="utf-8")
    assert 'id="E01"' in html and 'data-stage-root="E01"' in html
    assert "two allowed" in js.lower() or "two separate" in js.lower()
    assert "16 J" in js and "17 J" in js
    assert "3 m/s" in js


def test_e02_instantaneous_signed_power_not_magnitudes():
    # Guide 1D: v=3 right, F_pull=6 right, resistance=2 left.
    close(6*3,18)
    close(-2*3,-6)
    close((6-2)*3,12)
    # Fresh 2D signed dot product.
    vx,vy=3,4
    fm=(6,0)
    fr=(-2,-1)
    Pm=fm[0]*vx+fm[1]*vy
    Pr=fr[0]*vx+fr[1]*vy
    close(Pm,18)
    close(Pr,-10)
    close(Pm+Pr,8)
    assert (4*vx-1*vy)!=math.sqrt(17)*5
    # Boundary speed remains positive despite zero instantaneous power.
    close(4*1-1*4,0)
    assert math.sqrt(1**2+4**2)>0 and 4**2+(-1)**2>0
    html=PAGE.read_text(encoding="utf-8")
    js=SCRIPT.read_text(encoding="utf-8")
    assert 'id="E02"' in html and 'data-stage-root="E02"' in html
    assert "−10 W" in js and "+8 W" in js and "0 W" in js
    assert "instantaneous" in html.lower()


def test_e03_spring_contact_friction_then_horizontal_flight():
    # Guided spring puck and separate horizontal projectile.
    guide_energy=.5*100*.2**2
    close(guide_energy,2)
    close(math.sqrt(2*guide_energy/1),2)
    close(math.sqrt(2*1.25/10),.5)
    close(3*.5,1.5)
    # Fresh 0.5kg dart at 1.25m; friction acts only over 0.2m contact.
    start=.5*125*.2**2
    friction=2.5*.2
    launch=start-friction
    close(start,2.5)
    close(friction,.5)
    close(launch,2)
    speed=math.sqrt(2*launch/.5)
    close(speed,math.sqrt(8))
    time=math.sqrt(2*1.25/10)
    close(time,.5)
    close(speed*time,math.sqrt(2))
    # Boundary frictionless launch changes v and range, not vertical time.
    speed_new=math.sqrt(2*start/.5)
    close(speed_new,math.sqrt(10))
    close(speed_new*time,math.sqrt(10)/2)
    assert speed_new*time>speed*time
    js=SCRIPT.read_text(encoding="utf-8")
    assert 'data-stage-root="E03"' in PAGE.read_text(encoding="utf-8")
    assert "1.414" in js and "1.581" in js
    assert "natural length" in js


def test_e04_first_impact_differs_from_later_geometric_ratio():
    # Guided: 2m initial height, 25% height retention EVERY impact.
    guide_sum=(.25*2)/(1-.25)
    close(guide_sum,2/3)
    close(2+2*guide_sum,10/3)
    # Fresh: h1=75% of 2m, repeated later retention of 50%.
    h1=.75*2
    h2=.5*h1
    h3=.5*h2
    for actual, expected in [(h1,1.5),(h2,.75),(h3,.375)]:
        close(actual,expected)
    total=2+2*h1/(1-.5)
    close(total,8)
    close(math.sqrt(.75),math.sqrt(3)/2)
    # Boundary: 75% retained each impact, including later ones.
    close(2+2*h1/(1-.75),14)
    assert 14>8
    js=SCRIPT.read_text(encoding="utf-8")
    assert 'data-stage-root="E04"' in PAGE.read_text(encoding="utf-8")
    assert "0.375 m" in js and "8.00 m" in js and "14 m" in js


def test_e05_inward_force_area_vs_local_orbital_force():
    # Guide: inward constant 3N with reference U(0)=0.
    close(3*2,6)
    close(math.sqrt(3*2/1),math.sqrt(6))
    close(.5*1*6,3)
    close(6+3,9)
    # Fresh: piecewise force magnitude; positive U is radial area.
    first=4*2
    second=.5*(4+6)*1
    U3=first+second
    f3=6
    m,r=2,3
    v3=math.sqrt(f3*r/m)
    K3=.5*m*v3**2
    close(first,8)
    close(second,5)
    close(U3,13)
    close(v3,3)
    close(K3,9)
    close(U3+K3,22)
    # Boundary: separate circular orbit at 4m; this requires different E.
    U4=first+.5*(4+8)*2
    v4=math.sqrt(8*4/m)
    K4=.5*m*v4**2
    close(U4,20)
    close(v4,4)
    close(K4,16)
    close(U4+K4,36)
    assert U4+K4!=U3+K3
    js=SCRIPT.read_text(encoding="utf-8")
    assert 'data-stage-root="E05"' in PAGE.read_text(encoding="utf-8")
    assert "13 J" in js and "22 J" in js and "36 J" in js
    assert "perpendicular" in js.lower()


def test_extension_rollout_retains_old_storage_and_no_admissions():
    j=load(META)
    b=j["extension_rollout_batch"]
    assert b["new_topics"]==["E01","E02","E03","E04","E05"]
    assert b["retained_topics"]==["C01","C02","C03","C04","C05","C06","C07","C08"]
    assert b["original_eight_storage_keys_preserved"] is True
    assert b["native_qrt_admissions_changed"] is False
    assert b["final_qrt_adjudications"]==0
    assert b["original_exam_figure_or_key_verifications"]==0
    assert b["real_student_sessions_conducted"]==0
    assert j["academic"]["qualified_learner_routes"]==0
    assert all(row["source_join_status"]=="PROPOSED_UNQUALIFIED" for row in j["lessons"])
    assert len(j["lessons"])==13
    for e in j["lessons"][8:]:
        assert len(e["required_prerequisites"])>=4
        assert e["author_pack"].startswith("WPE_Source_to_Core1A_Concept/learning-bridge/")
        assert e["revision"]==1
    script=SCRIPT.read_text(encoding="utf-8")
    assert 'return "g9:wpe:d3d4:self-tutor:v1:"+lesson;' in script
    assert "state.first=values;state.stage=2;state.draft=null;" in script
    assert "state.boundary=answer" in script


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
