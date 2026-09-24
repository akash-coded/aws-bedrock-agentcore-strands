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

# Roles in journey order. Those without a JSON file render as "in progress" on the home page.
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
# /simulator/, and this forwards those routes there before anything renders. Runs in <head> on the
# home page only; every other page is new and has no legacy routes to honour.
LEGACY_HASH_REDIRECT = (
    "\n<script>(function(){var h=location.hash;"
    "if(h&&h.charAt(1)===\"/\"){location.replace(\"simulator/\"+h);}})();</script>"
)


# A role page overrides --accent. Emitting the literal hex defeats dark mode, because
# base.css already defines a lifted value for each of these tokens and a hard-coded
# light hex cannot follow it — which is how the phase label on every role page came to
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


HOUSE = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 11.5 12 4l9 7.5"/>'
         '<path d="M5.5 10v10h13V10"/><path d="M10 20v-6h4v6"/></svg>')
BURGER = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>')
ROLE_LESSON = {"product-manager": "agentic-pdlc-for-product-managers", "solution-architect": "agentic-pdlc-for-solution-architects",
               "engineering": "agentic-pdlc-for-engineers", "qa": "agentic-pdlc-for-qa", "devops": "agentic-pdlc-for-devops"}
NAV_LABEL = {"product-manager": "Product", "solution-architect": "Architect",
             "engineering": "Engineering", "qa": "QA", "devops": "DevOps"}


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
                   ("learn/interviews/", "Interview banks and careers", "")]),
        ("Your role, end to end", roles),
        ("For leadership", [("protocol/", "The operating protocol", "protocol"),
                            ("models/", "Twelve mental models", "models")]),
        ("Libraries", [("templates/", "Artefact templates", "templates"),
                       ("prompts/", "Prompts to paste", "prompts"),
                       ("frameworks/", "Frameworks, acronyms and the pictures", "frameworks")]),
        ("Play", [("simulator/", "The SkyWays playbook · interactive simulator", "simulator")]),
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
    return (f'<details class="menu" data-menu><summary aria-label="All pages" title="All pages">{BURGER}'
            f'<span>Menu</span></summary><div class="mp"><div class="mph"><b>Everything, by category</b>'
            f'<button type="button" class="mx" data-menu-close aria-label="Close menu">×</button></div>'
            f'<div class="ms"><input type="search" data-search data-index="{up}search.json" placeholder="Search lessons, steps, pages…" '
            f'aria-label="Search the manual" autocomplete="off"><ol class="mr" data-search-results hidden></ol></div>'
            f'{"".join(out)}<p class="mpf">Lost? Every page has a <b>Show me around</b> button near the top.</p>'
            f"</div></details>")


def shell(*, title: str, desc: str, body: str, depth: int, accent: str | None = None,
          nav_id: str = "", canonical: str = "", head_extra: str = "", own_ld: bool = False,
          crumbs: list[tuple[str, str]] | None = None, tour: list[dict] | None = None,
          kind: str = "", og: str = "") -> str:
    """The frame every page shares. ``crumbs`` are (label, href) after Home, href relative to the
    page; ``tour`` is the page's walkthrough for guide.js; ``kind`` names the page type so the
    tour is offered once per type, not once per page."""
    up = "../" * depth
    accent_css = f"<style>:root{{--accent:{accent_var(accent)}}}</style>" if accent else ""
    og_img = og_image(og)
    nav = [f'<a class="home" href="{up}" aria-label="Home"{" aria-current=page" if nav_id == "home" else ""}>{HOUSE}</a>',
           f'<a href="{up}learn/"{' aria-current="page"' if nav_id == "learn" else ""}>Learn</a>']
    for rid, name, short, _c, _t in ROLE_ORDER:
        if not (CONTENT / f"{rid}.json").exists():
            continue
        cur = ' aria-current="page"' if nav_id == rid else ""
        nav.append(f'<a href="{up}{rid}/"{cur}>{_E(NAV_LABEL.get(rid, name))}</a>')
    for slug, label in (("protocol", "Leadership"), ("models", "Mental models"),
                        ("templates", "Templates"), ("prompts", "Prompts"),
                        ("frameworks", "Frameworks")):
        cur = ' aria-current="page"' if nav_id == slug else ""
        nav.append(f'<a href="{up}{slug}/"{cur}>{label}</a>')
    nav.append(f'<a href="{up}simulator/" class="play">Playbook</a>')

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
        "publisher": PERSON,
        "isPartOf": {"@type": "WebSite", "name": "The agentic manual", "url": BASE_URL},
        "license": REPO + "/blob/main/LICENSE", "inLanguage": "en",
    }
    if ld_crumbs and not own_ld:
        ld = {"@context": "https://schema.org", "@graph": [{k: v for k, v in ld.items() if k != "@context"}, ld_crumbs]}
    tour_html = (f'<script type="application/json" id="tour-steps">{json.dumps(tour, ensure_ascii=False)}</script>'
                 if tour else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_E(title)}</title>
<meta name="description" content="{_E(desc, quote=True)}">
<meta name="author" content="{AUTHOR}">
<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">
<link rel="canonical" href="{_E(canonical or BASE_URL, quote=True)}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F7F6F2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121316" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="article">
<meta property="og:site_name" content="The agentic manual">
<meta property="og:title" content="{_E(title, quote=True)}">
<meta property="og:description" content="{_E(desc, quote=True)}">
<meta property="og:url" content="{_E(canonical or BASE_URL, quote=True)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_img}">
{"" if own_ld else f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap">
<link rel="stylesheet" href="{up}theme/base.css">{accent_css}{head_extra}
</head>
<body{f' data-page="{_E(kind, quote=True)}"' if kind else ""}>
<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="in">
  {_menu(up, nav_id)}
  <a class="brand" href="{up}">The agentic manual<small>PDLCs for the agentic era</small></a>
  <nav aria-label="Sections">{''.join(nav)}</nav>
  <button class="tgl" data-theme-toggle aria-label="Switch theme" title="Light or dark">◐</button>
</div></header>
{crumb_html}
{body}
<footer class="ft" data-site-footer><div class="in">
  <section>
    <h2>About</h2>
    <p><strong>The agentic manual</strong> is an original work and the intellectual property of
    <strong>{AUTHOR}</strong>, open-sourced under the <a href="{REPO}/blob/main/LICENSE">MIT licence</a>
    for knowledge and experience sharing. Keep the attribution when you reuse it.</p>
    <p style="font-size:13.5px;color:var(--soft)">SkyWays is a fictional airline. Every figure is
    illustrative and dated; check it against your own numbers. Not affiliated with, sponsored by or
    endorsed by Amazon Web Services or any airline.</p>
  </section>
  <section><h2>Go deeper</h2><ul>
    <li><a href="{up}simulator/">The SkyWays playbook — the same ninety days, playable</a></li>
    <li><a href="{up}learn/">The tutorial — every lesson, in order</a></li>
    <li><a href="{WIKI}/The-Agentic-PDLC">The method, as a wiki</a></li>
    <li><a href="{WIKI}/Formulas-and-Calculators">Every formula, worked</a></li>
    <li><a href="{WIKI}/Scenario-Library">37 scenarios across twenty sectors</a></li>
  </ul></section>
  <section><h2>Pitch in</h2><ul>
    <li><a href="{REPO}/discussions/101">Suggest an improvement</a></li>
    <li><a href="{REPO}/issues/new/choose">Report a problem</a></li>
    <li><a href="{REPO}">The repository</a></li>
  </ul></section>
  <div class="lg"><span>&copy; 2026 {AUTHOR}</span>
    <a href="{REPO}/blob/main/LICENSE">MIT licence</a>
    <a href="{REPO}/tree/main/site/content">Source content</a>
    <a href="{WIKI}/Sources-and-Confidence">Sources and confidence</a></div>
</div></footer>
{tour_html}
<link rel="stylesheet" href="{up}frame/frame.css">
<script src="{up}frame/config.js" defer></script>
<script src="{up}frame/frame.js" defer></script>
<script src="{up}theme/site.js" defer></script>
<script src="{up}theme/engine.js" defer></script>
<script src="{up}theme/guide.js" defer></script>
</body>
</html>
"""


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


PHASE_TITLE = {"P0": "P0 · Frame — is this worth doing, and is it AI at all?",
               "P1": "P1 · Design & Spec — what exactly, and under whose authority?",
               "P2": "P2 · Build & Prove — does it meet the bar, slice by slice?",
               "P3": "P3 · Run & Learn — is it still doing it, and what did it cost?"}


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
    <span class="wh">{md(s['when'])}</span></span>
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

  <section><div class="lbl">Prompts you can paste</div>{prompts}</section>

  <section><div class="lbl">Worked example</div>
    <div class="eg"><h4>{md(s['example']['title'])}</h4><p>{md(s['example']['body'])}</p></div>
    {figure_html(s)}</section>
  {calc_section(s)}

  <section><div class="lbl">Pitfalls</div><ul class="ticks no">{pitfalls}</ul></section>

  <section><div class="done"><span class="k">Done when</span><p>{md(s['done_when'])}</p></div></section>
</div>
</details>"""


def role_page(role: dict) -> str:
    from pages import _kit as k
    rail = "".join(
        f'<li><a class="rl" data-for="{s["id"]}" href="#{s["id"]}">'
        f'<span class="rn">{s["n"]}</span><span>{_E(s["phase"])}</span></a></li>'
        for s in role["steps"])
    arc = "".join(
        f'<a href="#{s["id"]}"><span class="an">{s["n"]}</span>{_E(s["phase"])}</a>'
        for s in role["steps"])
    intro = "".join(f"<p>{md(p)}</p>" for p in role["intro"])
    owns = "".join(f"<li>{md(x)}</li>" for x in role["owns"])
    nots = "".join(f"<li>{md(x)}</li>" for x in role["not_yours"])
    reads = "".join(
        f'<li><a href="{_E(h, quote=True)}"'
        f'{" target=_blank rel=noopener" if h.startswith("http") else ""}>{_E(l)}</a></li>'
        for l, h in role["reads"])
    steps = "".join(step_html(role, s) for s in role["steps"])
    toc = "".join(f'<li><a href="#{s["id"]}">{s["n"]}. {_E(s["phase"])}</a></li>' for s in role["steps"])
    n_p = sum(len(s["prompts"]) for s in role["steps"])
    n_a = sum(len(s["activities"]) for s in role["steps"])
    n_f = sum(1 for s in role["steps"] if s.get("figure"))
    n_c = sum(1 for s in role["steps"] if s.get("calc"))
    extra_pills = ""
    if n_f:
        extra_pills += f' <span class="pill">{n_f} figures</span>'
    if n_c:
        extra_pills += f' <span class="pill">{n_c} calculators</span>'
    first = role["steps"][0]
    orient = k.orient(
        f"<strong>{_E(role['name'])}s</strong> and anyone who has to work with one — plus the "
        f"forward-deployed version of the role, who does this on a customer's site.",
        f"Walk the {len(role['steps'])} steps of this role in order, from <em>{_E(first['phase'])}</em> "
        f"to <em>{_E(role['steps'][-1]['phase'])}</em>, and leave each with the artefact the next person needs.",
        ["Read <b>Yours to own</b> and <b>Not yours</b> first: they are the two boundaries that moved.",
         "Open a step: what you do, where a model helps and where it must not, the artefact, the template, the prompts.",
         "Copy the template, paste the prompts into your model, and check the <b>Done when</b> line before you move on."],
        extra=f'<a class="btn" href="../learn/{ROLE_LESSON[role["id"]]}/">The lesson for this role →</a>')
    tour = k.tour([
        {"sel": ".arc", "title": "The journey", "body": f"{len(role['steps'])} steps in the order they happen. Click one to jump to it; the left rail keeps your place as you scroll."},
        {"sel": ".two", "title": "Two boundaries moved", "body": "What is yours to own, and what to stop signing. In agentic delivery these are the two lists that change; everything else is your job as it was."},
        {"sel": "details.step", "title": "A step, unpacked", "body": "Every step has the same shape: <b>what you actually do</b>, <b>where a model helps and where it must not</b>, the artefact you owe the next person, its template, prompts to paste, a worked SkyWays example, pitfalls and a <b>Done when</b> line."},
        {"sel": "details.step .cp", "title": "Copy, paste, fill in", "body": "Templates and prompts each have a copy button. Fill in the angle brackets; the step explains why each field is there."},
        {"sel": "[data-expand]", "title": "Read it straight through", "body": "Expand all opens every step, which is also how the page prints."},
    ])

    body = f"""<div class="cols">
<aside class="rail" aria-label="Steps"><h2>The journey</h2><ol>{rail}</ol>
  <p style="margin-top:18px"><button class="cp" data-expand
     style="background:var(--paper);color:var(--ink2);border-color:var(--rule)">Expand all</button></p>
</aside>
<main id="main">
  <div class="sec">
    <div class="kicker">Eight steps, end to end</div>
    <h1>{_E(role['name'])}</h1>
    <p class="lede">{md(role['tagline'])}</p>
    <p><span class="pill acc">{len(role['steps'])} steps</span> <span class="pill">{n_a} sub-steps</span>
       <span class="pill">{len(role['steps'])} templates</span> <span class="pill">{n_p} prompts</span>{extra_pills}</p>
  </div>

  {orient}

  <div class="arc">{arc}</div>

  <div class="sec">{intro}</div>

  <h2 style="margin:0 0 12px">What is yours, and what is not</h2>
  <div class="sec two">
    <div class="card"><h3 class="h4" style="color:var(--accent)">Yours to own</h3><ul class="ticks">{owns}</ul></div>
    <div class="card"><h3 class="h4" style="color:var(--soft)">Not yours — stop signing these</h3>
      <ul class="ticks no">{nots}</ul></div>
  </div>

  <div class="sec"><div class="note"><h3 class="h4">How to use a model in this role</h3>
    <p>{md(role['ai_stance'])}</p></div></div>

  <h2 style="margin:0 0 16px">The journey, step by step</h2>
  {steps}

  <div class="sec" style="margin-top:36px"><div class="lbl">Read next</div>
    <ul class="ticks">{reads}</ul></div>
</main>
<aside class="toc" aria-label="On this page"><h2>On this page</h2><ul>{toc}</ul></aside>
</div>"""
    desc = (f"{role['name']}: {role['tagline']}. {len(role['steps'])} steps, {n_a} sub-steps, "
            f"{len(role['steps'])} templates and {n_p} copy-paste prompts for building with AI.")
    return shell(title=f"{role['name']} · The agentic manual", desc=desc, body=body, depth=1,
                 accent=role["accent"], nav_id=role["id"], canonical=f"{BASE_URL}{role['id']}/",
                 crumbs=[("Roles", ""), (role["name"], "")], tour=tour, kind="role", og=role["id"])


def library_page(roles: list[dict], kind: str) -> str:
    """One page holding every template, or every prompt, across all roles."""
    from pages import _kit as k
    is_t = kind == "templates"
    label = "Artefact templates" if is_t else "Prompts to paste"
    short = "templates" if is_t else "prompts"
    lede = ("Every artefact in the manual has a fill-in skeleton: the pain register, the eight-field spec, "
            "the bar sheet, the two-number report and thirty-six more. These are <strong>documents you "
            "write</strong>, not prompts you send — the prompts are on their own page."
            if is_t else
            "Every prompt in the manual, on one page. These are <strong>messages you paste into a model</strong> "
            "— Claude, ChatGPT, Bedrock, your coding agent — and edit: each states the job, the rules and the "
            "output shape, because a prompt that does not say what shape it wants gets a different shape "
            "every time. The documents they help you write are on the templates page.")
    secs, toc, count = [], [], 0
    for role in roles:
        rows = []
        for s in role["steps"]:
            if is_t:
                count += 1
                rows.append(f'<h3 style="margin:22px 0 8px">{s["n"]}. {md(s["template"]["title"])}'
                            f' <span class="pill" style="margin-left:6px">{_E(s["phase"])}</span></h3>'
                            f'<p class="bwhy">Produced by <a href="../{role["id"]}/#{s["id"]}">step {s["n"]}, '
                            f'{_E(s["phase"])}</a>. Good looks like: {md(s["artifact"]["good"])}</p>'
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
        secs.append(f'<section id="{role["id"]}" style="scroll-margin-top:84px;margin:0 0 44px">'
                    f'<h2 style="color:{accent_var(role["accent"])}">{_E(role["name"])}</h2>'
                    f'<p class="lede" style="font-size:16px">{md(role["tagline"])} · '
                    f'<a href="../{role["id"]}/">open the journey</a></p>{"".join(rows)}</section>')
        toc.append(f'<li><a href="#{role["id"]}">{_E(role["name"])}</a></li>')

    other = ("prompts", "Prompts to paste") if is_t else ("templates", "Artefact templates")
    compare = f"""<h2 style="margin:0 0 12px">Templates or prompts?</h2>
<div class="sec two tvp">
  <div class="card{' on' if is_t else ''}"><h3 class="h4">Templates</h3><p>Skeletons for the <b>documents each step produces</b>: a
    register, a spec, a bar sheet, a report. You fill the angle brackets and keep the file.</p>
    <p class="eg2">e.g. <code># Pain register · &lt;product&gt;</code></p></div>
  <div class="card{'' if is_t else ' on'}"><h3 class="h4">Prompts</h3><p>Messages you <b>paste into a model</b> to draft, check or
    decompose something — with the job, the rules and the output shape spelled out.</p>
    <p class="eg2">e.g. <code>You are helping a product manager consolidate discovery notes…</code></p></div>
</div>"""
    orient = k.orient(
        ("Anyone about to <strong>write an artefact</strong> the manual asks for — a product manager drafting a pain "
         "register, an architect writing the spec, a QA lead building the bar sheet, a sponsor's two-number report."
         if is_t else
         "Anyone about to <strong>ask a model for help</strong> with a step — drafting, deduplicating, checking, "
         "decomposing — and who wants a prompt that says what shape the answer must take."),
        (f"Find the template for the step you are on, copy it, fill in the angle brackets, and keep it as the "
         f"artefact you hand to the next person." if is_t else
         "Find the prompt for the step you are on, copy it, paste it into your model, replace the angle "
         "brackets with your own material, and edit the rules to taste."),
        ["Pick your role in the left rail (or scroll: they are in journey order).",
         f"Press <b>Copy</b> on the block. {'Paste it into your document.' if is_t else 'Paste it into the model of your choice.'}",
         f"Unsure why a field is there? The line above each block links to the step that explains it."],
        extra=f'<a class="btn" href="../{other[0]}/" style="margin-top:8px">{other[1]} →</a>')
    tour = k.tour([
        {"sel": ".tvp", "title": "Templates or prompts?", "body": "Two libraries, two jobs. <b>Templates</b> are documents you write and keep. <b>Prompts</b> are messages you send to a model. This page is the " + ("templates" if is_t else "prompts") + "."},
        {"sel": ".rail", "title": "By role", "body": "Five roles, in journey order. Jump to yours; each section links back to the role's own page."},
        {"sel": ".blk", "title": "One block per " + ("template" if is_t else "prompt"), "body": "The header says which step it belongs to. The line above says " + ("what good looks like." if is_t else "when to use it.") + " Angle brackets are yours to fill."},
        {"sel": ".blk .cp", "title": "Copy", "body": "One click copies the whole block, ready to paste."},
    ])
    body = f"""<div class="cols">
<aside class="rail" aria-label="Roles"><h2>By role</h2><ul class="ticks">{''.join(toc)}</ul></aside>
<main id="main">
  <div class="sec"><div class="kicker">The {"template" if is_t else "prompt"} library</div><h1>{label}</h1>
  <p class="lede">{lede}</p>
  <p><span class="pill acc">{count} {short}</span>
     <span class="pill">copy button on each</span> <span class="pill">every angle bracket is yours to fill</span></p></div>
  {orient}
  {compare}
  {''.join(secs)}
</main>
<aside class="toc" aria-label="On this page"><h2>On this page</h2><ul>{''.join(toc)}</ul></aside>
</div>"""
    return shell(title=f"{label} · The agentic manual",
                 desc=(f"{count} copy-paste {short} for building software with AI, by role: "
                       + ("the documents each step of the agentic PDLC produces." if is_t else
                          "each states the job, the rules and the output shape.")),
                 body=body, depth=1, nav_id=kind, canonical=f"{BASE_URL}{kind}/",
                 crumbs=[("Libraries", ""), (label, "")], tour=tour, kind=kind, og=kind)


def home_page(roles: list[dict]) -> str:
    from pages import boards, illos, learn, _kit as k
    built = {r["id"]: r for r in roles}
    cards = []
    for rid, name, short, colour, tagline in ROLE_ORDER:
        r = built.get(rid)
        if r:
            n_p = sum(len(s["prompts"]) for s in r["steps"])
            n_a = sum(len(s["activities"]) for s in r["steps"])
            stats = (f'<div class="rs"><i>{len(r["steps"])} steps</i><i>{n_a} sub-steps</i>'
                     f'<i>{len(r["steps"])} templates</i><i>{n_p} prompts</i></div>')
            cards.append(f'<a class="rc" href="{rid}/" style="--rc:{colour}">'
                         f'<span class="rb">{_E(short)}</span><div class="rt">{_E(name)}</div>'
                         f'<div class="rg">{md(tagline)}</div>{stats}</a>')
        else:
            cards.append(f'<div class="rc soon" style="--rc:{colour}">'
                         f'<span class="rb">{_E(short)}</span><div class="rt">{_E(name)}</div>'
                         f'<div class="rg">{md(tagline)}</div>'
                         f'<div class="rs"><i>in progress</i></div></div>')
    total_steps = sum(len(r["steps"]) for r in roles)
    total_prompts = sum(len(s["prompts"]) for r in roles for s in r["steps"])
    total_acts = sum(len(s["activities"]) for r in roles for s in r["steps"])
    _meta, tracks, lessons = learn.load()
    n_lessons = len(lessons)
    n_banks = sum(1 for l in lessons.values() if l.slug.endswith("-interview-questions"))

    who = [
        ("learn/ai-dlc-for-forward-deployed-engineers/", "a forward-deployed engineer", "var(--sage)"),
        ("product-manager/", "a product manager or FDPM", "var(--slate)"),
        ("solution-architect/", "a solution architect", "var(--ochre)"),
        ("engineering/", "an engineer or GenAI engineer", "var(--sage)"),
        ("qa/", "in QA", "var(--plum)"),
        ("devops/", "in DevOps or platform", "var(--violet)"),
        ("protocol/", "the sponsor or an executive", "var(--ink)"),
        ("learn/organisation/", "an organisation adopting agents", "var(--ink)"),
        ("learn/interviews/", "preparing for an interview", "var(--ink)"),
    ]
    who_html = "".join(f'<li><a href="{h}" style="--w:{c}"><i></i>{_E(t)}</a></li>' for h, t, c in who)
    stats = [(n_lessons, "lessons"), (len(roles), "roles, end to end"), (total_steps, "templates"),
             (total_prompts, "prompts"), (12, "mental models"), (n_banks, "interview banks")]
    stats_html = "".join(f"<span><b>{n}</b>{_E(t)}</span>" for n, t in stats)
    tour = k.tour([
        {"sel": ".hero .who", "title": "Pick your chair", "body": "Nine entrances, one per kind of reader. Each opens the pages written for that chair. Start with yours; the rest will make sense from there."},
        {"sel": ".hero .ill", "title": "The spine", "body": "Four phases, one hard gate, and a loop back from production. Every lesson, board and role page on this site hangs off this picture. Click a phase to open it."},
        {"sel": ".hd nav", "title": "The top bar", "body": "<b>Learn</b> is the tutorial. The five roles are the manual itself. Then leadership, the twelve mental models, the libraries — and the <b>Playbook</b>, the same case as an interactive simulator."},
        {"sel": ".menu", "title": "The menu", "body": "Everything, by category: the tutorial's tracks, the interview banks, the libraries, the wiki. Esc closes it."},
        {"sel": ".how3", "title": "Three ways in", "body": "Learn the method in short lessons, walk your own role step by step, or go straight to the templates and prompts and play the case."},
        {"sel": "#pdlc", "title": "The boards", "body": "Below the fold the home page reads as four boards: the spine in detail, the eight loops, your role across the phases, and where a model helps. Hover a cell to light its row and column."},
        {"sel": ".tgl", "title": "Light or dark", "body": "The whole site follows this, pictures included."},
    ])

    hero = f"""<section class="hero" id="top" aria-label="Introduction"><div class="in">
  <div class="hx">
    <p class="kicker">PDLCs for the agentic era</p>
    <h1>Every agentic delivery method. One manual. <em>Your role, end to end.</em></h1>
    <p class="lede">AI-DLC, AIDD, BMAD, spec-driven development and the PDLC that ties them together,
    walked from the first conversation to the number you report. Free, credited, method-agnostic.</p>
    <div class="who"><p class="wl">If you are…</p><ul>{who_html}</ul></div>
    <div class="guide">{k.pip()}<div class="bubble"><p><b>Hi, I'm Pip.</b> New here? I can show you round in
      thirty seconds, or take you straight to the tutorial or the playbook.</p>
      <div class="ba"><button type="button" class="btn pri" data-tour-start>Show me around</button>
      <a class="btn" href="learn/">Start the tutorial</a>
      <a class="btn" href="simulator/">Play the playbook</a></div></div></div>
  </div>
  <div class="ill">{illos.spine()}</div>
</div></section>"""

    body = f"""{hero}
<div class="wrap">
<main id="main" style="padding:34px 0 80px">
  <div class="stats" aria-label="What is here">{stats_html}</div>
  <div class="sec">
    <h2>Three ways in</h2>
    <div class="ways">
      <div><h3>Learn the method</h3>
        <p>{n_lessons} short lessons: the four phases, the methods decoded, running delivery, every role, the
        organisation, the SkyWays case and {n_banks} interview banks with answer frameworks.</p>
        <a class="more" href="learn/">Start the tutorial →</a></div>
      <div><h3>Walk your role</h3>
        <p>Eight steps per role, in order. Each says what you do, where a model helps and where it must not,
        the artefact you owe the next person, its template and the prompts to draft it.</p>
        <a class="more" href="product-manager/">Open a role →</a></div>
      <div><h3>Use the libraries, then play</h3>
        <p>{total_steps} templates, {total_prompts} prompts, twelve mental models and the frameworks decoder,
        and the SkyWays playbook: ninety days of one airline's build you can replay.</p>
        <a class="more" href="simulator/">Open the playbook →</a></div>
    </div>
  </div>

  <div class="sec" style="max-width:74ch">
    <p class="lede" style="font-size:16.5px">One running case throughout: <strong>SkyWays</strong>, an
    airline building a rebooking assistant for disrupted passengers. Each role sees the same ninety days
    from its own angle, so you can switch roles and stay oriented.</p>
  </div>

  {boards.pdlc()}

  {boards.loops()}

  <div class="sec" style="max-width:74ch">
    <h2>Pick the chair you sit in</h2>
    <p>The same ninety days look different from each seat. Each role page walks eight steps
    in order, and every step says what you do, where a model helps, what artefact you owe the
    next person, the template to write it and the prompts to draft it faster.</p>
  </div>

  <div class="roles">{''.join(cards)}</div>

  {boards.by_role()}

  <div class="sec more">
    <div><h3>Templates, not theory</h3><p>Every artefact has a fill-in skeleton with a copy button.
      <a href="templates/">All templates →</a></p></div>
    <div><h3>Prompts you can paste</h3><p>Written to be edited: the job, the rules, the output shape.
      <a href="prompts/">All prompts →</a></p></div>
    <div><h3>The SkyWays playbook</h3><p>An interactive simulator of the whole method: thirteen dated
      episodes, nine simulations, seventeen calculators. <a href="simulator/">Open the playbook →</a></p></div>
    <div><h3>Not doing the work, funding it?</h3><p>The whole operating model on one screen: what changes,
      who does what, the four decisions only leadership can make, and ninety days.
      <a href="protocol/">The operating protocol →</a></p></div>
    <div><h3>The method, written down</h3><p>Four phases, eight loops, 37 scenarios, 31 exercises, every
      formula. <a href="{WIKI}/The-Agentic-PDLC" target="_blank" rel="noopener">The wiki →</a></p></div>
  </div>

  <hr>

  {boards.delegation()}

  <hr>

  <div class="sec" style="max-width:74ch">
    <h2>What this is, and what it is not</h2>
    <p>It <strong>is</strong> an operating manual: the sub-steps of a real role, in order, with the
    artefact each one owes the next person. It assumes you already know your job and want to know what
    changes when part of the product is right <em>a share of the time</em> rather than always.</p>
    <p>It is <strong>not</strong> a tool tutorial. Tools change every quarter; the decisions do not.
    Where a specific tool matters — a context file a coding agent reads, a documented cache multiplier —
    it is named and dated. Everything else is about the judgement.</p>
    <div class="note"><p><strong>Honesty about numbers.</strong> Figures are marked where they come
    from. Vendor-documented numbers carry their date. Thresholds this manual invented are defaults to
    tune on your own traffic, not findings.
    <a href="{WIKI}/Sources-and-Confidence" target="_blank" rel="noopener">Sources and confidence →</a></p></div>
  </div>

  <div class="sec">
    <h2>Where to start</h2>
    <div class="tw" tabindex="0"><table><thead><tr><th>You are</th><th>Start here</th><th>Time</th></tr></thead><tbody>
      <tr><td>New to agentic delivery</td><td><a href="learn/what-is-the-agentic-pdlc/">What is the agentic PDLC?</a> — the
        four phases in one sitting</td><td>8 min</td></tr>
      <tr><td>A forward-deployed engineer</td><td><a href="learn/ai-dlc-for-forward-deployed-engineers/">AI-DLC and AIDD in the
        field</a> — their pain, their risk owner, their stack</td><td>10 min</td></tr>
      <tr><td>About to write a spec</td><td><a href="product-manager/#specify">The eight-field spec</a>, with
        the template</td><td>20 min</td></tr>
      <tr><td>About to launch</td><td><a href="product-manager/#launch">Shadow, then five percent</a></td><td>15 min</td></tr>
      <tr><td>Asked for a business case</td><td><a href="product-manager/#frame">The value line</a>, with the
        arithmetic</td><td>15 min</td></tr>
      <tr><td>Funding this, not building it</td><td><a href="protocol/">The operating protocol</a> — what
        changes, who does what, and the four questions to ask</td><td>20 min</td></tr>
      <tr><td>Preparing for an interview</td><td><a href="learn/how-to-answer-ai-interview-questions/">Six answer
        frameworks</a>, then the bank for your role</td><td>25 min</td></tr>
      <tr><td>Running a workshop</td><td><a href="{WIKI}/Scenario-Library" target="_blank" rel="noopener">37
        scenarios</a> across twenty sectors</td><td>—</td></tr>
    </tbody></table></div>
  </div>
</main></div>"""
    desc = (f"Every agentic delivery method in one manual: AI-DLC, AIDD, BMAD, spec-driven development and "
            f"the agentic PDLC, by role. {n_lessons} lessons, {total_steps} templates, {total_prompts} prompts.")
    site_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": BASE_URL + "#site", "name": "The agentic manual", "url": BASE_URL,
         "description": desc, "inLanguage": "en", "author": PERSON, "publisher": PERSON,
         "license": REPO + "/blob/main/LICENSE"},
        {"@type": "WebPage", "@id": BASE_URL, "url": BASE_URL, "name": "The agentic manual", "isPartOf": {"@id": BASE_URL + "#site"},
         "description": desc, "dateModified": date.today().isoformat()}]}
    return shell(title="The agentic manual · every agentic PDLC, by role, end to end", desc=desc, body=body,
                 depth=0, nav_id="home", canonical=BASE_URL, own_ld=True,
                 head_extra=LEGACY_HASH_REDIRECT + f'<script type="application/ld+json">{json.dumps(site_ld, ensure_ascii=False)}</script>',
                 tour=tour, kind="home", og="home")


# --------------------------------------------------------------------------- diagrams
# Confidence marks. Tokens, so the pills follow the theme — the literals these
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

    key = ("<p>"
           + _key_pill("doc", "a vendor’s published documentation, dated &nbsp; ")
           + _key_pill("est", "a named, published practice &nbsp; ")
           + _key_pill("wm", "this manual’s own default, to tune on your own traffic")
           + "</p>")
    pic = lambda fn: bb.rebase(fn(), "../")  # noqa: E731
    orient = k.orient(
        "Anyone who keeps meeting <strong>AI-DLC, AIDD, BMAD, SDD</strong> and forty acronyms and wants them "
        "placed on one map — and anyone who wants to know how much to trust a number in this manual.",
        "Settle three questions fast: which method covers what, what an acronym means here, and where a "
        "framework came from. Then carry four pictures in your head.",
        ["Start with <b>Four methods, one spine</b>: they are not competitors, they cover different phases.",
         "Use the <b>pictures</b> as arguments: each one ends in a rule you can apply tomorrow.",
         "Check the <b>lineage</b> column before you quote a figure: documented, established, or this manual's own default."])
    tour = k.tour([
        {"sel": "#methods", "title": "One spine, four methods", "body": "A filled cell is where a method speaks to a phase; a dashed cell is where you bring your own answer. The bottom row is what this manual adds."},
        {"sel": "#vs", "title": "What actually changed", "body": "A traditional lifecycle decides everything once. The agentic one adds a bar per slice, an authority budget, one hard gate — and brings production back to the next frame."},
        {"sel": "#ladder", "title": "Gate by risk", "body": "Five bands from a reversible draft to an action nobody delegates. The band belongs to what the change touches, never to its size."},
        {"sel": "#chain", "title": "Why length is the enemy", "body": "Every probabilistic step multiplies. The bars show what survives; the list says what to do about it."},
        {"sel": "#decoder", "title": "The acronym decoder", "body": "Every short form this manual uses, with what it means here and where it came from."},
        {"sel": "#lineage", "title": "How much to trust it", "body": "Every framework carries a lineage pill: a vendor's documentation, a published practice, or this manual's own working default."},
    ])
    body = (
        '<div class="wrap"><main id="main" style="padding:34px 0 80px">'
        '<div class="sec" style="max-width:72ch"><div class="kicker">Reference</div>'
        "<h1>Frameworks, acronyms and the pictures</h1>"
        '<p class="lede">The named methods and where each one actually sits, every acronym this manual '
        "uses, and the four pictures worth carrying in your head. Every framework says where it came "
        "from and how much to trust it.</p></div>"
        + orient +
        '<div class="sec" id="methods"><h2>Four methods, one spine</h2>'
        "<p>They are not competitors; they occupy different parts of the same lifecycle. The decision "
        "that matters is not <em>which method</em> but <strong>how deep to go on this change</strong>.</p>"
        + pic(illos.methods) +
        '<div class="tw" tabindex="0"><table><thead><tr><th>Method</th><th>What it is</th><th>Where it sits</th>'
        f"<th>When to use it</th></tr></thead><tbody>{m_rows}</tbody></table></div></div>"

        '<div class="sec" id="vs"><h2>What changes when the product decides</h2>'
        + pic(illos.pdlc_vs) +
        "<p>Only one of the four hand-offs is a hard gate. Everything downstream is built and measured "
        "against the spec, the bar and the guardrails, so those three are settled before P2 opens.</p></div>"

        '<div class="sec" id="ladder"><h2>Gate by risk, never by size</h2>'
        + pic(illos.ladder) +
        "<p>Size measures typing. Four hundred lines of help text cannot move money; three lines in a "
        "refund cap can.</p></div>"

        '<div class="sec" id="chain"><h2>Why length is the enemy</h2>'
        + pic(illos.chain) +
        "<p>Four chained steps at 90% succeed 66% of the time, and they fail <em>fluently</em>. Two "
        "defences, in order: keep chains short, then put an independent checker after the steps that "
        "are costly and easy to miss.</p></div>"

        '<div class="sec" id="decoder"><h2>The acronym decoder</h2>'
        '<div class="tw" tabindex="0"><table><thead><tr><th>Short</th><th>Long</th><th>What it means here</th>'
        f"<th>From</th></tr></thead><tbody>{a_rows}</tbody></table></div></div>"

        '<div class="sec" id="lineage"><h2>Every framework, with its lineage</h2>' + key +
        '<div class="tw" tabindex="0"><table><thead><tr><th>Framework</th><th>What it is</th><th>Lineage</th>'
        f'<th><span class="vh">Confidence</span></th></tr></thead><tbody>{"".join(f_rows)}</tbody></table></div>'
        f'<p style="margin-top:14px"><a href="{WIKI}/Sources-and-Confidence" target="_blank" '
        'rel="noopener">The full sources page &rarr;</a></p></div>'
        "</main></div>")
    return shell(title="Frameworks and acronyms · The agentic manual",
                 desc="The four named methods and where each sits, every acronym, and four pictures: "
                      "traditional vs agentic, four methods on one spine, the risk ladder, chained probability.",
                 body=body, depth=1, nav_id="frameworks", canonical=BASE_URL + "frameworks/",
                 crumbs=[("Reference", ""), ("Frameworks, acronyms and the pictures", "")], tour=tour,
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
        {"t": "Frameworks, acronyms and the pictures", "d": "AI-DLC, AIDD, BMAD and SDD on one spine; every acronym; the risk ladder and chained probability.", "u": "frameworks/", "k": "Reference"},
        {"t": "Artefact templates", "d": "Every artefact skeleton, copyable, by role.", "u": "templates/", "k": "Library"},
        {"t": "Prompts to paste", "d": "Every prompt in the manual, copyable, by role.", "u": "prompts/", "k": "Library"},
        {"t": "The SkyWays playbook", "d": "The whole method as an interactive simulator: thirteen episodes, nine simulations, seventeen calculators.", "u": "simulator/", "k": "Play"},
    ]
    for w in sorted((SITE.parent / "wiki").glob("*.md")):
        if w.name.startswith("_") or w.name in ("README.md", "Scoreboard.md"):
            continue
        text = w.read_text(encoding="utf-8")
        if "generated by site/learn_export.py" in text[:400] or w.name.startswith("Journey-"):
            continue
        h = _re.search(r"^# (.+)$", text, _re.M)
        first = _re.search(r"^(?!#|<|\||>|-|!|\s*$)(.{40,220}?)(?:\.\s|$)", text, _re.M)
        snippet = _re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", first.group(1)).replace("*", "").replace("`", "").strip() + "." if first else ""
        rows.append({"t": h.group(1).strip() if h else w.stem.replace("-", " "), "d": snippet, "u": f"{WIKI}/{w.stem}", "k": "Wiki"})
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
    from pages import models, protocol
    ctx = {"base": BASE_URL, "repo": REPO, "wiki": WIKI}
    put("protocol/index.html", protocol.build(shell, ctx))
    put("models/index.html", models.build(shell, ctx))
    from pages import learn
    written += learn.render(out_dir, shell)
    return written


def urls() -> list[str]:
    u = [BASE_URL, BASE_URL + "protocol/", BASE_URL + "models/", BASE_URL + "templates/",
         BASE_URL + "prompts/",
         BASE_URL + "frameworks/",
         BASE_URL + "app/SkyWays-Architect.html"]
    return u + [f"{BASE_URL}{r['id']}/" for r in load_roles()]


def dated_urls() -> list[tuple[str, str | None]]:
    """Every URL with its own last-modified date where it has one (the tutorial does)."""
    from pages import learn
    return [(u, None) for u in urls()] + learn.urls()
