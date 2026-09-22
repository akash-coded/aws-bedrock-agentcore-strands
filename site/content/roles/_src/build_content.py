#!/usr/bin/env python3
"""Dump the authored Python role content to JSON for the renderer.

Authoring happens in Python because templates and prompts are multi-line strings with quotes in
them, and hand-escaping those into JSON is how mistakes get in. Run this after editing any
``<role>_*.py`` here; commit both the source and the generated JSON.

    python site/content/roles/_src/build_content.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent

REQUIRED_STEP = {"n", "id", "phase", "title", "when", "purpose", "activities", "ai",
                 "artifact", "template", "prompts", "example", "pitfalls", "done_when"}
REQUIRED_ROLE = {"id", "name", "short", "accent", "tagline", "arc", "intro", "owns",
                 "not_yours", "ai_stance", "reads"}

# role id -> module stem. A role is built when all three of <stem>_a/_b/_c.py exist, so a role in
# progress simply does not appear on the site until its three files land.
STEMS = {
    "product-manager": "product_manager",
    "solution-architect": "solution_architect",
    "engineering": "engineering",
    "qa": "qa",
    "devops": "devops",
}


def discover() -> dict[str, tuple[str, list[str]]]:
    found = {}
    for rid, stem in STEMS.items():
        mods = [f"{stem}_{suffix}" for suffix in ("a", "b", "c")]
        if all((SRC / f"{m}.py").exists() for m in mods):
            found[rid] = (mods[0], mods)
    return found


def load(mod: str) -> dict:
    ns: dict = {}
    exec((SRC / f"{mod}.py").read_text(encoding="utf-8"), ns)  # noqa: S102 - our own authored content
    return ns


def check(role: dict) -> list[str]:
    bad = []
    missing = REQUIRED_ROLE - set(role)
    if missing:
        bad.append(f"role {role.get('id')}: missing {sorted(missing)}")
    seen_ids, seen_n = set(), set()
    for s in role["steps"]:
        where = f"{role['id']} step {s.get('n')}"
        m = REQUIRED_STEP - set(s)
        if m:
            bad.append(f"{where}: missing {sorted(m)}")
        if s["id"] in seen_ids:
            bad.append(f"{where}: duplicate id {s['id']}")
        if s["n"] in seen_n:
            bad.append(f"{where}: duplicate number")
        seen_ids.add(s["id"]); seen_n.add(s["n"])
        if not s["activities"]:
            bad.append(f"{where}: no activities")
        if not s["template"].get("body", "").strip():
            bad.append(f"{where}: empty template")
        if not s["prompts"]:
            bad.append(f"{where}: no prompts")
        for p in s["prompts"]:
            if not {"title", "when", "body"} <= set(p):
                bad.append(f"{where}: prompt missing a field")
        if not s["done_when"].strip():
            bad.append(f"{where}: no done_when")
    if [s["n"] for s in role["steps"]] != list(range(1, len(role["steps"]) + 1)):
        bad.append(f"{role['id']}: steps are not numbered 1..n in order")
    if len(role["arc"]) != len(role["steps"]):
        bad.append(f"{role['id']}: arc has {len(role['arc'])} labels for {len(role['steps'])} steps")
    return bad


def main() -> int:
    problems, built = [], []
    roles = discover()
    skipped = sorted(set(STEMS) - set(roles))
    for rid, (head_mod, step_mods) in roles.items():
        role = dict(load(head_mod)["HEAD"])
        steps: list[dict] = []
        for m in step_mods:
            ns = load(m)
            for key in sorted(k for k in ns if k.startswith("STEPS")):
                steps.extend(ns[key])
        role["steps"] = sorted(steps, key=lambda s: s["n"])
        problems += check(role)
        if problems:
            continue
        path = OUT / f"{rid}.json"
        path.write_text(json.dumps(role, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        n_p = sum(len(s["prompts"]) for s in role["steps"])
        n_a = sum(len(s["activities"]) for s in role["steps"])
        built.append(f"  {rid}.json — {len(role['steps'])} steps, {n_a} activities, "
                     f"{n_p} prompts, {len(role['steps'])} templates ({path.stat().st_size:,} bytes)")
    if problems:
        print("content problems:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1
    print("\n".join(["built:"] + built))
    if skipped:
        print("not yet authored: " + ", ".join(skipped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
