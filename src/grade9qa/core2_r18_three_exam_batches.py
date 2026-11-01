"""Read-only nine existing Core2 conditional exam source leads in three batches.

Source stems and figures remain private. Neither the user-generated per-cell
draft adapter versions nor these reports are academic/Owner approvals.
"""
from __future__ import annotations

import re

BLUEPRINT_SHA = "e6030a5933a803ddc39708414e6831c89c9565def78c09c99f58f95052c2b45f"
EXTRACT_SHA = "cfa7368f9504cc72c3f05fa61328a3086496e89f6eb56c389927d2673b895071"
BATCHES = {
    "BATCH-04_APPLY_D3": {
        "ids": ("EX-M105","EX-M62","EX-M79"), "operation":"APPLY","cell":"D3.3",
        "adapter_sha":"3d84e7c02a4058a38deb5cc28b00ff40dfdd32f1f7e080eadf32c3aa7b1f534c",
    },
    "BATCH-05_MODEL_D3": {
        "ids":("EX-M16","EX-M73","EX-M81"), "operation":"MODEL","cell":"D3.4",
        "adapter_sha":"f0ad6bfd114bdd7640ad784651809ecd934d8de66c1a9307b512e4e0887b1fd1",
    },
    "BATCH-06_REPRESENT_D3": {
        "ids":("EX-M56","EX-M61","EX-M69"), "operation":"REPRESENT","cell":"D3.5",
        "adapter_sha":"471edab47b5ad79e7323cf4d560e348b0de30da3689bcfe4762db460b24e31e2",
    },
}
BINDING_RISKS = {
    "EX-M62":"QRT_D3_V_D2_DISPUTE",
    "EX-M79":"APPLY_V_SYNTHESIZE_DISPUTE",
    "EX-M73":"SELECTED_MODEL_BUT_APPLY_ADAPTER_ANCHOR",
    "EX-M81":"MODEL_D3_V_SYNTHESIZE_D4_DISPUTE",
    "EX-M56":"FOUR_ORIGINAL_GRAPHS_UNBOUND",
    "EX-M61":"ORIGINAL_GRAPH_AND_INCORRECT_OPTION_KEY_DISPUTE",
    "EX-M69":"ORIGINAL_OPTION_GRAPHS_UNBOUND",
}
FORBIDDEN_FIELDS = {
    "stem", "options", "explanation", "official_key", "source_image_bytes",
    "native_html", "solution_html", "model_answer", "accepted_answer"
}

def audit_three_exam_batches(records: object) -> dict:
    issues=[]
    if not isinstance(records,list):
        return _report([("RECORD_LIST_REQUIRED","FAIL")],[])
    seen=set()
    sanitized=[]
    if len(records)!=9:
        issues.append(("NINE_EXISTING_CANDIDATES_REQUIRED","FAIL"))
    for i,r in enumerate(records):
        if not isinstance(r,dict):
            issues.append(("RECORD_NOT_OBJECT","FAIL"));continue
        sid=r.get("source_id")
        if not isinstance(sid,str) or not re.fullmatch(r"EX-M\d+",sid):
            issues.append(("INVALID_EXAM_LEAD_ID","FAIL"));continue
        if sid in seen:
            issues.append(("DUPLICATED_EXAM_LEAD_ID","FAIL"))
        seen.add(sid)
        batch=r.get("batch")
        cfg=BATCHES.get(batch)
        if cfg is None or sid not in cfg["ids"]:
            issues.append(("INCORRECT_BATCH_OR_SOURCE_ID","FAIL"));continue
        if r.get("qrt_blueprint_cell")!=cfg["cell"] or r.get("selected_operation_provisional")!=cfg["operation"] or r.get("selected_band_provisional")!="D3":
            issues.append(("PROVISIONAL_QRT_CELL_CHANGED","FAIL"))
        if r.get("blueprint_original_sha256")!=BLUEPRINT_SHA or r.get("draft_adapter_sha256")!=cfg["adapter_sha"] or r.get("original_extract_member_sha256")!=EXTRACT_SHA:
            issues.append(("ORIGINAL_SOURCE_OR_ADAPTER_BYTE_PIN_CHANGED","FAIL"))
        if r.get("draft_adapter_version")!="0.1.1" or r.get("draft_adapter_status")!="DRAFT_OWNER_REVIEW":
            issues.append(("UNREVIEWED_ADAPTER_UPGRADED_OR_CHANGED","FAIL"))
        if r.get("paper_and_official_key")!="NOT_AUTHENTICATED":
            issues.append(("UNTRUSTED_OFFICIAL_KEY_PROMOTION","FAIL"))
        if r.get("owner_selected_adapter")!="NOT_SELECTED":
            issues.append(("OWNER_ADAPTER_SELECTION_NOT_ATTESTED","FAIL"))
        if r.get("academic_admission")!="HOLD" or r.get("reviewer_decision")!="HOLD":
            issues.append(("UNAUTHORIZED_ACADEMIC_ADMISSION","FAIL"))
        if r.get("native_html_admission")!="NOT_PERFORMED" or r.get("original_learner_html_modified") is not False:
            issues.append(("NATIVE_HTML_ADMISSION_FABRICATED","FAIL"))
        if any(k in r for k in FORBIDDEN_FIELDS):
            issues.append(("ORIGINAL_QUESTION_OR_SOLUTION_CONTENT_IN_METADATA","FAIL"))
        if r.get("draft_subtopic_fit_status")=="DRAFT_SUBTOPIC_EXACT_ANCHOR" and not r.get("draft_adapter_subtopic_candidate"):
            issues.append(("DRAFT_SUBTOPIC_ANCHOR_MISSING","FAIL"))
        if sid in BINDING_RISKS:
            issues.append(("EXPLICIT_REVIEW_RISK_"+BINDING_RISKS[sid],"HOLD"))
        sanitized.append({
            "source_id":sid,"batch":batch,"provisional_qrt_cell":cfg["cell"],
            "academic_status":"HOLD","source_paper_key":"UNVERIFIED",
            "owner_selected_adapter":False,"original_native_html_modified":False,
        })
    if seen!={x for v in BATCHES.values() for x in v["ids"]}:
        issues.append(("ORIGINAL_LOT_ONE_NINE_IDENTITIES_CHANGED","FAIL"))
    issues.extend((("NO_AUTHENTICATED_ORIGINAL_PAPER_KEY","HOLD"),
                   ("NO_INDEPENDENT_SL2_QRT_PHYSICS_APPROVAL","HOLD"),
                   ("NO_CANONICAL_SELECTED_WPE_ADAPTER","HOLD"),
                   ("SEVEN_VACANT_21_PLACES_NOT_FILLED","HOLD")))
    return _report(issues,sanitized)

def _report(issues,records):
    return {
        "schema_version":"1.0.0","audit_type":"PHYSICS_WPE_R18_3X3_EXAM_LEAD_REVIEW_GATE",
        "batch_counts":{name:sum(r["batch"]==name for r in records) for name in BATCHES},
        "identified_existing_leads":len(records),
        "distinct_exam_source_ids_added":0,"original_tb_html_cards_changed":0,
        "core2_21_conditional_count_unchanged":14,"core2_21_vacancies_unchanged":7,
        "mechanical_status":"FAIL" if any(sev=="FAIL" for _,sev in issues) else "HOLD",
        "academic_status":"HOLD","native_shared_admission":"NOT_PERFORMED",
        "release_status":"HOLD","source_metadata_only":records,
        "diagnostics":[{"code":code,"severity":sev} for code,sev in sorted(set(issues))],
        "warning":"Existing nine of fourteen conditional exam leads only; never treat third-party solutions or private calculations as official keys.",
    }
