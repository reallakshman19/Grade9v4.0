"""Three-batch WPE Core2 R17 independent-review preflight; no approvals.

The source diagram SVGs and copyrighted textbook stems are intentionally
private Owner-local artifacts, not public repository materials.
Scope: Physics/WPE only; original nine native cards unchanged.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

EXPECTED = {
    "BATCH-01":("TB-WPE-ILL-01","TB-WPE-ILL-02","TB-WPE-ILL-06"),
    "BATCH-02":("TB-WPE-ILL-03","TB-WPE-ILL-11"),
    "BATCH-03":("TB-WPE-ILL-05",),
}
SOURCE_ARCHIVE_SHA256="ed0880d9ff314853c084834f2a8ac4ced69d2b8f5b019612ca999a1222b20565"
HTML_SHA256="44d052d8e163ab7e15e8ca13aba1cd90482cbb42df096a14a5a4e72c1f58a6a5"
RECEIPT_SHA256="8c5dcff73495b393927e55b902aa753fe7f9e014da3584a7790715c76e5c46bd"
BAD_SVG=re.compile(r"(?i)<script\b|<foreignObject\b|<image\b|<use\b|(?:xlink:)?href\s*=|url\s*\(|(?:kinetic\s+energy|integral|work\s+done)\s*=|\b21\s*J\b")
SVG_NS="{http://www.w3.org/2000/svg}"

def _issue(issues, code, subject, severity="FAIL"):
    issues.append({"code":code,"subject":subject,"severity":severity})

def _hash(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        while data:=f.read(1048576):
            h.update(data)
    return h.hexdigest()

def inspect_three_batches(root:Path, *, sources:Path|None=None,
                          native_html:Path|None=None, native_receipt:Path|None=None) -> dict:
    root=Path(root)
    issues=[]; rows=[]; assets=[]
    # Sources are optional at reviewer workstations but mismatches are never ignored.
    for label,path,pin in (("SOURCE_ARCHIVE",sources,SOURCE_ARCHIVE_SHA256),
                           ("ORIGINAL_HTML",native_html,HTML_SHA256),
                           ("ORIGINAL_RECEIPT",native_receipt,RECEIPT_SHA256)):
        if path is None:
            _issue(issues,"OWNER_ORIGINAL_EVIDENCE_NOT_ATTACHED",label,"HOLD")
        elif _hash(path)!=pin:
            _issue(issues,"OWNER_ORIGINAL_BYTE_PIN_MISMATCH",label)
    if native_receipt is not None and _hash(native_receipt)==RECEIPT_SHA256:
        receipt=json.loads(Path(native_receipt).read_bytes())
        if (len(receipt.get("gaps",[]))!=10 or receipt.get("draft") is not True
                or receipt.get("held_to")!="REFERENCE"):
            _issue(issues,"NATIVE_10_GAP_DRAFT_RECEIPT_CHANGED","RECEIPT")
    ids=set()
    for label, expected in EXPECTED.items():
        manifest=root/label/"batch-manifest.json"
        if not manifest.is_file():
            _issue(issues,"BATCH_MANIFEST_MISSING",label)
            continue
        doc=json.loads(manifest.read_text("utf8"))
        if doc.get("ids")!=list(expected) or doc.get("original_native_gaps_still_open")!=10:
            _issue(issues,"BATCH_IDENTITY_OR_GAP_COUNT_MISMATCH",label)
        if doc.get("owner_decision")!="PENDING" or doc.get("academic_status")!="HOLD":
            _issue(issues,"FORGED_BATCH_APPROVAL",label)
        for rid in doc.get("ids",[]):
            if rid in ids:
                _issue(issues,"QUESTION_DUPLICATED_ACROSS_BATCHES",rid)
            ids.add(rid)
            rows.append({"batch":label,"question_id":rid,"academic_status":"HOLD"})
    if ids != set(sum((list(x) for x in EXPECTED.values()),[])):
        _issue(issues,"SIX_RECORD_COVERAGE_CHANGED","GENERAL")
    waiver=root/"BATCH-01"/"waiver-proposals-NOT-APPLIED.json"
    if not waiver.is_file():_issue(issues,"WAIVER_DRAFTS_MISSING","BATCH-01")
    else:
        proposals=json.loads(waiver.read_text("utf8"))
        if (proposals.get("DO_NOT_APPLY_TO_ORIGINAL_BANK") is not True
                or proposals.get("owner_approval")!="NOT_SUPPLIED"
                or proposals.get("native_waiver_extension_key")!="grade9v3:component_waivers"
                or {r.get("question_id") for r in proposals.get("proposals",[])}!=set(EXPECTED["BATCH-01"])):
            _issue(issues,"UNAUTHORIZED_WAIVER_OR_SCOPE_CHANGED","BATCH-01")
    bindings=root/"BATCH-02"/"candidate-asset-bindings-NOT-IN-NATIVE.json"
    if not bindings.is_file():_issue(issues,"NEUTRAL_ASSET_MANIFEST_MISSING","BATCH-02")
    else:
        data=json.loads(bindings.read_text("utf8"))
        if data.get("native_figure_refs_modified") != 0 or data.get("status")!="AUTHOR_CANDIDATES_UNREVIEWED":
            _issue(issues,"FIGURE_ADDED_TO_NATIVE_WITHOUT_APPROVAL","BATCH-02")
        refs=set()
        for record in data.get("assets",[]):
            rid=record.get("question_id")
            refs.add(rid)
            rel=record.get("svg_candidate")
            if not isinstance(rel,str) or rel.startswith("/") or ".." in Path(rel).parts or not rel.endswith(".svg"):
                _issue(issues,"INVALID_ASSET_PATH",str(rid));continue
            file=root/"BATCH-02"/rel
            if not file.is_file() or _hash(file)!=record.get("svg_sha256"):
                _issue(issues,"FIGURE_SOURCE_HASH_MISMATCH",str(rid));continue
            try:
                content=file.read_text("utf8")
                doc=ET.fromstring(content)
            except (UnicodeError,ET.ParseError):
                _issue(issues,"SVG_XML_INVALID",str(rid));continue
            if doc.tag!=SVG_NS+"svg" or not doc.get("viewBox") or not doc.get("aria-labelledby"):
                _issue(issues,"SVG_ACCESSIBILITY_OR_VIEWBOX_INVALID",str(rid))
            if not doc.find(SVG_NS+"title") is not None or doc.find(SVG_NS+"desc") is None:
                _issue(issues,"SVG_TITLE_DESCRIPTION_MISSING",str(rid))
            if BAD_SVG.search(content):
                _issue(issues,"ANSWER_OR_EXTERNAL_SVG_CONTENT_DETECTED",str(rid))
            if rid=="TB-WPE-ILL-03" and ("F(x) = 10 + 0.50x" not in content or "2.0" not in content):
                _issue(issues,"SOURCE_GIVEN_FORCE_OR_INTERVAL_CHANGED",rid)
            if rid=="TB-WPE-ILL-11" and ("2ℓ / 3 on table" not in content or "Overhang" not in content):
                _issue(issues,"SOURCE_GIVEN_CHAIN_CONFIGURATION_CHANGED",rid)
            assets.append({"question_id":rid,"source_sha256":record["svg_sha256"],
                           "native_figure_bound":False,"approved":False})
        if refs != set(EXPECTED["BATCH-02"]):
            _issue(issues,"TWO_NEUTRAL_ASSET_IDENTITIES_CHANGED","BATCH-02")
    hold=root/"BATCH-03"/"physics-source-hold.json"
    if not hold.is_file():_issue(issues,"SOURCE_PHYSICS_HOLD_MISSING","BATCH-03")
    else:
        case=json.loads(hold.read_text("utf8"))
        if (case.get("question_id")!="TB-WPE-ILL-05" or
            case.get("initial_speed_specified_in_extracted_problem") is not False or
            case.get("source_repair_authorized") is not False or
            case.get("native_question_changed") is not False or
            case.get("academic_status")!="HOLD"):
            _issue(issues,"INITIAL_SPEED_UNSUPPORTED_PROMOTION","BATCH-03")
    return {"schema_version":"1.0.0","audit_type":"PHYS_WPE_CORE2_R17_THREE_BATCH_OWNER_PREFLIGHT",
            "lots":[{"batch":key,"question_ids":list(value)} for key,value in EXPECTED.items()],
            "identified_records":len(ids),"native_questions_changed":0,
            "waivers_authorized":0,"neutral_assets_bound_to_native":0,
            "original_renderer_receipt_gaps_closed":0,
            "candidate_svg_assets":assets,"academic_status":"HOLD",
            "core2_exam_admissions":0,"native_release":"HOLD",
            "mechanical_status":"FAIL" if any(x["severity"]=="FAIL" for x in issues) else "HOLD",
            "diagnostics":sorted(issues,key=lambda x:(x["subject"],x["code"])),
            "warning":"Private proposed applicability/authoring only; neither academic approval nor original Shared native render receipt."}

def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description="Three WPE Core2 batches: review preflight only")
    parser.add_argument("--private-root",required=True)
    parser.add_argument("--sources")
    parser.add_argument("--native-html")
    parser.add_argument("--render-receipt")
    parser.add_argument("--out",required=True)
    a=parser.parse_args(argv)
    output=Path(a.out).resolve()
    inputs=[Path(x).resolve() for x in (a.sources,a.native_html,a.render_receipt) if x]
    if output in inputs or output.is_relative_to(Path(a.private_root).resolve()):
        raise ValueError("CANNOT_OVERWRITE_OWNER_SOURCE_OR_PRIVATE_BATCH")
    result=inspect_three_batches(Path(a.private_root),
                                sources=Path(a.sources) if a.sources else None,
                                native_html=Path(a.native_html) if a.native_html else None,
                                native_receipt=Path(a.render_receipt) if a.render_receipt else None)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("CORE2_R17_3BATCH mechanical="+result["mechanical_status"]+" academic=HOLD")
    return 1 if result["mechanical_status"]=="FAIL" else 3

if __name__=="__main__":
    raise SystemExit(main())
