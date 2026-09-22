#!/usr/bin/env python3
"""Export each role journey to a wiki page, from the same JSON the site renders.

The site and the wiki say the same thing because they are generated from one source. The wiki page
is the reading copy: no collapsing, no copy buttons, everything on the page, so it can be read in a
browser tab, printed, or pasted into a document.

    python site/wiki_export.py          # writes ../wiki/Journey-<Role>.md

Existing hand-written ``Role-*.md`` pages are left alone; they cover the method, these cover the
day-to-day. Each links to the other.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent
CONTENT = SITE / "content" / "roles"
WIKI = SITE.parent / "wiki"
LIVE = "https://akash-coded.github.io/aws-bedrock-agentcore-strands/"

# role id -> (wiki page name for the journey, wiki page name for the method page, if one exists)
PAGES = {
    "product-manager": ("Journey-Product-Manager", "Role-Product-Manager"),
    "solution-architect": ("Journey-Solution-Architect", "Role-Solution-Architect"),
    "engineering": ("Journey-Engineering-Lead", "Role-Engineering-Lead"),
    "qa": ("Journey-QA-Lead", "Role-QA-Lead"),
    "devops": ("Journey-DevOps", None),
}


def unmd(s: str) -> str:
    """Site markdown-lite is already markdown; only relative hrefs need absolutising."""
    return re.sub(r"\]\((?!https?:|#)([^)]+)\)", lambda m: f"]({LIVE}{m.group(1)})", s)


def fence(body: str, lang: str) -> str:
    lang = {"markdown": "markdown", "md": "markdown"}.get(lang, lang or "text")
    ticks = "````" if "```" in body else "```"
    return f"{ticks}{lang}\n{body.rstrip()}\n{ticks}"


def page(role: dict) -> str:
    slug, method_page = PAGES[role["id"]]
    live = f"{LIVE}{role['id']}/"
    n_p = sum(len(s["prompts"]) for s in role["steps"])
    n_a = sum(len(s["activities"]) for s in role["steps"])

    L = [f"# {role['name']} · the journey, end to end", "",
         f"**{unmd(role['tagline'])}**", "",
         f"{len(role['steps'])} steps · {n_a} sub-steps · {len(role['steps'])} templates · {n_p} prompts",
         "",
         f"This is the reading copy. The [interactive version]({live}) has a copy button on every "
         f"template and prompt, which is what you want when you are actually doing the work."]
    if method_page:
        L += ["", f"For the method behind it — the loops, the gates, the formulas — see "
                  f"[{method_page.replace('-', ' ')}]({method_page})."]
    L += ["", "---", ""]
    for para in role["intro"]:
        L += [unmd(para), ""]
    L += ["## The arc", "",
          "| # | Step | What it produces |", "| --- | --- | --- |"]
    for s in role["steps"]:
        L.append(f"| {s['n']} | [**{s['phase']}** — {unmd(s['title'])}](#{s['n']}--"
                 f"{re.sub(r'[^a-z0-9]+', '-', s['phase'].lower()).strip('-')}) | {unmd(s['artifact']['name'])} |")

    L += ["", "## What is yours, and what is not", "",
          "| Yours to own | Not yours — stop signing these |", "| --- | --- |"]
    owns, nots = role["owns"], role["not_yours"]
    for i in range(max(len(owns), len(nots))):
        a = unmd(owns[i]) if i < len(owns) else ""
        b = unmd(nots[i]) if i < len(nots) else ""
        L.append(f"| {a} | {b} |")

    L += ["", "## How to use a model in this role", "", f"> {unmd(role['ai_stance'])}", "", "---", ""]

    for s in role["steps"]:
        L += [f"## {s['n']} · {s['phase']}", "",
              f"### {unmd(s['title'])}", "",
              f"*{unmd(s['when'])}*", "",
              unmd(s["purpose"]), "",
              "**What you actually do**", ""]
        for i, a in enumerate(s["activities"], 1):
            L.append(f"{i}. **{unmd(a['do'])}** — {unmd(a['detail'])}")
        L += ["", "**Where a model helps, and where it must not**", "",
              "| Tool | Use it for |", "| --- | --- |"]
        for a in s["ai"]:
            cell = unmd(a["use"])
            if a.get("caution"):
                cell += f"<br>⚠ {unmd(a['caution'])}"
            L.append(f"| **{unmd(a['tool'])}** | {cell} |")
        L += ["", "**The artefact**", "",
              f"| | |", "| --- | --- |",
              f"| Produces | **{unmd(s['artifact']['name'])}** |",
              f"| Good looks like | {unmd(s['artifact']['good'])} |",
              f"| Owner | {unmd(s['artifact']['owner'])} |",
              "", f"<details><summary><b>Template · {s['template']['title']}</b></summary>", "",
              fence(s["template"]["body"], s["template"].get("lang", "markdown")), "", "</details>", ""]
        for p in s["prompts"]:
            L += [f"<details><summary><b>Prompt · {p['title']}</b> — {unmd(p['when'])}</summary>", "",
                  fence(p["body"], "text"), "", "</details>", ""]
        L += [f"**Worked example · {unmd(s['example']['title'])}**", "",
              f"> {unmd(s['example']['body'])}", "", "**Pitfalls**", ""]
        L += [f"- {unmd(p)}" for p in s["pitfalls"]]
        L += ["", f"**Done when** — {unmd(s['done_when'])}", "", "---", ""]

    L += ["## Read next", ""]
    L += [f"- [{l}]({h if h.startswith('http') else LIVE + h})" for l, h in role["reads"]]
    others = [f"[{PAGES[r][0].replace('-', ' ').replace('Journey ', '')}]({PAGES[r][0]})"
              for r in PAGES if r != role["id"] and (CONTENT / f"{r}.json").exists()]
    if others:
        L += ["", "**Other roles:** " + " · ".join(others)]
    L += ["", f"- [The manual, interactive]({LIVE}) · [every template]({LIVE}templates/) · "
              f"[every prompt]({LIVE}prompts/) · [frameworks and acronyms]({LIVE}frameworks/)", ""]
    return "\n".join(L)


def main() -> int:
    written = []
    for rid, (slug, _m) in PAGES.items():
        src = CONTENT / f"{rid}.json"
        if not src.exists():
            continue
        role = json.loads(src.read_text(encoding="utf-8"))
        out = WIKI / f"{slug}.md"
        out.write_text(page(role) + "\n", encoding="utf-8")
        written.append(f"  {out.name} ({out.stat().st_size:,} bytes)")
    print("\n".join(["wiki pages written:"] + written) if written else "no role JSON found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
