"""stages c + e: human confirm/edit, and post-compute override.

stage c: show every parsed value next to its source; flag low-confidence; user
edits/deletes/adds; nothing computes until confirm. to_inputs() strips the
{value,src,confidence} wrappers into the clean inputs dict the solver eats.
stage e: user can override any computed line ("you changed it, you own it").
"""


def to_inputs(draft: dict) -> dict:
    """strip tag wrappers -> {key: value}. plain values pass through."""
    out = {}
    for k, v in draft.items():
        if isinstance(v, dict) and "value" in v:
            out[k] = v["value"]
        else:
            out[k] = v
    return out


def low_confidence(draft: dict) -> list:
    """keys flagged low-confidence — surface these for human check."""
    return [
        k for k, v in draft.items()
        if isinstance(v, dict) and v.get("confidence") == "low"
    ]


def apply_overrides(solution_lines: dict, overrides: dict) -> dict:
    """override computed lines for one form. returns new dict; user owns these."""
    out = dict(solution_lines)
    out.update(overrides)
    return out
