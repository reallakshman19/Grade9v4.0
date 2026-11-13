from .models import Diagnostic
FACTORS = ("conceptual", "representation", "reasoning_chain", "algebraic", "misconception_trap")
BANDS = {"D1": range(0, 3), "D2": range(3, 6), "D3": range(6, 8), "D4": range(8, 11)}

def check_demand(data):
    findings = []
    construction_index = {row["id"]: row for row in data["constructions"]}
    for name in ("constructions", "assessments"):
        for item in data[name]:
            for factor in FACTORS:
                if not item["demand_evidence"][factor].strip():
                    findings.append(Diagnostic("MISSING_DEMAND_EVIDENCE", f"{name}.{item['id']}.{factor}",
                                               "Empty factor evidence.", "Provide a reasoning explanation.", item["id"]))
            construction = item if name == "constructions" else construction_index.get(item["construction_id"])
            if construction is None:
                continue
            band = construction["band"]
            score = sum(item["demand_scores"][factor] for factor in FACTORS)
            if score not in BANDS[band]:
                findings.append(Diagnostic("BAND_MISMATCH", f"{name}.{item['id']}.demand_scores",
                                           f"{score} points cannot be {band}.", "Correct the rubric or band.", item["id"]))
    return findings
