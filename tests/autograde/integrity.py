"""Detects pasted output that does not belong to the clone being graded."""
from __future__ import annotations

import os
from typing import List, Optional

from . import lsparse
from .context import Ctx
from .textutil import header_field

CAST = {"asha verma", "ben carter", "chitra rao", "course staff"}
MARKER = "/file-operations-lab"
MAX_WARNINGS = 5


def _root(path: str) -> Optional[str]:
    """The part of a pasted path before the lab folder (None for a ~ path or a path outside the lab folder)."""
    if path.startswith("~") or MARKER not in path:
        return None
    return path.split(MARKER, 1)[0]


def _live_owner(ctx: Ctx) -> Optional[str]:
    """The account that owns this clone, when the operating system can tell (not on Windows)."""
    if os.name == "nt" or not ctx.facts.repo:
        return None
    try:
        import pwd
        return pwd.getpwuid(os.stat(ctx.facts.repo).st_uid).pw_name
    except (ImportError, KeyError, OSError):
        return None


def integrity_warnings(ctx: Ctx) -> List[str]:
    """Human-readable warnings; an empty list means the pasted text looks like it came from this clone."""
    if not ctx.repo_mode:
        return []
    warnings: List[str] = []
    name = header_field(ctx.text, "Name")
    if not name:
        warnings.append("the Name line at the top of submission/outputs.txt is blank")
    elif name.lower() in CAST:
        warnings.append(f"the Name line holds a teammate's name ('{name}'); put your own name there")
    first = lsparse.paths(ctx.step("1.1"))
    if first and os.name != "nt" and not ctx.facts.is_this_clone(first[0]):
        warnings.append(f"the pwd you pasted for step 1.1 ({first[0]}) is not this clone; "
                        "the outputs were not produced in this folder")
    reference = _root(first[0]) if first else None
    for step_id, text in sorted(ctx.steps.items()):
        if reference is None or step_id == "1.1" or len(warnings) >= MAX_WARNINGS:
            continue
        for path in lsparse.paths(text):
            root = _root(path)
            if root is not None and root != reference:
                warnings.append(f"the path pasted for step {step_id} ({path}) comes from a different folder than step 1.1")
                break
    accounts = sorted({row.account for text in ctx.steps.values() for row in lsparse.parse_ls_rows(text)})
    live = _live_owner(ctx)
    if len(accounts) > 1:
        warnings.append(f"the listings you pasted show different owners ({', '.join(accounts)}); "
                        "they were not all produced by you in this clone")
    elif accounts and live and accounts[0] != live:
        warnings.append(f"the listings you pasted show the owner '{accounts[0]}' but this clone belongs to '{live}'")
    return warnings
