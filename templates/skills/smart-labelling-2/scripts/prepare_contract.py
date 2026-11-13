"""Prepare current byte/payload pins, never manufacture semantic qualification.

Output is a new sidecar only. Unresolved extraction, official custody, semantic
seeds, review and binder work remain visibly open. No source/label edits.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qrt_contract import Invalid, SCHEMA, digest, file_digest, object_, read_json, source_payloads, unique


def ref(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": file_digest(path)}


def prepare(sl1_path, library, vocabulary, adapter, sl2_path=None, attempts_path=None, adapter_map=None):
    s1 = object_(read_json(sl1_path), "SL1")
    r1 = unique(s1.get("records"), "question_id", "sl1.records")
    s2 = object_(read_json(sl2_path), "SL2") if sl2_path else None
    r2 = unique(s2.get("records"), "question_id", "sl2.records") if s2 else {}
    attempts = unique(object_(read_json(attempts_path), "attempts").get("attempts"), "attempt_id", "attempts") if attempts_path else {}
    contract = {"schema": SCHEMA, "preparation_status": "UNREVIEWED_SNAPSHOT_ONLY", "inputs": {
        "sl1": ref(sl1_path), "library": ref(library), "vocabulary": ref(vocabulary)}, "records": [], "preparation_issues": []}
    if sl2_path:
        contract["inputs"]["sl2"] = ref(sl2_path)
    for qid, record in r1.items():
        chosen_adapter = (adapter_map or {}).get(qid, adapter)
        entry = {"question_id": qid, "sl1_record_digest": digest(record), "cognitive_seed": None,
                 "answer_reference": {"kind": "UNRESOLVED"}, "preparation_notes": []}
        if qid in r2:
            entry["sl2_record_digest"] = digest(r2[qid])
        custody = object_(record.get("custody"), "custody")
        source_path = custody.get("text_file") if chosen_adapter == "text-file/v1" else custody.get("source_file")
        try:
            if not isinstance(source_path, str) or not Path(source_path).is_absolute():
                raise Invalid("ABSOLUTE_LEGACY_PATH_REQUIRED", "Resolve legacy overlay paths explicitly before v2 snapshot preparation")
            item_id = custody.get("source_item_id")
            item, payload, answer_payload = source_payloads(source_path, chosen_adapter, item_id)
            entry["source"] = {**ref(source_path), "adapter": chosen_adapter, "item_id": item_id,
                               "question_digest": digest(payload), "answer_digest": digest(answer_payload), "figure_assets": []}
            if "key" in item and item["key"] not in (None, ""):
                entry["answer_reference"] = {"kind": "PUBLISHER_FIELD", "value": item["key"]}
            else:
                entry["preparation_notes"].append("No explicit source key: reviewed extraction or an honest NO_KEY declaration remains open")
            entry["preparation_notes"].append("Bind actual saved figure assets where present; snapshotting does not verify historical figure freshness")
            if qid in r2 and r2[qid].get("mode") == "EVIDENCE":
                attempt_id = object_(r2[qid].get("learner"), "learner").get("attempt_ref")
                attempt = attempts.get(attempt_id)
                if attempt is not None:
                    entry["observation"] = {"attempts_ref": ref(attempts_path), "attempt_id": attempt_id, "snapshot_digest": digest(attempt),
                                            "stage": attempt.get("stage", "UNKNOWN"), "task_id": attempt.get("task_id", "UNKNOWN")}
                else:
                    entry["preparation_notes"].append("Actual saved attempt is missing; no independent observation can be inferred")
        except Invalid as exc:
            contract["preparation_issues"].append({"question_id": qid, "code": exc.code, "detail": exc.detail})
        contract["records"].append(entry)
    return contract


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sl1")
    parser.add_argument("--library", required=True)
    parser.add_argument("--vocab", required=True)
    parser.add_argument("--adapter", choices=("examside-json/v1", "anchors-json/v1", "explicit-key-json/v1", "text-file/v1"))
    parser.add_argument("--adapter-map", help="JSON object mapping exact question IDs to declared adapter IDs")
    parser.add_argument("--sl2")
    parser.add_argument("--attempts")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if not args.adapter and not args.adapter_map:
        parser.error("Specify a default --adapter or a complete --adapter-map")
    destination = Path(args.out).resolve()
    if destination.exists():
        parser.error("--out must be a new file; preparation never overwrites an existing artifact")
    try:
        adapters = object_(read_json(args.adapter_map), "adapter map") if args.adapter_map else None
        contract = prepare(args.sl1, args.library, args.vocab, args.adapter, args.sl2, args.attempts, adapters)
        destination.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "PREPARED_UNREVIEWED", "path": str(destination), "records": len(contract["records"]),
                          "preparation_issues": contract["preparation_issues"], "qualification": "NOT_RUN"}, indent=2))
        return 0
    except (Invalid, OSError) as exc:
        print(json.dumps({"status": "HOLD", "code": getattr(exc, "code", "OUTPUT_ERROR"), "detail": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
