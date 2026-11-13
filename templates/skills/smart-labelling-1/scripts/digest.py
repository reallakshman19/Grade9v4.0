"""Digest of one question's exact stored text, so a later change to the source is caught.

Usage:
  python -X utf8 -I digest.py <source.json> <item id> [--fields stem,options,figure_note] [--id-field id]
  python -X utf8 -I digest.py --text <file holding the exact item text>
Prints sha256:<hex>. A JSON item is hashed as canonical JSON of the listed fields (a missing field counts as null).
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

DEFAULT_FIELDS = ["stem", "options", "figure_note"]


def canonical_digest(obj) -> str:
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()


def text_digest(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_item(source: Path, item_id, id_field: str = "id"):
    data = json.loads(source.read_text(encoding="utf-8"))
    items = data.get("items", []) if isinstance(data, dict) else data
    for item in items:
        if isinstance(item, dict) and str(item.get(id_field)) == str(item_id):
            return item
    return None


def item_digest(source: Path, item_id, fields=None, id_field: str = "id"):
    item = find_item(source, item_id, id_field)
    if item is None:
        return None
    return canonical_digest({f: item.get(f) for f in (fields or DEFAULT_FIELDS)})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", nargs="?")
    ap.add_argument("item_id", nargs="?")
    ap.add_argument("--fields", default=",".join(DEFAULT_FIELDS))
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--text")
    a = ap.parse_args()
    if a.text:
        print(text_digest(Path(a.text)))
        return 0
    if not (a.source and a.item_id):
        ap.error("give <source.json> <item id>, or --text <file>")
    digest = item_digest(Path(a.source), a.item_id, a.fields.split(","), a.id_field)
    if digest is None:
        print(f"item {a.item_id} not found in {a.source}", file=sys.stderr)
        return 1
    print(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
