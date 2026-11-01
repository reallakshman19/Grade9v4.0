import json
from pathlib import Path
from .errors import InputError

def confined_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise InputError("PATH_ESCAPE: expected a relative path")
    if ".." in Path(relative).parts:
        raise InputError("PATH_ESCAPE: parent traversal")
    root = root.resolve()
    result = (root / relative).resolve()
    if not result.is_relative_to(root):
        raise InputError("PATH_ESCAPE: symlink or path outside bundle")
    return result

def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise InputError(f"Could not read {path}: {exc}") from exc

def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
