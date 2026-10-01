#!/usr/bin/env python3
"""Render the role journeys in ``content/roles/*.json`` to static HTML.

Static, not client-rendered: the content is the product, so it ships in the HTML where a crawler,
a reader-mode and a printer can all see it. The only JavaScript is progressive enhancement.

Pages produced:

    index.html              pick a role, and what this is
    <role>/index.html       the journey: steps, activities, AI leverage, artefacts, templates, prompts
    templates/index.html    every template on one page, copyable
    prompts/index.html      every prompt on one page, copyable

Run through ``build.py``; this module is importable and has no side effects on import.
"""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

SITE = Path(__file__).resolve().parent
CONTENT = SITE / "content" / "roles"
BASE_URL = "https://akash-coded.github.io/aws-bedrock-agentcore-strands/"
# Google Search Console ownership of the URL-prefix property for BASE_URL. Public by design: Google
# reads it from the home page. Remove the property in Search Console before removing this.
GOOGLE_SITE_VERIFICATION = "Vs7qR2LsTIfuxi6iYvweDaC4f5nEVaRWcgzGEv2C0-0"
REPO = "https://github.com/akash-coded/aws-bedrock-agentcore-strands"
WIKI = REPO + "/wiki"
AUTHOR = "Akash Das"
PERSON = {"@type": "Person", "name": AUTHOR, "url": "https://github.com/akash-coded",
          "sameAs": ["https://github.com/akash-coded"], "jobTitle": "Solution architect and trainer, agentic AI on AWS"}
ORG = {"@type": "Organization", "@id": BASE_URL + "#org", "name": "SkyWays Consultancy", "url": BASE_URL,
       "founder": PERSON, "sameAs": [REPO, "https://github.com/akash-coded"],
       "description": "The SkyWays PDLC: the best of every agentic way of working, in one operating model. "
                      "The agentic manual and the SkyWays PDLC Simulator are its products."}

# Roles in journey order. One without a JSON file yet is left out of the nav and the home page.
ROLE_ORDER = [
    ("product-manager", "Product manager", "PM", "var(--slate)", "From a vibe to a number you can defend"),
    ("solution-architect", "Solution architect", "SA", "var(--ochre)", "From requirements to a system that holds"),
    ("engineering", "Engineering lead", "ENG", "var(--sage)", "From a story file to a shipped bolt"),
    ("qa", "QA lead", "QA", "var(--plum)", "From 'it works' to a number you can defend"),
    ("devops", "DevOps and platform", "OPS", "var(--violet)", "From a laptop to production, repeatably"),
]

_E = html.escape


def md(text: str) -> str:
    """Markdown-lite: **bold**, `code`, [text](href). Everything else is escaped."""
    out = _E(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", out)

    def link(m: re.Match) -> str:
        href = m.group(2)
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        return f'<a href="{_E(href, quote=True)}"{ext}>{m.group(1)}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, out)

# Before the manual existed, the tool was served at the root, so links of the form
# ".../#/pm/step-6" are in the wiki, in discussions and in people's bookmarks. The tool now lives at
# /workbench/, and this forwards those routes there before anything renders. Runs in <head> on the
# home page only; every other page is new and has no legacy routes to honour.
LEGACY_HASH_REDIRECT = (
    "\n<script>(function(){var h=location.hash;"
    "if(h&&h.charAt(1)===\"/\"){location.replace(\"workbench/\"+h);}"
    "else if(/^#(pdlc|loops|by-role|delegation)$/.test(h)){location.replace(\"method/\"+h);}})();</script>"
)


# A role page overrides --accent. Emitting the literal hex defeats dark mode, because
# base.css already defines a lifted value for each of these tokens and a hard-coded
# light hex cannot follow it, which is how the phase label on every role page came to
# sit at about 3:1 against a dark background. Emit the token, not the colour.
ACCENT_TOKEN = {"#3E6B8A": "slate", "#2F6B57": "sage", "#7A6A46": "ochre",
                "#8C5B6B": "plum", "#6B4E8A": "violet"}


def accent_var(accent: str) -> str:
    if accent.startswith("var("):
        return accent
    token = ACCENT_TOKEN.get(accent.upper()) or ACCENT_TOKEN.get(accent.lower())
    if not token:
        raise SystemExit(f"accent {accent!r} has no theme token; add it to ACCENT_TOKEN "
                         f"or dark mode will render it at the light value")
    return f"var(--{token})"


# The mark: one loop, flown. The same ring and plane the simulator carries, drawn in tokens so it
# follows the theme; the plane keeps one colour on every page, whatever the page's own accent is.
MARK = ('<svg class="mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<circle cx="16" cy="16" r="13" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-dasharray="58 24" stroke-linecap="round" transform="rotate(-38 16 16)"/>'
        '<path d="M8 17.5 24.5 9 19 24l-3.4-5.6z" fill="var(--brand)"/>'
        '<path d="M15.6 18.4 24.5 9" stroke="var(--bone)" stroke-width="1.2"/></svg>')
# Anything that moves on its own for more than a few seconds can be stilled. A checkbox, so it works
# without script: the stylesheet pauses the animations of whatever holds a checked one, and the
# script that draws the globe listens to the same box.
MOTION_TOGGLE = ('<label class="mpause"><input type="checkbox" data-motion-toggle autocomplete="off">'
                 '<span class="vh">Pause the animation</span><i aria-hidden="true"></i></label>')
BURGER = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>')
ROLE_LESSON = {"product-manager": "agentic-pdlc-for-product-managers", "solution-architect": "agentic-pdlc-for-solution-architects",
               "engineering": "agentic-pdlc-for-engineers", "qa": "agentic-pdlc-for-qa", "devops": "agentic-pdlc-for-devops"}



def og_image(name: str) -> str:
    """The page's own social card if it has been rendered (assets/og/<name>.jpg), else the site's."""
    if name and (SITE / "assets" / "og" / f"{name}.jpg").exists():
        return f"{BASE_URL}assets/og/{name}.jpg"
    return f"{BASE_URL}assets/og.png"


def _menu(up: str, nav_id: str) -> str:
    """The categorised drawer. A <details>, so it opens without script; guide.js adds Esc and the
    scrim. Each category is its own <details>, open by default, so it collapses on a small screen."""
    roles = [(f"{rid}/", name, rid) for rid, name, *_ in ROLE_ORDER if (CONTENT / f"{rid}.json").exists()]
    groups = [
        ("Start", [("", "Home", "home"), ("learn/", "The tutorial · lessons in order", "learn"),
                   ("method/", "The method · four phases on one page", "method"),
                   ("learn/interviews/", "Interview banks and careers", "")]),
        ("Your role, end to end", roles),
        ("For leadership", [("protocol/", "The operating protocol", "protocol"),
                            ("models/", "Twelve mental models", "models")]),
        ("Libraries", [("templates/", "Artefact templates", "templates"),
                       ("prompts/", "Prompt templates", "prompts"),
                       ("pictures/", "The picture pack", "pictures"),
                       ("frameworks/", "Frameworks, acronyms and the pictures", "frameworks")]),
        ("Play", [("simulator/", "Ninety Days · the simulator", "simulator"),
                  ("workbench/", "The workbench · calculators, playbooks, the case in depth", "workbench")]),
        ("Elsewhere", [(WIKI, "The wiki", ""), (REPO, "The repository", ""),
                       (REPO + "/discussions/101", "Ideas and contact", "")]),
    ]
    out = []
    for title, items in groups:
        li = []
        for href, label, nid in items:
            ext = href.startswith("http")
            h = href if ext else up + href
            cur = ' aria-current="page"' if nid and nid == nav_id else ""
            tgt = ' target="_blank" rel="noopener"' if ext else ""
            li.append(f'<li><a href="{h}"{cur}{tgt}>{_E(label)}</a></li>')
        out.append(f'<details open><summary>{_E(title)}</summary><ul>{"".join(li)}</ul></details>')
    return (f'<details class="menu" data-menu><summary aria-label="Every page, and search" title="Every page, and search">{BURGER}'
            f'</summary><div class="mp"><div class="mph"><b>Everything, by category</b>'
            f'<button type="button" class="mx" data-menu-close aria-label="Close menu">×</button></div>'
            f'<div class="ms"><input type="search" data-search data-index="{up}search.json" placeholder="Search lessons, steps, pages…" '
            f'aria-label="Search the manual" autocomplete="off"><ol class="mr" data-search-results hidden></ol></div>'
            f'{"".join(out)}</div></details>')


# The top bar: five places, two of them a short list. Everything else is one click deeper, in the
# drawer or on the page it belongs to.
LIBRARY = [("templates", "Templates", "The document each step produces"),
           ("prompts", "Prompts", "Paste into your model, then edit"),
           ("models", "Mental models", "Rules of thumb for agent work"),
           ("frameworks", "Frameworks", "The four methods and every acronym"),
           ("pictures", "Picture pack", "Every diagram, free to reuse"),
           ("workbench", "Workbench", "Seventeen calculators and the case in depth")]


def _nav(up: str, nav_id: str) -> str:
    def link(slug: str, label: str) -> str:
        cur = ' aria-current="page"' if nav_id == slug else ""
        return f'<a href="{up}{slug}/"{cur}>{label}</a>'

    def drop(label: str, items: list[tuple[str, str, str]]) -> str:
        on = any(slug == nav_id for slug, _l, _h in items)
        rows = "".join(
            f'<a href="{up}{slug}/"{" aria-current=page" if slug == nav_id else ""}>'
            f'<b>{_E(name)}</b><small>{_E(hint)}</small></a>' for slug, name, hint in items)
        return (f'<details class="dd{" on" if on else ""}" data-dd><summary>{label}</summary>'
                f'<div class="ddp">{rows}</div></details>')

    roles = [(rid, name, tagline) for rid, name, _s, _c, tagline in ROLE_ORDER if (CONTENT / f"{rid}.json").exists()]
    return (link("learn", "Tutorial") + drop("Roles", roles) + link("method", "Method")
            + drop("Library", LIBRARY) + link("protocol", "Leadership"))


def _wiki_blank(html_: str) -> str:
    """Every link into the wiki opens in a new tab: the wiki is a different site, and a reader
    who followed a reference should still have the manual where they left it."""
    import re as _re

    def fix(m: _re.Match) -> str:
        tag = m.group(0)
        return tag if "target=" in tag else tag[:-1] + ' target="_blank" rel="noopener">'
    return _re.sub(r'<a\b[^>]*href="' + _re.escape(WIKI) + r'[^"]*"[^>]*>', fix, html_)


def shell(*, title: str, desc: str, body: str, depth: int, accent: str | None = None,
          nav_id: str = "", canonical: str = "", head_extra: str = "", own_ld: bool = False,
          crumbs: list[tuple[str, str]] | None = None, tour: list[dict] | None = None,
          kind: str = "", og: str = "", modified: str = "") -> str:
    """The frame every page shares. ``crumbs`` are (label, href) after Home, href relative to the
    page; ``tour`` is the page's walkthrough for guide.js; ``kind`` names the page type so the
    tour is offered once per type, not once per page."""
    up = "../" * depth
    accent_css = f"<style>:root{{--accent:{accent_var(accent)}}}</style>" if accent else ""
    og_img = og_image(og)
    nav = _nav(up, nav_id)

    crumb_html = ""
    ld_crumbs = None
    if crumbs:
        items = [f'<li><a href="{up}">Home</a></li>']
        for i, (label, href) in enumerate(crumbs):
            last = i == len(crumbs) - 1
            items.append(f'<li><span aria-current="page">{_E(label)}</span></li>' if last or not href
                         else f'<li><a href="{_E(href, quote=True)}">{_E(label)}</a></li>')
        crumb_html = (f'<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol>'
                      f'{"".join(items)}</ol></nav></div>')
        base = canonical or BASE_URL
        ld_crumbs = {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL}] + [
            {"@type": "ListItem", "position": i + 2, "name": label,
             "item": base if i == len(crumbs) - 1 or not href else urljoin(base, href)}
            for i, (label, href) in enumerate(crumbs)]}

    ld = {
        "@context": "https://schema.org", "@type": "TechArticle", "headline": title,
        "description": desc, "url": canonical or BASE_URL,
        "author": PERSON,
        "publisher": ORG,
        "image": og_img,
        "isPartOf": {"@type": "WebSite", "name": "The agentic manual", "url": BASE_URL},
        "license": REPO + "/blob/main/LICENSE", "inLanguage": "en",
    }
    if modified:
        ld["dateModified"] = modified
    if ld_crumbs and not own_ld:
        ld = {"@context": "https://schema.org", "@graph": [{k: v for k, v in ld.items() if k != "@context"}, ld_crumbs]}
    tour_html = (f'<script type="application/json" id="tour-steps">{json.dumps(tour, ensure_ascii=False)}</script>'
                 if tour else "")
    return _wiki_blank(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add("js");try{{var t=localStorage.getItem("manual-theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<title>{_E(title)}</title>
<meta name="description" content="{_E(desc, quote=True)}">
<meta name="author" content="{AUTHOR}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">
<link rel="canonical" href="{_E(canonical or BASE_URL, quote=True)}">
<link rel="alternate" type="application/atom+xml" title="The agentic manual: new and updated lessons" href="{up}feed.xml">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#121316">
<meta property="og:type" content="article">
<meta property="og:site_name" content="The agentic manual">
<meta property="og:title" content="{_E(title, quote=True)}">
<meta property="og:description" content="{_E(desc, quote=True)}">
<meta property="og:url" content="{_E(canonical or BASE_URL, quote=True)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{_E(title, quote=True)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_img}">
{"" if own_ld else f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'}
<link rel="preload" href="{up}assets/fonts/geist.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}theme/base.css">
<link rel="stylesheet" href="{up}frame/frame.css">{accent_css}{head_extra}
</head>
<body{f' data-page="{_E(kind, quote=True)}"' if kind else ""}>
<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="in">
  {_menu(up, nav_id)}
  <a class="brand" href="{up}" aria-label="SkyWays, the agentic manual: home">{MARK}<span class="wm">SkyWays</span><small>The agentic manual</small></a>
  <nav aria-label="Sections">{nav}</nav>
  <a class="play" href="{up}simulator/">Simulator</a>
  <button class="tgl" data-theme-toggle aria-label="Switch theme" title="Light or dark">◐</button>
</div></header>
{crumb_html}
{body}
<footer class="ft" data-site-footer><div class="in">
  <div class="fb">{MARK}<b>SkyWays</b><span>The agentic manual and its simulator, free and open source.</span></div>
  <section>
    <h2>About</h2>
    <p><strong>The agentic manual</strong>, its simulator and its workbench are products of
    <strong>SkyWays Consultancy</strong>, conceptualised and built by <strong>{AUTHOR}</strong> and open-sourced
    under the <a href="{REPO}/blob/main/LICENSE">MIT licence</a> for knowledge and experience sharing. Keep the
    attribution when you reuse them.</p>
    <p style="font-size:13.5px;color:var(--soft)">The worked case is set at a fictional airline, also called
    SkyWays. Every figure is illustrative and dated; check it against your own numbers. Not affiliated with, sponsored by or
    endorsed by Amazon Web Services or any airline.</p>
  </section>
  <section><h2>Go deeper</h2><ul>
    <li><a href="{up}simulator/">Ninety Days, the simulator: the worked case as a game</a></li>
    <li><a href="{up}workbench/">The workbench: calculators, playbooks, the case in depth</a></li>
    <li><a href="{up}learn/">The tutorial, every lesson in order</a></li>
    <li><a href="{WIKI}/The-Agentic-PDLC">The method, as a wiki</a></li>
    <li><a href="{WIKI}/Formulas-and-Calculators">Every formula, worked</a></li>
    <li><a href="{WIKI}/Scenario-Library">37 scenarios across twenty sectors</a></li>
  </ul></section>
  <section><h2>Pitch in</h2><ul>
    <li><a href="{REPO}/discussions/101">Suggest an improvement</a></li>
    <li><a href="{REPO}/issues/new/choose">Report a problem</a></li>
    <li><a href="{REPO}">The repository</a></li>
  </ul></section>
  <div class="lg"><span>&copy; 2026 SkyWays Consultancy · {AUTHOR}</span>
    <a href="{REPO}/blob/main/LICENSE">MIT licence</a>
    <a href="{REPO}/tree/main/site/content">Source content</a>
    <a href="{WIKI}/Sources-and-Confidence">Sources and confidence</a></div>
</div></footer>
{tour_html}
<script src="{up}frame/config.js" defer></script>
<script src="{up}frame/frame.js" defer></script>
<script src="{up}theme/site.js" defer></script>
<script src="{up}theme/engine.js" defer></script>
<script src="{up}theme/guide.js" defer></script>
</body>
</html>
""")


def block(kind: str, title: str, subtitle: str, body: str, bid: str) -> str:
    """A copyable code block: template or prompt."""
    return f"""<div class="blk">
<div class="bh"><span class="bt">{_E(title)}</span>{f'<span class="bw">{_E(subtitle)}</span>' if subtitle else ''}
<button class="cp" data-copy="{bid}" aria-label="Copy {_E(kind, quote=True)}">Copy</button></div>
<pre id="{bid}" tabindex="0"><code>{_E(body)}</code></pre></div>"""


def figure_html(step: dict) -> str:
    """A step draws a figure only where the shape of the thing is the lesson."""
    name = step.get("figure")
    if not name:
        return ""
    from pages.figures import FIGURES
    fn = FIGURES.get(name)
    return fn() if fn else ""


def calc_section(step: dict) -> str:
    """A step embeds a calculator only where the reader is about to do arithmetic."""
    name = step.get("calc")
    if not name:
        return ""
    from pages import calcs
    if name not in calcs.SPECS:
        return ""
    return (f'<section><div class="lbl">Work it out on your numbers</div>'
            f"{calcs.render(name)}</section>")


PHASE_TITLE = {"P0": "P0 · Frame: is this worth doing, and is it AI at all?",
               "P1": "P1 · Design & Spec: what exactly, and under whose authority?",
               "P2": "P2 · Build & Prove: does it meet the bar, slice by slice?",
               "P3": "P3 · Run & Learn: is it still doing it, and what did it cost?"}


def step_html(role: dict, s: dict) -> str:
    acts = "".join(
        f'<li><b>{md(a["do"])}</b><span>{md(a["detail"])}</span></li>' for a in s["activities"])
    ai_rows = []
    for a in s["ai"]:
        dont = a["tool"].lower().startswith("do not")
        cau = f'<span class="cau">{md(a["caution"])}</span>' if a.get("caution") else ""
        ai_rows.append(f'<tr class="{"dont" if dont else ""}"><td>{md(a["tool"])}</td>'
                       f'<td>{md(a["use"])}{cau}</td></tr>')
    prompts = "".join(
        block("prompt", p["title"], p["when"], p["body"], f'p-{s["id"]}-{i}')
        for i, p in enumerate(s["prompts"]))
    pitfalls = "".join(f"<li>{md(p)}</li>" for p in s["pitfalls"])
    return f"""<details class="step" id="{s['id']}"{' open' if s['n'] == 1 else ''}>
<summary>
  <span class="sn">{s['n']}</span>
  <span class="sh"><span class="ph">{_E(s['phase'])}<i class="pd" title="{PHASE_TITLE[s['pdlc']]}">{s['pdlc']}</i></span><h3>{md(s['title'])}</h3>
    <span class="wh">{md(s['when'])}</span>
    <span class="jl"><a href="#t-{s['id']}" data-jump>The template</a><a href="#pr-{s['id']}" data-jump>{len(s['prompts'])} prompt{"" if len(s['prompts']) == 1 else "s"}</a></span></span>
  <span class="chev" aria-hidden="true">▾</span>
</summary>
<div class="sb">
  <section><p class="lede" style="font-size:16.5px">{md(s['purpose'])}</p></section>

  <section><div class="lbl">What you actually do</div>
    <ol class="acts">{acts}</ol></section>

  <section><div class="lbl">Where a model helps, and where it must not</div>
    <div class="tw" tabindex="0"><table class="ai"><thead><tr><th>Tool</th><th>Use it for</th></tr></thead>
      <tbody>{''.join(ai_rows)}</tbody></table></div></section>

  <section><div class="lbl">The artefact</div>
    <dl class="art">
      <dt>Produces</dt><dd><strong>{md(s['artifact']['name'])}</strong></dd>
      <dt>Good looks like</dt><dd>{md(s['artifact']['good'])}</dd>
      <dt>Owner</dt><dd>{md(s['artifact']['owner'])}</dd>
    </dl></section>

  <section><div class="lbl">The template</div>
    {block('template', s['template']['title'], 'fill in the angle brackets', s['template']['body'], f"t-{s['id']}")}
  </section>

  <section id="pr-{s['id']}" tabindex="-1"><div class="lbl">Prompts you can paste</div>{prompts}</section>

  <section><div class="lbl">Worked example</div>
    <div class="eg"><h4>{md(s['example']['title'])}</h4><p>{md(s['example']['body'])}</p></div>
    {figure_html(s)}</section>
  {calc_section(s)}

  <section><div class="lbl">Pitfalls</div><ul class="ticks no">{pitfalls}</ul></section>

  <section><div class="done"><span class="k">Done when</span><p>{md(s['done_when'])}</p></div></section>
</div>
</details>"""



STEP_ICON = {
    "search": "Discover Elicit", "check": "Qualify Check Measure", "frame": "Frame Map Baseline Floor",
    "doc": "Specify Define Detail Prepare", "list": "Plan Curate", "lock": "Gate Bound Protect",
    "flag": "Launch Ship Deploy", "chart": "Learn Watch Observe Evolve", "sliders": "Constrain Shape Decide",
    "layers": "Layer Environments Slice", "tool": "Harness Pipeline Operate", "key": "Access",
    "shield": "Attack", "eye": "Shadow", "refresh": "Recover",
}
STEP_ICON_SVG = {
    "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="m20 20-5-5"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    "frame": '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3"/><rect x="8" y="8" width="8" height="8" rx="1"/>',
    "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="5" cy="6" r="1.2"/><circle cx="5" cy="12" r="1.2"/><circle cx="5" cy="18" r="1.2"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "flag": '<path d="M6 21V4"/><path d="M6 4h11l-2 4 2 4H6"/>',
    "chart": '<path d="M4 20h16"/><path d="M7 17v-6M12 17V7M17 17v-9"/>',
    "sliders": '<path d="M5 8h14M5 16h14"/><circle cx="9" cy="8" r="2.2" fill="var(--paper)"/><circle cx="15" cy="16" r="2.2" fill="var(--paper)"/>',
    "layers": '<path d="m12 4 8 4-8 4-8-4z"/><path d="m4 12 8 4 8-4M4 16l8 4 8-4"/>',
    "tool": '<path d="M14.5 5.5a4 4 0 0 0-5 5L4 16l4 4 5.5-5.5a4 4 0 0 0 5-5l-2.5 2.5-2-2z"/>',
    "key": '<circle cx="8" cy="14" r="4"/><path d="m11 11 8-8M16 6l2 2M13 9l2 2"/>',
    "shield": '<path d="M12 3 5 6v6c0 4 3 7 7 9 4-2 7-5 7-9V6z"/>',
    "eye": '<path d="M3 12s3.5-6 9-6 9 6 9 6-3.5 6-9 6-9-6-9-6z"/><circle cx="12" cy="12" r="2.5"/>',
    "refresh": '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v5h-5"/>',
}
_ICON_BY_STEP = {name: ic for ic, names in STEP_ICON.items() for name in names.split()}
PHASE_HUE = {"P0": "slate", "P1": "indigo", "P2": "teal", "P3": "amber"}
PHASE_SHORT = {"P0": "Frame", "P1": "Design &amp; Spec", "P2": "Build &amp; Prove", "P3": "Run &amp; Learn"}


def roadmap(role: dict) -> str:
    """The role's steps as one connected track, grouped by the phase each belongs to."""
    groups: list[tuple[str, list[dict]]] = []
    for s in role["steps"]:
        if groups and groups[-1][0] == s["pdlc"]:
            groups[-1][1].append(s)
        else:
            groups.append((s["pdlc"], [s]))
    out = []
    for ph, steps in groups:
        nodes = "".join(
            f'<a class="rn" href="#{s["id"]}" style="--i:{s["n"] - 1}"><span class="ri"><svg viewBox="0 0 24 24" aria-hidden="true">'
            f'{STEP_ICON_SVG[_ICON_BY_STEP.get(s["phase"], "doc")]}</svg></span>'
            f'<span class="rnum">{s["n"]}</span><span class="rname">{_E(s["phase"])}</span></a>'
            for s in steps)
        out.append(f'<div class="rg" style="--c:var(--dg-{PHASE_HUE[ph]});--n:{len(steps)}">'
                   f'<span class="rp"><b>{ph}</b> {PHASE_SHORT[ph]}</span><div class="rns">{nodes}</div></div>')
    n = len(role["steps"])
    return (f'<section class="roadmap" aria-label="The steps of this role, by phase">'
            f'<div class="rh"><h2>Your {NUM.get(n, str(n))} steps, in order</h2>'
            f'<p>The things this role already does, in the order they happen. Each has gained a part a '
            f'model can do, and each ends on the artefact the next person needs.</p></div>'
            f'<div class="rt">{"".join(out)}</div></section>')


NUM = {6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}

def role_page(role: dict) -> str:
    from pages import _kit as k
    rail = "".join(
        f'<li><a class="rl" data-for="{s["id"]}" href="#{s["id"]}">'
        f'<span class="rn">{s["n"]}</span><span>{_E(s["phase"])}</span></a></li>'
        for s in role["steps"])
    arc = roadmap(role)
    intro = "".join(f"<p>{md(p)}</p>" for p in role["intro"])
    owns = "".join(f"<li>{md(x)}</li>" for x in role["owns"])
    nots = "".join(f"<li>{md(x)}</li>" for x in role["not_yours"])
    reads = "".join(
        f'<li><a href="{_E(h, quote=True)}"'
        f'{" target=_blank rel=noopener" if h.startswith("http") else ""}>{_E(l)}</a></li>'
        for l, h in role["reads"])
    steps = "".join(step_html(role, s) for s in role["steps"])
    n_p = sum(len(s["prompts"]) for s in role["steps"])
    n_a = sum(len(s["activities"]) for s in role["steps"])
    n_f = sum(1 for s in role["steps"] if s.get("figure"))
    n_c = sum(1 for s in role["steps"] if s.get("calc"))
    extra_pills = ""
    if n_f:
        extra_pills += f'<span>{n_f} figures</span>'
    if n_c:
        extra_pills += f'<span>{n_c} calculators</span>'
    first = role["steps"][0]
    orient = k.orient(
        f"<strong>{_E(role['name'])}s</strong> and anyone who has to work with one, plus the "
        f"forward-deployed version of the role, who does this on a customer's site.",
        f"Walk the {len(role['steps'])} steps of this role in order, from <em>{_E(first['phase'])}</em> "
        f"to <em>{_E(role['steps'][-1]['phase'])}</em>, and leave each with the artefact the next person needs.",
        ["Read <b>Yours to own</b> and <b>Not yours</b> first: they are the two boundaries that moved.",
         "Open a step: what you do, where a model helps and where it must not, the artefact, the template, the prompts.",
         "Copy the template, paste the prompts into your model, and check the <b>Done when</b> line before you move on."],
        extra=f'<a class="btn" href="../learn/{ROLE_LESSON[role["id"]]}/">The lesson for this role →</a>')
    tour = k.tour([
        {"sel": ".roadmap", "title": "The journey", "body": f"{len(role['steps'])} steps in the order they happen, grouped by the phase each belongs to. Click one to jump to it; the left rail keeps your place as you scroll."},
        {"sel": ".two", "title": "Two boundaries moved", "body": "What is yours to own, and what to stop signing. In agentic delivery these are the two lists that change; everything else is your job as it was."},
        {"sel": "details.step", "title": "A step, unpacked", "body": "Every step has the same shape: <b>what you actually do</b>, <b>where a model helps and where it must not</b>, the artefact you owe the next person, its template, prompts to paste, a worked SkyWays example, pitfalls and a <b>Done when</b> line."},
        {"sel": "details.step .cp", "title": "Copy, paste, fill in", "body": "Templates and prompts each have a copy button. Fill in the angle brackets; the step explains why each field is there."},
        {"sel": "[data-expand]", "title": "Read it straight through", "body": "Expand all opens every step, which is also how the page prints."},
    ])

    body = f"""<div class="cols two-col">
<aside class="rail wideonly" aria-label="Steps"><p class="railh">The journey</p><ol>{rail}</ol></aside>
<main id="main">
  <header class="phead in-col">
    <p class="kicker">Your role, end to end</p>
    <h1 style="view-transition-name:role-{role['id']}">{_E(role['name'])}</h1>
    <p class="lede">{md(role['tagline'])}.</p>
    <p class="pmeta"><span>{len(role['steps'])} steps</span><span>{n_a} sub-steps</span><span>{len(role['steps'])} templates</span><span>{n_p} prompts</span>{extra_pills}</p>
  </header>

  {orient}

  {arc}

  <div class="sec">{intro}</div>

  <h2 style="margin:0 0 12px">What is yours, and what is not</h2>
  <div class="sec two">
    <div class="card yes"><h3 class="h4">Yours to own</h3><ul class="ticks">{owns}</ul></div>
    <div class="card no"><h3 class="h4">Not yours: stop signing these</h3>
      <ul class="ticks no">{nots}</ul></div>
  </div>

  <div class="sec"><div class="note"><h3 class="h4">How to use a model in this role</h3>
    <p>{md(role['ai_stance'])}</p></div></div>

  <div class="rolehead"><h2>The journey, step by step</h2>
    <button type="button" class="btn ghost sm" data-expand>Expand all</button></div>
  {steps}

  <div class="sec" style="margin-top:36px"><h2 style="margin:0 0 12px">Read next</h2>
    <ul class="readsg">{reads}</ul></div>
</main>
</div>"""
    desc = (f"{role['name']}: {role['tagline']}. {len(role['steps'])} steps, {n_a} sub-steps, "
            f"{len(role['steps'])} templates and {n_p} copy-paste prompts for building with AI.")
    return shell(title=f"{role['name']} · The agentic manual", desc=desc, body=body, depth=1,
                 accent=role["accent"], nav_id=role["id"], canonical=f"{BASE_URL}{role['id']}/",
                 crumbs=[("Roles", ""), (role["name"], "")], tour=tour, kind="role", og=role["id"])


def next_up(lead: str, href: str, label: str, also: tuple[str, str] | None = None) -> str:
    """The foot of a reference page: one sentence, one button and at most one quiet link beside it,
    so no page is a dead end."""
    more = f'<a class="more" href="{also[0]}">{also[1]} <i aria-hidden="true">→</i></a>' if also else ""
    return (f'<div class="nextup"><p>{lead}</p><div class="ba"><a class="btn pri" href="{href}">{label}</a>'
            f"{more}</div></div>")


def library_page(roles: list[dict], kind: str) -> str:
    """One page holding every template, or every prompt, across all roles."""
    from pages import _kit as k
    is_t = kind == "templates"
    label = "Artefact templates" if is_t else "Prompt templates"
    short = "templates" if is_t else "prompts"
    lede = ("A fill-in skeleton for every document the manual asks you to write, from the pain register to "
            "the two-number report."
            if is_t else
            "Every prompt in the manual. Paste one into your model, fill the angle brackets, and edit the "
            "rules to taste.")
    other = ("prompts", "Prompt templates") if is_t else ("templates", "Artefact templates")
    secs, toc, count = [], [], 0
    for role in roles:
        rows = []
        for s in role["steps"]:
            if is_t:
                count += 1
                art = s["artifact"]
                first_do = s["activities"][0]["do"] if s.get("activities") else ""
                rows.append(f'<h3 style="margin:22px 0 8px">{s["n"]}. {md(s["template"]["title"])}'
                            f' <span class="pill pp{s["pdlc"][1]}" title="Phase {s["pdlc"]}">{s["pdlc"]}</span>'
                            f' <span class="pill" style="margin-left:2px">{_E(s["phase"])}</span></h3>'
                            f'<ul class="usewhen"><li><b>Use it when</b><span>{md(s["when"])}.</span></li>'
                            f'<li><b>You produce</b><span>{md(art["name"])}'
                            + (f', owned by {md(art["owner"])}' if art.get("owner") else "") + '.</span></li>'
                            + (f'<li><b>Start with</b><span>{md(first_do)}.</span></li>' if first_do else "")
                            + f'<li><b>Good looks like</b><span>{md(art["good"])}</span></li>'
                            f'<li><b>Explained in</b><span><a href="../{role["id"]}/#{s["id"]}">step {s["n"]}, '
                            f'{_E(s["phase"])}</a></span></li></ul>'
                            + block("template", s["template"]["title"],
                                    f'{role["short"]} step {s["n"]} · {s["artifact"]["name"]}',
                                    s["template"]["body"], f'lt-{role["id"]}-{s["id"]}'))
            else:
                for i, p in enumerate(s["prompts"]):
                    count += 1
                    rows.append(f'<h3 style="margin:22px 0 8px">{md(p["title"])}'
                                f' <span class="pill" style="margin-left:6px">{_E(s["phase"])}</span></h3>'
                                f'<p class="bwhy">Use it {md(p["when"][0].lower() + p["when"][1:])}. From '
                                f'<a href="../{role["id"]}/#{s["id"]}">step {s["n"]}, {_E(s["phase"])}</a>.</p>'
                                + block("prompt", p["title"], p["when"], p["body"],
                                        f'lp-{role["id"]}-{s["id"]}-{i}'))
        n_here = len(role["steps"]) if is_t else sum(len(s["prompts"]) for s in role["steps"])
        secs.append(f'<section id="{role["id"]}" style="scroll-margin-top:84px;margin:0 0 44px">'
                    f'<div class="rolehead"><h2 style="color:{accent_var(role["accent"])}">{_E(role["name"])}: {n_here} {short}, P0 to P3</h2>'
                    f'<div class="try"><span class="tl">Also</span><a href="../{role["id"]}/">The role, step by step</a>'
                    f'<a href="../{other[0]}/#{role["id"]}">The {other[0]} for this role</a></div></div>{"".join(rows)}</section>')
        toc.append(f'<li><a href="#{role["id"]}">{_E(role["name"])}</a></li>')

    compare = f"""<h2 style="margin:0 0 12px">Templates or prompts?</h2>
<div class="sec two tvp">
  <div class="card{' on' if is_t else ''}"><h3 class="h4">Templates</h3><p>Skeletons for the <b>documents each step produces</b>: a
    register, a spec, a bar sheet, a report. You fill the angle brackets and keep the file.</p>
    <p class="eg2">e.g. <code># Pain register · &lt;product&gt;</code></p></div>
  <div class="card{'' if is_t else ' on'}"><h3 class="h4">Prompts</h3><p>Messages you <b>paste into a model</b> to draft, check or
    decompose something: with the job, the rules and the output shape spelled out.</p>
    <p class="eg2">e.g. <code>You are helping a product manager consolidate discovery notes…</code></p></div>
</div>"""
    orient = k.orient(
        ("Anyone about to <strong>write an artefact</strong> the manual asks for, a product manager drafting a pain "
         "register, an architect writing the spec, a QA lead building the bar sheet, a sponsor's two-number report."
         if is_t else
         "Anyone about to <strong>ask a model for help</strong> with a step (drafting, deduplicating, checking, "
         "decomposing) and who wants a prompt that says what shape the answer must take."),
        (f"Find the template for the step you are on, copy it, fill in the angle brackets, and keep it as the "
         f"artefact you hand to the next person." if is_t else
         "Find the prompt for the step you are on, copy it, paste it into your model, replace the angle "
         "brackets with your own material, and edit the rules to taste."),
        ["Pick your role in the left rail (or scroll: they are in journey order).",
         f"Press <b>Copy</b> on the block. {'Paste it into your document.' if is_t else 'Paste it into the model of your choice.'}",
         f"Unsure why a field is there? The line above each block links to the step that explains it."],
        extra=f'<a class="btn" href="../{other[0]}/" style="margin-top:8px">{other[1]} →</a>',
        more="__MORE__")
    tour = k.tour([
        {"sel": ".tvp", "title": "Templates or prompts?", "body": "Two libraries, two jobs. <b>Templates</b> are documents you write and keep. <b>Prompts</b> are messages you send to a model. This page is the " + ("templates" if is_t else "prompts") + "."},
        {"sel": ".rail", "title": "By role", "body": "Five roles, in journey order. Jump to yours; each section links back to the role's own page."},
        {"sel": ".blk", "title": "One block per " + ("template" if is_t else "prompt"), "body": "The header says which step it belongs to. The line above says " + ("what good looks like." if is_t else "when to use it.") + " Angle brackets are yours to fill."},
        {"sel": ".blk .cp", "title": "Copy", "body": "One click copies the whole block, ready to paste."},
    ])
    opener = "" if not is_t else """<div class="sec tmplopen"><h2 style="margin:0 0 12px">What these templates are for, and how to use one</h2>
<div class="tmplgrid">
  <div class="card"><h3 class="h4">What they are for</h3><ul class="ticks">
    <li>Each is the document one step of the SkyWays PDLC produces and the next person needs: a register, a spec, a bar sheet, a report.</li>
    <li>They carry the fields that get forgotten, so the next person never has to ask what you meant.</li>
    <li>Kept in the repository, they are the evidence pack a gate is judged on.</li></ul></div>
  <div class="card"><h3 class="h4">How to use one</h3><ol class="acts">
    <li><b>Find your step.</b><span>Pick your role, then the step you are on; the phase badge says where it sits, P0 to P3.</span></li>
    <li><b>Copy and fill.</b><span>Press Copy, paste it into your document, and replace every angle bracket with your own material. Delete what does not apply; do not leave a placeholder.</span></li>
    <li><b>Hand it on.</b><span>Check the "Good looks like" line, then give it to the person the step names. The step it comes from explains every field.</span></li></ol></div>
  <div class="card ex"><h3 class="h4">One of them, filled in</h3>
    <p style="font-size:13.5px;margin:0 0 8px">The pain register, after two discovery calls at SkyWays:</p>
<pre class="exblk"><code># Pain register · SkyWays rebooking
Pain: Rebooking after a cancellation takes 40 minutes on the phone
Who said it: 6 of 6 transcripts (3 agents, 3 passengers)
Count: 1,850 a month (ticket export, June)
Cost per case: $11.20 agent time + $38 goodwill credit when it goes wrong
Source: tickets tagged REBOOK, Jan to Jun
Owner of the number: Priya (PM)</code></pre>
    <p style="font-size:13.5px;margin:8px 0 0">One line per pain, every number with a source. That is what turns a vibe into something a sponsor can fund.</p></div>
</div></div>"""
    from pages import posters
    posters_html = "" if is_t else (
        '<div class="sec postersec"><h2 style="margin:0 0 6px">How a prompt template is built</h2>'
        '<p class="lede" style="font-size:15.5px">Every prompt in this library has the same five parts, in the same order. '
        'The second picture is the whole library at a glance, by role and by step.</p>'
        + posters.prompt_anatomy() + posters.prompts_by_role()
        + '<p class="lalt">Both pictures are in <a href="../pictures/#pics-posters">the picture pack</a>, with every other diagram of the method.</p></div>')
    body = f"""<div class="cols two-col">
<aside class="rail" aria-label="Roles"><p class="railh">By role</p><ul class="ticks">{''.join(toc)}</ul></aside>
<main id="main">
  <header class="phead in-col"><p class="kicker">The library</p><h1>{label}</h1>
    <p class="lede">{lede}</p>
    <p class="pmeta"><span>{count} {short}</span><span>{len(roles)} roles, in journey order</span><span>a copy button on each</span></p>
  </header>
  {orient.replace("__MORE__", opener + compare)}
  {posters_html}
  {''.join(secs)}
  {next_up("Each one belongs to a step. The role pages walk them in order." if is_t else "Each prompt drafts one of the documents the manual asks for.",
           "../product-manager/" if is_t else "../templates/", "Walk a role, step by step" if is_t else "The templates they fill",
           ("../prompts/", "The prompts that draft them") if is_t else ("../product-manager/", "Walk a role"))}
</main>
</div>"""
    return shell(title=f"{label} · The agentic manual",
                 desc=(f"{count} copy-paste {short} for building software with AI, by role: "
                       + ("the documents each step of the agentic PDLC produces." if is_t else
                          "each states the job, the rules and the output shape.")),
                 body=body, depth=1, nav_id=kind, canonical=f"{BASE_URL}{kind}/",
                 crumbs=[("Libraries", ""), (label, "")], tour=tour, kind=kind, og=kind)


PHASES = [
    ("P0", "Frame", "Is it worth building, and is it AI at all?", "slate", "learn/p0-frame/"),
    ("P1", "Design &amp; Spec", "What exactly, and who signs for it?", "indigo", "learn/p1-design-and-spec/"),
    ("P2", "Build &amp; Prove", "Does it meet the bar, slice by slice?", "teal", "learn/p2-build-and-prove/"),
    ("P3", "Run &amp; Learn", "Is it still working, and what did it cost?", "amber", "learn/p3-run-and-learn/"),
]
# What a team hears when a phase's question went unasked: one line per phase, each from that phase's own
# lesson ("Sound familiar?").
SKIPPED = [
    "The business case says 'significantly faster', and nobody has a number.",
    "The refund limit is $400 in the deck and in the prompt, and nowhere in the code.",
    "The overall score went up after a prompt change, and so did the complaints.",
    "Finance found the token bill before the product manager reported the saving.",
]
# How far each method reaches along the spine: 2 covers the phase, 1 touches it lightly, 0 says nothing,
# "x" is a stage this manual adds to the method (extended BMAD). The same reading as the frameworks
# page's plug board, which carries the detail.
COVERAGE = [
    ("AI-DLC", "learn/what-is-ai-dlc/", "From AWS, built in bolts of days", (2, 2, 2, 2)),
    ("BMAD Method", "learn/what-is-the-bmad-method/", "AI personas, working as an agile team", (2, 2, 2, "x")),
    ("Spec-driven development", "learn/what-is-spec-driven-development/", "The spec is what you maintain", (1, 2, 2, 1)),
    ("AIDD", "learn/what-is-aidd/", "The daily craft with a coding agent", (0, 0, 2, 0)),
]


def home_page(roles: list[dict]) -> str:
    from pages import globe, illos, learn, pictures, spine
    built = {r["id"]: r for r in roles}
    total_steps = sum(len(r["steps"]) for r in roles)
    total_prompts = sum(len(s["prompts"]) for r in roles for s in r["steps"])
    _meta, _tracks, lessons = learn.load()
    n_lessons = len(lessons)
    n_pics = len(pictures.catalogue())
    tracks = "".join(f'<li><a href="learn/{t.id}/"><b>{_E(t.title)}</b>'
                     f'<span>{len(t.lessons)} lessons</span></a></li>' for t in _tracks)
    # the tutorial's "Start where you are" table: one row per kind of reader
    start = (SITE / "content" / "learn" / "start-here.md").read_text(encoding="utf-8")
    table = start.split("## Start where you are", 1)[1].split("\n## ", 1)[0]
    n_starts = sum(1 for ln in table.splitlines() if re.match(r"\| (?!If you|---)", ln))

    # one row per role: where you start, where you end up
    seats = []
    for rid, name, short, colour, tagline in ROLE_ORDER:
        r = built.get(rid)
        if not r:
            continue
        m = re.match(r"From (.+) to (.+)", tagline)
        frm, to = (m.group(1), m.group(2)) if m else ("", tagline)
        n_p = sum(len(s["prompts"]) for s in r["steps"])
        seats.append(f'<li><a href="{rid}/" style="--rc:{colour}"><span class="s-code">{_E(short)}</span>'
                     f'<span class="s-name" style="view-transition-name:role-{rid}">{_E(name)}</span>'
                     f'<span class="s-route"><span>{md(frm)}</span><i aria-hidden="true">→</i><span class="vh"> to </span><b>{md(to)}</b></span>'
                     f'<span class="s-meta">{len(r["steps"])} steps · {n_p} prompts</span>'
                     f'<span class="s-go" aria-hidden="true">→</span></a></li>')
    # Two rows that are not role journeys: the field guide for forward-deployed engineers, and the sponsor's page.
    seats.append('<li><a href="learn/ai-dlc-for-forward-deployed-engineers/" style="--rc:var(--dg-sky)"><span class="s-code">FDE</span>'
                 '<span class="s-name">Forward-deployed engineer</span>'
                 '<span class="s-route"><span>a customer\'s pain</span><i aria-hidden="true">→</i><span class="vh"> to </span>'
                 '<b>a system they run after you leave</b></span>'
                 '<span class="s-meta">8 steps · 1 lesson</span><span class="s-go" aria-hidden="true">→</span></a></li>')
    seats.append('<li><a href="protocol/" style="--rc:var(--ink2)"><span class="s-code">EXEC</span>'
                 '<span class="s-name">Sponsor or executive</span>'
                 '<span class="s-route"><span>funding the work</span><i aria-hidden="true">→</i><span class="vh"> to </span>'
                 '<b>the four decisions only you can make</b></span>'
                 '<span class="s-meta">20 minute read</span><span class="s-go" aria-hidden="true">→</span></a></li>')

    hero = f"""<section class="hero2" id="top" aria-label="Introduction">
  {globe.scene()}
  {MOTION_TOGGLE}
  <div class="in"><div class="hx">
    <p class="eyebrow">The agentic manual</p>
    <h1>One manual for building software <em>with AI agents.</em></h1>
    <p class="lede">It follows one lifecycle through five roles, worked end to end on a fictional airline's
    ninety-day build. Free and open source.</p>
    <div class="ba"><a class="btn pri" href="learn/">Start the tutorial</a>
      <a class="btn ghost" href="simulator/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>Play the simulator</a></div>
    <p class="meta"><span><i><b>{n_lessons}</b> lessons</i><i><b>{total_steps}</b> templates</i><i><b>{total_prompts}</b> prompts</i></span>
      <span><i>MIT licence</i><i>by {AUTHOR}</i></span></p>
  </div></div>
</section>"""

    body = f"""{hero}
<main id="main" class="home">

<section class="band" id="why" aria-labelledby="h-why"><div class="wrap">
  <header class="sec-h split rv"><p class="eyebrow">Sound familiar?</p>
    <h2 id="h-why">Agent projects fail quietly. <span>A phase ended on a date instead of on evidence.</span></h2>
    <p>The SkyWays PDLC is four phases, each ending on evidence, with one hard gate and a way back. Skip a
    phase's question, and you hear the line beneath it.</p></header>
  <div class="rv">{spine.figure(PHASES, SKIPPED, "learn/what-is-the-agentic-pdlc/")}</div>
  <p class="links rv"><a class="more" href="method/">See the whole spine on one page <i aria-hidden="true">→</i></a>
    <a class="more" href="learn/why-agentic-ai-projects-fail/">Seven ways these projects fail <i aria-hidden="true">→</i></a></p>
</div></section>

<section class="band" id="method" aria-labelledby="h-method"><div class="wrap">
  <header class="sec-h split rv"><p class="eyebrow">The methods</p>
    <h2 id="h-method">Which agentic method should you follow? <span>Whichever fits your team. Each has
    its place on the spine.</span></h2>
    <p>A method tells you how to build. The spine keeps the part each does best, and adds what none of
    them decides.</p></header>
  <div class="rv">{spine.coverage(PHASES, COVERAGE, illos.ADDS, "learn/what-is-the-agentic-pdlc/")}</div>
  <p class="links rv"><a class="more" href="frameworks/">How the four merge into one <i aria-hidden="true">→</i></a>
    <a class="more" href="learn/ai-dlc-vs-aidd-vs-agentic-sdlc/">Agentic SDLC, agentic STLC, AIDLC: every name, sorted <i aria-hidden="true">→</i></a></p>
</div></section>

<section class="band" id="roles" aria-labelledby="h-roles"><div class="wrap">
  <header class="sec-h split rv"><p class="eyebrow">By role</p>
    <h2 id="h-roles">Start from the job you do. <span>Eight steps per role, from the first question to
    production.</span></h2>
    <p>Every step names what you owe the next person, and comes with the template and the prompts to draft it.</p></header>
  <ol class="seats rv">{''.join(seats)}</ol>
  <p class="links rv"><a class="more" href="learn/#start-where-you-are">Not on the list? {n_starts} places to start <i aria-hidden="true">→</i></a></p>
</div></section>

<section class="band play" id="simulator" aria-labelledby="h-play"><div class="wrap">
  <div class="play-t rv"><p class="eyebrow">The simulator</p>
    <h2 id="h-play">Or play the ninety days yourself.</h2>
    <p>SkyWays is a fictional airline building a rebooking assistant for stranded passengers. Thirteen
    days decide the ninety. Every call has a price in days, and some prices arrive later.</p>
    <dl class="nums"><div><dt>13</dt><dd>calls to make</dd></div><div><dt>5</dt><dd>hands-on tasks</dd></div>
      <div><dt>3</dt><dd>ways to play</dd></div></dl>
    <div class="ba"><a class="btn pri" href="simulator/">Play Ninety Days</a>
      <a class="more" href="workbench/">Open the workbench <i aria-hidden="true">→</i></a></div>
  </div>
  <a class="simshot rv" href="simulator/" aria-label="Play Ninety Days, the SkyWays simulator">
    <span class="simbar" aria-hidden="true"><i></i><i></i><i></i><b>Ninety Days</b></span>
    <img class="light" src="assets/pictures/sim-home.light.webp" width="1360" height="850" loading="lazy" decoding="async"
      alt="The simulator on Day 45: the airline's head office cut open, seven rooms on four floors, the QA room lit, and the day's decision beside it with its price in days">
    <img class="dark" src="assets/pictures/sim-home.dark.webp" width="1360" height="850" loading="lazy" decoding="async" alt=""></a>
</div></section>

<section class="band" id="tutorial" aria-labelledby="h-learn"><div class="wrap">
  <header class="sec-h rv"><p class="eyebrow">The tutorial</p>
    <h2 id="h-learn">Or learn it in order. <span>{n_lessons} lessons in {NUM.get(len(_tracks), len(_tracks))} tracks. The first takes eight minutes.</span></h2></header>
  <ol class="jump tracks rv">{tracks}</ol>
  <div class="ba rv"><a class="btn pri" href="learn/what-is-the-agentic-pdlc/">Start with lesson one</a></div>
</div></section>

<section class="band" id="library" aria-labelledby="h-lib"><div class="wrap">
  <header class="sec-h rv"><p class="eyebrow">The library</p>
    <h2 id="h-lib">Take what you need. <span>Everything here is free to copy and reuse.</span></h2></header>
  <div class="shelf rv">
    <a class="tile" href="templates/"><span class="tile-k">{total_steps} templates</span><b>Templates</b>
      <span class="tile-d">One document to fill in for every step.</span><span class="tile-go" aria-hidden="true">→</span></a>
    <a class="tile" href="prompts/"><span class="tile-k">{total_prompts} prompts</span><b>Prompts</b>
      <span class="tile-d">Each states the job, the inputs and the shape of the answer.</span><span class="tile-go" aria-hidden="true">→</span></a>
    <a class="tile" href="models/"><span class="tile-k">12 rules of thumb</span><b>Mental models</b>
      <span class="tile-d">Each one names the mistake it prevents.</span><span class="tile-go" aria-hidden="true">→</span></a>
    <a class="tile" href="pictures/"><span class="tile-k">{n_pics} pictures</span><b>The picture pack</b>
      <span class="tile-d">Every diagram here, light and dark, free to reuse.</span><span class="tile-go" aria-hidden="true">→</span></a>
  </div>
</div></section>

</main>"""
    desc = (f"One lifecycle for building software with AI agents, the agentic PDLC, with AI-DLC, BMAD, AIDD and "
            f"spec-driven development placed on it, by role. {n_lessons} lessons, {total_steps} templates, {total_prompts} prompts.")
    site_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": BASE_URL + "#site", "name": "The agentic manual", "url": BASE_URL,
         "description": desc, "inLanguage": "en", "author": PERSON, "publisher": ORG,
         "license": REPO + "/blob/main/LICENSE"},
        ORG,
        {"@type": "WebPage", "@id": BASE_URL, "url": BASE_URL, "name": "The agentic manual", "isPartOf": {"@id": BASE_URL + "#site"},
         "description": desc, "dateModified": date.today().isoformat()}]}
    return shell(title="The agentic manual · the agentic PDLC, by role, end to end", desc=desc, body=body,
                 depth=0, nav_id="home", canonical=BASE_URL, own_ld=True,
                 head_extra=(LEGACY_HASH_REDIRECT
                             + f'<script type="application/ld+json">{json.dumps(site_ld, ensure_ascii=False)}</script>'
                             + f'<script type="application/json" id="globe-land">{globe.land_json()}</script>'
                             + '<script src="theme/hero.js" defer></script>'),
                 kind="home", og="home")


def method_page() -> str:
    """The lifecycle on one page: the four boards that used to sit on the home page, each answering
    one question. They keep their ids, so a link to #loops still lands on the loops."""
    from pages import boards, bb, illos
    asks = [("pdlc", "What happens in each phase?", "The four phases and the one hard gate"),
            ("loops", "What brings production back?", "Eight loops, three of them backwards"),
            ("by-role", "Who does what, and when?", "Five roles across the four phases"),
            ("delegation", "What may a model draft?", "And the one thing per step that stays with you")]
    jump = "".join(f'<li><a href="#{i}"><b>{_E(q)}</b><span>{_E(a)}</span></a></li>' for i, q, a in asks)
    body = f"""<div class="wrap"><main id="main" class="page">
  <header class="phead"><div class="pcols"><div><p class="eyebrow">The method</p>
    <h1>The SkyWays PDLC, on one page</h1>
    <p class="lede">The product development lifecycle this whole manual hangs from, called the agentic PDLC
    in the lessons: four phases (P0 to P3), one hard gate and eight loops. Each board below answers one
    question about it.</p></div>
    <figure class="pfig">{illos.tower()}{MOTION_TOGGLE}</figure></div>
    <ol class="jump">{jump}</ol></header>
  {bb.rebase(boards.pdlc(), "../")}
  {bb.rebase(boards.loops(), "../")}
  {bb.rebase(boards.by_role(), "../")}
  {bb.rebase(boards.delegation(), "../")}
  <div class="next"><a class="btn pri" href="../learn/what-is-the-agentic-pdlc/">Read it as a lesson</a>
    <a class="btn ghost" href="../frameworks/">How the four methods fit it</a></div>
</main></div>"""
    return shell(title="The SkyWays PDLC on one page: four phases, one hard gate, eight loops · The agentic manual",
                 desc="The agentic product development lifecycle in four boards: what happens in each phase, the "
                      "eight loops that bring production back, each role across the phases, and what a model may "
                      "draft against what stays with a person.",
                 body=body, depth=1, nav_id="method", canonical=BASE_URL + "method/",
                 crumbs=[("The method", "")], kind="method", og="method")


# --------------------------------------------------------------------------- diagrams
# Confidence marks. Tokens, so the pills follow the theme, the literals these
# replaced sat on a dark page at the value they were picked for a light one.
CONF = {"doc": ("documented", "var(--dg-indigo)"),
        "est": ("established", "var(--dg-teal)"),
        "wm": ("working method", "var(--dg-amber)")}


def frameworks_page() -> str:
    from pages import illos, bb, _kit as k
    d = json.loads((SITE / "content" / "library" / "frameworks.json").read_text(encoding="utf-8"))
    m_rows = "".join(
        f'<tr><td><strong>{_E(m["name"])}</strong><br>'
        f'<span style="font-size:13px;color:var(--soft)">{_E(m["full"])}</span></td>'
        f'<td>{md(m["what"])}</td><td>{md(m["where"])}</td><td>{md(m["when"])}</td></tr>'
        for m in d["methods"])
    a_rows = "".join(
        f'<tr><td><strong>{_E(a[0])}</strong></td><td>{_E(a[1])}</td><td>{md(a[2])}</td>'
        f'<td style="font-size:13px;color:var(--soft);white-space:nowrap">{_E(a[3])}</td></tr>'
        for a in d["acronyms"])
    f_rows = []
    for name, what, lineage, conf in d["frameworks"]:
        label, colour = CONF[conf]
        f_rows.append(
            f'<tr><td><strong>{_E(name)}</strong></td><td>{md(what)}</td>'
            f'<td style="font-size:13.5px;color:var(--soft)">{_E(lineage)}</td>'
            f'<td><span class="pill" style="color:color-mix(in oklab,{colour} 82%,var(--ink));'
            f'border-color:color-mix(in oklab,{colour} 42%,transparent);'
            f'background:color-mix(in oklab,{colour} 10%,transparent);'
            f'white-space:nowrap">{label}</span></td></tr>')
    def _key_pill(conf: str, gloss: str) -> str:
        label, colour = CONF[conf]
        return (f'<span class="pill" style="color:color-mix(in oklab,{colour} 82%,var(--ink));'
                f'border-color:color-mix(in oklab,{colour} 42%,transparent);'
                f'background:color-mix(in oklab,{colour} 10%,transparent)">{label}</span> {gloss}')

    key = ('<ul style="list-style:none;padding:0;display:grid;gap:7px">'
           + "".join(f"<li>{_key_pill(c, g)}</li>" for c, g in (
               ("doc", "a vendor’s published documentation, dated"),
               ("est", "a named, published practice"),
               ("wm", "this manual’s own default, to tune on your own traffic")))
           + "</ul>")
    pic = lambda fn: bb.rebase(fn(), "../")  # noqa: E731
    orient = k.orient(
        "Anyone who keeps meeting <strong>AI-DLC, AIDD, BMAD, SDD</strong> and forty acronyms and wants them "
        "placed on one map, and anyone who wants to know how much to trust a number in this manual.",
        "Settle three questions fast: which method covers what, what an acronym means here, and where a "
        "framework came from. Then carry four pictures in your head.",
        ["Start with the picture: <b>four methods on one spine</b>. They are not competitors, they cover different phases.",
         "Use the <b>pictures</b> as arguments: each one ends in a rule you can apply tomorrow.",
         "Check the <b>lineage</b> column before you quote a figure: documented, established, or this manual's own default."])
    tour = k.tour([
        {"sel": "#methods", "title": "One spine, four methods", "body": "A filled cell is where a method speaks to a phase; a dashed cell is where you bring your own answer. The bottom row is what this manual adds."},
        {"sel": "#vs", "title": "What actually changed", "body": "A traditional lifecycle decides everything once. The agentic one adds a bar per slice, an authority budget, one hard gate, and brings production back to the next frame."},
        {"sel": "#ladder", "title": "Gate by risk", "body": "Five bands from a reversible draft to an action nobody delegates. The band belongs to what the change touches, never to its size."},
        {"sel": "#merge", "title": "How they merge", "body": "Each method's parts land in the phase they serve. The bottom row is what the SkyWays PDLC adds and none of them carries."},
        {"sel": "#chain", "title": "Why long chains fail", "body": "Every probabilistic step multiplies. The bars show what survives; the list says what to do about it."},
        {"sel": "#decoder", "title": "The acronym decoder", "body": "Every short form this manual uses, with what it means here and where it came from."},
        {"sel": "#lineage", "title": "How much to trust it", "body": "Every framework carries a lineage pill: a vendor's documentation, a published practice, or this manual's own working default."},
    ])
    def rowh(head: str, aside_title: str, aside: str) -> str:
        return f'<div class="rowh"><div>{head}</div><div class="rowa"><b>{aside_title}</b>{aside}</div></div>'
    def try_(links: list[tuple[str, str]]) -> str:
        return '<div class="try">' + "".join(f'<a href="{h}">{t}</a>' for h, t in links) + "</div>"
    body = (
        '<div class="wrap"><main id="main" style="padding:34px 0 28px">'
        + rowh('<div class="kicker">The four methods</div><h1>The frameworks, and how they merge into P0 to P3</h1>'
               '<p class="lede">AI-DLC, AIDD, BMAD and spec-driven development placed on one spine, how their parts '
               "come together into the SkyWays PDLC, every acronym this manual uses, and where each framework came "
               "from, so you know how much to trust it.</p>",
               "On this page",
               '<ol><li><a href="#methods">Four methods, one spine</a></li>'
               '<li><a href="#merge">How they merge into the SkyWays PDLC</a></li>'
               '<li><a href="#vs">Traditional versus agentic</a></li>'
               '<li><a href="#ladder">Gate by risk, never by size</a></li>'
               '<li><a href="#chain">Why long chains fail</a></li>'
               '<li><a href="#decoder">The acronym decoder</a></li>'
               '<li><a href="#lineage">Where each framework came from</a></li></ol>')
        + orient +
        '<div class="sec" id="methods">' + pic(illos.methods)
        + rowh("<h2>Four methods, one spine: where each one sits</h2>"
               "<p>They are not competitors. Each speaks to part of the lifecycle, and the decision that matters is "
               "not which method to adopt but how deep to go on this change. A filled cell is where a method says "
               "something about that phase; a dashed cell is where you bring your own answer.</p>",
               "Try it in the simulator", try_([("../workbench/#/compare", "Compare any two methods side by side")]))
        + '<div class="tw" tabindex="0"><table><thead><tr><th>Method</th><th>What it is</th><th>Where it sits</th>'
        f"<th>When to use it</th></tr></thead><tbody>{m_rows}</tbody></table></div></div>"

        '<div class="sec" id="merge">'
        + rowh("<h2>How the four methods merge into the SkyWays PDLC</h2>"
               "<p>Each method contributes the part it does best, and the spine keeps those parts in one order with "
               "one owner per phase. What none of them carries, the SkyWays PDLC adds: the hard gate, a bar per "
               "slice, an authority budget and the report that starts the next pass.</p>",
               "What the SkyWays PDLC adds",
               "<ul><li>One hard gate: the signed spec, before anything is built</li>"
               "<li>A bar per slice, derived from money at risk</li>"
               "<li>An authority budget for every step the agent takes</li>"
               "<li>The two-number report that starts the next P0</li></ul>")
        + pic(illos.merge) + "</div>"

        '<div class="sec" id="vs">'
        + rowh("<h2>Traditional versus agentic: what changes when the product decides</h2>"
               "<p>A traditional lifecycle decides everything once, up front. When part of the product is right a "
               "share of the time rather than always, three things move: a bar per slice, an authority budget, and "
               "one hard gate before anything is built. Production then feeds the next frame instead of ending the "
               "story.</p>",
               "Try it in the simulator", try_([("../workbench/#/loopmap", "See which loops close each phase")]))
        + pic(illos.pdlc_vs) + "</div>"

        '<div class="sec" id="ladder">'
        + rowh("<h2>Gate by risk, never by size</h2>"
               "<p>Size measures typing. Four hundred lines of help text cannot move money; three lines in a refund "
               "cap can. The band a change sits in comes from what it touches, and the band decides who reviews it "
               "and whether a person signs before it ships.</p>",
               "Try it in the simulator",
               try_([("../workbench/#/toolkit/gateclass", "Classify a change as a hard or soft gate"),
                     ("../workbench/#/toolkit/gates", "Map the control each tool carries")]))
        + pic(illos.ladder) + "</div>"

        '<div class="sec" id="chain">'
        + rowh("<h2>Why long chains of steps fail, and what to do about it</h2>"
               "<p>Every step that is only probably right multiplies. Four chained steps at 90 percent succeed 66 "
               "percent of the time, and they fail fluently, with no error to catch. Two defences, in order: keep "
               "chains short, then put an independent checker after the steps that are costly and easy to miss.</p>",
               "Try it in the simulator", try_([("../workbench/#/toolkit/confidence", "Check whether a score has proven the bar")]))
        + pic(illos.chain) + "</div>"

        '<div class="sec" id="decoder"><h2>The acronym decoder</h2>'
        "<p>Every short form this manual uses, what it means here, and where it came from.</p>"
        '<div class="tw" tabindex="0"><table><thead><tr><th>Short</th><th>Long</th><th>What it means here</th>'
        f"<th>From</th></tr></thead><tbody>{a_rows}</tbody></table></div></div>"

        '<div class="sec" id="lineage">'
        + rowh("<h2>Where each framework came from, and how much to trust it</h2>"
               "<p>Every framework in this manual carries a lineage pill. Check it before you quote a figure: a "
               "vendor's documentation is dated, a published practice is named, and this manual's own defaults are "
               "there to tune on your own traffic, not to cite.</p>",
               "The three pills", key)
        + '<div class="tw" tabindex="0"><table><thead><tr><th>Framework</th><th>What it is</th><th>Lineage</th>'
        f'<th><span class="vh">Confidence</span></th></tr></thead><tbody>{"".join(f_rows)}</tbody></table></div>'
        f'<p style="margin-top:14px"><a href="{WIKI}/Sources-and-Confidence" target="_blank" '
        'rel="noopener">The full sources page</a></p></div>'
        + next_up("Seen where the methods sit. The method page draws the lifecycle they sit on.",
                  "../method/", "The SkyWays PDLC on one page", ("../learn/ai-dlc-vs-aidd-vs-agentic-sdlc/", "The methods, compared in a lesson"))
        + "</main></div>")
    return shell(title="The frameworks, and how they merge · The agentic manual",
                 desc="AI-DLC, AIDD, BMAD and spec-driven development on one spine, how their parts merge into the "
                      "SkyWays PDLC, every acronym decoded, and where each framework came from.",
                 body=body, depth=1, nav_id="frameworks", canonical=BASE_URL + "frameworks/",
                 crumbs=[("Libraries", ""), ("The frameworks, and how they merge", "")], tour=tour,
                 kind="frameworks", og="frameworks")


def load_roles() -> list[dict]:
    out = []
    for rid, *_ in ROLE_ORDER:
        p = CONTENT / f"{rid}.json"
        if p.exists():
            out.append(json.loads(p.read_text(encoding="utf-8")))
    return out


def search_index(roles: list[dict]) -> str:
    """What the drawer's search box looks through: title, one line, URL and kind, per thing."""
    import re as _re
    from pages import learn, models
    _m, tracks, lessons = learn.load()
    rows = []
    for t in tracks:
        rows.append({"t": t.title, "d": t.blurb, "u": f"learn/{t.id}/", "k": "Track"})
        for l in t.lessons:
            rows.append({"t": l.title, "d": l.description, "u": f"learn/{l.slug}/", "k": f"Lesson · {t.short}"})
    for r in roles:
        rows.append({"t": r["name"], "d": r["tagline"], "u": f"{r['id']}/", "k": "Role"})
        for st in r["steps"]:
            rows.append({"t": f"{st['n']} · {st['phase']}: {_re.sub(r'[*`]', '', st['title'])}",
                         "d": _re.sub(r'[*`]', '', st["purpose"])[:160], "u": f"{r['id']}/#{st['id']}", "k": f"{r['short']} step"})
    for m in models.MODELS:
        rows.append({"t": m["name"], "d": _re.sub(r"<[^>]+>", "", m["one"]), "u": f"models/#{m['id']}", "k": "Mental model"})
    rows += [
        {"t": "The operating protocol", "d": "For whoever funds the work: what changes, who does what, the four decisions only leadership can make.", "u": "protocol/", "k": "Leadership"},
        {"t": "The SkyWays PDLC on one page", "d": "Four phases, one hard gate, eight loops, each role across the phases, and what a model may draft.", "u": "method/", "k": "Method"},
        {"t": "Frameworks, acronyms and the pictures", "d": "AI-DLC, AIDD, BMAD and SDD on one spine; every acronym; the risk ladder and chained probability.", "u": "frameworks/", "k": "Reference"},
        {"t": "Artefact templates", "d": "Every artefact skeleton, copyable, by role.", "u": "templates/", "k": "Library"},
        {"t": "Prompt templates", "d": "Every prompt in the manual as a template, copyable, by role.", "u": "prompts/", "k": "Library"},
{"t": "The picture pack", "d": "Every diagram of the method as an image to share, with a caption, light and dark.", "u": "pictures/", "k": "Library"},
        {"t": "Ninety Days, the simulator", "d": "The SkyWays case as a game: thirteen decisions, each with a price in days, and consequences that arrive later. Play one role, the whole team, or the sponsor.", "u": "simulator/", "k": "Play"},
        {"t": "The workbench", "d": "Thirteen episodes in depth, nine step-through simulations, seventeen calculators and the role playbooks.", "u": "workbench/", "k": "Play"},
    ]
    for w in sorted((SITE.parent / "wiki").glob("*.md")):
        if w.name.startswith("_") or w.name in ("README.md", "Scoreboard.md"):
            continue
        text = w.read_text(encoding="utf-8")
        gen = _re.match(r"<!-- generated by site/(\w+)\.py", text)
        if (gen and gen.group(1) == "learn_export") or w.name.startswith("Journey-"):
            continue
        kind = "Course" if gen and gen.group(1) == "course_export" else "Wiki"
        h = _re.search(r"^# (.+)$", text, _re.M)
        first = _re.search(r"^(?!#|<|\||>|-|!|\s*$)(.{40,220}?)(?:\.\s|$)", text, _re.M)
        snippet = _re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", first.group(1)).replace("*", "").replace("`", "").strip() + "." if first else ""
        rows.append({"t": h.group(1).strip() if h else w.stem.replace("-", " "), "d": snippet, "u": f"{WIKI}/{w.stem}", "k": kind})
    return json.dumps(rows, ensure_ascii=False, separators=(",", ":"))


def render(out_dir: Path) -> list[str]:
    roles = load_roles()
    if not roles:
        raise SystemExit("no role content found in " + str(CONTENT))
    written = []

    def put(rel: str, text: str) -> None:
        p = out_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        written.append(rel)

    put("search.json", search_index(roles))
    put("index.html", home_page(roles))
    for r in roles:
        put(f"{r['id']}/index.html", role_page(r))
    put("templates/index.html", library_page(roles, "templates"))
    put("prompts/index.html", library_page(roles, "prompts"))
    put("frameworks/index.html", frameworks_page())
    put("method/index.html", method_page())
    from pages import models, protocol, pictures, play
    ctx = {"base": BASE_URL, "repo": REPO, "wiki": WIKI}
    put("simulator/index.html", play.build(shell, ctx))
    put("protocol/index.html", protocol.build(shell, ctx))
    put("models/index.html", models.build(shell, ctx))
    put("pictures/index.html", pictures.build(shell, ctx))
    from pages import learn
    written += learn.render(out_dir, shell)
    return written


def urls() -> list[str]:
    u = [BASE_URL, BASE_URL + "protocol/", BASE_URL + "models/", BASE_URL + "templates/",
         BASE_URL + "prompts/",
         BASE_URL + "pictures/",
         BASE_URL + "frameworks/",
         BASE_URL + "method/",
         BASE_URL + "app/SkyWays-Architect.html"]
    return u + [f"{BASE_URL}{r['id']}/" for r in load_roles()]


def dated_urls() -> list[tuple[str, str | None]]:
    """Every URL with its own last-modified date where it has one (the tutorial does)."""
    from pages import learn
    return [(u, None) for u in urls()] + learn.urls()
