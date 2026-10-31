"""Public-safe synthetic tests: real textbook stems and private SVGs never enter Git."""
import copy
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET

from grade9qa.core2_three_batch_gate import EXPECTED, inspect_three_batches


def neutral(rid):
    if rid.endswith("03"):
        text="F(x) = 10 + 0.50x; x 2.0"
    else:
        text="2ℓ / 3 on table; Overhang"
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 344" '
            'role="img" aria-labelledby="title desc"><title id="title">Synthetic neutral</title>'
            '<desc id="desc">Synthetic only, no sourced question</desc>'
            f'<text x="10" y="50">{text}</text></svg>')


def make(tmp_path):
    root=tmp_path/"private"
    root.mkdir()
    for label,ids in EXPECTED.items():
        folder=root/label;folder.mkdir()
        (folder/"batch-manifest.json").write_text(json.dumps({
            "ids":list(ids),"original_native_gaps_still_open":10,
            "owner_decision":"PENDING","academic_status":"HOLD",
        }))
    w=root/"BATCH-01"/"waiver-proposals-NOT-APPLIED.json"
    w.write_text(json.dumps({"DO_NOT_APPLY_TO_ORIGINAL_BANK":True,
        "owner_approval":"NOT_SUPPLIED",
        "native_waiver_extension_key":"grade9v3:component_waivers",
        "proposals":[{"question_id":x} for x in EXPECTED["BATCH-01"]]}))
    assets=root/"BATCH-02"/"svg";assets.mkdir()
    rows=[]
    for rid in EXPECTED["BATCH-02"]:
        path=assets/(rid+".svg")
        path.write_text(neutral(rid))
        rows.append({"question_id":rid,"svg_candidate":"svg/"+rid+".svg",
                     "svg_sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    (root/"BATCH-02"/"candidate-asset-bindings-NOT-IN-NATIVE.json").write_text(json.dumps({
        "status":"AUTHOR_CANDIDATES_UNREVIEWED",
        "native_figure_refs_modified":0,"assets":rows}))
    (root/"BATCH-03"/"physics-source-hold.json").write_text(json.dumps({
        "question_id":"TB-WPE-ILL-05",
        "initial_speed_specified_in_extracted_problem":False,
        "source_repair_authorized":False,
        "native_question_changed":False,"academic_status":"HOLD",
    }))
    return root


def diag(report):
    return {x["code"] for x in report["diagnostics"]}


def test_all_three_batches_are_exact_3_2_1(tmp_path):
    result=inspect_three_batches(make(tmp_path))
    assert [len(x["question_ids"]) for x in result["lots"]]==[3,2,1]
    assert result["identified_records"]==6
    assert result["mechanical_status"]=="HOLD"
    assert result["core2_exam_admissions"]==0


def test_private_svg_candidates_not_native_admitted(tmp_path):
    r=inspect_three_batches(make(tmp_path))
    assert len(r["candidate_svg_assets"])==2
    assert r["waivers_authorized"]==r["neutral_assets_bound_to_native"]==0
    assert r["original_renderer_receipt_gaps_closed"]==0


def test_waiver_autoapproval_rejected(tmp_path):
    root=make(tmp_path);p=root/"BATCH-01"/"waiver-proposals-NOT-APPLIED.json"
    x=json.loads(p.read_text());x["DO_NOT_APPLY_TO_ORIGINAL_BANK"]=False;p.write_text(json.dumps(x))
    assert "UNAUTHORIZED_WAIVER_OR_SCOPE_CHANGED" in diag(inspect_three_batches(root))


def test_reject_wrong_batch_identity(tmp_path):
    root=make(tmp_path);p=root/"BATCH-03"/"batch-manifest.json"
    x=json.loads(p.read_text());x["ids"]=["TB-WPE-ILL-06"];p.write_text(json.dumps(x))
    assert "BATCH_IDENTITY_OR_GAP_COUNT_MISMATCH" in diag(inspect_three_batches(root))


def test_duplicate_question_across_batches_rejected(tmp_path):
    root=make(tmp_path);p=root/"BATCH-03"/"batch-manifest.json"
    x=json.loads(p.read_text());x["ids"]=["TB-WPE-ILL-03"];p.write_text(json.dumps(x))
    assert "QUESTION_DUPLICATED_ACROSS_BATCHES" in diag(inspect_three_batches(root))


def test_svg_tamper_hash_mismatch(tmp_path):
    root=make(tmp_path)
    p=root/"BATCH-02"/"svg"/"TB-WPE-ILL-03.svg"
    p.write_text(p.read_text().replace("0.50x","1.50x"))
    assert "FIGURE_SOURCE_HASH_MISMATCH" in diag(inspect_three_batches(root))


def test_answer_leak_script_rejected_even_if_hash_adjusted(tmp_path):
    root=make(tmp_path)
    p=root/"BATCH-02"/"svg"/"TB-WPE-ILL-03.svg"
    x=p.read_text().replace("</svg>","<script>alert(1)</script></svg>")
    p.write_text(x)
    manifest=root/"BATCH-02"/"candidate-asset-bindings-NOT-IN-NATIVE.json"
    m=json.loads(manifest.read_text())
    m["assets"][0]["svg_sha256"]=hashlib.sha256(p.read_bytes()).hexdigest()
    manifest.write_text(json.dumps(m))
    assert "ANSWER_OR_EXTERNAL_SVG_CONTENT_DETECTED" in diag(inspect_three_batches(root))


def test_answer_result_rejected_even_if_hash_adjusted(tmp_path):
    root=make(tmp_path)
    p=root/"BATCH-02"/"svg"/"TB-WPE-ILL-11.svg"
    p.write_text(p.read_text().replace("</svg>","<text>K = 21 J</text></svg>"))
    m=root/"BATCH-02"/"candidate-asset-bindings-NOT-IN-NATIVE.json"
    rows=json.loads(m.read_text())
    rows["assets"][1]["svg_sha256"]=hashlib.sha256(p.read_bytes()).hexdigest()
    m.write_text(json.dumps(rows))
    assert "ANSWER_OR_EXTERNAL_SVG_CONTENT_DETECTED" in diag(inspect_three_batches(root))


def test_native_figure_binding_without_approval_rejected(tmp_path):
    root=make(tmp_path);m=root/"BATCH-02"/"candidate-asset-bindings-NOT-IN-NATIVE.json"
    rows=json.loads(m.read_text());rows["native_figure_refs_modified"]=2;m.write_text(json.dumps(rows))
    assert "FIGURE_ADDED_TO_NATIVE_WITHOUT_APPROVAL" in diag(inspect_three_batches(root))


def test_ill05_unsupported_rest_assumption_rejected(tmp_path):
    root=make(tmp_path);p=root/"BATCH-03"/"physics-source-hold.json"
    x=json.loads(p.read_text());x["initial_speed_specified_in_extracted_problem"]=True;p.write_text(json.dumps(x))
    assert "INITIAL_SPEED_UNSUPPORTED_PROMOTION" in diag(inspect_three_batches(root))


def test_source_correction_without_review_rejected(tmp_path):
    root=make(tmp_path);p=root/"BATCH-03"/"physics-source-hold.json"
    x=json.loads(p.read_text());x["source_repair_authorized"]=True;p.write_text(json.dumps(x))
    assert "INITIAL_SPEED_UNSUPPORTED_PROMOTION" in diag(inspect_three_batches(root))


def test_unreviewed_originals_hold_not_fake_complete(tmp_path):
    result=inspect_three_batches(make(tmp_path))
    assert "OWNER_ORIGINAL_EVIDENCE_NOT_ATTACHED" in diag(result)
    assert result["academic_status"]==result["native_release"]=="HOLD"


def test_original_hash_mismatch_fails_closed(tmp_path):
    root=make(tmp_path);original=tmp_path/"wrong.zip";original.write_bytes(b"not the original")
    result=inspect_three_batches(root,sources=original)
    assert result["mechanical_status"]=="FAIL"
    assert "OWNER_ORIGINAL_BYTE_PIN_MISMATCH" in diag(result)


def test_public_report_does_not_echo_private_question_words(tmp_path):
    root=make(tmp_path)
    (root/"BATCH-01"/"PRIVATE_STEM.txt").write_text("UNPUBLISHED_SOURCE_STEM")
    result=inspect_three_batches(root)
    assert "UNPUBLISHED_SOURCE_STEM" not in json.dumps(result)


def test_native_receipt_is_never_claimed_regenerated(tmp_path):
    result=inspect_three_batches(make(tmp_path))
    assert result["original_renderer_receipt_gaps_closed"]==0
    assert result["native_questions_changed"]==0
