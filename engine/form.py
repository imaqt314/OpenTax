"""engine core types. tax-agnostic. never changes per year.

Form = pure fn wrapper. engine treats all forms identically.
Ctx  = store of computed lines; forms read upstream forms through it.
"""
from dataclasses import dataclass
from typing import Callable, Protocol

from engine.money import Missing


class Ctx:
    """holds computed form lines. forms read upstream via ctx.get."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def store(self, form_id: str, lines: dict) -> None:
        self._store[form_id] = lines

    def get(self, form_id: str, line_id: str):
        """read upstream line. fail loud if form not run or line absent."""
        if form_id not in self._store:
            raise Missing(f"form {form_id!r} not run before read of line {line_id!r}")
        lines = self._store[form_id]
        if line_id not in lines:
            raise Missing(f"form {form_id!r} has no line {line_id!r}")
        return lines[line_id]

    def all(self) -> dict:
        """whole solution: {form_id: {line_id: value}}."""
        return {fid: dict(lines) for fid, lines in self._store.items()}


@dataclass(frozen=True)
class Form:
    """engine view of a form. built from a form module by the registry."""

    id: str
    depends_on: list
    compute: Callable[[dict, "Ctx"], dict]


class FormModule(Protocol):
    """shape every form module under years/<yr>/.../forms/ must satisfy."""

    ID: str
    DEPENDS_ON: list

    def compute(self, inp: dict, ctx: Ctx) -> dict: ...
