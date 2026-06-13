"""registry. forms register here; load() builds Form list for the solver.

form modules use relative imports for their year constants, so they are loaded
by dotted path via importlib (a dir named "2025" can't be a statement-import).
"""
import importlib

from engine.form import Form

# federal v1 form modules (dotted paths). order irrelevant — solver topo-sorts.
FEDERAL_2025 = [
    "years.2025.federal.forms.sch_eic",
    "years.2025.federal.forms.sch8812",
    "years.2025.federal.forms.f1040",
]


def load(module_paths: list) -> list:
    """import each form module, wrap as engine Form."""
    forms = []
    for path in module_paths:
        mod = importlib.import_module(path)
        forms.append(Form(id=mod.ID, depends_on=list(mod.DEPENDS_ON), compute=mod.compute))
    return forms
