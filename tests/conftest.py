from pathlib import Path
import shutil
import pytest

@pytest.fixture
def candidate(tmp_path):
    source = Path(__file__).resolve().parents[1] / "examples" / "wpe-n01-candidate"
    target = tmp_path / "candidate"
    shutil.copytree(source, target)
    return target
