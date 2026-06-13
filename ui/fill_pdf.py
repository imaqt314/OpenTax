"""stage f: solution + pdf_map -> filled IRS PDF (print & mail). NO e-file.

generic: any form with a pdf_map works (federal or state). pdf_map is
{line_id: fully-qualified AcroForm field name}. fail loud if the blank PDF or
map is missing — never emit a half-filled return silently.
"""
import json
from pathlib import Path

import pypdf


def field_values(solution_lines: dict, pdf_map_path) -> dict:
    """map computed line values onto pdf field names via the pdf_map.
    returns {field_name: "value"} for every mapped line present in the solution."""
    pdf_map = json.loads(Path(pdf_map_path).read_text())
    out = {}
    for line_id, field in pdf_map.items():
        if line_id.startswith("_"):
            continue
        if line_id in solution_lines:
            out[field] = str(solution_lines[line_id])
    return out


def fill(solution_lines: dict, blank_pdf_path, pdf_map_path, out_path) -> str:
    """stamp computed values into the blank IRS PDF, write filled PDF to out_path."""
    blank = Path(blank_pdf_path)
    if not blank.is_file():
        raise FileNotFoundError(f"blank PDF not found: {blank_pdf_path}")
    values = field_values(solution_lines, pdf_map_path)

    reader = pypdf.PdfReader(str(blank))
    writer = pypdf.PdfWriter()
    writer.append(reader)
    for page in writer.pages:
        writer.update_page_form_field_values(page, values, auto_regenerate=False)
    # tell viewers to render the field appearances we just set
    writer.set_need_appearances_writer(True)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return str(out_path)
