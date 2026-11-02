"""Proposed D3/D4 source-to-learning bridge invariants; NOT an academic/QRT test."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "WPE_Source_to_Core1A_Concept"
BRIDGE_PATH = BASE / "learning-bridge/P0_P1_CONSTRUCTION_BRIDGE.json"
SELECTION_PATH = BASE / "evidence/RECEIVED_selection_21_places.json"
READER_PATH = ROOT / "workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_bridge_reconciles_current_selected_claims_without_promoting_them():
    bridge, selection, reader = map(load, (BRIDGE_PATH, SELECTION_PATH, READER_PATH))
    candidates = [p for p in selection["places"] if p["candidate_id"] is not None]
    source = {q["source_id"]: q for q in reader["questions"]}
    assert len(selection["places"]) == 21
    assert len(candidates) == 14
    assert len([p for p in selection["places"] if p["status"] == "VACANT"]) == 7
    assert selection["admitted"] == bridge["native_admissions"] == 0
    assert bridge["counts"]["pilot_places"] == len(selection["places"])
    assert bridge["counts"]["pending_candidates"] == len(candidates)
    assert {r["candidate_id"] for r in bridge["reconciliation"]} == {p["candidate_id"] for p in candidates}
    assert len(bridge["reconciliation"]) == 14

    for item in bridge["reconciliation"]:
        selected = next(p for p in candidates if p["candidate_id"] == item["candidate_id"])
        assert item["pilot_operation"] == selected["operation"]
        assert item["pilot_band"] == selected["band"]
        found = source.get(item["candidate_id"])
        expected = (
            "ABSENT_FROM_SELECTED_READER" if found is None
            else "AGREES_IN_READER"
            if found["op"] == selected["operation"] and found["band"] == selected["band"]
            else "CONFLICT_IN_READER"
        )
        assert item["comparison"] == expected
        assert item["academic_status"] == "PENDING__NO_AUTHORITY_TO_REPLACE"
    observed = {key: sum(r["comparison"] == status for r in bridge["reconciliation"])
                for key, status in (("reader_agree", "AGREES_IN_READER"),
                                    ("reader_conflicts", "CONFLICT_IN_READER"),
                                    ("reader_absent", "ABSENT_FROM_SELECTED_READER"))}
    assert observed == {k: bridge["counts"][k] for k in observed}
    assert observed == {"reader_agree": 3, "reader_conflicts": 8, "reader_absent": 3}
    assert {r["candidate_id"] for r in bridge["reconciliation"]
            if r["comparison"] == "ABSENT_FROM_SELECTED_READER"} == {"EX-M81", "EX-M44", "EX-M60"}


def test_eight_distinct_construction_specs_and_six_step_self_tutor_cycle():
    bridge = load(BRIDGE_PATH)
    specs = bridge["constructions"]
    assert len(specs) == 8
    assert len({row["id"] for row in specs}) == 8
    assert sum(row["priority"] == "P0" for row in specs) == 6
    assert sum(row["priority"] == "P1" for row in specs) == 2
    assert bridge["core1b_contract"] == ["PREDICT", "ATTEMPT", "RECONSTRUCT",
                                         "DIAGNOSE", "REPAIR", "BOUNDARY_TEST"]
    assert all(len(s["core1a"]) >= 4 and len(s["core1b"]) == 6 for s in specs)
    assert all(s["links"] and s["misconception"] and s["starting_foundation"] for s in specs)
    assert bridge["status"].endswith("NOT_ACADEMICALLY_ADMITTED")
    assert bridge["owner_approval"] is False
    assert bridge["qrt_approval"] is False

    for row in specs:
        if row["first_pair"]:
            pack = BASE / "learning-bridge" / row["first_pair"]
            content = pack.read_text(encoding="utf-8")
            assert "## Core1A" in content and "## Core1B" in content
            assert "Author-only reference" in content
            assert all(f"### {i:02d}" in content for i in range(1, 7))
            assert "Separation check" in content
            assert "\\\\(" not in content, "Markdown maths must not be double-escaped"


def test_foundational_teaching_remains_unadmitted_and_review_is_historical():
    bridge = load(BRIDGE_PATH)
    mapping = load(ROOT / "physics/wpe/learn-challenge-source-map.json")
    assert mapping["auth"]["native_core1a"] == "NOT_ACCEPTED"
    assert mapping["auth"]["native_core1b"] == "NOT_ACCEPTED"
    assert mapping["auth"]["qrt"] == "NOT_RUN"
    assert mapping["auth"]["owner"] == "PENDING"
    assert bridge["stale_review"]["conclusion"].startswith("REVIEW_SUPERSEDED")
    assert bridge["stale_review"]["reviewed_page_blob_sha"] != bridge["stale_review"]["current_page_blob_sha"]
    assert bridge["stale_review"]["reviewed_map_blob_sha"] != bridge["stale_review"]["current_map_blob_sha"]
