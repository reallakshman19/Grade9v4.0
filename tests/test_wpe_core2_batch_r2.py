"""Core-2 R2 high-ROI batch: source custody, hint separation and exact record parity."""
from pathlib import Path
import json
import re
import hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102"
BANK=OUT/"native-candidate/selected_bank.review.json"
PAGE=ROOT/"preview/question-status.html"
AUDIT=OUT/"review/BATCH_R2_HIGHROI_AUDIT.json"
MANIFEST=OUT/"MANIFEST.review.json"

def read():
    bank=json.loads(BANK.read_text(encoding="utf-8"))
    html=PAGE.read_text(encoding="utf-8")
    m=re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>',html,re.S)
    assert m, "missing embedded data"
    embedded=json.loads(m.group(1))
    return bank,html,embedded

def q(bank,source_id):
    found=[item for item in bank["questions"] if item["source_id"]==source_id]
    assert len(found)==1
    return found[0]

def test_exact_candidate_and_page_question_parity():
    b,h,e=read()
    assert b["academic_admission"]=="NOT_ADMITTED"
    assert len(b["questions"])==len(e["questions"])==74
    assert b["questions"]==e["questions"]
    assert len({x["id"] for x in b["questions"]})==74
    assert "if(!s?.committed)return" in h

def test_authored_cues_are_separate_from_original_hint_custody():
    b,h,_=read()
    a=json.loads(AUDIT.read_text(encoding="utf-8"))
    covered=[x for x in b["questions"] if x.get("scaffolds")]
    assert len(covered)==29
    assert {x["source_id"] for x in covered}==set(a["changed_questions"])
    assert "q.scaffolds?.length?q.scaffolds:q.hints" in h
    for x in covered:
        assert len(x["hints"])>0
        assert len(x["scaffolds"])>=2
        assert all(y["origin"]=="AUTHORED_PEDAGOGICAL" and y["reveals"]=="HINT_ONLY" for y in x["scaffolds"])
        assert all("crux move:" not in y["text"].lower() for y in x["scaffolds"])

def test_specific_wrong_science_corrected_without_false_admission():
    b,_,_=read()
    s=q(b,"EX-M101")
    assert "path independence" in " ".join(x["text"].lower() for x in s["hints"])
    assert "equal stretches" in " ".join(x["text"].lower() for x in s["scaffolds"])
    assert "k1<k2" in s["steps"][2] and "W1=2 W2" in s["check"]
    assert "Do not substitute gravitational potential" in s["steps"][0]
    p=q(b,"EX-M61")
    assert p["answer"].startswith("Source/coaching proposal: B, NOT VERIFIED")
    r=q(b,"JEE-2026-04-06-S1-Q28")
    assert "-9.9875" in r["answer"] and "-9.99" in r["answer"] and "-9.98" in r["answer"]
    t=q(b,"TB-WPE-ILL-11")
    assert "K_initial" in t["answer"]
    x=q(b,"EX-M2")
    assert "7.75" in x["answer"] and "7.74" in x["answer"]
    y=q(b,"EX-M39")
    assert "4/5" in y["check"] and "3/5" in y["check"]

def test_raw_stems_are_identity_preserved():
    b,_,_=read()
    for x in b["questions"]:
        assert len(x["stem_sha256"])==64
    for source_id,digest in {
      "EX-M101": "c6caf00ac4069a7c971ef146bba439ffb17602663de90cb408c805f887fc639c",
    }.items():
        item=q(b,source_id)
        assert hashlib.sha256(item["stem"].encode("utf-8")).hexdigest()==item["stem_sha256"]

def test_flag_disposition_and_scanned_hints():
    b,_,_=read()
    a=json.loads(AUDIT.read_text(encoding="utf-8"))
    assert a["role"]=="AUTHOR_ORACLE_SELF_ASSESSED_NOT_INDEPENDENT"
    assert len(a["review_flags"])==16
    assert a["question_inventory"]["with_literal_crux_move_pre_attempt_hint"]==sum(
       any("crux move" in h["text"].lower() for h in item["hints"])
       for item in b["questions"])
    assert all(f["academic_acceptance"]=="NOT_RUN" for f in a["review_flags"])

def test_manifest_exact_git_blob_ids():
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    for path in [BANK,PAGE,AUDIT,OUT/"review/BATCH_R2_HIGHROI_README.md"]:
        relative=path.relative_to(ROOT).as_posix()
        rows=[x for x in manifest["artifacts"] if x["path"]==relative]
        assert len(rows)==1
        raw=path.read_bytes()
        sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
        assert sha==rows[0]["sha"]
