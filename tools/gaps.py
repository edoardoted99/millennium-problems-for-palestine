"""Shared helpers: load gap files and map gap ids to Lean module names."""
from __future__ import annotations

import os
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAPS_DIR = ROOT / "gaps"
# MPP_LEAN_DIR lets you build outside the repo (e.g. to keep .lake out of a synced folder).
LEAN_DIR = pathlib.Path(os.environ.get("MPP_LEAN_DIR", ROOT / "lean"))
SOLUTIONS_DIR = LEAN_DIR / "MPP" / "Solutions"

ID_RE = re.compile(r"^[a-z]+-[0-9]{3}[a-z]?$")
IMPORT_RE = re.compile(r"^(Mathlib(\.\w+)*|MPP\.Defs(\.\w+)+|MPP\.Solutions\.\w+)$")
REQUIRED = ("id", "problem", "title", "status", "statement")
STATUSES = ("open", "closed")


def module_name(gap_id: str) -> str:
    """pnp-001 -> Pnp001"""
    return "".join(part[:1].upper() + part[1:] for part in gap_id.split("-"))


def solution_path(gap_id: str) -> pathlib.Path:
    return SOLUTIONS_DIR / f"{module_name(gap_id)}.lean"


def load_gaps() -> list[dict]:
    gaps = []
    for path in sorted(GAPS_DIR.glob("*/*.yaml")):
        g = yaml.safe_load(path.read_text(encoding="utf-8"))
        missing = [k for k in REQUIRED if k not in g]
        if missing:
            raise ValueError(f"{path}: missing fields {missing}")
        if not ID_RE.match(g["id"]) or path.stem != g["id"]:
            raise ValueError(f"{path}: id {g['id']!r} must match the file name and {ID_RE.pattern}")
        if path.parent.name != g["problem"]:
            raise ValueError(f"{path}: problem {g['problem']!r} must match the folder name")
        if g["status"] not in STATUSES:
            raise ValueError(f"{path}: bad status {g['status']!r}")
        for key, default in (("imports", ["Mathlib"]), ("open", []), ("depends", []),
                             ("context", ""), ("sketch", ""), ("dead", []), ("main", False)):
            if g.get(key) is None:
                g[key] = default
        for m in g["imports"]:
            if not IMPORT_RE.match(m):
                raise ValueError(f"{path}: import {m!r} not allowed")
        g["statement"] = g["statement"].strip()
        g["module"] = module_name(g["id"])
        g["proved"] = solution_path(g["id"]).exists()
        gaps.append(g)
    ids = [g["id"] for g in gaps]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate gap ids: {sorted(dupes)}")
    return gaps


def gap_by_module(gaps: list[dict], module: str) -> dict | None:
    return next((g for g in gaps if g["module"] == module), None)
