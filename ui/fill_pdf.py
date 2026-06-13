"""stage f: solution + pdf_map -> filled IRS PDF (print & mail). NO e-file.

generic: any form with a pdf_map works (federal or state).
SKELETON: field_values() builds the field->value map now. stamp() RAISES until
a PDF lib (pypdf) + the real blank PDF in source_pdfs are wired, so we never
emit a fake filled return.
"""
import json
from pathlib import Path


def field_values(solution_lines: dict, pdf_map_path) -> dict:
    """map computed lines onto pdf acroform field names via the pdf_map."""
    pdf_map = json.loads(Path(pdf_map_path).read_text())
    out = {}
    for line_id, field in pdf_map.items():
        if line_id.startswith("_"):
            continue
        if line_id in solution_lines:
            out[field] = solution_lines[line_id]
    return out


def stamp(field_values: dict, blank_pdf_path, out_path):
    raise NotImplementedError(
        "PDF stamp not wired. add pypdf, load the blank IRS PDF from "
        "source_pdfs, set acroform fields from field_values, write out_path."
    )
