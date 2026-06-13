"""Schedule 1 — Additional Income & Adjustments. v1 SKELETON.

v1 channel: taxable interest (1099-INT). carries to 1040 line 8.
NOTE: on the real 1040, 1099-INT taxable interest lands on line 2b, not Sch1.
this wires the additional-income path per the project example; revise placement
against the real 1040 / Schedule 1 instructions before trust.
"""
from engine.money import money, need

ID = "sch1"
DEPENDS_ON: list = []


def compute(inp, ctx):
    L = {}
    interest = need(inp, "interest_income")     # 1099-INT box 1 sum
    L["10"] = money(interest)                    # total additional income -> 1040 L8
    return L
