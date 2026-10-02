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
            f'<div class="foot"><span class="brand">{MARK}SkyWays<i>The agentic manual</i></span>'
            f'<span class="url">akash-coded.github.io/aws-bedrock-agentcore-strands</span></div></div>')


# the site's mark, in the card's own two inks
MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="13" fill="none" stroke="currentColor" '
        'stroke-width="2.4" stroke-dasharray="58 24" stroke-linecap="round" transform="rotate(-38 16 16)"/>'
        '<path d="M8 17.5 24.5 9 19 24l-3.4-5.6z" fill="var(--mk,#3F51C4)"/>'
        '<path d="M15.6 18.4 24.5 9" stroke="var(--mkl,#F7F6F2)" stroke-width="1.2"/></svg>')


def home_card(title: str, line: str, facts: str) -> str:
    """The home page's card is the home page: the headline beside the Earth and the one flight."""
    from pages import globe
    return (f'<div class="ogcard oghome" data-og="home"><div class="scene">{globe.still()}</div>'
            f'<div class="body"><p class="brand">{MARK}SkyWays<i>The agentic manual</i></p>'
            f'<h1>{title}</h1><p class="l">{E(line)}</p></div>'
            f'<div class="foot"><span class="facts">{E(facts)}</span>'
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
.ogcard .brand{font-family:"Instrument Sans",Inter,sans-serif;font-weight:700;font-size:27px;letter-spacing:-.02em;display:flex;align-items:center;gap:12px}
.ogcard .brand svg{width:36px;height:36px}
.ogcard .brand i{font:400 21px Inter,sans-serif;font-style:normal;letter-spacing:0;color:#696660;padding-left:14px;border-left:1.5px solid #D5D0C4}
.oghome{background:#121316;color:#ECEAE4;background-image:radial-gradient(60% 90% at 78% 50%,rgba(127,169,204,.2),transparent 70%),radial-gradient(40% 60% at 0% 110%,rgba(169,140,208,.16),transparent 70%)}
.oghome::after{display:none}
.oghome .scene{position:absolute;right:-8px;top:-28px;width:690px;height:690px}
.oghome .scene svg{width:100%;height:100%;display:block}
.oghome .body{padding:0 0 0 72px;max-width:560px}
.oghome .brand{margin:0 0 54px;color:#ECEAE4;--mk:#8E9BF0;--mkl:#121316}
.oghome .brand i{color:#93908A;border-left-color:#2B2E34}
.oghome h1{font-size:62px;line-height:1.02;letter-spacing:-.045em;font-weight:650;color:#ECEAE4;margin:0 0 24px;max-width:560px;text-wrap:balance}
.oghome h1 em{font-style:normal;color:#7E7D7A}
.oghome .l{font-size:23px;line-height:1.45;color:#C3C0B8;max-width:500px;-webkit-line-clamp:3}
.oghome .foot{padding:0 80px 40px 72px;display:grid;gap:6px;justify-content:start}
.oghome .facts{font:500 19px "Geist Mono",ui-monospace,Menlo,monospace;color:#93908A}
.oghome .url{color:#93908A}
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
    n_t = sum(len(r["steps"]) for r in roles)
    n_p = sum(len(s["prompts"]) for r in roles for s in r["steps"])
    C = [home_card("One manual for building software <em>with AI agents.</em>",
                   "One lifecycle through five roles, worked end to end on a fictional airline's ninety-day build.",
                   f"{len(lessons)} lessons · {n_t} templates · {n_p} prompts"),
         card("method", "home", "The method", "The SkyWays PDLC on one page",
              "Four phases, one hard gate and eight loops, with each role across them and what a model may draft."),
         card("learn", "learn", "A free tutorial", "Agentic PDLC Tutorial: Run AI Agent Projects, Step by Step",
              f"{len(lessons)} short lessons on running software where an AI model does part of the work."),
         card("protocol", "protocol", "For leadership", "Four decisions only you can make",
              "Twenty minutes, and you leave with four questions for your next review."),
         card("models", "models", "Mental models", "Twelve rules of thumb for software that decides",
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
