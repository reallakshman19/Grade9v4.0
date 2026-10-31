"""Synthetic tests for Physics/WPE QRT Blueprint + topic adapter and four-lot controls."""
import copy
import csv
import hashlib
import json
from pathlib import Path

from grade9qa.cli import main
from grade9qa.core2_semantic import resolve_wpe_cells
from grade9qa.core2_inventory import audit_core2_coverage

OPS=("RETRIEVE","EXPLAIN","APPLY","MODEL","REPRESENT","SYNTHESIZE","JUSTIFY")
HASH="a"*64


def blueprint():
    return {
        "blueprint_id":"PHYS-QRT-BLUEPRINT","version":"0.2.0","status":"DRAFT_OWNER_REVIEW",
        "subject":"Physics","column_order":list(OPS),
        "cells":{f"D{band}.{k}":{"template_ref":f"QRT-{name}-D{band}"}
                 for band in (3,4) for k,name in enumerate(OPS,1)},
    }


def adapter():
    return {
        "adapter_id":"PHYS-TOPIC-WPE","version":"0.1.1","status":"DRAFT_OWNER_REVIEW",
        "subject":"Physics","topic_id":"WPE","for_blueprint":"PHYS-QRT-BLUEPRINT 0.2.0",
        "families":[{"id":f"WEP-{x:02d}"} for x in range(1,11)],
        "cells":{"D3.3":{
            "tile_id":"PHY-WPE-D3.3","blueprint_cell":"D3.3 (Apply, D3)",
            "subtopics":[{"id":"WPE-SYN","family_refs":["WEP-01"],
                          "canonical_refs":["SYN-PHYS-CAP-01"]}]
        }},
    }


def entry(**kwargs):
    obj={"source_id":"EX-SYN-1","operation":"APPLY","band":"D3",
         "topic_family":"WEP-01","capability_refs":["SYN-PHYS-CAP-01"]}
    obj.update(kwargs)
    return obj


def resolve(b=None,a=None,q=None,selected=HASH):
    return resolve_wpe_cells(
        blueprint() if b is None else b,adapter() if a is None else a,
        [entry()] if q is None else q,
        blueprint_digest=HASH,adapter_digest=HASH,selected_adapter_digest=selected)


def codes(r):
    return {x["code"] for x in r["diagnostics"]}


def test_valid_candidate_match_never_qualifies():
    r=resolve()
    assert r["mechanical_status"]=="HOLD"
    assert r["question_bindings"][0]["resolution"]=="STRUCTURAL_MATCH_CANDIDATE_ONLY"
    assert r["core2_admission"]=="NOT_PERFORMED"
    assert r["academic_status"]==r["release_status"]=="HOLD"
    assert {"BLUEPRINT_OWNER_APPROVAL_MISSING","WPE_ADAPTER_APPROVAL_MISSING",
            "OWNER_ADAPTER_SELECTION_NOT_INDEPENDENTLY_ATTESTED"}.issubset(codes(r))


def test_no_owner_selection_holds():
    assert "OWNER_ADAPTER_SELECTION_NOT_SUPPLIED" in codes(resolve(selected=None))


def test_wrong_adapter_digest_is_fail():
    r=resolve(selected="b"*64)
    assert "OWNER_SELECTION_ADAPTER_BYTE_MISMATCH" in codes(r)
    assert r["mechanical_status"]=="FAIL"


def test_blueprint_pin_mismatch_is_fail():
    a=adapter();a["for_blueprint"]="PHYS-QRT-BLUEPRINT 0.2.1"
    assert "BLUEPRINT_ADAPTER_VERSION_INCOMPATIBLE" in codes(resolve(a=a))


def test_latest_subtiles_require_matching_blueprint_version():
    a=adapter()
    a.pop("cells");a.pop("families")
    a["version"]="0.2.2"
    a["for_blueprint"]={"id":"PHYS-QRT-BLUEPRINT","version":"0.2.1"}
    a["subtiles"]={"D3.1.1":{"units":["SYN-CAP"]}}
    r=resolve(a=a)
    assert "BLUEPRINT_ADAPTER_VERSION_INCOMPATIBLE" in codes(r)


def test_missing_adapter_cell_is_hold():
    q=[entry(operation="MODEL")]
    r=resolve(q=q)
    assert "ADAPTER_CELL_UNWRITTEN" in codes(r)
    assert r["question_bindings"][0]["adapter_cell"] is None


def test_unreviewed_wpe_family_holds():
    assert "WPE_TOPIC_FAMILY_NOT_ADJUDICATED" in codes(resolve(q=[entry(topic_family=None)]))


def test_wrong_wpe_family_rejected():
    r=resolve(q=[entry(topic_family="WEP-04")])
    assert "ADAPTER_CELL_WRONG_TOPIC_FAMILY" in codes(r)
    assert r["mechanical_status"]=="FAIL"


def test_cross_subject_family_rejected():
    assert "WPE_TOPIC_FAMILY_INVALID" in codes(resolve(q=[entry(topic_family="MATHS-01")]))


def test_wrong_capability_ref_rejected():
    r=resolve(q=[entry(capability_refs=["SYN-PHYS-OTHER"])])
    assert "ADAPTER_CAPABILITY_FOREIGN_KEY_UNRESOLVED" in codes(r)
    assert r["mechanical_status"]=="FAIL"


def test_no_capability_ref_holds():
    assert "QRT_CAPABILITY_REVIEW_MISSING" in codes(resolve(q=[entry(capability_refs=[])]))


def test_d1_d2_do_not_sneak_into_d3_blueprint():
    r=resolve(q=[entry(band="D2")])
    assert "D1_D2_BLUEPRINT_NOT_AUTHORED" in codes(r)
    assert r["question_bindings"][0]["blueprint_cell"] is None


def test_corrupt_blueprint_14_cell_map_fails():
    b=blueprint();del b["cells"]["D4.7"]
    r=resolve(b=b)
    assert "BLUEPRINT_14_CELL_COVERAGE_MISMATCH" in codes(r)
    assert r["mechanical_status"]=="FAIL"


def test_blueprint_wrong_template_fails():
    b=blueprint();b["cells"]["D3.3"]["template_ref"]="QRT-MODEL-D3"
    assert "BLUEPRINT_CELL_TEMPLATE_CHANGED" in codes(resolve(b=b))


def test_adapter_different_subject_fails():
    a=adapter();a["subject"]="Chemistry"
    assert "ADAPTER_DISCIPLINE_MISMATCH" in codes(resolve(a=a))


def test_duplicate_source_ids_fail():
    assert "DUPLICATE_EXAM_IDENTITY_IN_SCOPE" in codes(resolve(q=[entry(),entry()]))


def test_subtile_explicit_valid_ref_keeps_hold():
    a=adapter()
    a.pop("cells");a.pop("families")
    a["for_blueprint"]={"id":"PHYS-QRT-BLUEPRINT","version":"0.2.0"}
    a["subtiles"]={"D3.3.1":{"units":["SYN-PHYS-CAP-01"]}}
    r=resolve(a=a,q=[entry(subtile_id="D3.3.1")])
    assert r["question_bindings"][0]["adapter_cell"]=="D3.3.1"
    assert r["academic_status"]=="HOLD"


def test_subtile_absent_is_held_not_fabricated():
    a=adapter();a.pop("cells");a["for_blueprint"]={"id":"PHYS-QRT-BLUEPRINT","version":"0.2.0"};a["subtiles"]={}
    assert "SUBTILE_NOT_IN_SELECTED_ADAPTER" in codes(resolve(a=a,q=[entry(subtile_id="D3.3.1")]))


def make_lots():
    kinds=(["CONDITIONAL_PRIMARY_HOLD"]*14+["SECONDARY_NOT_COUNTED"]*6+
           ["NO_PLACEMENT_IN_RETURN"]*43)
    groups=[]
    selections=[]
    for i in range(63):
        if i <14:
            op=OPS[2+i//3] if i<12 else "JUSTIFY"
            slot=f"{op}-{i%3+1}" if i<12 else f"JUSTIFY-{i-12+1}"
        else:slot=""
        selections.append(slot) if slot else None
    # Ensure seven explicitly vacant slots with no invented source.
    sel=[{"21-place ID":slot,"Candidate source ID":"(VACANT)","Selection state":"VACANT"}
         for slot in ["RETRIEVE-1","RETRIEVE-2","RETRIEVE-3","EXPLAIN-1","EXPLAIN-2","EXPLAIN-3","JUSTIFY-3"]]
    for i in range(14):
        sel.append({"21-place ID":selections[i], "Candidate source ID":f"EX-SYN-{i+1}",
                    "Selection state":"PENDING_REVIEW_HOLD"})
    all_rows=[]
    for i in range(79):
        lot=i//20+1 if i<60 else 4
        if i<63:
            disp=kinds[i]
            all_rows.append({"Lot":f"LOT-{lot:02d}","Lot position":i%20+1 if i<60 else i-60+1,
                             "Identity status":"SOURCE_ID_IDENTIFIED",
                             "Source ID":f"EX-SYN-{i+1}",
                             "Counting identity":f"EX-SYN-{i+1}",
                             "Selection disposition":disp,
                             "Core2 place":selections[i] if i<14 else ""})
        else:
            all_rows.append({"Lot":f"LOT-{lot:02d}","Lot position":i%20+1 if i<60 else i-60+1,
                             "Identity status":"IDENTITY_NOT_YET_RECONCILED",
                             "Source ID":f"RECONCILE-{lot:02d}-{i}",
                             "Counting identity":"UNKNOWN — DO NOT COUNT AS EXAM QUESTION",
                             "Selection disposition":"79-RECORD_LEDGER_ROW_NOT_PROVIDED",
                             "Core2 place":""})
    # Interleave sixteen reconciliation slots: 4 per lot, positions 17-20 (lot4 16-19).
    known=[r for r in all_rows if r["Identity status"]=="SOURCE_ID_IDENTIFIED"]
    missing=[r for r in all_rows if r["Identity status"]!="SOURCE_ID_IDENTIFIED"]
    groups=[];cursor=0;miss=0
    for lot, cap in enumerate((20,20,20,19),1):
        take=cap-4
        group=[]
        for k in range(take):
            item=known[cursor];cursor+=1
            item.update(Lot=f"LOT-{lot:02d}",**{"Lot position":k+1})
            group.append(item)
        for k in range(4):
            item=missing[miss];miss+=1
            item.update(Lot=f"LOT-{lot:02d}",**{"Lot position":take+k+1})
            group.append(item)
        groups.append(group)
    # Ensure selection references retained even after reorder.
    return {"schema":"core2-review-lots/v1","scope":"WPE_PHYSICS_PILOT_ONLY","lots":groups},sel


def native():
    return {"rendered_product":"WPE-CORE2-NATIVE-INTEGRATION-R1",
            "draft":True,"held_to":"REFERENCE","receipt_gaps_count":10,
            "question_records":[
                {"record_id":f"TB-WPE-ILL-{i:02d}","source_class":"TEXTBOOK_CANDIDATE",
                 "native_rendered":True} for i in (1,2,3,4,5,6,11,12)
            ]+[{"record_id":"SYN-WPE-CONTROL","source_class":"SYNTHETIC_CONTROL",
                 "native_rendered":True}]}


def test_coverage_identifies_63_leads_without_claiming_79_verified():
    lots,sel=make_lots()
    r=audit_core2_coverage(lots,sel,native())
    assert r["mechanical_status"]=="HOLD"
    assert r["review_positions"]==79
    assert r["identified_lot_leads"]==63
    assert r["unreconciled_review_positions_not_source_records"]==16
    assert r["verified_from_four_lot_inputs"] is False


def test_native_nine_cards_never_subtracted_from_exam_inventory():
    lots,sel=make_lots();r=audit_core2_coverage(lots,sel,native())
    assert r["native_html_cards_separate"]==9
    assert r["native_html_textbook_candidates"]==8
    assert r["independently_admitted_exam_questions"]==0


def test_all_21_selection_slots_seven_remain_vacant():
    lots,sel=make_lots();r=audit_core2_coverage(lots,sel,native())
    assert len(r["selection_places"])==21
    assert sum(x["state"]=="VACANT" for x in r["selection_places"])==7


def test_lot_position_duplication_fails():
    lots,sel=make_lots()
    lots["lots"][0][1]["Lot position"]=lots["lots"][0][0]["Lot position"]
    assert "REVIEW_POSITION_IDENTITY_INVALID" in codes(audit_core2_coverage(lots,sel,native()))


def test_lot_duplicate_source_identity_fails():
    lots,sel=make_lots()
    lots["lots"][1][0]["Source ID"]=lots["lots"][0][0]["Source ID"]
    assert "IDENTIFIED_SOURCE_ID_REPEATED_OR_MISSING" in codes(audit_core2_coverage(lots,sel,native()))


def test_unreconciled_placeholder_cannot_be_promoted_to_real_source():
    lots,sel=make_lots()
    lots["lots"][0][-1]["Source ID"]="EX-FAKE-SOURCE"
    assert "UNRECONCILED_SLOT_FABRICATED_AS_SOURCE" in codes(audit_core2_coverage(lots,sel,native()))


def test_vacant_slot_cannot_be_silently_filled():
    lots,sel=make_lots()
    sel[0]["Candidate source ID"]="EX-SYN-40"
    assert "VACANT_SLOT_CONTAINS_SOURCE" in codes(audit_core2_coverage(lots,sel,native()))


def test_passing_technical_render_is_not_academic_admission():
    lots,sel=make_lots()
    n=native();n["passed"]=True;n["academic_approved"]=True
    r=audit_core2_coverage(lots,sel,n)
    assert r["release_status"]=="HOLD"
    assert r["independently_admitted_exam_questions"]==0


def test_native_source_class_reassignment_fails():
    lots,sel=make_lots()
    n=native();n["question_records"][0]["source_class"]="AUTHENTIC_EXAM_APPROVED"
    assert "RENDERED_CARD_CLASS_NOT_ALLOWED" in codes(audit_core2_coverage(lots,sel,n))


def test_source_payload_not_emitted():
    lots,sel=make_lots()
    lots["lots"][0][0]["question_stem"]="PRIVATE_EXAM_STEM"
    r=audit_core2_coverage(lots,sel,native())
    assert "PRIVATE_EXAM_STEM" not in json.dumps(r)


def test_incorrect_four_lot_capacity_fails():
    lots,sel=make_lots()
    lots["lots"][0].pop()
    assert "EXPECTED_LOT_REVIEW_POSITION_COUNT_CHANGED" in codes(audit_core2_coverage(lots,sel,native()))


def test_cli_semantic_audit_is_hold(tmp_path):
    bp=tmp_path/"blueprint.json";ad=tmp_path/"adapter.json";entries=tmp_path/"entries.json";out=tmp_path/"out.json"
    bp.write_text(json.dumps(blueprint()));ad.write_text(json.dumps(adapter()))
    entries.write_text(json.dumps([entry()]))
    rc=main(["core2-cell-audit","--blueprint",str(bp),"--adapter",str(ad),
             "--entries",str(entries),"--out",str(out)])
    assert rc==3
    assert json.loads(out.read_text())["academic_status"]=="HOLD"


def test_cli_core2_inventory_uses_real_csv_parser(tmp_path):
    lots,sel=make_lots()
    p=tmp_path/"lots.json";p.write_text(json.dumps(lots))
    s=tmp_path/"selections.csv"
    with s.open("w",newline="") as fp:
        writer=csv.DictWriter(fp,fieldnames=["21-place ID","Candidate source ID","Selection state"])
        writer.writeheader();writer.writerows(sel)
    n=tmp_path/"native.json";n.write_text(json.dumps(native()))
    out=tmp_path/"report.json"
    assert main(["core2-inventory-audit","--lots",str(p),
                 "--selections",str(s),"--native",str(n),"--out",str(out)])==3
    assert json.loads(out.read_text())["academic_status"]=="HOLD"
