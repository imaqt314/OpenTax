"""stage a: ingest. point at a local folder, list input PDFs. NO network.

core principle: 100% local. app reads disk only.
"""
from pathlib import Path

INPUT_SUFFIXES = {".pdf"}


def find_inputs(folder) -> list:
    """return sorted paths of candidate input PDFs in folder."""
    p = Path(folder)
    if not p.is_dir():
        raise FileNotFoundError(f"not a folder: {folder}")
    return sorted(str(f) for f in p.iterdir() if f.suffix.lower() in INPUT_SUFFIXES)
