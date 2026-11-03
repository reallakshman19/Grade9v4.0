"""New authored practice for three previously unmapped reader-D3 source themes.

This tests authored Physics arithmetic, storage and provenance contracts ONLY.
It does not authenticate source/key, validate SL2, run independent QRT, or grade
an actual learner's thinking.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WPE=ROOT/"physics"/"wpe"
PACKS=ROOT/"WPE_Source_to_Core1A_Concept"/"learning-bridge"
ROUTES=WPE/"reasoning-paths.review.json"
REGISTER=ROOT/"architecture"/"qrt-blueprint-protocol"/"wpe-coverage-register.json"
SOURCES={
    "E06":("EX-M97","VERTICAL_PUSH_POWER_LEARNING_PACK.md"),
    "E07":("EX-N39","INCLINE_ROUND_TRIP_FRICTION_LEARNING_PACK.md"),
    "E08":("WEP07-01","SWITCHED_SPRING_FORCE_LEARNING_PACK.md"),
}

def data(path):
    return json.loads(path.read_text(encoding="utf-8"))

def close(a,b):
    assert math.isclose(a,b,abs_tol=1e-10,rel_tol=1e-10),(a,b)

def git_blob(path):
    x=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(x)).encode()+b"\0"+x).hexdigest()

def test_three_separate_author_packs_and_source_routes_are_not_admissions():
    bank={q["source_id"]:q for q in data(ROOT/"workspace"/"output"/"WPE_Core2_Consolidated_20261102"/"native-candidate"/"selected_bank.review.json")["questions"]}
    routes=data(ROUTES)
    assert routes["policy"]=="REVIEW_NAVIGATION_ONLY__NOT_CANONICAL_PREREQUISITE"
    assert routes["counts"]["primary_constructions"]==8
    assert routes["counts"]["proposed_extensions"]==8
    assert routes["counts"]["author_packs"]==16
    assert routes["academic"]["admitted"]==0
    for topic,(qid,pack) in SOURCES.items():
        path=PACKS/pack
        assert path.is_file()
        text=path.read_text(encoding="utf-8")
        assert "## Core1A" in text and "## Core1B" in text
        for section in ("Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"):
            assert section in text
        assert "NOT_ADMITTED" in text or "not admitted" in text.lower()
        row=next(x for x in routes["constructions"] if x["id"]=="WPE-"+topic)
        assert [x["id"] for x in row["proposed_source_ids"]]==[qid]
        assert row["group"]=="EXTENSION"
        assert row["authored_pack_present"] is True
        assert row["approved_core1a_url"] is None
        assert row["approved_core1b_url"] is None
        assert row["acceptance"]=="AUTHOR_DRAFT_ONLY"
        assert bank[qid]["band"]=="D3"
        assert bank[qid]["review_state"]=="NOT_ADMITTED"
        assert bank[qid]["key_state"].startswith("HOLD")

def test_e06_applied_push_power_not_net_kinetic_rate():
    # Guided: mass2, push30N, gravity20N, contact distance1m.
    m,g=2,10
    F,s=30,1
    net=F-m*g
    K=net*s
    v=math.sqrt(2*K/m)
    close(K,10)
    close(v,math.sqrt(10))
    close(F*v,30*math.sqrt(10))
    close(net*v,10*math.sqrt(10))
    close(v*v/(2*g),0.5)
    assert F*v>net*v

    # Fresh: infer the takeoff speed from height AFTER contact.
    mass,contact,flight=4,.5,.8
    v=math.sqrt(2*g*flight)
    K=.5*mass*v*v
    gravity_contact=mass*g*contact
    F=(K+gravity_contact)/contact
    close(v,4)
    close(K,32)
    close(gravity_contact,20)
    close(F,104)
    close(F*v,416)
    close((F-mass*g)*v,256)
    close(F*contact,K+gravity_contact)

    # Change ONLY later flight rise.
    v_b=math.sqrt(2*g*.45)
    K_b=.5*mass*v_b*v_b
    F_b=(K_b+gravity_contact)/contact
    close(v_b,3)
    close(K_b,18)
    close(F_b,76)
    close(F_b*v_b,228)
    close((F_b-mass*g)*v_b,108)

    # Reader's source coaching result computes NET force x speed, not the
    # constant applied contact force x speed. This remains a held query.
    source_mass,source_contact,source_flight=70,.5,1
    source_v=math.sqrt(2*g*source_flight)
    a=source_v**2/(2*source_contact)
    applied_force=source_mass*(a+g)
    net_force=source_mass*a
    assert applied_force*source_v>net_force*source_v
    close(applied_force,2100)

def test_e07_friction_on_both_incline_legs():
    # Guided: 1kg, 4m/s, gravity downhill6N, friction2N.
    m,v=1,4
    K0=.5*m*v*v
    up_resistance=6+2
    d=K0/up_resistance
    down_net=6-2
    returned_K=down_net*d
    close(K0,8)
    close(d,1)
    close(returned_K,4)
    close(math.sqrt(2*returned_K/m),math.sqrt(8))
    close(K0-returned_K,2*2*d)
    close((-6*d)+(6*d),0)

    # Fresh: 45deg incline; sin=cos, return ratio2/3.
    def mu_for_return_ratio(p,q):
        ratio_sq=(p/q)**2
        return (1-ratio_sq)/(1+ratio_sq)
    close(mu_for_return_ratio(2,3),5/13)
    close(mu_for_return_ratio(3,4),7/25)
    assert 0<7/25<5/13<1
    for p,q in ((2,3),(3,4)):
        mu=mu_for_return_ratio(p,q)
        close((1-mu)/(1+mu),(p/q)**2)

def test_e08_new_post_switch_effective_potential_turns():
    # Guided: k100, initial +.1, new F+20.
    k,xi,F=100,.1,20
    xeq=F/k
    xo=2*xeq-xi
    U=lambda x:.5*k*x*x-F*x
    close(xeq,.2)
    close(xo,.3)
    close(U(xi),-1.5)
    close(U(xo),-1.5)

    # Fresh: initially compressed -.2m, old F=-10, new F=+15.
    k,xi,F=50,-.2,15
    xeq=F/k
    xo=2*xeq-xi
    U=lambda x:.5*k*x*x-F*x
    close(-k*xi,10)
    close(xeq,.3)
    close(xo,.8)
    close(U(xi),4)
    close(U(xo),4)

    # Boundary new F +5, old initial conditions unchanged.
    F=5
    xeq=F/k
    xo=2*xeq-xi
    U=lambda x:.5*k*x*x-F*x
    close(xeq,.1)
    close(xo,.4)
    close(U(xi),2)
    close(U(xo),2)
    assert xo != .8

def test_current_eight_extension_ui_preserves_five_preexisting_topic_keys():
    script=(WPE/"extension-learning.js").read_text(encoding="utf-8")
    page=(WPE/"extension-learning.html").read_text(encoding="utf-8")
    routes=data(ROUTES)
    for topic in [f"E0{x}" for x in range(1,9)]:
        assert f"    {topic}: {{" in script
        assert f'\"WPE-{topic}\"' in json.dumps(routes)
    assert script.count('visual:"')==8
    assert 'const storagePrefix = "g9:wpe:extensions:v1:";' in script
    assert 'const allIds = Object.keys(lessons)' in script
    assert 'allIds.length+" boundary challenges completed"' in script
    assert '"#extension-meter").max=allIds.length' in script
    assert 'allIds[(i+1)%allIds.length]' in script
    assert 'max="8" value="0"' in page
    assert "0 of 8 boundary challenges completed" in page
    assert "innerHTML" not in script
    assert "s.first={...values};s.attemptDraft={};s.stage=2" in script
    assert "s.repair=val;s.stage=5" in script
    assert "s.boundary=val" in script

def test_22_high_reader_source_themes_now_have_related_practice_but_not_admission():
    report=data(REGISTER)
    high=[q for q in report["questions"] if q["reader_proposal"]["band"] in ("D3","D4")]
    assert len(high)==22
    assert report["summary"]["reader_d3d4_learning"]=={
        "INTERACTIVE_RELATED_PRACTICE":22,"AUTHOR_PACK_ONLY":0,"UNMAPPED":0}
    assert report["summary"]["all_learning"]=={
        "INTERACTIVE_RELATED_PRACTICE":28,"AUTHOR_PACK_ONLY":0,"UNMAPPED":46}
    assert report["summary"]["reader_d3d4_unmapped_ids"]==[]
    assert report["summary"]["admitted"]==0
    assert all(q["learning"]["status"]=="INTERACTIVE_RELATED_PRACTICE" for q in high)
    assert all(q["learning"]["semantic_join"]=="PROPOSED_UNQUALIFIED"
               and not q["learning"]["exact_inference_independently_verified"]
               and not q["qrt_evidence"]["independent_final_adjudication"]
               and q["admission"]=="NOT_ADMITTED" for q in report["questions"])
    for topic,(qid,pack) in SOURCES.items():
        q=next(q for q in high if q["source_id"]==qid)
        assert "WPE-"+topic in q["learning"]["interactive_ids"]
        assert q["next_actions"]["qrt"]=="OBTAIN_AUTHORIZED_INDEPENDENT_FIRST_PASS"
