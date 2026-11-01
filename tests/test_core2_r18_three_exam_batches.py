"""Synthetic, source-free regressions for 3x3 exam-review batches."""
import copy
from grade9qa.core2_r18_three_exam_batches import (
    BATCHES,BLUEPRINT_SHA,EXTRACT_SHA,BINDING_RISKS,audit_three_exam_batches
)

def rows():
    return [
        {"source_id":sid,"batch":batch,
         "qrt_blueprint_cell":cfg["cell"],
         "selected_operation_provisional":cfg["operation"],
         "selected_band_provisional":"D3",
         "blueprint_original_sha256":BLUEPRINT_SHA,
         "draft_adapter_sha256":cfg["adapter_sha"],
         "original_extract_member_sha256":EXTRACT_SHA,
         "draft_adapter_version":"0.1.1",
         "draft_adapter_status":"DRAFT_OWNER_REVIEW",
         "draft_subtopic_fit_status":"CROSS_CELL_ANCHOR_CONFLICT" if sid=="EX-M73" else "NOT_AUTHORITY",
         "draft_adapter_subtopic_candidate":None,
         "paper_and_official_key":"NOT_AUTHENTICATED",
         "owner_selected_adapter":"NOT_SELECTED",
         "academic_admission":"HOLD",
         "reviewer_decision":"HOLD",
         "native_html_admission":"NOT_PERFORMED",
         "original_learner_html_modified":False,
        }
        for batch,cfg in BATCHES.items() for sid in cfg["ids"]
    ]

def codes(data):
    return {x["code"] for x in data["diagnostics"]}

def test_3x3_existing_source_review_counts():
    r=audit_three_exam_batches(rows())
    assert r["batch_counts"]=={x:3 for x in BATCHES}
    assert r["identified_existing_leads"]==9
    assert r["mechanical_status"]=="HOLD"
    assert r["core2_21_conditional_count_unchanged"]==14
    assert r["core2_21_vacancies_unchanged"]==7

def test_no_html_duplicate_or_admission():
    r=audit_three_exam_batches(rows())
    assert r["original_tb_html_cards_changed"]==0
    assert r["distinct_exam_source_ids_added"]==0
    assert r["academic_status"]==r["release_status"]=="HOLD"

def test_duplicate_source_fails():
    d=rows();d[1]["source_id"]=d[0]["source_id"]
    assert "DUPLICATED_EXAM_LEAD_ID" in codes(audit_three_exam_batches(d))

def test_hypothetical_new_exam_id_fails():
    d=rows();d[1]["source_id"]="EX-M999"
    assert "INCORRECT_BATCH_OR_SOURCE_ID" in codes(audit_three_exam_batches(d))

def test_wrong_operation_fails():
    d=rows();d[4]["selected_operation_provisional"]="APPLY"
    assert "PROVISIONAL_QRT_CELL_CHANGED" in codes(audit_three_exam_batches(d))

def test_m73_cross_cell_risk_never_silent():
    r=audit_three_exam_batches(rows())
    assert "EXPLICIT_REVIEW_RISK_SELECTED_MODEL_BUT_APPLY_ADAPTER_ANCHOR" in codes(r)

def test_m61_source_key_dispute_retained():
    r=audit_three_exam_batches(rows())
    assert "EXPLICIT_REVIEW_RISK_ORIGINAL_GRAPH_AND_INCORRECT_OPTION_KEY_DISPUTE" in codes(r)

def test_wrong_blueprint_byte_hash_fails():
    d=rows();d[0]["blueprint_original_sha256"]="0"*64
    assert "ORIGINAL_SOURCE_OR_ADAPTER_BYTE_PIN_CHANGED" in codes(audit_three_exam_batches(d))

def test_wrong_adapter_hash_fails():
    d=rows();d[0]["draft_adapter_sha256"]="0"*64
    assert "ORIGINAL_SOURCE_OR_ADAPTER_BYTE_PIN_CHANGED" in codes(audit_three_exam_batches(d))

def test_draft_upgrade_without_review_fails():
    d=rows();d[0]["draft_adapter_status"]="APPROVED"
    assert "UNREVIEWED_ADAPTER_UPGRADED_OR_CHANGED" in codes(audit_three_exam_batches(d))

def test_fake_official_key_authentication_fails():
    d=rows();d[0]["paper_and_official_key"]="AUTHENTICATED"
    assert "UNTRUSTED_OFFICIAL_KEY_PROMOTION" in codes(audit_three_exam_batches(d))

def test_fake_owner_adapter_selection_fails():
    d=rows();d[0]["owner_selected_adapter"]="SELECTED"
    assert "OWNER_ADAPTER_SELECTION_NOT_ATTESTED" in codes(audit_three_exam_batches(d))

def test_fake_academic_admission_fails():
    d=rows();d[0]["academic_admission"]="ACCEPTED"
    assert "UNAUTHORIZED_ACADEMIC_ADMISSION" in codes(audit_three_exam_batches(d))

def test_forged_native_html_fails():
    d=rows();d[0]["native_html_admission"]="RENDERED"
    assert "NATIVE_HTML_ADMISSION_FABRICATED" in codes(audit_three_exam_batches(d))

def test_copying_exam_stem_into_repo_data_fails():
    d=rows();d[0]["stem"]="PRIVATE_EXAM_TEXT"
    r=audit_three_exam_batches(d)
    assert "ORIGINAL_QUESTION_OR_SOLUTION_CONTENT_IN_METADATA" in codes(r)
    assert "PRIVATE_EXAM_TEXT" not in str(r)

def test_exact_subtopic_anchor_must_have_id():
    d=rows();d[0]["draft_subtopic_fit_status"]="DRAFT_SUBTOPIC_EXACT_ANCHOR"
    assert "DRAFT_SUBTOPIC_ANCHOR_MISSING" in codes(audit_three_exam_batches(d))

def test_figure_risk_for_all_three_represent_cases():
    r=audit_three_exam_batches(rows())
    c=codes(r)
    assert "EXPLICIT_REVIEW_RISK_FOUR_ORIGINAL_GRAPHS_UNBOUND" in c
    assert "EXPLICIT_REVIEW_RISK_ORIGINAL_OPTION_GRAPHS_UNBOUND" in c
    assert "EXPLICIT_REVIEW_RISK_ORIGINAL_GRAPH_AND_INCORRECT_OPTION_KEY_DISPUTE" in c
