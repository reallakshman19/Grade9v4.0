"""C01/C02 author-practice source binding and public-page protections, not academic review."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WPE = ROOT / "physics" / "wpe"
BRIDGE = ROOT / "WPE_Source_to_Core1A_Concept" / "learning-bridge"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def test_six_stage_records_bind_to_exact_author_packs_without_approval():
    spec = read(WPE / "construction-lab-map.json")
    assert spec["schema"] == "wpe-six-stage-learning-journeys/v1"
    assert spec["stages"] == [
        "PREDICT", "ATTEMPT", "RECONSTRUCT",
        "DIAGNOSE", "REPAIR", "BOUNDARY_TEST"
    ]
    assert spec["status"].endswith("NO_NATIVE_ADMISSION")
    assert spec["academic"] == {
        "native_core1a": "NOT_ACCEPTED",
        "native_core1b": "NOT_ACCEPTED",
        "qrt": "NOT_RUN", "owner": "PENDING", "admitted": 0,
    }
    assert "DRAFT_NOT_MERGED" in spec["review_only_pr40"]
    assert "not secure" in spec["answer_delivery"]
    assert len(spec["journeys"]) == 2
    assert {row["code"] for row in spec["journeys"]} == {"C01", "C02"}
    for row in spec["journeys"]:
        path = ROOT / row["source_pack"]
        assert path.exists()
        assert row["source_pack_git_blob"] == blob(path)
        author_pack = path.read_text(encoding="utf-8")
        assert "## Core1A" in author_pack and "## Core1B" in author_pack
        assert all(f"### {i:02d}" in author_pack for i in range(1, 7))
        assert row["local_key"].endswith(row["code"])
        assert len(row["first_attempt_fields"]) >= 6
        assert row["proposed_source_ids"]
        assert "REFLECTION_COMPLETED_NOT_MASTERED" == row["progress_status"]
    original = read(WPE / "learn-challenge-source-map.json")
    assert original["auth"]["native_core1a"] == "NOT_ACCEPTED"
    assert original["auth"]["native_core1b"] == "NOT_ACCEPTED"
    assert len(original["program"]) == 5


def test_existing_five_lessons_and_distinct_new_lab_in_same_page():
    page = (WPE / "learn-challenge.html").read_text(encoding="utf-8")
    js = (WPE / "construction-lab.js").read_text(encoding="utf-8")
    css = (WPE / "construction-lab.css").read_text(encoding="utf-8")
    assert page.count('<article class="lesson"') == 5
    assert page.count('class="lab-card"') == 2
    assert 'id="construction-lab"' in page
    assert 'id="lab-c01"' in page and 'id="lab-c02"' in page
    assert 'href="construction-lab.css"' in page
    assert 'src="construction-lab.js"' in page
    assert 'href="#construction-lab"' in page
    assert js.count('localStorage.setItem(') == 1
    assert "reconstructionViewed" in js and "state.attempt={values,explanation}" in js
    assert 'fetch("construction-lab-answers.json"' in js
    assert "postAttemptPromise" in js
    assert "state.step===6" in js
    assert "Your work is stored in this browser only" in page
    assert "not securely protected" in page
    assert ".lab-input-grid" in css
    assert "@media(max-width:670px)" in css
    # The public template and pre-attempt code must not contain the independent
    # task's complete worked reconstruction. It is in a separate post-lock fetch.
    assert "net work = 30 − 6 − 15 + 0 = +9 J" not in page + js
    assert "Kinetic energy at the strip's end is 1.00 − 0.50" not in page + js


def test_separate_learner_post_attempt_reconstruction_and_boundary():
    doc = read(WPE / "construction-lab-answers.json")
    assert doc["schema"] == "wpe-construction-lab-post-attempt/v1"
    assert "NOT_SECURE" in doc["scope"]
    assert set(doc) == {"schema", "scope", "C01", "C02"}
    for code in ("C01", "C02"):
        row = doc[code]
        assert len(row["reconstruction"]) >= 4
        assert len(row["criteria"]) == 3
        assert len(row["boundary"]) >= 3
    assert "√6" in "\n".join(doc["C01"]["reconstruction"])
    assert "2.45" in "\n".join(doc["C01"]["reconstruction"])
    assert "0.707" in "\n".join(doc["C02"]["reconstruction"])
    assert "negative kinetic energy" in "\n".join(doc["C01"]["boundary"])
    assert "zero speed" in "\n".join(doc["C02"]["boundary"])
