"""IRS money. Decimal. whole dollar. half-up. never float. ONE place.

core principle 5: money is int whole-dollar, rounded half-up via Decimal.
core principle 2: fail loud — missing input raises, never silent zero.
"""
from decimal import Decimal, ROUND_HALF_UP


class Missing(Exception):
    """input or upstream line missing. fail loud. never guess, never zero."""


def money(x) -> int:
    """to whole-dollar int. half-up. str() first so no float drift."""
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def need(inp: dict, key: str):
    """pull key from inputs or raise. no silent default."""
    if key not in inp:
        raise Missing(f"need input {key!r}")
    return inp[key]
