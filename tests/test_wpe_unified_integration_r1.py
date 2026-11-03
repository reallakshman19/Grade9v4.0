"""WPE unified student journey integration: static integrity and independent Physics checks.
Software validation only: this neither grades learner reasoning nor admits a source task.
"""
from __future__ import annotations
import json
import math
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WPE=ROOT/"physics/wpe"
READER=ROOT/"preview/question-status.html"
BANK=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"

def source(path):
    return (ROOT/path).read_text(encoding="utf-8")

def test_one_gateway_and_direct_existing_lessons():
    index=source("physics/wpe/index.html")
    gateway=source("physics/wpe/learn-challenge.html")
    routes=source("physics/wpe/learn-challenge-coverage.js")
    bridge=source("physics/wpe/study-bridge.html")
    assert index.count("<h2>Learn → Challenge</h2>")==1
    assert index.count("<h2>Question Bank</h2>")==1
    assert index.count("<h2>Practice my skills</h2>")==1
    assert "Start from my question" in gateway and "Explore a Physics skill" in gateway
    assert gateway.count('<article class="lesson"')==5
    for name in ("C01","C08","E01","E05","F01","F03"):
        assert name in gateway
    assert "row.primary_lesson" in routes and "study-bridge.html" in routes
    assert "<iframe" not in bridge.lower()
    assert "location.replace(target.href)" in bridge
    for filename in ("d3d4-self-tutor.html","extension-learning.html","focused-journeys.html"):
        text=source("physics/wpe/"+filename)
        assert "<iframe" not in text.lower()
        assert '<script src="student-journey.js" defer></script>' in text

def test_exact_74_source_records_untouched_and_local_state_versioned():
    bank=json.loads(BANK.read_text(encoding="utf-8"))
    html=READER.read_text(encoding="utf-8")
    data=json.loads(re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>',html,re.S).group(1))
    assert len(data["questions"])==74
    assert data["questions"]==bank["questions"]
    assert "g9:wpe:core2:attempt:v1:" in html
    assert "stem_sha256:q.stem_sha256" in html
    assert "s.first={selected:s.selected.slice()" in html
    assert "revealed:false" in html
    assert "if(!s?.committed)return" in html
    for label in ("Resume","Start again","Clear saved practice"):
        assert label in html
    assert "window.WPE_F_TRANSFER" in source("physics/wpe/focused-journeys.js")
    map_=json.loads((WPE/"learning-coverage-r1.json").read_text(encoding="utf-8"))
    assert len(map_["questions"])==74
    assert map_["counts"]["focused_new"]==3
    assert map_["counts"]["targeted"]==18
    assert map_["counts"]["related"]==48
    assert map_["counts"]["missing"]==5

def test_donor_transfer_variants_and_separate_saved_attempts():
    text=source("physics/wpe/focused-transfer-challenges.js")
    d=json.loads(text.split("Object.freeze(",1)[1].rsplit(");",1)[0])
    assert set(d)=={"F01","F02","F03"}
    assert [d[x]["donor"] for x in ("F01","F02","F03")]==[
        "PR #55 · E06","PR #55 · E07","PR #55 · E08"]
    for id_,cfg in d.items():
        for key in ("prediction","challenge","fields","worked","hints","diagnoses","diagnosisTips","boundary","boundaryCheck","boundaryFields"):
            assert cfg[key],(id_,key)
        assert len(cfg["hints"])==3
        assert cfg["fields"][0]["type"] in ("number","select")
        assert any(f["id"]=="model" and f["type"]=="select" for f in cfg["fields"])
        assert any(f["id"]=="reason" and f["type"]=="textarea" for f in cfg["fields"])
    focused=source("physics/wpe/focused-journeys.js")
    assert 'variant==="transfer"?id+":transfer":id' in focused
    assert "Try another challenge" in focused
    assert "ground contact can be stationary" in focused
    assert "pseudo-work rate" in focused
    assert '<script src="focused-transfer-challenges.js" defer></script>' in source("physics/wpe/focused-journeys.html")
    assert '"E06:"' not in source("physics/wpe/extension-learning.js")

def test_three_distinct_models_and_boundary_conditions():
    g=10
    m,s,h=4,.5,.8
    v=math.sqrt(2*g*h)
    force=(m*v*v/2+m*g*s)/s
    assert v==4 and force==104 and force*v==416
    assert (force-m*g)*v==256
    h2=.45
    v2=math.sqrt(2*g*h2)
    force2=(m*v2*v2/2+m*g*s)/s
    assert v2==3 and force2==76 and force2*v2==228
    assert math.isclose((1-(2/3)**2)/(1+(2/3)**2),5/13)
    assert math.isclose((1-(3/4)**2)/(1+(3/4)**2),7/25)
    k,x0,f=50,-.2,15
    eq=f/k
    other=2*eq-x0
    energy=lambda x,force: k*x*x/2-force*x
    assert eq==.3 and other==.8
    assert math.isclose(energy(x0,f),4) and math.isclose(energy(other,f),4)
    eq2=5/k;other2=2*eq2-x0
    assert eq2==.1 and other2==.4
    assert math.isclose(energy(x0,5),2) and math.isclose(energy(other2,5),2)


def test_skill_explorer_four_tables_preserve_all_existing_destinations():
    from urllib.parse import urlsplit
    gateway=source("physics/wpe/learn-challenge.html")
    area=gateway.split('<section class="skill-explorer"',1)[1].split('<section class="practice-manager"',1)[0]
    expected={
        "foundation-skills-title": [("#work-sign","01"),("#momentum-energy","02"),("#energy-motion","03"),
                                    ("#potential-force","04"),("#momentum-fragments","05")],
        "core-skills-title": [(f"d3d4-self-tutor.html#C{i:02}",f"C{i:02}") for i in range(1,9)],
        "extension-skills-title": [(f"extension-learning.html#E{i:02}",f"E{i:02}") for i in range(1,6)],
        "focused-skills-title": [(f"focused-journeys.html#F{i:02}",f"F{i:02}") for i in range(1,4)]
    }
    groups=re.findall(r'<section class="skill-group" aria-labelledby="([^"]+)">(.*?)</table></section>',area,re.S)
    assert [name for name,_ in groups]==list(expected)
    assert area.count('<table class="skill-table"')==4
    assert area.count('<th scope="col">')==12
    for name,group in groups:
        rows=re.findall(r'<tr><th scope="row" class="skill-code">([^<]+)</th><td>.*?</td><td><a class="skill-open" href="([^"]+)"',group,re.S)
        assert [(href,code) for code,href in rows]==expected[name],name
        assert group.count('class="skill-open"')==len(expected[name])
        for href,_ in expected[name]:
            parsed=urlsplit(href)
            target=WPE/parsed.path if parsed.path else WPE/"learn-challenge.html"
            assert target.is_file(),(name,href)
            if parsed.path in ("extension-learning.html","focused-journeys.html"):
                # These existing pages generate lesson anchors from JS data at runtime.
                js=WPE/("extension-learning.js" if parsed.path.startswith("extension") else "focused-journeys.js")
                assert f"{parsed.fragment}: {{" in js.read_text(encoding="utf-8"),(name,href)
            else:
                assert f'id="{parsed.fragment}"' in target.read_text(encoding="utf-8"),(name,href)
    css=source("physics/wpe/student-journey.css")
    assert ".skill-table" in css and ".skill-open" in css and "@media(max-width:560px)" in css
    assert ".skill-links" not in area
