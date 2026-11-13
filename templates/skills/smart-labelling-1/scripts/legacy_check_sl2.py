"""Check a Smart Labelling 2 overlay (smart-labels-2.<topic>.v1.json) against its Smart Labelling 1 overlay.

Usage:
  python -X utf8 -I check_sl2.py <overlay.json> --sl1 <smart-labels-1 overlay> --vocab <learner-question-metadata.v1.json> [--attempts <p1-attempts.json>]
  python -X utf8 -I check_sl2.py --binding <smart-labels-1 overlay> <question_id>   (prints the binding block to copy)
Prints one line per problem and a summary; exit code 1 if anything FAILs.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA = "g9v35-smart-labels-2/v1"
DEMANDS = {"RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"}
COMPONENTS = ["concept_model_selection", "representation_translation", "reasoning_chain_length",
              "algebra_computational_load", "trap_exception_sensitivity"]
ENUMS = {
    "mode": {"QUESTION", "EVIDENCE"},
    "status": {"UNREVIEWED", "REVIEWED", "STALE"},
    "key_status": {"KEY_VERIFIED", "KEY_FROM_PUBLISHER", "KEY_DOUBTFUL", "NO_KEY"},
    "representation": {"DIAGRAM", "FREE_BODY_DIAGRAM", "VECTOR", "GRAPH", "EQUATION", "TABLE", "ENERGY_BARS", "WORDS"},
    "check": {"UNITS", "LIMITING_CASE", "SIGN", "ROUND_TRIP", "ENERGY_LEDGER", "COUNTEREXAMPLE", "ALTERNATE_DERIVATION"},
    "result": {"CORRECT", "INCORRECT", "NO_ANSWER", "NOT_EVALUATED"},
    "confidence": {"SURE", "UNSURE", "GUESSING", "MISSING"},
    "help": {"INDEPENDENT", "HINT", "SCAFFOLD", "EXPLANATION", "WORKED_EXAMPLE", "FULL_SOLUTION", "NOT_APPLICABLE"},
    "prereq": {"DEMONSTRATED", "UNCERTAIN", "MISSING", "UNKNOWN"},
    "route": {"PREREQUISITE_BRIDGE", "CORE1A_CONSTRUCTION", "CORE1B_RECONSTRUCTION", "FRESH_RECHECK"},
}
GROUPS = ["question_id", "mode", "status", "derivation_version", "binding", "route", "difficulty_evidence",
          "demand_proposal", "representation_requirement", "independent_checks", "wrong_route_hypotheses",
          "learner", "learning_route"]
FORBIDDEN_KEY = re.compile(r"mastery|percent|competen", re.I)


def key_digest(key) -> str:
    blob = json.dumps(key, ensure_ascii=False, sort_keys=True)
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()


def binding_for(sl1_record: dict) -> dict:
    check = sl1_record["content_integrity"]["answer_check"]
    status = "KEY_DOUBTFUL" if check.get("status") == "DISAGREES" else (
        "KEY_FROM_PUBLISHER" if check.get("key") not in (None, "") else "NO_KEY")
    return {"sl1_item_digest": sl1_record["custody"]["item_digest"],
            "answer_ref_status": status,
            "answer_ref_digest": key_digest(check.get("key"))}


def keys_in(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from keys_in(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from keys_in(v)


def load_records(path: str, field: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {r[field]: r for r in data.get("records" if field == "question_id" else "attempts", [])}


def main() -> int:
    if len(sys.argv) == 4 and sys.argv[1] == "--binding":
        record = load_records(sys.argv[2], "question_id").get(sys.argv[3])
        if record is None:
            print(f"{sys.argv[3]} is not in {sys.argv[2]}", file=sys.stderr)
            return 1
        print(json.dumps(binding_for(record), indent=2))
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("overlay")
    ap.add_argument("--sl1", required=True)
    ap.add_argument("--vocab", required=True)
    ap.add_argument("--attempts")
    a = ap.parse_args()
    overlay = json.loads(Path(a.overlay).read_text(encoding="utf-8"))
    sl1 = load_records(a.sl1, "question_id")
    ranges = json.loads(Path(a.vocab).read_text(encoding="utf-8"))["question_difficulty_score_ranges"]
    attempts = load_records(a.attempts, "attempt_id") if a.attempts else None
    fails, warns = [], []

    def fail(qid, msg):
        fails.append(f"FAIL {qid}: {msg}")

    def warn(qid, msg):
        warns.append(f"WARN {qid}: {msg}")

    def enum(qid, name, value):
        if value not in ENUMS[name]:
            fail(qid, f"{name} '{value}' is not one of {sorted(ENUMS[name])}")

    if overlay.get("schema") != SCHEMA:
        fail("file", f"schema must be {SCHEMA}")
    for key in ("derivation_version", "topic", "sl1_ref", "rubric_ref", "labeller", "date", "records"):
        if key not in overlay:
            fail("file", f"missing {key}")

    for r in overlay.get("records", []):
        qid = r.get("question_id", "?")
        missing = [g for g in GROUPS if g not in r]
        if missing:
            fail(qid, f"missing groups {missing}")
            continue
        enum(qid, "mode", r["mode"])
        enum(qid, "status", r["status"])
        stale = r["status"] == "STALE"
        for key in keys_in(r):
            if FORBIDDEN_KEY.search(str(key)):
                fail(qid, f"field '{key}' looks like a mastery score: Smart 2 never assigns mastery")

        s1 = sl1.get(qid)
        if s1 is None:
            fail(qid, "no Smart 1 record for this question")
        else:
            if s1.get("status") == "STALE" and not stale:
                fail(qid, "its Smart 1 record is STALE: re-label Smart 1 first")
            expected = binding_for(s1)
            binding = r["binding"]
            enum(qid, "key_status", binding.get("answer_ref_status"))
            if not stale and binding.get("sl1_item_digest") != expected["sl1_item_digest"]:
                fail(qid, "question text changed since this record: mark STALE and re-derive")
            if not stale and binding.get("answer_ref_digest") != expected["answer_ref_digest"]:
                fail(qid, "answer key changed since this record: mark STALE and re-derive")
            if s1["content_integrity"]["answer_check"].get("status") == "DISAGREES" and \
                    binding.get("answer_ref_status") != "KEY_DOUBTFUL":
                fail(qid, "Smart 1 found the key disagrees with the worked answer: answer_ref_status must be KEY_DOUBTFUL")

        route = r["route"]
        move_ids = [m.get("id") for m in route.get("moves", [])]
        if len(move_ids) < 2:
            fail(qid, "route needs at least two moves")
        if route.get("crux_move_ref") not in move_ids:
            fail(qid, "crux_move_ref must name one of the moves")
        if len(str(route.get("crux", ""))) < 20:
            fail(qid, "crux must state the decisive move in a sentence")

        evidence = r["difficulty_evidence"]
        comps = evidence.get("components", {})
        total = 0
        for name in COMPONENTS:
            part = comps.get(name)
            if not isinstance(part, dict):
                fail(qid, f"missing component {name}")
                continue
            if part.get("score") not in (0, 1, 2):
                fail(qid, f"{name} score must be 0, 1 or 2")
            else:
                total += part["score"]
            if len(str(part.get("evidence", ""))) < 20:
                fail(qid, f"{name} needs an evidence sentence about this question")
        if evidence.get("total") != total:
            fail(qid, f"total {evidence.get('total')} is not the sum of the parts ({total})")
        band = next((b for b, rng in ranges.items() if rng["min"] <= total <= rng["max"]), None)
        if evidence.get("band") != band:
            fail(qid, f"band {evidence.get('band')} does not match the total {total} ({band})")
        prior = evidence.get("prior_proposal")
        if prior and prior.get("total") != total and len(str(evidence.get("differences", ""))) < 10:
            fail(qid, "the total differs from the earlier proposal: say why under differences")

        demand = r["demand_proposal"]
        primary = demand.get("primary")
        if primary not in DEMANDS:
            fail(qid, f"primary demand '{primary}' is not one of {sorted(DEMANDS)}")
        for s in demand.get("secondary", []):
            if s not in DEMANDS or s == primary:
                fail(qid, f"secondary demand '{s}' is invalid or repeats the primary")
        if not demand.get("rationale"):
            fail(qid, "demand_proposal.rationale is empty")
        if demand.get("candidate_cell") != f"QRT-{primary}-{band}":
            fail(qid, f"candidate_cell must be QRT-{primary}-{band}")
        if demand.get("status") != "PROPOSED":
            fail(qid, "demand_proposal.status must be PROPOSED: QRT alone resolves the cell")

        if not r["representation_requirement"]:
            fail(qid, "representation_requirement is empty")
        for rep in r["representation_requirement"]:
            enum(qid, "representation", rep.get("kind"))
            if not rep.get("transformation"):
                fail(qid, "each representation needs its transformation")
        if not r["independent_checks"]:
            fail(qid, "at least one independent check is needed")
        for chk in r["independent_checks"]:
            enum(qid, "check", chk.get("kind"))
            if not chk.get("check"):
                fail(qid, "each independent check must be written out")
        for hyp in r["wrong_route_hypotheses"]:
            if hyp.get("status") != "HYPOTHESIS":
                fail(qid, "wrong routes are HYPOTHESIS until her own work shows them")
            if not (hyp.get("route") and hyp.get("confirming_evidence") and hyp.get("alternative")):
                fail(qid, "each wrong route needs route, confirming_evidence and alternative")

        learner = r["learner"]
        enum(qid, "result", learner.get("result"))
        enum(qid, "confidence", learner.get("confidence"))
        enum(qid, "help", learner.get("help_exposure"))
        states = learner.get("prerequisite_state", {})
        for cap, state in states.items():
            enum(qid, "prereq", state)
        if r["mode"] == "QUESTION":
            observed = [k for k in ("attempt_ref", "committed_before_feedback", "original_answer", "reasoning",
                                    "failure_hypothesis") if learner.get(k) is not None]
            if observed or learner.get("result") != "NOT_EVALUATED" or learner.get("confidence") != "MISSING" \
                    or learner.get("help_exposure") != "NOT_APPLICABLE" or any(s != "UNKNOWN" for s in states.values()):
                fail(qid, "QUESTION mode has no attempt: learner fields must say nothing was observed")
        else:
            ref = learner.get("attempt_ref")
            if not ref:
                fail(qid, "EVIDENCE mode needs attempt_ref")
            elif attempts is not None and ref not in attempts:
                fail(qid, f"attempt {ref} is not in the attempts file")
            elif attempts is None:
                warn(qid, "attempts file not given, so attempt_ref was not checked")
            if learner.get("result") == "NOT_EVALUATED":
                warn(qid, "EVIDENCE mode with a result NOT_EVALUATED")
            independent = (learner.get("result") == "CORRECT" and learner.get("help_exposure") == "INDEPENDENT"
                           and learner.get("committed_before_feedback") is True)
            for cap, state in states.items():
                if state == "DEMONSTRATED" and not independent:
                    fail(qid, f"{cap} DEMONSTRATED needs a correct, independent answer committed before help (else UNCERTAIN)")

        enum(qid, "route", r["learning_route"].get("value"))
        if not r["learning_route"].get("reason"):
            fail(qid, "learning_route.reason is empty")

    for line in fails + warns:
        print(line)
    print(f"{len(overlay.get('records', []))} records: {len(fails)} FAIL, {len(warns)} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
