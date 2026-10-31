"""Read-only, metadata-only four-lot / native Core2 reconciliation.

A review *position* is not a known examination-source record. The 79/78
owner claim cannot be independently reconstructed from a partially supplied
62+1 ID register. Never promote selected, rendered or reviewed candidates.
"""
from __future__ import annotations

from collections import Counter


def _code(code, severity="HOLD"):
    return {"code": code, "severity": severity}


def audit_core2_coverage(lots: object, selections: object, native: object) -> dict:
    problems=[]
    if (not isinstance(lots, dict) or lots.get("schema") != "core2-review-lots/v1"
            or lots.get("scope") != "WPE_PHYSICS_PILOT_ONLY"
            or not isinstance(lots.get("lots"), list)):
        return _finish([_code("FOUR_LOT_INPUT_INVALID", "FAIL")], [], [], [])
    if not isinstance(selections, list) or not isinstance(native, dict):
        return _finish([_code("SELECTION_OR_NATIVE_REPORT_INVALID", "FAIL")], [], [], [])
    rows=[x for group in lots["lots"] if isinstance(group, list) for x in group]
    if len(lots["lots"]) != 4 or any(not isinstance(x,list) for x in lots["lots"]):
        problems.append(_code("FOUR_LOT_GROUP_COUNT_INVALID", "FAIL"))
    if [len(x) for x in lots["lots"] if isinstance(x,list)] != [20,20,20,19]:
        problems.append(_code("EXPECTED_LOT_REVIEW_POSITION_COUNT_CHANGED", "FAIL"))
    if len(rows) != 79:
        problems.append(_code("REVIEW_POSITION_TOTAL_NOT_79", "FAIL"))
    identified=[]
    unresolved=[]
    all_ids=set()
    positions=set()
    dispositions=Counter()
    counts={}
    for i,lot in enumerate(lots["lots"]):
        if not isinstance(lot,list):
            continue
        counts[f"LOT-{i+1:02d}"]={"positions":len(lot),"identified":0,"unreconciled":0}
        for row in lot:
            if not isinstance(row,dict):
                problems.append(_code("REVIEW_POSITION_NOT_OBJECT", "FAIL"))
                continue
            raw=row.get("Source ID")
            position=(row.get("Lot"),row.get("Lot position"))
            if position in positions or row.get("Lot") != f"LOT-{i+1:02d}" or type(row.get("Lot position")) is not int:
                problems.append(_code("REVIEW_POSITION_IDENTITY_INVALID", "FAIL"))
            positions.add(position)
            state=row.get("Identity status")
            disposition=row.get("Selection disposition")
            dispositions[disposition]+=1
            if state=="SOURCE_ID_IDENTIFIED":
                if not isinstance(raw,str) or not raw or raw in all_ids:
                    problems.append(_code("IDENTIFIED_SOURCE_ID_REPEATED_OR_MISSING", "FAIL"))
                    continue
                all_ids.add(raw)
                if disposition not in ("CONDITIONAL_PRIMARY_HOLD",
                                       "SECONDARY_NOT_COUNTED","NO_PLACEMENT_IN_RETURN"):
                    problems.append(_code("SOURCE_SELECTION_DISPOSITION_INVALID", "FAIL"))
                identified.append({
                    "source_id":raw,"lot":row["Lot"],"position":row["Lot position"],
                    "selection_disposition":disposition,
                    "selection_place":row.get("Core2 place") or None,
                    "proposed_operation":row.get("Proposed operation") or None,
                    "proposed_band":row.get("Proposed demand") or None,
                    "academic_status":"HOLD",
                })
                counts[row["Lot"]]["identified"]+=1
            elif state=="IDENTITY_NOT_YET_RECONCILED":
                if (not isinstance(raw,str) or not raw.startswith("RECONCILE-")
                        or disposition!="79-RECORD_LEDGER_ROW_NOT_PROVIDED"):
                    problems.append(_code("UNRECONCILED_SLOT_FABRICATED_AS_SOURCE", "FAIL"))
                unresolved.append({"review_position":raw,"lot":row["Lot"],
                                   "academic_status":"HOLD",
                                   "not_a_source_record":True})
                counts[row["Lot"]]["unreconciled"]+=1
            else:
                problems.append(_code("REVIEW_IDENTITY_STATUS_UNKNOWN", "FAIL"))
    if len(identified)!=63 or len(unresolved)!=16:
        problems.append(_code("IDENTIFIABLE_SOURCE_COUNTS_CHANGED", "FAIL"))
    if dict(dispositions)!={"CONDITIONAL_PRIMARY_HOLD":14,
                            "SECONDARY_NOT_COUNTED":6,
                            "NO_PLACEMENT_IN_RETURN":43,
                            "79-RECORD_LEDGER_ROW_NOT_PROVIDED":16}:
        problems.append(_code("LOT_SELECTION_DISPOSITION_TOTALS_CHANGED", "FAIL"))
    if any(c["identified"]!=(16 if n!="LOT-04" else 15) or c["unreconciled"]!=4
           for n,c in counts.items()):
        problems.append(_code("LOT_COVERAGE_INCONSISTENT", "FAIL"))

    selection_rows=[]
    slots=set()
    for i,row in enumerate(selections):
        if not isinstance(row,dict):
            problems.append(_code("SELECTION_ROW_NOT_OBJECT", "FAIL"))
            continue
        slot=row.get("21-place ID")
        proposed=row.get("Candidate source ID")
        if not isinstance(slot,str) or slot in slots:
            problems.append(_code("SELECTION_SLOT_REPEATED_OR_MISSING", "FAIL"))
            continue
        slots.add(slot)
        state=row.get("Selection state")
        if state=="VACANT":
            if proposed!="(VACANT)":
                problems.append(_code("VACANT_SLOT_CONTAINS_SOURCE", "FAIL"))
        elif state=="PENDING_REVIEW_HOLD":
            if proposed not in all_ids:
                problems.append(_code("SELECTION_SOURCE_NOT_IN_FOUR_LOTS", "FAIL"))
            entry=next((item for item in identified if item["source_id"]==proposed),None)
            if entry is None or entry["selection_place"]!=slot:
                problems.append(_code("LOT_AND_SELECTION_SLOT_DISAGREE","FAIL"))
        else:
            problems.append(_code("UNAUTHORIZED_SELECTION_STATUS","FAIL"))
        selection_rows.append({
            "slot":slot,
            "source_id":proposed if state=="PENDING_REVIEW_HOLD" else None,
            "state":state,"academic_status":"HOLD"
        })
    if len(selection_rows)!=21 or sum(x["state"]=="PENDING_REVIEW_HOLD" for x in selection_rows)!=14:
        problems.append(_code("SELECTION_21_PLACE_COVERAGE_CHANGED","FAIL"))
    if sum(x["state"]=="VACANT" for x in selection_rows)!=7:
        problems.append(_code("SEVEN_VACANCIES_NOT_PRESERVED","FAIL"))

    rendered=native.get("question_records")
    if (native.get("rendered_product") != "WPE-CORE2-NATIVE-INTEGRATION-R1"
            or native.get("draft") is not True or native.get("held_to")!="REFERENCE"
            or not isinstance(rendered,list)):
        problems.append(_code("NATIVE_RENDER_AUDIT_SHAPE_CHANGED","FAIL"))
        rendered=[]
    normal=[]
    for row in rendered:
        if not isinstance(row,dict) or not isinstance(row.get("record_id"),str):
            problems.append(_code("RENDERED_CARD_ID_INVALID","FAIL"))
            continue
        sid=row["record_id"]
        kind=row.get("source_class")
        if kind not in ("TEXTBOOK_CANDIDATE","SYNTHETIC_CONTROL"):
            problems.append(_code("RENDERED_CARD_CLASS_NOT_ALLOWED","FAIL"))
        if sid in all_ids:
            # Even a coincident identifier cannot itself prove original-asset identity.
            problems.append(_code("RENDERED_SOURCE_ID_COLLIDES_WITH_EXAM_INVENTORY","FAIL"))
        normal.append({"record_id":sid,"record_type":kind,
                       "native_rendered":row.get("native_rendered") is True,
                       "exam_inventory_join":"NOT_ESTABLISHED",
                       "academic_status":"HOLD"})
    if len(normal)!=9 or len({x["record_id"] for x in normal})!=9:
        problems.append(_code("EXISTING_NINE_CARD_BASELINE_CHANGED","FAIL"))
    if sum(x["record_type"]=="TEXTBOOK_CANDIDATE" for x in normal)!=8:
        problems.append(_code("TEXTBOOK_AND_SYNTHETIC_SEPARATION_CHANGED","FAIL"))
    if native.get("receipt_gaps_count")!=10:
        problems.append(_code("ORIGINAL_RENDER_RECEIPT_GAPS_CHANGED","FAIL"))

    problems += [
        _code("FULL_79_ROW_OWNER_DISPOSITION_LEDGER_NOT_SUPPLIED"),
        _code("79_SOURCE_RECORD_78_IDENTITY_CLAIM_NOT_REPRODUCED_FROM_LOTS"),
        _code("EX_M4_ALIAS_REQUIRES_CANONICAL_SOURCE_JOIN"),
        _code("RENDERED_TEXTBOOK_CARDS_SEPARATE_FROM_EXAM_INVENTORY"),
        _code("INDEPENDENT_CORE2_ADMISSIONS_MISSING"),
    ]
    return _finish(problems,identified,unresolved,normal,selection_rows,counts)


def _finish(problems, identified,unresolved,rendered,selection_rows=None,counts=None):
    return {
        "schema_version":"1.0.0",
        "audit_type":"WPE_CORE2_FOUR_LOTS_AND_EXISTING_NATIVE_HTML_READBACK",
        "subject_id":"PHYSICS","unit_id":"WPE",
        "mechanical_status":"FAIL" if any(p["severity"]=="FAIL" for p in problems) else "HOLD",
        "academic_status":"HOLD","release_status":"HOLD",
        "official_exam_source_inventory_reported":79,
        "distinct_exam_identities_reported":78,
        "verified_from_four_lot_inputs":False,
        "review_positions":len(identified)+len(unresolved),
        "identified_lot_leads":len(identified),
        "unreconciled_review_positions_not_source_records":len(unresolved),
        "native_html_cards_separate":len(rendered),
        "native_html_textbook_candidates":sum(x["record_type"]=="TEXTBOOK_CANDIDATE" for x in rendered),
        "native_html_synthetic_controls":sum(x["record_type"]=="SYNTHETIC_CONTROL" for x in rendered),
        "independently_admitted_exam_questions":0,
        "lot_counts":counts or {},
        "selection_places":selection_rows or [],
        "identified_questions":identified,
        "unreconciled_positions":unresolved,
        "existing_native_cards":rendered,
        "diagnostics":sorted(problems,key=lambda p:p["code"]),
        "blocked_by":["FULL_ORIGINAL_79_ROW_OWNER_LEDGER",
                      "ORIGINAL_OFFICIAL_PAPER_KEY_FIGURE_CUSTODY",
                      "APPOINTED_INDEPENDENT_QRT_PHYSICS_REVIEWS",
                      "SELECTED_PINNED_WPE_ADAPTER_AND_BLUEPRINT",
                      "GOVERNED_SHARED_RENDER_AND_RELEASE"],
        "warning":"79 review positions are not 79 separately verified exam identities. The nine existing HTML cards are separate textbook/synthetic work.",
    }
