"""Schedule 8812 — Child Tax Credit / Additional CTC. v1 SKELETON.

placeholder: ctc = children * CTC_PER_CHILD. NO phaseout, NO earned-income
test, NO refundable ACTC split. real logic from 8812 instructions + worksheet.
constants are placeholder zeros — do not trust output.
"""
from engine.money import money, need

from .. import constants as C

ID = "sch8812"
DEPENDS_ON: list = []


def compute(inp, ctx):
    L = {}
    kids = need(inp, "num_qualifying_children")
    # TODO #3 real: phaseout vs AGI, limit to tax liability, refundable ACTC
    # (lesser of remaining credit or 15% * (earned income - 2500), cap 1700/child).
    L["ctc"] = money(kids * C.CTC_PER_CHILD)   # nonrefundable, NO phaseout/limit yet
    L["actc"] = 0                              # refundable portion — stub until #3
    return L
