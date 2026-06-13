"""local CLI. pipeline: ingest -> parse -> confirm -> compute -> review -> fill.

100% local, no network, no LLM. run `python cli.py demo` for the end-to-end
skeleton on sample inputs. numbers are PLACEHOLDER until constants are filled.
"""
import sys

from engine.registry import FEDERAL_2025, load
from engine.solver import run
from ui.fill_pdf import fill
from ui.parsers import f1099int, w2
from ui.review import low_confidence, to_inputs

BANNER = (
    "=" * 64 + "\n"
    "  OpenTax SKELETON — PLACEHOLDER constants. numbers are NOT real.\n"
    "  fill years/2025/federal/constants.py from IRS source_pdfs. do NOT file.\n"
    + "=" * 64
)

PDF_MAP = "years/2025/federal/pdf_maps/f1040.json"
BLANK_PDF = "years/2025/federal/source_pdfs/f1040.pdf"
OUT_PDF = "out/f1040_filled.pdf"


def demo():
    print(BANNER)

    # stage b: parse. real parse() raises until implemented; use samples here.
    draft = {
        **w2.sample(),
        **f1099int.sample(),
        "filing_status": "single",
        "num_qualifying_children": 2,
    }
    print("\nlow-confidence (human must check):", low_confidence(draft))

    # stage c: confirm -> strip tags into clean inputs.
    inputs = to_inputs(draft)
    print("confirmed inputs:", inputs)

    # stage d: compute (solver runs forms in dependency order).
    forms = load(FEDERAL_2025)
    sol = run(forms, inputs).all()

    # stage e: review computed lines.
    print("\ncomputed f1040 lines:")
    for line, val in sol["f1040"].items():
        print(f"  line {line:>4}: {val}")

    # stage f: stamp the filled 1040 PDF.
    out = fill(sol["f1040"], BLANK_PDF, PDF_MAP, OUT_PDF)
    print(f"\nfilled PDF written: {out}")
    print("NOTE: placeholder numbers. do not file.")


def main(argv):
    if len(argv) >= 2 and argv[1] == "demo":
        demo()
    else:
        print("usage: python cli.py demo")


if __name__ == "__main__":
    main(sys.argv)
