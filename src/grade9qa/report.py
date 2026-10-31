from datetime import datetime, timezone
from .bridge import evaluate as bridges
from .gates import evaluate as gates

def make_report(bundle, data, diagnostics):
    return {
        "schema_version": "1.0.0",
        "bundle_id": bundle.get("id", "unknown") if isinstance(bundle, dict) else "unknown",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mechanical_status": "FAIL" if diagnostics else "PASS",
        "qualification_status": "HOLD",
        "gate_results": gates(data),
        "bridge_results": bridges(data),
        "coverage": {"candidate_constructions": len({row["id"] for row in data["constructions"]}),
                     "qualified_constructions": 0, "admitted_exam_items": 0,
                     "message": "NOT_ACADEMIC_APPROVAL; only P0.1 checks implemented."},
        "diagnostics": [item.as_dict() for item in diagnostics]
    }

def markdown(report):
    lines = ["# Grade9QA report", "", "**NOT_ACADEMIC_APPROVAL**", "",
             "- Structural status: " + report["mechanical_status"],
             "- Academic qualification: HOLD",
             "- Qualified constructions: 0", "",
             "## Diagnostics"]
    lines.extend("- " + d["code"] + ": " + d["message"] for d in report["diagnostics"])
    if not report["diagnostics"]:
        lines.append("- No P0.1 errors; all further academic gates remain HOLD.")
    return "\n".join(lines) + "\n"
