"""P0.4 is deliberately not implemented; do not infer a PASS."""
def evaluate(data):
    return [{"construction_id": item["id"], "result": "HOLD", "code": "B1_B7_PENDING_IMPLEMENTATION"}
            for item in data.get("constructions", [])]
