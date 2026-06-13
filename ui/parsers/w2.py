"""parse a W-2 PDF -> draft inputs. each value tagged {value, src, confidence}.

core principle 6: parsers NEVER feed compute directly. output goes through
ui/review.py for human confirm/edit first.

SKELETON: real parse needs text/OCR extract. parse() RAISES until implemented
so we never silently emit a guessed number. sample() shows the target shape.
"""


def parse(pdf_path) -> dict:
    raise NotImplementedError(
        f"W-2 parser not implemented for {pdf_path!r}. implement text/OCR "
        "extract; return tagged draft like sample()."
    )


def sample() -> dict:
    """hand sample of the tagged shape parse() must return."""
    return {
        "w2_wages": {"value": 50000, "src": "W-2 box 1", "confidence": "low"},
        "w2_withholding": {"value": 6000, "src": "W-2 box 2", "confidence": "low"},
    }
