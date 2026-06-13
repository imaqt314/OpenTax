"""2025 federal constants. DATA ONLY. no logic.
"""

FILING_STATUSES = ("single", "mfj", "mfs", "hoh", "qss")

# TODO real 2025 standard deduction — from 1040 instructions.
STD_DEDUCTION = {
    "single": 15750,
    "mfj": 31500,
    "mfs": 15750,
    "hoh": 23625,
    "qss": 31500,
}

# Real 2025 brackets. each = list of (lower_bound, marginal_rate).
# NOTE: real returns for taxable < $100k use the IRS Tax Tables, not formula.
BRACKETS = {
    "single": [(0, 0.10), (11926, 0.12), (48476, 0.22), (103351, 0.24), (197301, 0.32), (250526, 0.35), (626351, 0.37)],
    "mfj": [(0, 0.10), (23851, 0.12), (96951, 0.22), (206701, 0.24), (394601, 0.32), (501051, 0.35), (751601, 0.37)],
    "mfs": [(0, 0.10), (11926, 0.12), (48476, 0.22), (103351, 0.24), (197301, 0.32), (250526, 0.35), (375801, 0.37)],
    "hoh": [(0, 0.10), (17001, 0.12), (65851, 0.22), (103351, 0.24), (197301, 0.32), (250526, 0.35), (626351, 0.37)],
    "qss": [(0, 0.10), (23851, 0.12), (96951, 0.22), (206701, 0.24), (394601, 0.32), (501051, 0.35), (751601, 0.37)],
}

# --- Schedule 8812 : Child Tax Credit ---------------------------------------
# TODO real per-child amount and phaseout thresholds — from 8812 instructions.
CTC_PER_CHILD = 2200
CTC_PHASEOUT_START = {
    "single": 200000,
    "mfj": 400000,
    "mfs": 200000,
    "hoh": 200000,
    "qss": 200000,
}

# --- Schedule EIC : Earned Income Tax Credit --------------------------------
# TODO real EITC. true value = worksheet + earned-income table + AGI and
# investment-income limits, all in the 1040 instructions (NOT on the form).
EITC_MAX = {0: 649, 1: 4328, 2: 7152, 3: 8046}  # by qualifying-child count (capped at 3)
