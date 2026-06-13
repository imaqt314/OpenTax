"""engine + form-wiring tests. these assert PLUMBING invariants that hold
regardless of the (still placeholder) IRS numbers, plus fail-loud behavior.

run: `python -m pytest` from repo root, or `python years/2025/tests/test_plumbing.py`.
NOTE: real tax-number cases live in tests/cases/*.json and assert EXACT match
once expecteds are filled from Pub 1436 — see test_cases() below.
"""
import json
from pathlib import Path

import pytest

from engine.money import Missing, money, need
from engine.registry import FEDERAL_2025, load
from engine.solver import run, topo_sort

CASES_DIR = Path(__file__).parent / "cases"

BASE_INPUTS = {
    "filing_status": "single",
    "w2_wages": 50000,
    "w2_withholding": 6000,
    "interest_income": 320,
    "num_qualifying_children": 2,
}


# --- engine: money -----------------------------------------------------------
def test_money_half_up():
    assert money("0.50") == 1
    assert money("1.49") == 1
    assert money("1.50") == 2
    assert money(50000) == 50000


def test_need_fails_loud():
    with pytest.raises(Missing):
        need({}, "w2_wages")


# --- engine: solver ----------------------------------------------------------
def test_topo_order_respects_depends_on():
    forms = load(FEDERAL_2025)
    order = [f.id for f in topo_sort(forms)]
    # f1040 depends on the three schedules -> must come after all of them.
    assert order.index("f1040") > order.index("sch1")
    assert order.index("f1040") > order.index("sch8812")
    assert order.index("f1040") > order.index("sch_eic")


# --- form wiring (independent of placeholder numbers) ------------------------
def test_f1040_cascade_wiring():
    sol = run(load(FEDERAL_2025), BASE_INPUTS).all()
    L = sol["f1040"]
    assert L["1a"] == BASE_INPUTS["w2_wages"]
    assert L["8"] == sol["sch1"]["10"]                 # additional income wired
    assert L["9"] == L["1a"] + L["8"]                  # total income
    assert L["15"] == max(0, L["11"] - L["12"])        # taxable income
    assert L["33"] == L["25a"] + L["27"]               # total payments
    # exactly one of refund / owe is nonzero
    assert (L["34"] == 0) != (L["37"] == 0) or L["34"] == L["37"] == 0


def test_missing_input_fails_loud():
    bad = dict(BASE_INPUTS)
    del bad["w2_wages"]
    with pytest.raises(Missing):
        run(load(FEDERAL_2025), bad)


# --- ground-truth cases (exact match; nulls skipped until filled) -----------
@pytest.mark.parametrize("case_path", sorted(CASES_DIR.glob("*.json")))
def test_cases(case_path):
    case = json.loads(case_path.read_text())
    sol = run(load(FEDERAL_2025), case["inputs"]).all()
    for form_id, lines in case["expect"].items():
        for line_id, expected in lines.items():
            if expected is None:
                continue  # TODO: fill from Pub 1436, then this asserts exact
            assert sol[form_id][line_id] == expected, (
                f"{form_id} line {line_id}: got {sol[form_id][line_id]}, "
                f"expected {expected}"
            )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
