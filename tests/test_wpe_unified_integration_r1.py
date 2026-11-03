"""WPE unified Core1A/Core1B/Core2 integration invariants (technical, not academic approval)."""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WPE = ROOT / "physics" / "wpe"
BANK = ROOT / "workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"


def read(path):
    return path.read_text(encoding="utf-8")


def load(path):
    return json.loads(read(path))


def transfer():
    source = read(WPE / "focused-transfer-variants.js")
    match = re.search(r"Object.freeze\((\{.*\})\);", source, re.S)
    assert match, "F transfer data must remain a declarative object"
    return json.loads(match.group(1))


def expected_page(lesson):
    return {"C": "d3d4-self-tutor", "E": "extension-learning", "F": "focused-journeys"}[lesson[0]]


def test_all_74_verified_routes_are_direct_without_changing_fits():
    coverage = load(WPE / "learning-coverage-r1.json")
    bank = load(BANK)
    assert len(coverage["questions"]) == len(bank["questions"]) == 74
    by_id = {q["source_id"]: q for q in bank["questions"]}
    assert len(by_id) == 74
    assert Counter(r["fit"] for r in coverage["questions"]) == {
        "FOCUSED_NEW": 3,
        "TARGETED_PRACTICE": 18,
        "RELATED_BRIDGE": 48,
        "MISSING_CONSTRUCTION": 5,
    }
    for row in coverage["questions"]:
        assert row["stem_sha256"] == by_id[row["source_id"]]["stem_sha256"]
        lesson, href = row["primary_lesson"], row["lesson_href"]
        if lesson is None:
            assert row["fit"] == "MISSING_CONSTRUCTION" and href is None
        else:
            assert lesson in (
                {f"C{i:02}" for i in range(1, 9)}
                | {f"E{i:02}" for i in range(1, 6)}
                | {"F01", "F02", "F03"}
            )
            assert href == (expected_page(lesson) + ".html?question="
                            + row["source_id"] + "#" + lesson)
            assert "study-bridge.html" not in href
    sample = next(r for r in coverage["questions"] if r["source_id"] == "EX-M79")
    assert sample["primary_lesson"] == "C03"
    assert sample["fit"] == "RELATED_BRIDGE"
    assert sample["lesson_href"] == "d3d4-self-tutor.html?question=EX-M79#C03"


def test_gateway_no_iframes_and_old_links_fail_closed():
    for file in ["index.html", "learn-challenge.html", "study-bridge.html",
                 "d3d4-self-tutor.html", "extension-learning.html",
                 "focused-journeys.html", "question-bank.html"]:
        assert "<iframe" not in read(WPE / file).lower(), file
    assert "location.replace(target)" in read(WPE / "study-bridge.html")
    assert "original.stem_sha256!==row.stem_sha256" in read(WPE / "study-bridge.html")
    index = read(WPE / "index.html")
    for heading in ("Learn → Challenge", "Question Bank", "Practice my skills"):
        assert f"<h2>{heading}</h2>" in index
    entry = read(WPE / "learn-challenge.html")
    for marker in ("Start from my question", "Explore a Physics skill",
                   "Resume", "Start again", "Clear saved practice"):
        assert marker in entry
    assert 'id="skill-links"' in entry
    assert "g9:wpe:journey:v1" in read(WPE / "learn-challenge-coverage.js")


def test_core2_attempt_storage_versioned_by_source_and_never_auto_reveals():
    html = read(ROOT / "preview/question-status.html")
    bank = load(BANK)
    match = re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>', html, re.S)
    assert match and json.loads(match.group(1))["questions"] == bank["questions"]
    assert 'ATTEMPT_PREFIX="g9:wpe:core2:attempt:v1:"' in html
    assert "const attemptKey=q=>ATTEMPT_PREFIX+q.source_id" in html
    assert "record.stem_sha256!==q.stem_sha256" in html
    assert "first:{selected:" not in html  # First-attempt storage uses committed snapshot, not the key.
    assert "s.first={selected:s.selected.slice()" in html
    assert "if(state.committed)return state" in html
    assert "if(st.revealed)showSolution(q)" not in html
    assert "if(!s?.committed)return" in html
    assert "persistAttempt(q)" in html
    assert "restart-source" in html


def test_pr55_only_data_reused_for_distinct_optional_f_challenges():
    data = transfer()
    assert set(data) == {"F01", "F02", "F03"}
    for f, donor in (("F01", "E06"), ("F02", "E07"), ("F03", "E08")):
        d = data[f]
        assert d["variantId"] == "transfer55" and d["donorId"] == donor
        assert len(d["hints"]) == 3 and len(d["worked"]) >= 4
        assert len(d["diagnoses"]) >= 4 and len(d["boundaryCheck"]) >= 100
        assert d["challenge"] and d["boundary"] and d["fields"]
        assert any(x["id"] == "model" for x in d["fields"])
        assert any(x["id"] == "reason" for x in d["fields"])
        assert all(x.get("mistake") for x in d["fields"] if x["type"] not in ("textarea", "text"))
    assert len([p for p in WPE.glob("extension-learning*.html")]) == 1
    focused = read(WPE / "focused-journeys.js")
    assert 'id+"-transfer55"' in focused
    assert 'const stateId=alternate?active+"-transfer55":active;' in focused
    assert "Try another challenge (optional)" in focused
    assert "s.first={answers:{...values}" in focused
    assert "ground contact can be stationary" in focused
    assert "pseudo-work rate" in focused
    assert 'focused-transfer-variants.js' in read(WPE / "focused-journeys.html")


def test_transfer_physics_and_changed_conditions():
    d = transfer()
    numeric = lambda entry: {x["id"]: x["expected"] for x in d[entry]["fields"] if x["type"] == "number"}
    bnums = lambda entry: {x["id"]: x["expected"] for x in d[entry]["boundaryFields"] if x["type"] == "number"}

    # Applied moving-launcher force is an ideal mechanical transfer, not a human muscle-power claim.
    m, g, contact, flight = 4, 10, .50, .80
    v = math.sqrt(2 * g * flight)
    gain = m * v * v / 2
    gravity_work = -m * g * contact
    force = (gain - gravity_work) / contact
    f = numeric("F01")
    assert math.isclose(v, f["takeoffSpeed"]) and math.isclose(gain, f["contactGain"])
    assert math.isclose(gravity_work, f["contactGravity"])
    assert math.isclose(force, f["appliedForce"]) and math.isclose(force * v, f["appliedPower"])
    assert math.isclose((force - m*g), f["netForce"])
    assert math.isclose(bnums("F01")["appliedForce"], 76)
    assert math.isclose(bnums("F01")["appliedPower"], 228)

    # Opposite friction directions, same climb/return distance.
    ratio = 2/3
    mu = (1 - ratio**2) / (1 + ratio**2)
    assert math.isclose(mu, 5/13)
    assert math.isclose(numeric("F02")["mu"], mu)
    assert math.isclose(bnums("F02")["mu"], 7/25)
    assert 0 < mu < 1  # 45° return is dynamically possible with stated static-friction assumption.

    # Force switch without an impulsive displacement preserves x_i and v_i.
    k, x_i, applied = 50, -.20, 15
    xeq = applied/k
    far = 2*xeq-x_i
    eff = lambda x: .5*k*x*x-applied*x
    assert math.isclose(xeq, numeric("F03")["newEquilibrium"])
    assert math.isclose(far, numeric("F03")["turning"])
    assert math.isclose(eff(x_i), eff(far)) and math.isclose(eff(far), 4)
    assert math.isclose(bnums("F03")["newEquilibrium"], .10)
    assert math.isclose(bnums("F03")["turning"], .40)
