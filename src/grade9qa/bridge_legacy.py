"""Sanitized readback for archived D3 WPE B1–B7 candidate witnesses.

Legacy shapes differ from the new v1 witness contract. Do NOT silently map
partial/preview/HOLD records into a new, supposedly completed witness.
"""
GATES = ("B1","B2","B3","B4","B5","B6","B7")

def _extract(record):
    if not isinstance(record, dict):
        return None
    if isinstance(record.get("B1_B7_status"), dict):
        return record["B1_B7_status"]
    if isinstance(record.get("witness_gates"), dict):
        return {key: val.get("status", "UNKNOWN") if isinstance(val, dict) else "UNKNOWN"
                for key,val in record["witness_gates"].items()}
    return None

def inspect_legacy_witness(source):
    """Expose legacy candidate statuses without copying stem, figures, text or learner data."""
    if not isinstance(source, dict):
        return {"schema_version":"1.0.0","mechanical_status":"FAIL","qualification_status":"HOLD",
                "records":[],"diagnostic_codes":["INVALID_ARCHIVED_RECORD"],
                "warning":"NOT_ACADEMIC_APPROVAL"}
    if isinstance(source.get("witnesses"), dict):
        rows = list(source["witnesses"].items())
    else:
        rows = [(source.get("construction_id") or source.get("instance_id") or "UNKNOWN", source)]
    records, problems = [], []
    for identity, item in rows:
        gates = _extract(item)
        if gates is None:
            problems.append("ARCHIVED_GATE_FORMAT_UNMAPPED")
            gates = {}
        accepted = {"HOLD", "PARTIAL", "PARTIAL_STRUCTURAL_ONLY",
                    "LOCAL_PREVIEW_CHECKS_ONLY", "NOT_RUN", "PASS", "APPROVED",
                    "REJECTED", "FAIL"}
        vals = {key: (value if isinstance(value := gates.get(key, "NOT_RUN"), str)
                      and value in accepted else "UNRECOGNIZED")
                for key in GATES}
        if any(v.upper() in ("REJECTED","FAIL") for v in vals.values()):
            outcome = "FAIL"
        else:
            outcome = "HOLD"
        records.append({"construction_id":str(identity), "source_native_gate_status":vals,
                        "result":outcome,"qualification_status":"HOLD",
                        "missing_or_unreviewed":[k for k,v in vals.items() if v not in ("APPROVED", "PASS")]})
    return {
        "schema_version":"1.0.0",
        "mechanical_status":"FAIL" if any(r["result"]=="FAIL" for r in records) else "HOLD",
        "qualification_status":"HOLD",
        "records":records,
        "diagnostic_codes":sorted(set(problems+["NATIVE_WITNESS_STATUSES_UNTRUSTED"])),
        "warning":"NOT_ACADEMIC_APPROVAL: candidate statuses, even PASS, are not independent B1–B7 review.",
    }
