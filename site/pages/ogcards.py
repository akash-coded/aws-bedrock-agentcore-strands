"""Social cards: one 1200×630 picture per page, drawn from the page's own title and one line.

``sheet(out)`` writes ``_site/og/_sheet.html`` during ``build.py --shots``; ``tools/ogshots.mjs``
screenshots each card as a JPEG into ``site/assets/og/``, and ``render.og_image`` points a page at
its card when the file exists. The card is the site's own grammar: bone paper, the section's hue as
a bar, the title set large, the line under it, the site's name and address at the foot.
"""
from __future__ import annotations

import html
from pathlib import Path

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731

HUE = {"lesson": "#3F51C4", "track": "#3F51C4", "learn": "#3F51C4", "home": "#2F6B57", "role": "#3E6B8A",
       "protocol": "#7A6A46", "models": "#6B4E8A", "templates": "#0E7F7C", "prompts": "#0E7F7C",
       "frameworks": "#8C5B6B", "simulator": "#2F6B57"}


def card(name: str, kind: str, kicker: str, title: str, line: str) -> str:
    hue = HUE.get(kind, "#3E6B8A")
    title = title.replace("-", "\u2011")   # a hyphenated word never breaks across lines
    big = 58 if len(title) <= 48 else 50 if len(title) <= 64 else 42
    return (f'<div class="ogcard" data-og="{E(name)}" style="--h:{hue}">'
            f'<div class="bar"></div><div class="body"><p class="k">{E(kicker)}</p>'
            f'<h1 style="font-size:{big}px">{E(title)}</h1><p class="l">{E(line)}</p></div>'
            f'<div class="foot"><span class="brand">The agentic manual</span>'
            f'<span class="url">akash-coded.github.io/aws-bedrock-agentcore-strands</span></div></div>')


CSS = """
body{margin:0;background:#2a2d33;padding:20px;display:grid;gap:20px;justify-items:start}
.ogcard{width:1200px;height:630px;box-sizing:border-box;background:#F7F6F2;color:#16150F;position:relative;overflow:hidden;
  font-family:Inter,-apple-system,"Segoe UI",Roboto,sans-serif;display:grid;grid-template-rows:1fr auto;
  background-image:linear-gradient(rgba(22,21,15,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(22,21,15,.06) 1px,transparent 1px);
  background-size:48px 48px}
.ogcard::after{content:"";position:absolute;right:-220px;top:-260px;width:720px;height:720px;border-radius:50%;
  background:radial-gradient(closest-side,color-mix(in oklab,var(--h) 26%,transparent),transparent 72%);filter:blur(10px)}
.ogcard .bar{position:absolute;left:0;top:0;bottom:0;width:18px;background:var(--h)}
.ogcard .body{padding:0 80px 0 96px;position:relative;z-index:1;align-self:center}
.ogcard .k{margin:0 0 22px;font-size:24px;font-weight:600;color:var(--h);display:flex;align-items:center;gap:14px}
.ogcard .k::before{content:"";width:34px;height:4px;background:var(--h);border-radius:2px}
.ogcard h1{margin:0 0 26px;font-family:"Instrument Sans",Inter,sans-serif;font-weight:700;letter-spacing:-.03em;line-height:1.06;
  max-width:980px;text-wrap:balance;color:#16150F}
.ogcard .l{margin:0;font-size:27px;line-height:1.4;color:#44423B;max-width:960px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.ogcard .foot{padding:0 80px 44px 96px;display:flex;justify-content:space-between;align-items:baseline;position:relative;z-index:1}
.ogcard .brand{font-family:"Instrument Sans",Inter,sans-serif;font-weight:650;font-size:26px}
.ogcard .url{font-size:20px;color:#696660}
"""


def sheet(out: Path, cards: list[str]) -> Path:
    p = out / "og" / "_sheet.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>og cards</title>'
                 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap">'
                 f"<style>{CSS}</style></head><body>{''.join(cards)}</body></html>", encoding="utf-8")
    return p


def all_cards(roles: list[dict]) -> list[str]:
    from pages import learn
    _m, tracks, lessons = learn.load()
    C = [card("home", "home", "PDLCs for the agentic era", "Every agentic delivery method. One manual. Your role, end to end.",
              "AI-DLC, AIDD, BMAD, spec-driven development and the PDLC that ties them together, by role."),
         card("learn", "learn", "A free tutorial", "Agentic PDLC Tutorial: Run AI Agent Projects, Step by Step",
              f"{len(lessons)} short lessons on running software where an AI model does part of the work."),
         card("protocol", "protocol", "For leadership", "The agentic operating protocol",
              "What changes, who does what, the four decisions only leadership can make, and ninety days."),
         card("models", "models", "Intuition", "Twelve mental models for software that decides",
              "What each predicts, the mistake it prevents, and a test for whether it has landed."),
         card("templates", "templates", "The template library", "Artefact templates", "Every artefact skeleton in the manual, by role, with a copy button."),
         card("prompts", "prompts", "The prompt library", "Prompts to paste", "Every prompt in the manual: the job, the rules and the output shape."),
         card("frameworks", "frameworks", "Reference", "Frameworks, acronyms and the pictures",
              "AI-DLC, AIDD, BMAD and SDD on one spine, every acronym, the risk ladder and chained probability."),
         card("simulator", "simulator", "The SkyWays playbook", "Ninety days of one airline's agentic build, playable",
              "Thirteen dated episodes, nine simulations, seventeen calculators.")]
    for r in roles:
        C.append(card(r["id"], "role", "Your role, end to end", r["name"], r["tagline"].replace("*", "")))
    for t in tracks:
        C.append(card(f"learn-{t.id}", "track", "A track of the tutorial", t.title, t.blurb))
        for l in t.lessons:
            C.append(card(f"learn-{l.slug}", "lesson", f"Lesson {l.n} · {t.title}", l.title, l.dek or l.description))
    return C
