"""parse a 1099-INT PDF -> draft inputs, tagged {value, src, confidence}.

core principle 6: never feeds compute directly — goes through ui/review.py.
SKELETON: parse() RAISES until real extract is implemented.
"""


def parse(pdf_path) -> dict:
    raise NotImplementedError(
        f"1099-INT parser not implemented for {pdf_path!r}. implement extract; "
        "return tagged draft like sample()."
    )


def sample() -> dict:
    return {
        "interest_income": {"value": 320, "src": "1099-INT box 1", "confidence": "low"},
    }
