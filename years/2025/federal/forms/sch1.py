"""Schedule 1 — Additional Income & Adjustments. NOT IN v1. FUTURE STUB.

v1 income (W-2 wages, 1099-INT interest) goes straight onto the 1040 — wages on
line 1a, taxable interest on line 2b. 1099-INT interest does NOT belong here.
Schedule 1 is for OTHER income (unemployment, business via Sch C, etc.) and
above-the-line adjustments — add those later. Not registered in FEDERAL_2025.
"""
from engine.money import money, need

ID = "sch1"
DEPENDS_ON: list = []


def compute(inp, ctx):
    L = {}
    # placeholder for future additional income -> 1040 line 8, adjustments -> line 10.
    L["10"] = money(need(inp, "additional_income"))
    return L
