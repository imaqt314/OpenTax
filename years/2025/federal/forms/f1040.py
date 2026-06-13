"""Form 1040. main cascade. reads schedules via ctx, numbers from constants.

v1 income: W-2 wages (line 1a) + 1099-INT taxable interest (line 2b). No
Schedule 1. Credits (CTC line 19, EITC line 27a, ACTC line 28) come from their
schedules — those schedules are still being built; f1040's own cascade is real.

2025 redesign line IDs (verified against the blank PDF in source_pdfs, NOT
memory): AGI = 11a (pg1) carried to 11b (pg2); standard deduction = 12e;
total deductions = 14 (12e+13a+13b); taxable income = 15; EIC = 27a.
"""
from engine.money import money, need

from .. import constants as C

ID = "f1040"
DEPENDS_ON = ["sch8812", "sch_eic"]


def _bracket_tax(amount: int, status: str) -> float:
    """exact progressive tax from constants.BRACKETS. tiers = (lower, rate);
    a tier runs [lower, next_lower). this IS the Tax Computation Worksheet."""
    tiers = C.BRACKETS[status]
    tax = 0.0
    for i, (lo, rate) in enumerate(tiers):
        if amount <= lo:
            break
        hi = tiers[i + 1][0] if i + 1 < len(tiers) else None
        top = amount if hi is None else min(amount, hi)
        tax += (top - lo) * rate
    return tax


def tax_line16(taxable: int, status: str) -> int:
    """1040 line 16 tax.
    < $100,000  -> Tax Table: tax on the midpoint of the $50 income row.
    >= $100,000 -> Tax Computation Worksheet: formula on exact taxable income.
    TODO: sub-$3,000 table rows use smaller increments; validate vs the Tax
    Table pages in source_pdfs before trusting very-low-income returns."""
    if taxable <= 0:
        return 0
    if taxable < 100000:
        midpoint = (taxable // 50) * 50 + 25
        return money(_bracket_tax(midpoint, status))
    return money(_bracket_tax(taxable, status))


def compute(inp, ctx):
    fs = need(inp, "filing_status")
    if fs not in C.FILING_STATUSES:
        raise ValueError(f"unknown filing_status {fs!r}")

    L = {}
    # --- income (page 1) ---
    L["1a"] = money(need(inp, "w2_wages"))          # W-2 box 1 wages (sum)
    L["1z"] = L["1a"]                               # add 1a-1h (v1: box 1 only)
    L["2b"] = money(need(inp, "interest_income"))   # taxable interest (1099-INT)
    L["9"] = money(L["1z"] + L["2b"])               # total income (1z+2b+3b+...+8)
    L["10"] = 0                                     # adjustments (Sch 1) — none in v1
    L["11a"] = money(L["9"] - L["10"])              # adjusted gross income

    # --- deduction & taxable income (page 2) ---
    L["11b"] = L["11a"]                             # AGI carried to page 2
    L["12e"] = C.STD_DEDUCTION[fs]                  # standard / itemized deduction
    L["13a"] = 0                                    # QBI deduction (8995) — none in v1
    L["13b"] = 0                                    # additional deductions (Sch 1-A) — none in v1
    L["14"] = money(L["12e"] + L["13a"] + L["13b"]) # total deductions
    L["15"] = money(max(0, L["11b"] - L["14"]))     # taxable income

    # --- tax ---
    L["16"] = tax_line16(L["15"], fs)               # tax
    L["17"] = 0                                     # Schedule 2 line 3 — none in v1
    L["18"] = money(L["16"] + L["17"])
    L["19"] = ctx.get("sch8812", "ctc")             # child tax credit / ODC
    L["20"] = 0                                     # Schedule 3 line 8 — none in v1
    L["21"] = money(L["19"] + L["20"])
    L["22"] = money(max(0, L["18"] - L["21"]))      # tax after nonrefundable credits
    L["23"] = 0                                     # Schedule 2 line 21 — none in v1
    L["24"] = money(L["22"] + L["23"])              # total tax

    # --- payments ---
    L["25a"] = money(need(inp, "w2_withholding"))   # W-2 box 2 federal withholding
    L["25d"] = L["25a"]                             # total withholding (25a+25b+25c)
    L["26"] = 0                                     # estimated payments — none in v1
    L["27a"] = ctx.get("sch_eic", "eitc")           # earned income credit (EIC)
    L["28"] = ctx.get("sch8812", "actc")            # additional CTC (refundable)
    L["32"] = money(L["27a"] + L["28"])             # total other payments & refundable credits (+29,30,31=0)
    L["33"] = money(L["25d"] + L["26"] + L["32"])   # total payments

    # --- refund / owe ---
    if L["33"] >= L["24"]:
        L["34"] = money(L["33"] - L["24"])          # overpayment / refund
        L["37"] = 0
    else:
        L["34"] = 0
        L["37"] = money(L["24"] - L["33"])          # amount you owe
    return L
