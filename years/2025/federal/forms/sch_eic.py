"""Schedule EIC + EITC worksheet. v1 SKELETON.

EITC real value = worksheet + earned-income table lookup (lives in the 1040
INSTRUCTIONS, not on any form) + AGI and investment-income limits. core
principle 4: worksheets hide in instructions.
placeholder: returns EITC_MAX by qualifying-child count. constants are zeros —
do not trust output.
"""
from engine.money import money, need

from .. import constants as C

ID = "sch_eic"
DEPENDS_ON: list = []


def compute(inp, ctx):
    L = {}
    kids = need(inp, "num_qualifying_children")
    n = min(kids, 3)
    # TODO real: earned-income table, AGI/investment limits, ineligibility cases.
    L["eitc"] = money(C.EITC_MAX.get(n, 0))
    return L
