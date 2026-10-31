"""Native Shared Core2 representation applicability readback (Physics/WPE only).

Read-only, exact Owner source and Blueprint pins. Outputs question IDs and
reviewer *proposals*, never original textbook words, diagrams or answers.
Original Core2 REPRESENTATION is EXPECTED, not universally REQUIRED:
question-specific justified author waivers are allowed, with independent
review and proper native records. All academic/release outcomes remain HOLD.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PRODUCT = "WPE-CORE2-NATIVE-INTEGRATION-R1"
DIGEST = "a13a70605acf789d"
HTML_PIN = "44d052d8e163ab7e15e8ca13aba1cd90482cbb42df096a14a5a4e72c1f58a6a5"
RECEIPT_PIN = "8c5dcff73495b393927e55b902aa753fe7f9e014da3584a7790715c76e5c46bd"
SHARED_WEB_BLUEPRINT_PIN = "75f6bd43b31dfdf555fb26e8b36417e9c830a563898264dbe917d4254828653e"
RECORDS = ("TB-WPE-ILL-01","TB-WPE-ILL-02","TB-WPE-ILL-03",
           "TB-WPE-ILL-05","TB-WPE-ILL-06","TB-WPE-ILL-11")
SOLUTION_FIGURES = {
    "TB-WPE-ILL-02":"REP-TB-FIG-03-FBD-STRING-RAISING",
    "TB-WPE-ILL-11":"REP-TB-FIG-09-OVERHANGING-CHAIN",
}
# Authored proposal reasons, not copied passages or blanket permissions.
CANDIDATES = {
    "TB-WPE-ILL-01":("WAIVER_PROPOSAL","VECTOR_COMPONENTS_SUFFICIENT",
        "The component-form vectors may suffice; a drawing risks introducing an unstated spatial projection. Reviewer must determine whether a figure adds real interpretive value."),
    "TB-WPE-ILL-02":("WAIVER_PROPOSAL","SOLUTION_ONLY_FBD",
        "Existing derived force-balance representation is solution-only. Review whether an additional neutral string-and-mass sketch would be redundant; never expose worked force relations before attempt."),
    "TB-WPE-ILL-03":("AUTHOR_NEUTRAL_CANDIDATE","VARIABLE_FORCE_GRAPH_HELPFUL",
        "A force-versus-position illustration may help interpret the stated relation. Use only stem-supplied law and bounds; no numerical integral, work result or added physical assumption."),
    "TB-WPE-ILL-05":("SOURCE_PHYSICS_HOLD","INITIAL_CONDITION_NOT_SPECIFIED",
        "Source/Physics review must resolve the unstated starting speed. A diagram or component waiver cannot cure an underdetermined question."),
    "TB-WPE-ILL-06":("WAIVER_PROPOSAL","MATHEMATICAL_LAW_SUFFICIENT",
        "The given circular-motion law and radius may be self-sufficient. Reviewer must establish that a generic circle would add meaningful understanding without leading the inference."),
    "TB-WPE-ILL-11":("AUTHOR_SAFE_SOURCE_PROJECTION","SOLUTION_FIGURE_EXPOSES_RESULT",
        "Existing chain diagram is solution-only and contains result-bearing material. A separate neutral geometry must be source-checked, answer-free and independently accepted."),
}
ARTICLE = re.compile(r'<article\b[^>]*\bdata-g9-unit="([A-Za-z0-9-]+)"[^>]*>(.*?)</article>', re.S)
FIGURE = re.compile(r'<figure\b[^>]*\bdata-g9-representation="([A-Za-z0-9-]+)"[^>]*>', re.S)
TEMPLATE = re.compile(r'<template\b[^>]*>.*?</template>', re.S)


def card_figures(html: str) -> dict[str,list[dict]]:
    figures={}
    for match in ARTICLE.finditer(html):
        rid,body=match.groups()
        if rid in figures:
            raise ValueError("DUPLICATE_NATIVE_QUESTION_ID")
        template_spans=[(x.start(),x.end()) for x in TEMPLATE.finditer(body)]
        figures[rid]=[
            {"figure_id":m.group(1),
             "phase":"POST_ATTEMPT_TEMPLATE" if any(a<=m.start()<b for a,b in template_spans)
                     else "PRE_ATTEMPT_DOM"}
            for m in FIGURE.finditer(body)
        ]
    return figures


def core2_blueprint(registry: object) -> dict:
    if not isinstance(registry,dict) or not isinstance(registry.get("blueprints"),list):
        raise ValueError("SHARED_NATIVE_BLUEPRINT_REGISTRY_INVALID")
    matches=[x for x in registry["blueprints"] if isinstance(x,dict)
             and x.get("id")=="BP-CORE2-SOURCE-QUESTION"
             and x.get("status")=="ACTIVE" and "CORE2" in (x.get("core_roles") or [])]
    if len(matches)!=1:
        raise ValueError("ACTIVE_CORE2_BLUEPRINT_NOT_UNIQUE")
    bp=matches[0]
    reps=[x for x in bp.get("components",[]) if x.get("id")=="REPRESENTATION"]
    if (len(reps)!=1 or reps[0].get("level")!="EXPECTED" or reps[0].get("min_items")!=1
            or "waive" not in (reps[0].get("authoring") or {}).get("hint","")):
        raise ValueError("NATIVE_REPRESENTATION_APPLICABILITY_CONTRACT_CHANGED")
    return bp


def inspect_original(original_html: bytes, original_receipt: bytes,
                     original_web_blueprints: bytes,
                     *, html_pin: str = HTML_PIN, receipt_pin: str = RECEIPT_PIN,
                     blueprint_pin: str = SHARED_WEB_BLUEPRINT_PIN) -> dict:
    for name,raw,pin in (("HTML",original_html,html_pin),
                         ("RECEIPT",original_receipt,receipt_pin),
                         ("BLUEPRINT",original_web_blueprints,blueprint_pin)):
        if hashlib.sha256(raw).hexdigest()!=pin:
            raise ValueError("OWNER_"+name+"_EXACT_BYTE_PIN_MISMATCH")
    html=original_html.decode("utf-8")
    receipt=json.loads(original_receipt)
    bp=core2_blueprint(json.loads(original_web_blueprints))
    root=re.search(r"<html\b[^>]+>",html)
    if not root or any(f'{key}="{val}"' not in root.group() for key,val in (
        ("data-g9-role","CORE2"),("data-g9-product",PRODUCT),
        ("data-g9-render-digest",DIGEST))):
        raise ValueError("ORIGINAL_NATIVE_CORE2_HTML_NOT_MATCHED")
    if (receipt.get("renderer")!="render_core/2" or receipt.get("digest")!=DIGEST
            or receipt.get("draft") is not True or receipt.get("held_to")!="REFERENCE"):
        raise ValueError("ORIGINAL_CORE2_RENDER_RECEIPT_NOT_MATCHED")
    gaps=receipt.get("gaps")
    if not isinstance(gaps,list) or len(gaps)!=10:
        raise ValueError("ORIGINAL_TEN_GAP_RECEIPT_CHANGED")
    missing={g.get("record") for g in gaps if isinstance(g,dict)
             and g.get("duty")=="AUTHOR_COMPONENT" and g.get("component")=="REPRESENTATION"}
    if missing!=set(RECORDS):
        raise ValueError("ORIGINAL_SIX_MISSING_REPRESENTATIONS_CHANGED")
    figures=card_figures(html)
    if len(figures)!=9 or not set(RECORDS).issubset(figures):
        raise ValueError("ORIGINAL_NINE_CORE2_CARDS_CHANGED")
    for rid in RECORDS:
        if any(x["phase"]=="PRE_ATTEMPT_DOM" for x in figures[rid]):
            raise ValueError("PREATTEMPT_FIGURE_CONTRADICTS_MISSING_COMPONENT")
    for rid,ref in SOLUTION_FIGURES.items():
        matches=[x for x in figures[rid] if x["figure_id"]==ref]
        if len(matches)!=1 or matches[0]["phase"]!="POST_ATTEMPT_TEMPLATE":
            raise ValueError("SOLUTION_ONLY_FIGURE_LEAK_OR_IDENTITY_CHANGED")
    tickets=[]
    for rid in RECORDS:
        action,code,reason=CANDIDATES[rid]
        tickets.append({
            "question_id":rid,"candidate_action":action,
            "proposed_rationale_code":code,"proposed_author_rationale":reason,
            "existing_figure_evidence":figures[rid],
            "native_waiver_extension_key":"grade9v3:component_waivers" if action=="WAIVER_PROPOSAL" else None,
            "native_waiver_applied":False,"new_diagram_authored":False,
            "source_physics_status":"HOLD","independent_reviewer_decision":"HOLD",
            "original_gap_status":"OPEN",
        })
    return {
        "schema_version":"1.0.0",
        "audit_type":"WPE_CORE2_NATIVE_REPRESENTATION_AUTHORING_DECISIONS",
        "native_blueprint_id":bp["id"],"native_blueprint_version":bp["version"],
        "native_component_level":"EXPECTED","specific_author_waiver_permitted":True,
        "original_html_sha256":hashlib.sha256(original_html).hexdigest(),
        "original_receipt_sha256":hashlib.sha256(original_receipt).hexdigest(),
        "original_blueprint_sha256":hashlib.sha256(original_web_blueprints).hexdigest(),
        "existing_native_cards":9,"missing_representation_records":len(tickets),
        "waiver_proposals":sum(t["candidate_action"]=="WAIVER_PROPOSAL" for t in tickets),
        "neutral_authoring_candidates":sum(t["candidate_action"].startswith("AUTHOR_") for t in tickets),
        "source_physics_holds":sum(t["candidate_action"]=="SOURCE_PHYSICS_HOLD" for t in tickets),
        "original_receipt_gaps":len(gaps),"original_receipt_modified":False,
        "native_question_bank_modified":False,
        "tickets":tickets,"mechanical_status":"HOLD","academic_status":"HOLD",
        "shared_native_acceptance":"NOT_PERFORMED","learner_release":"HOLD",
        "warning":"Recommendations only. No existing source questions, figures, solutions or native record modified; independent waiver/Physics/Owner decisions mandatory.",
    }


def main(argv=None):
    import argparse
    p=argparse.ArgumentParser(description="Read original six Core2 representation gaps, proposals only")
    p.add_argument("--original-html",required=True)
    p.add_argument("--render-receipt",required=True)
    p.add_argument("--shared-web-blueprints",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args(argv)
    paths=[Path(x).resolve() for x in (args.original_html,args.render_receipt,
                                       args.shared_web_blueprints,args.out)]
    if len(set(paths))!=4:
        raise ValueError("CANNOT_OVERWRITE_OWNER_ORIGINAL")
    result=inspect_original(*(p.read_bytes() for p in paths[:3]))
    paths[3].parent.mkdir(parents=True,exist_ok=True)
    paths[3].write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("CORE2-REPRESENTATION review=HOLD native-waiver=NOT_PERFORMED")
    return 3


if __name__=="__main__":
    raise SystemExit(main())
