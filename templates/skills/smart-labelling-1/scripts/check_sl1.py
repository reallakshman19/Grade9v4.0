"""Candidate SL entrypoint; see --help and references/hardening-contract.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qrt_cli import main
if __name__ == "__main__":
    raise SystemExit(main(1))
