"""engine + form-wiring tests. these assert PLUMBING invariants that hold
regardless of the (still placeholder) IRS numbers, plus fail-loud behavior.

run: `python -m pytest` from repo root, or `python years/2025/tests/test_plumbing.py`.
NOTE: real tax-number cases live in tests/cases/*.json and assert EXACT match
once expecteds are filled from Pub 1436 — see test_cases() below.
"""
import importlib
import json
from pathlib import Path

import pytest

from engine.money import Missing, money, need
from engine.registry import FEDERAL_2025, load
from engine.solver import run, topo_sort

f1040 = importlib.import_module("years.2025.federal.forms.f1040")

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
    # f1040 depends on the schedules -> must come after all of them.
    assert order.index("f1040") > order.index("sch8812")
    assert order.index("f1040") > order.index("sch_eic")


# --- form wiring (independent of bracket numbers) ---------------------------
def test_f1040_cascade_wiring():
    sol = run(load(FEDERAL_2025), BASE_INPUTS).all()
    L = sol["f1040"]
    assert L["1a"] == BASE_INPUTS["w2_wages"]           # wages -> 1a
    assert L["2b"] == BASE_INPUTS["interest_income"]    # interest -> 2b (not Sch 1)
    assert L["9"] == L["1z"] + L["2b"]                  # total income
    assert L["11a"] == L["9"] - L["10"]                 # AGI (2025: line 11a)
    assert L["15"] == max(0, L["11b"] - L["14"])        # taxable income (11b - total deductions)
    assert L["24"] == L["22"] + L["23"]                 # total tax
    assert L["33"] == L["25d"] + L["26"] + L["32"]      # total payments
    # never both a refund and a balance due
    assert L["34"] == 0 or L["37"] == 0


def test_tax_line16_formula_path_exact():
    # >= $100k uses the Tax Computation Worksheet (pure bracket formula), so this
    # is hand-computable ground truth, independent of the code:
    #   single, taxable $150,000 (2025 brackets):
    #   .10*11925 + .12*(48475-11925) + .22*(103350-48475) + .24*(150000-103350)
    #   = 1192.50 + 4386.00 + 12072.50 + 11196.00 = 28847
    assert f1040.tax_line16(150_000, "single") == 28847


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
