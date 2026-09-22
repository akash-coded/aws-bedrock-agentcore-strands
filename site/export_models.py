#!/usr/bin/env python3
"""Export the mental models to a wiki page, from the same data the site renders.

The site page carries the drawings; the wiki copy carries the words. Both come from
``pages/models.py`` so a change to a model reaches both.

    python3 site/export_models.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
sys.path.insert(0, str(SITE))
from pages import models as M  # noqa: E402

WIKI = SITE.parent / "wiki"
LIVE = "https://akash-coded.github.io/aws-bedrock-agentcore-strands/"


def clean(s: str) -> str:
    """The site content carries a little inline HTML; the wiki wants markdown."""
    s = re.sub(r"</?em>", "*", s)
    s = re.sub(r"</?strong>", "**", s)
    s = re.sub(r"<code>([^<]*)</code>", r"`\1`", s)
    return re.sub(r"\s+", " ", s).strip()


def link(label: str, href: str) -> str:
    if href.startswith("http"):
        return f"[{label}]({href})"
    return f"[{label}]({LIVE}{href.lstrip('./')})"


def page() -> str:
    L = ["# Mental models", "",
         "**Twelve shapes that make the rest of this playbook predictable.**", "",
         "A procedure tells you what to do on Tuesday. A model tells you what to expect before you "
         "start, which is what lets somebody make a good call on a case this playbook never covered.",
         "",
         f"Each one below is the model, what it predicts, the mistake it prevents, the part that is "
         f"easy to miss, and a test for whether it has landed. The [illustrated version]({LIVE}models/) "
         f"draws each one; this copy is the reading text.", "",
         "---", "", "## The twelve", "",
         "| # | Model | In one line |", "| --- | --- | --- |"]
    for i, m in enumerate(M.MODELS, 1):
        anchor = re.sub(r"[^a-z0-9]+", "-", m["name"].lower()).strip("-")
        L.append(f"| {i} | [**{m['name']}**](#{anchor}) | {clean(m['one'])} |")
    L += ["", "---", ""]
    for i, m in enumerate(M.MODELS, 1):
        L += [f"## {m['name']}", "",
              f"> {clean(m['one'])}", "",
              f"**What it predicts.** {clean(m['predicts'])}", "",
              f"**The mistake it prevents.** {clean(m['prevents'])}", "",
              f"**The part that is easy to miss.** {clean(m['subtle'])}", "",
              f"**Landed when** — {clean(m['landed'])}", "",
              "Where you meet it: " + " · ".join(link(l, h) for l, h in m["where"]), "",
              "---", ""]
    L += ["## How to use these", "",
          "1. **Teach one a week, not twelve at once.** A model lands when somebody uses it "
          "unprompted in an argument, which takes a fortnight of availability rather than an hour "
          "of exposure.",
          "2. **Use the landed-when line as the test.** Not whether the team can define it — "
          "whether the question it implies has started appearing in reviews.",
          "3. **Expect three to be resisted.** Usually the hold as a lever, the average hiding the "
          "slice, and depth as a dial, because each contradicts something a competent person "
          "currently believes is good practice.",
          "4. **Pair each with its arithmetic once.** The intuition is what you carry; the formula "
          "is what settles the argument. See [Formulas and Calculators](Formulas-and-Calculators).",
          "5. **Keep the subtlety visible.** A model applied past its boundary does more damage "
          "than no model, because it arrives with confidence.", "",
          "---", "",
          "**Next:** [Decision Trees](Decision-Trees) · [Formulas and Calculators](Formulas-and-Calculators) "
          "· [Anti-Patterns](Anti-Patterns) · [The Agentic PDLC](The-Agentic-PDLC)", ""]
    return "\n".join(L)


def main() -> int:
    out = WIKI / "Mental-Models.md"
    out.write_text(page(), encoding="utf-8")
    print(f"wrote {out.name} — {len(M.MODELS)} models, {out.stat().st_size:,} bytes, "
          f"{len(out.read_text(encoding='utf-8').splitlines())} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
