from .models import Diagnostic
COLLECTIONS = ("sources", "warrants", "constructions", "lessons", "assessments", "approvals")
REFERENCES = {
    "warrants": {"source_ids": "sources", "review_approval_ids": "approvals"},
    "constructions": {"source_ids": "sources", "warrant_ids": "warrants", "prerequisite_ids": "constructions", "lesson_ids": "lessons", "assessment_ids": "assessments"},
    "lessons": {"construction_id": "constructions", "directional_match_approval_id": "approvals"},
    "assessments": {"construction_id": "constructions", "source_ids": "sources", "key_source_id": "sources", "solution_source_id": "sources", "review_approval_ids": "approvals"},
}

def check_references(data):
    diagnostics, all_ids, indexes = [], {}, {}
    for collection in COLLECTIONS:
        indexes[collection] = {}
        for index, item in enumerate(data[collection]):
            key = item["id"]
            if key in all_ids:
                diagnostics.append(Diagnostic("DUPLICATE_ID", f"{collection}[{index}].id",
                                              f"Duplicate of {all_ids[key]}", "Use a globally unique ID.", key))
            else:
                all_ids[key] = f"{collection}[{index}]"
            indexes[collection][key] = item
    for collection, fields in REFERENCES.items():
        for item in data[collection]:
            for field, target in fields.items():
                if field not in item:
                    continue
                values = item[field] if isinstance(item[field], list) else [item[field]]
                for value in values:
                    if value not in indexes[target]:
                        diagnostics.append(Diagnostic("INVALID_REFERENCE", f"{collection}.{item['id']}.{field}",
                                                      f"Unknown {target} ID {value}", "Fix or provide the referenced record.", item["id"]))
    graph = {k: v["prerequisite_ids"] for k, v in indexes["constructions"].items()}
    visited, active, stack = set(), set(), []
    def walk(k):
        if k in active:
            cycle = stack[stack.index(k):] + [k]
            diagnostics.append(Diagnostic("PREREQUISITE_CYCLE", " -> ".join(cycle),
                                          "Prerequisite graph contains a cycle.", "Make a directed acyclic graph.", k))
            return
        if k in visited or k not in graph:
            return
        active.add(k)
        stack.append(k)
        for prerequisite in graph[k]:
            walk(prerequisite)
        stack.pop()
        active.remove(k)
        visited.add(k)
    for key in graph:
        walk(key)
    return diagnostics
