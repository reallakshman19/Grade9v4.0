"""Read-only native SL1/SL2 R2 -> QRT Physics Blueprint -> WPE adapter binding.

Never executes/replaces native checkers, authenticates exams, approves physics,
or issues QRT/academic/release receipts. All outcomes remain HOLD.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

OPERATIONS = ("RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY")
FACTORS = ("concept_model_selection", "representation_translation", "reasoning_chain_length",
           "algebra_computational_load", "trap_exception_sensitivity")
BANDS = {"D1": (0, 2), "D2": (3, 5), "D3": (6, 7), "D4": (8, 10)}


def fingerprints(paths: dict[str, Path]) -> dict:
    """Byte identities only; neither custody nor scientific verification."""
    result = {}
    for name, path in sorted(paths.items()):
        if path is not None:
            p = Path(path)
            result[name] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "size": p.stat().st_size}
    return result


def inspect_binding(sl1: object, sl2: object, contract: object, blueprint: object,
                    adapter: object, handoff: object | None = None,
                    native_sl1: object | None = None, native_sl2: object | None = None,
                    input_fingerprints: dict | None = None) -> dict:
    issues = []

    def add(code, severity, subject, detail):
        issues.append({"code": code, "severity": severity, "subject": subject, "detail": detail})

    def obj(data, name):
        if not isinstance(data, dict):
            add("INPUT_NOT_OBJECT", "FAIL", name, "Expected JSON object.")
            return {}
        return data

    sl1, sl2, contract = obj(sl1, "SL1"), obj(sl2, "SL2"), obj(contract, "R2_CONTRACT")
    blueprint, adapter = obj(blueprint, "PHYSICS_BLUEPRINT"), obj(adapter, "WPE_ADAPTER")
    for data, name, schema, code in (
        (sl1, "SL1", "g9v35-smart-labels-1/v1", "SL1_OVERLAY_SCHEMA_MISMATCH"),
        (sl2, "SL2", "g9v35-smart-labels-2/v1", "SL2_OVERLAY_SCHEMA_MISMATCH"),
        (contract, "R2_CONTRACT", "smart-labelling-qrt-contract/v2", "R2_CONTRACT_SCHEMA_MISMATCH"),
    ):
        if data.get("schema") != schema:
            add(code, "FAIL", name, "Original native record shape required; do not reinterpret digests.")

    if blueprint.get("blueprint_id") != "PHYS-QRT-BLUEPRINT":
        add("BLUEPRINT_ID_MISMATCH", "FAIL", "PHYSICS_BLUEPRINT", "Expected common Physics Blueprint identity.")
    if blueprint.get("version") != "0.2.0":
        add("BLUEPRINT_VERSION_UNREVIEWED", "HOLD", "PHYSICS_BLUEPRINT", "Only v0.2.0 candidate inspected.")
    if blueprint.get("status") != "APPROVED":
        add("BLUEPRINT_NOT_APPROVED", "HOLD", "PHYSICS_BLUEPRINT", "Candidate Blueprint is not Owner approved.")
    order = blueprint.get("column_order")
    if order != list(OPERATIONS):
        add("BLUEPRINT_OPERATION_ORDER_MISMATCH", "FAIL", "PHYSICS_BLUEPRINT", "Preserve canonical seven operations.")
    if adapter.get("adapter_id") != "PHYS-TOPIC-WPE" or adapter.get("topic_id") != "WPE":
        add("WPE_ADAPTER_ID_MISMATCH", "FAIL", "WPE_ADAPTER", "Expected WPE topic adapter identity.")
    if adapter.get("for_blueprint") != f"{blueprint.get('blueprint_id')} {blueprint.get('version')}":
        add("WPE_ADAPTER_BLUEPRINT_PIN_MISMATCH", "FAIL", "WPE_ADAPTER", "Wrong blueprint identity/version pin.")
    if adapter.get("status") != "APPROVED":
        add("WPE_ADAPTER_NOT_APPROVED", "HOLD", "WPE_ADAPTER", "WPE adapter remains draft.")
    if not isinstance(adapter.get("cells"), dict):
        add("WPE_ADAPTER_CELLS_MISSING", "FAIL", "WPE_ADAPTER", "Topic adapter cells must be a map.")

    def index(records, subject):
        found = {}
        if not isinstance(records, list):
            add("RECORDS_NOT_ARRAY", "FAIL", subject, "Expected array of native records.")
            return found
        for i, row in enumerate(records):
            if not isinstance(row, dict) or not isinstance(row.get("question_id"), str) or not row["question_id"]:
                add("QUESTION_ID_MISSING", "FAIL", subject, f"Row {i} has no question ID.")
                continue
            qid = row["question_id"]
            if qid in found:
                add("QUESTION_ID_DUPLICATED", "FAIL", subject, f"Duplicate question ID {qid}.")
            found[qid] = row
        return found

    left = index(sl1.get("records"), "SL1")
    right = index(sl2.get("records"), "SL2")
    sidecar = index(contract.get("records"), "R2_CONTRACT")
    if set(left) != set(right):
        add("SL1_SL2_QUESTION_SET_MISMATCH", "FAIL", "QUESTION_BINDING", "Paired question sets differ.")
    if set(left) != set(sidecar):
        add("CONTRACT_QUESTION_SET_MISMATCH", "FAIL", "R2_CONTRACT", "Sidecar must bind the paired question set.")

    for name, report in (("sl1", native_sl1), ("sl2", native_sl2)):
        if report is None:
            add("NATIVE_REPORT_ABSENT", "HOLD", name, "Native checker report absent; no gate witness.")
        elif not isinstance(report, dict) or report.get("schema") != "smart-labelling-check-report/v2":
            add("NATIVE_REPORT_SCHEMA_MISMATCH", "FAIL", name, "Unsupported native checker report.")
        elif report.get("selected_gate_status") != "PASS":
            add("NATIVE_GATE_NOT_PASS", "HOLD", name, "Native selected gate has not passed.")
        else:
            add("NATIVE_REPORT_UNTRUSTED", "HOLD", name, "Unattested JSON is not a trusted native run or reviewer receipt.")

    b_cells = blueprint.get("cells") if isinstance(blueprint.get("cells"), dict) else {}
    a_cells = adapter.get("cells") if isinstance(adapter.get("cells"), dict) else {}
    bindings = []
    for qid in sorted(set(left) | set(right) | set(sidecar)):
        l1, l2, side = left.get(qid), right.get(qid), sidecar.get(qid)
        record = {"question_id": qid, "sl2_operation": None, "sl2_band": None,
                  "blueprint_cell": None, "topic_adapter_cell_present": False,
                  "source_role": "UNADJUDICATED", "qrt_status": "HOLD",
                  "qualification_status": "HOLD"}
        if l1 and l2:
            expected = (l1.get("custody") or {}).get("item_digest")
            actual = (l2.get("binding") or {}).get("sl1_item_digest")
            if not expected or expected != actual:
                add("LEGACY_SL1_SL2_DIGEST_MISMATCH", "FAIL", qid, "Do not regenerate or silently reinterpret legacy digest.")
            proposal = l2.get("demand_proposal") or {}
            evidence = l2.get("difficulty_evidence") or {}
            primary, band = proposal.get("primary"), evidence.get("band")
            record["sl2_operation"], record["sl2_band"] = primary, band
            if primary not in OPERATIONS:
                add("SL2_OPERATION_INVALID", "FAIL", qid, "SL2 proposal must use canonical operation.")
            if proposal.get("status") != "PROPOSED" or l2.get("status") not in ("UNREVIEWED", "PROPOSED"):
                add("SL2_STATUS_NEEDS_NATIVE_REVIEW", "HOLD", qid, "Self-promoted SL2 REVIEWED status is not trusted.")
            if band not in BANDS:
                add("SL2_BAND_INVALID", "FAIL", qid, "Only D1–D4 supported.")
            factors = evidence.get("components")
            if not isinstance(factors, dict) or set(factors) != set(FACTORS):
                add("SL2_RUBRIC_SHAPE_MISMATCH", "FAIL", qid, "Five exact R2 factor names required.")
            else:
                values = []
                for factor in FACTORS:
                    item = factors[factor]
                    if (not isinstance(item, dict) or type(item.get("score")) is not int
                            or not 0 <= item["score"] <= 2
                            or not str(item.get("evidence", "")).strip()):
                        add("SL2_FACTOR_EVIDENCE_INVALID", "FAIL", qid, "Invalid score/evidence for " + factor)
                    else:
                        values.append(item["score"])
                if len(values) == 5:
                    total = sum(values)
                    if total != evidence.get("total"):
                        add("SL2_TOTAL_MISMATCH", "FAIL", qid, "Rubric sum and reported total differ.")
                    if band in BANDS and not BANDS[band][0] <= total <= BANDS[band][1]:
                        add("SL2_BAND_SCORE_MISMATCH", "FAIL", qid, "Demand vector contradicts D-band.")
            if primary in OPERATIONS and band in ("D3", "D4") and order == list(OPERATIONS):
                key = f"{band}.{OPERATIONS.index(primary) + 1}"
                record["blueprint_cell"] = key
                if proposal.get("candidate_cell") != f"QRT-{primary}-{band}":
                    add("SL2_CANDIDATE_CELL_MISMATCH", "FAIL", qid, "SL2 candidate-cell label contradicts operation and band.")
                if key not in b_cells:
                    add("BLUEPRINT_CELL_MISSING", "HOLD", qid, "Missing common Blueprint cell " + key)
                elif not isinstance(b_cells[key], dict) or b_cells[key].get("template_ref") != f"QRT-{primary}-{band}":
                    add("BLUEPRINT_TEMPLATE_MISMATCH", "FAIL", qid, "Common Blueprint template contradicts SL2 proposal.")
                if key not in a_cells:
                    add("TOPIC_ADAPTER_CELL_MISSING", "HOLD", qid, "Missing topic-specific cell " + key)
                else:
                    record["topic_adapter_cell_present"] = True
            elif band in ("D1", "D2"):
                add("D1_D2_BLUEPRINT_SPEC_PENDING", "HOLD", qid, "Common Physics Blueprint covers D3/D4 only.")
            if (l1.get("source_verification") or {}).get("status") == "VERIFIED":
                add("SL1_CLAIM_NOT_INDEPENDENT_CUSTODY", "HOLD", qid, "Self-declared VERIFIED is not official source custody.")
            add("QRT_INDEPENDENT_DECISION_MISSING", "HOLD", qid, "Independent QRT adjudication must verify operation/band/source role.")
        if side:
            for field in ("sl1_record_digest", "sl2_record_digest"):
                pin = side.get(field)
                if not isinstance(pin, str) or not pin.startswith("sha256:") or len(pin) != 71:
                    add("CONTRACT_RECORD_PIN_MISSING", "FAIL", qid, "Missing native sidecar record pin: " + field)
        bindings.append(record)

    preparation = "NOT_SUPPLIED"
    if handoff is not None:
        h = obj(handoff, "CORE1A_HANDOFF")
        if h.get("schema") != "core1a-source-handoff/v1":
            add("HANDOFF_SCHEMA_MISMATCH", "FAIL", "CORE1A_HANDOFF", "Expected native source handoff v1.")
        elif h.get("status") != "APPROVED":
            add("HANDOFF_NOT_APPROVED", "HOLD", "CORE1A_HANDOFF", "Preparation dossier is not an approved lesson.")
        if not isinstance(h.get("construction"), dict) or not h["construction"].get("decisive_move"):
            add("HANDOFF_DECISIVE_MOVE_MISSING", "FAIL", "CORE1A_HANDOFF", "Handoff has no decisive move.")
        if not h.get("question_links"):
            preparation = "SOURCE_PREPARATION_ONLY"
            add("HANDOFF_NO_REVIEWED_QUESTION_JOIN", "HOLD", "CORE1A_HANDOFF", "Zero question links: no Core2/QRT equivalence.")
        else:
            preparation = "CANDIDATE_LINKED_NOT_QUALIFIED"
            add("HANDOFF_QUESTION_LINKS_UNREVIEWED", "HOLD", "CORE1A_HANDOFF", "Links require independent matching review.")
    bad = any(x["severity"] == "FAIL" for x in issues)
    return {
        "schema_version": "1.0.0", "audit_type": "SMART_R2_QRT_WPE_READ_ONLY_BINDING",
        "mechanical_status": "FAIL" if bad else ("HOLD" if issues else "PASS"),
        "qualification_status": "HOLD", "integration_status": "HOLD",
        "question_count": len(bindings), "question_bindings": bindings,
        "core1a_preparation": preparation, "input_fingerprints": input_fingerprints or {},
        "diagnostics": sorted(issues, key=lambda x: (x["subject"], x["code"])),
        "blocked_by": ["TRUSTED_NATIVE_R2_SOURCE_AND_REPORTS", "INDEPENDENT_QRT_ADJUDICATION",
                       "QUALIFIED_PHYSICS_WARRANTS", "REVIEWED_WPE_TOPIC_ADAPTER",
                       "REVIEWED_CORE1A_TO_CORE1B_B1_B7", "SHARED_GOVERNANCE_AND_RUNTIME"],
        "warning": "NOT_ACADEMIC_APPROVAL: SL2 proposal and file hashes cannot approve QRT, Physics or release.",
    }
