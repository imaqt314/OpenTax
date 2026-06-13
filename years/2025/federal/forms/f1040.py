"""Form 1040. main cascade. reads schedules via ctx, numbers from constants.

SKELETON: line cascade wired per 1040 layout, but constants are PLACEHOLDER.
do NOT trust output numbers until constants are filled from source_pdfs and
tests pass exact (core principle 3, test harness rule).
"""
from engine.money import money, need

from .. import constants as C

ID = "f1040"
DEPENDS_ON = ["sch1", "sch8812", "sch_eic"]


def tax_from_brackets(taxable: int, status: str) -> int:
    """progressive tax from constants.BRACKETS. PLACEHOLDER method — real
    returns for taxable < $100k must use the IRS Tax Tables, not a formula."""
    tiers = C.BRACKETS[status]
    tax = 0.0
    for i, (lo, rate) in enumerate(tiers):
        hi = tiers[i + 1][0] if i + 1 < len(tiers) else None
        if taxable > lo:
            top = taxable if hi is None else min(taxable, hi)
            tax += (top - lo) * rate
    return money(tax)


def compute(inp, ctx):
    fs = need(inp, "filing_status")
    if fs not in C.FILING_STATUSES:
        raise ValueError(f"unknown filing_status {fs!r}")

    L = {}
    L["1a"] = money(need(inp, "w2_wages"))         # W-2 box 1 sum
    L["8"] = ctx.get("sch1", "10")                 # additional income (Sch 1)
    L["9"] = money(L["1a"] + L["8"])               # total income
    L["11"] = L["9"]                               # AGI (no adjustments in v1)
    L["12"] = C.STD_DEDUCTION[fs]                  # std deduction, from constants
    L["15"] = money(max(0, L["11"] - L["12"]))     # taxable income
    L["16"] = tax_from_brackets(L["15"], fs)       # tax
    L["19"] = ctx.get("sch8812", "ctc")            # child tax credit
    L["22"] = money(max(0, L["16"] - L["19"]))     # tax after CTC
    L["24"] = L["22"]                              # total tax (v1: no other taxes)
    L["25a"] = money(need(inp, "w2_withholding"))  # W-2 box 2 fed withholding
    L["27"] = ctx.get("sch_eic", "eitc")           # EITC
    L["33"] = money(L["25a"] + L["27"])            # total payments
    if L["33"] >= L["24"]:
        L["34"] = money(L["33"] - L["24"])         # overpayment / refund
        L["37"] = 0
    else:
        L["34"] = 0
        L["37"] = money(L["24"] - L["33"])         # amount you owe
    return L
