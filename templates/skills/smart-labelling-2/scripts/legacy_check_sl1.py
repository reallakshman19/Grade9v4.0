"""Check a Smart Labelling 1 overlay (smart-labels-1.<topic>.v1.json).

Usage:
  python -X utf8 -I check_sl1.py <overlay.json> --library <subject library.json> --vocab <learner-question-metadata.v1.json>
Prints one line per problem and a summary; exit code 1 if anything FAILs.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from digest import item_digest, text_digest  # noqa: E402

SCHEMA = "g9v35-smart-labels-1/v1"
ENUMS = {
    "status": {"UNREVIEWED", "REVIEWED", "STALE"},
    "authority": {"JEE_MAIN", "NCERT", "CBSE", "TEXTBOOK", "ALLEN", "BYJUS", "AUTHORED", "OTHER"},
    "discovered_via": {"OFFICIAL", "EXAMSIDE", "TEXTBOOK_EXTRACT", "OWNER", "AGENT_RESEARCH", "OTHER"},
    "verification": {"VERIFIED", "PARTIAL", "UNVERIFIED"},
    "stage": {"GRADE9_CORE", "GRADE9_EXTENSION", "BRIDGE_10_12", "JEE_MAIN_TARGET"},
    "badge": {"EASY", "MEDIUM", "HARD"},
    "edge": {"ESSENTIAL", "SUPPORTING"},
    "figure": {"NONE", "HELPFUL", "ESSENTIAL"},
    "answer_check": {"AGREES", "DISAGREES", "NOT_CHECKED"},
    "figure_validated": {"VALIDATED", "NOT_VALIDATED", "NOT_APPLICABLE"},
    "rights": {"OWNER_LOCAL_ONLY", "OPEN", "UNKNOWN"},
    "duplicate": {"UNIQUE", "DUPLICATE", "VARIANT"},
    "action": {"READY_FOR_FIRST_TRY", "RESEARCH_SOURCE", "REPAIR_QUESTION", "QUALIFY_PREREQUISITE",
               "EXCLUDE_FROM_ASSESSMENT"},
}
GROUPS = ["question_id", "version", "status", "custody", "source_identity", "source_verification",
          "canonical_identity", "subject_classification", "curriculum_stage", "concept_difficulty",
          "prerequisites", "question_family", "format", "assessment_fitness", "content_integrity",
          "workflow_action", "learner_card"]
CARD_KEYS = {"title", "subject", "topic", "concept", "stage", "concept_badge", "format", "required", "hints"}
CARD_SPOILERS = re.compile(r"\b(answer|correct option|crux|solution|distractor|because)\b", re.I)
VERIFIED_ONLY = {"PYQ_VERIFIED", "PYQ_ADAPTED"}
PROTECTED_TEXT = {"JEE_MAIN", "TEXTBOOK", "ALLEN", "BYJUS", "NCERT", "CBSE"}
ID_RE = re.compile(r"^Q-[A-Z]+-[A-Z0-9]+-[A-Z0-9]+-[A-Za-z0-9.\-]+$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("overlay")
    ap.add_argument("--library", required=True)
    ap.add_argument("--vocab", required=True)
    a = ap.parse_args()
    overlay = json.loads(Path(a.overlay).read_text(encoding="utf-8"))
    library = json.loads(Path(a.library).read_text(encoding="utf-8"))
    vocab = json.loads(Path(a.vocab).read_text(encoding="utf-8"))
    microtopics = {m["id"]: m for m in library.get("microtopics", [])}
    capabilities = {c["id"] for c in library.get("capabilities", [])}
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
    for key in ("derivation_version", "topic", "library_ref", "vocabulary_ref", "labeller", "date", "records"):
        if key not in overlay:
            fail("file", f"missing {key}")

    seen = set()
    for r in overlay.get("records", []):
        qid = r.get("question_id", "?")
        missing = [g for g in GROUPS if g not in r]
        if missing:
            fail(qid, f"missing groups {missing}")
            continue
        if not ID_RE.match(qid):
            fail(qid, "question_id must look like Q-PHY-WPE-JEEM-M84")
        if qid in seen:
            fail(qid, "question_id repeated")
        seen.add(qid)
        enum(qid, "status", r["status"])
        stale = r["status"] == "STALE"

        custody = r["custody"]
        if not str(custody.get("item_digest", "")).startswith("sha256:"):
            fail(qid, "custody.item_digest missing")
        now = None
        if custody.get("text_file"):
            text_file = Path(custody["text_file"])
            now = text_digest(text_file) if text_file.exists() else None
        else:
            source = Path(custody.get("source_file", ""))
            if source.suffix == ".json" and source.exists():
                now = item_digest(source, custody.get("source_item_id"), custody.get("digest_fields"))
        if now is None:
            warn(qid, "source not readable here, so the digest was not re-checked")
        elif now != custody.get("item_digest") and not stale:
            fail(qid, "source text changed since labelling: mark STALE and re-label")

        identity, verification = r["source_identity"], r["source_verification"]
        enum(qid, "authority", identity.get("authority"))
        enum(qid, "discovered_via", identity.get("discovered_via"))
        enum(qid, "verification", verification.get("status"))
        provenance = verification.get("provenance")
        if provenance not in vocab.get("provenance", {}):
            fail(qid, f"provenance '{provenance}' is not in the vocabulary")
        if provenance in VERIFIED_ONLY and verification.get("status") != "VERIFIED":
            fail(qid, f"{provenance} needs status VERIFIED (official paper or key seen)")
        if not verification.get("basis"):
            fail(qid, "source_verification.basis is empty")

        classification = r["subject_classification"]
        refs = classification.get("microtopic_refs") or []
        if not refs:
            fail(qid, "microtopic_refs is empty (use [\"UNMAPPED\"] and say what is missing)")
        if refs == ["UNMAPPED"]:
            warn(qid, "UNMAPPED: say in missing_links what the library lacks")
        for ref in refs:
            if ref != "UNMAPPED" and ref not in microtopics:
                fail(qid, f"microtopic {ref} is not in the library")
        badge = r["concept_difficulty"].get("value")
        enum(qid, "badge", badge)
        if refs and refs[0] in microtopics:
            first = microtopics[refs[0]]
            if classification.get("primary_capability_ref") != first.get("primary_capability_ref"):
                warn(qid, f"primary capability differs from {refs[0]}'s {first.get('primary_capability_ref')}")
            if badge != first.get("intrinsic_badge"):
                fail(qid, f"concept_difficulty must be the library badge of {refs[0]}: {first.get('intrinsic_badge')}")
        enum(qid, "stage", r["curriculum_stage"].get("value"))
        if not r["curriculum_stage"].get("reason"):
            fail(qid, "curriculum_stage.reason is empty")

        for edge in r["prerequisites"].get("edges", []):
            enum(qid, "edge", edge.get("kind"))
            cap = edge.get("capability_ref", "")
            if cap not in capabilities:
                if cap.startswith("CAP-"):
                    warn(qid, f"prerequisite {cap} is from another topic: confirm it exists")
                else:
                    fail(qid, f"prerequisite '{cap}' is not a capability id")

        fmt = r["format"]
        if fmt.get("question_type") not in vocab.get("question_types", {}):
            fail(qid, f"question_type '{fmt.get('question_type')}' is not in the vocabulary")
        enum(qid, "figure", fmt.get("figure"))

        integrity = r["content_integrity"]
        check = integrity.get("answer_check", {})
        enum(qid, "answer_check", check.get("status"))
        if check.get("status") in ("AGREES", "DISAGREES") and not (check.get("worked_answer") and check.get("basis")):
            fail(qid, "answer_check needs worked_answer and basis")
        enum(qid, "figure_validated", integrity.get("figure_validated"))
        enum(qid, "rights", integrity.get("rights"))
        enum(qid, "duplicate", integrity.get("duplicate_status"))
        if identity.get("authority") in PROTECTED_TEXT and integrity.get("rights") != "OWNER_LOCAL_ONLY":
            fail(qid, "exam and book text is OWNER_LOCAL_ONLY")

        fitness, action = r["assessment_fitness"], r["workflow_action"]
        enum(qid, "action", action.get("value"))
        if not action.get("reason"):
            fail(qid, "workflow_action.reason is empty")
        if action.get("value") == "READY_FOR_FIRST_TRY":
            why = []
            if check.get("status") != "AGREES":
                why.append("answer not checked as AGREES")
            if fitness.get("first_try_ok") is not True:
                why.append("first_try_ok is not true")
            if fitness.get("ambiguity_found"):
                why.append("an ambiguity was found")
            if r.get("flags"):
                why.append(f"source flags {r['flags']}")
            if fmt.get("figure") == "ESSENTIAL" and integrity.get("figure_validated") != "VALIDATED":
                why.append("essential figure not validated")
            if why:
                fail(qid, "READY_FOR_FIRST_TRY is not allowed: " + "; ".join(why))

        card = r["learner_card"]
        extra = set(card) - CARD_KEYS
        if extra:
            fail(qid, f"learner_card has fields she must not see: {sorted(extra)}")
        card_text = " ".join(str(v) for v in card.values())
        spoiler = CARD_SPOILERS.search(card_text)
        if spoiler:
            fail(qid, f"learner_card gives too much away: '{spoiler.group(0)}'")
        worked = str(check.get("worked_answer") or "")
        if len(worked) >= 3 and worked in card_text:
            fail(qid, "learner_card contains the worked answer")

    for line in fails + warns:
        print(line)
    print(f"{len(overlay.get('records', []))} records: {len(fails)} FAIL, {len(warns)} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
