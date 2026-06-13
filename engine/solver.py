"""solver. topo-sort forms by depends_on, run each once in order.

engine knows no tax. it just resolves dependency order and runs pure fns.
"""
from engine.form import Ctx
from engine.money import Missing


def topo_sort(forms: list) -> list:
    """order forms so every form runs after its depends_on. detect cycles."""
    by_id = {f.id: f for f in forms}
    order: list = []
    done: set = set()
    active: set = set()

    def visit(fid: str, stack: list) -> None:
        if fid in done:
            return
        if fid in active:
            raise ValueError(f"dependency cycle: {' -> '.join(stack + [fid])}")
        if fid not in by_id:
            raise Missing(f"form {fid!r} is required but not loaded")
        active.add(fid)
        for dep in by_id[fid].depends_on:
            visit(dep, stack + [fid])
        active.discard(fid)
        done.add(fid)
        order.append(by_id[fid])

    for f in forms:
        visit(f.id, [])
    return order


def run(forms: list, inputs: dict) -> Ctx:
    """run all forms in dependency order. return filled Ctx (the solution)."""
    ctx = Ctx()
    for f in topo_sort(forms):
        ctx.store(f.id, f.compute(inputs, ctx))
    return ctx
