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
from pathlib import Path

SITE = Path(__file__).resolve().parent
CONTENT = SITE / "content" / "roles"
BASE_URL = "https://akash-coded.github.io/aws-bedrock-agentcore-strands/"
REPO = "https://github.com/akash-coded/aws-bedrock-agentcore-strands"
WIKI = REPO + "/wiki"
AUTHOR = "Akash Das"

# Roles in journey order. Those without a JSON file render as "in progress" on the home page.
ROLE_ORDER = [
    ("product-manager", "Product manager", "PM", "#3E6B8A", "From a vibe to a number you can defend"),
    ("solution-architect", "Solution architect", "SA", "#7A6A46", "From requirements to a system that holds"),
    ("engineering", "Engineering lead", "ENG", "#2F6B57", "From a story file to a shipped bolt"),
    ("qa", "QA lead", "QA", "#8C5B6B", "From 'it works' to a number you can defend"),
    ("devops", "DevOps and platform", "OPS", "#6B4E8A", "From a laptop to production, repeatably"),
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


def shell(*, title: str, desc: str, body: str, depth: int, accent: str | None = None,
          nav_id: str = "", canonical: str = "") -> str:
    up = "../" * depth
    accent_css = f'<style>:root{{--accent:{accent}}}</style>' if accent else ""
    nav = []
    for rid, name, short, _c, _t in ROLE_ORDER:
        if not (CONTENT / f"{rid}.json").exists():
            continue
        cur = ' aria-current="page"' if nav_id == rid else ""
        nav.append(f'<a href="{up}{rid}/"{cur}>{_E(name)}</a>')
    for slug, label in (("templates", "Templates"), ("prompts", "Prompts")):
        cur = ' aria-current="page"' if nav_id == slug else ""
        nav.append(f'<a href="{up}{slug}/"{cur}>{label}</a>')
    nav.append(f'<a href="{up}app/SkyWays-Architect.html">Simulator</a>')

    ld = {
        "@context": "https://schema.org", "@type": "TechArticle", "headline": title,
        "description": desc, "url": canonical or BASE_URL,
        "author": {"@type": "Person", "name": AUTHOR, "url": "https://github.com/akash-coded"},
        "publisher": {"@type": "Person", "name": AUTHOR},
        "isPartOf": {"@type": "WebSite", "name": "The agentic manual", "url": BASE_URL},
        "license": REPO + "/blob/main/LICENSE", "inLanguage": "en",
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_E(title)}</title>
<meta name="description" content="{_E(desc, quote=True)}">
<meta name="author" content="{AUTHOR}">
<link rel="canonical" href="{_E(canonical or BASE_URL, quote=True)}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F7F6F2">
<meta property="og:type" content="article">
<meta property="og:site_name" content="The agentic manual">
<meta property="og:title" content="{_E(title, quote=True)}">
<meta property="og:description" content="{_E(desc, quote=True)}">
<meta property="og:url" content="{_E(canonical or BASE_URL, quote=True)}">
<meta property="og:image" content="{BASE_URL}assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{up}theme/base.css">{accent_css}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="in">
  <a class="brand" href="{up}">The agentic manual<small>by role, end to end</small></a>
  <nav aria-label="Roles">{''.join(nav)}</nav>
  <button class="tgl" data-theme-toggle aria-label="Switch theme" title="Light or dark">◐</button>
</div></header>
{body}
<footer class="ft" data-site-footer><div class="in">
  <section>
    <h2>About</h2>
    <p><strong>The agentic manual</strong> is an original work and the intellectual property of
    <strong>{AUTHOR}</strong>, open-sourced under the <a href="{REPO}/blob/main/LICENSE">MIT licence</a>
    for knowledge and experience sharing. Keep the attribution when you reuse it.</p>
    <p style="font-size:13px;color:var(--soft)">SkyWays is a fictional airline. Every figure is
    illustrative and dated; check it against your own numbers. Not affiliated with, sponsored by or
    endorsed by Amazon Web Services or any airline.</p>
  </section>
  <section><h2>Go deeper</h2><ul>
    <li><a href="{up}app/SkyWays-Architect.html">The simulator — the same case, playable</a></li>
    <li><a href="{WIKI}/The-Agentic-PDLC">The method, as a wiki</a></li>
    <li><a href="{WIKI}/Formulas-and-Calculators">Every formula, worked</a></li>
    <li><a href="{WIKI}/Scenario-Library">37 scenarios, ten industries</a></li>
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
<link rel="stylesheet" href="{up}frame/frame.css">
<script src="{up}frame/config.js" defer></script>
<script src="{up}frame/frame.js" defer></script>
<script src="{up}theme/site.js" defer></script>
</body>
</html>
"""


def block(kind: str, title: str, subtitle: str, body: str, bid: str) -> str:
    """A copyable code block: template or prompt."""
    return f"""<div class="blk">
<div class="bh"><span class="bt">{_E(title)}</span>{f'<span class="bw">{_E(subtitle)}</span>' if subtitle else ''}
<button class="cp" data-copy="{bid}" aria-label="Copy {_E(kind, quote=True)}">Copy</button></div>
<pre id="{bid}"><code>{_E(body)}</code></pre></div>"""


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
  <span class="sh"><span class="ph">{_E(s['phase'])}</span><h3>{md(s['title'])}</h3>
    <span class="wh">{md(s['when'])}</span></span>
  <span class="chev" aria-hidden="true">▾</span>
</summary>
<div class="sb">
  <section><p class="lede" style="font-size:16.5px">{md(s['purpose'])}</p></section>

  <section><div class="lbl">What you actually do</div>
    <ol class="acts">{acts}</ol></section>

  <section><div class="lbl">Where a model helps, and where it must not</div>
    <div class="tw"><table class="ai"><thead><tr><th>Tool</th><th>Use it for</th></tr></thead>
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
    <div class="eg"><h4>{md(s['example']['title'])}</h4><p>{md(s['example']['body'])}</p></div></section>

  <section><div class="lbl">Pitfalls</div><ul class="ticks no">{pitfalls}</ul></section>

  <section><div class="done"><span class="k">Done when</span><p>{md(s['done_when'])}</p></div></section>
</div>
</details>"""


def role_page(role: dict) -> str:
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

    body = f"""<div class="cols">
<aside class="rail" aria-label="Steps"><h2>The journey</h2><ol>{rail}</ol>
  <p style="margin-top:18px"><button class="cp" data-expand
     style="background:var(--paper);color:var(--ink2);border-color:var(--rule)">Expand all</button></p>
</aside>
<main id="main">
  <div class="sec">
    <div class="kicker">{_E(role['short'])} · end to end</div>
    <h1>{_E(role['name'])}</h1>
    <p class="lede">{md(role['tagline'])}</p>
    <p><span class="pill acc">{len(role['steps'])} steps</span> <span class="pill">{n_a} sub-steps</span>
       <span class="pill">{len(role['steps'])} templates</span> <span class="pill">{n_p} prompts</span></p>
  </div>

  <div class="arc">{arc}</div>

  <div class="sec">{intro}</div>

  <div class="sec two">
    <div class="card"><h4 style="color:var(--accent)">Yours to own</h4><ul class="ticks">{owns}</ul></div>
    <div class="card"><h4 style="color:var(--soft)">Not yours — stop signing these</h4>
      <ul class="ticks no">{nots}</ul></div>
  </div>

  <div class="sec"><div class="note"><h4>How to use a model in this role</h4>
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
                 accent=role["accent"], nav_id=role["id"], canonical=f"{BASE_URL}{role['id']}/")


def library_page(roles: list[dict], kind: str) -> str:
    """One page holding every template, or every prompt, across all roles."""
    is_t = kind == "templates"
    label = "Templates" if is_t else "Prompts"
    lede = ("Every artefact template in the manual, on one page. Fill in the angle brackets. "
            "Each one is the output of a step, so if a template feels unclear, the step it belongs "
            "to explains why each field is there."
            if is_t else
            "Every prompt in the manual, on one page. They are written to be pasted and edited, not "
            "admired: each states the job, the rules and the output shape, because a prompt that does "
            "not say what shape it wants gets a different shape every time.")
    secs, toc, count = [], [], 0
    for role in roles:
        rows = []
        for s in role["steps"]:
            if is_t:
                count += 1
                rows.append(f'<h3 style="margin:22px 0 8px">{s["n"]}. {md(s["template"]["title"])}'
                            f' <span class="pill" style="margin-left:6px">{_E(s["phase"])}</span></h3>'
                            + block("template", s["template"]["title"],
                                    f'{role["short"]} step {s["n"]} · {s["artifact"]["name"]}',
                                    s["template"]["body"], f'lt-{role["id"]}-{s["id"]}'))
            else:
                for i, p in enumerate(s["prompts"]):
                    count += 1
                    rows.append(f'<h3 style="margin:22px 0 8px">{md(p["title"])}'
                                f' <span class="pill" style="margin-left:6px">{_E(s["phase"])}</span></h3>'
                                + block("prompt", p["title"], p["when"], p["body"],
                                        f'lp-{role["id"]}-{s["id"]}-{i}'))
        secs.append(f'<section id="{role["id"]}" style="scroll-margin-top:84px;margin:0 0 44px">'
                    f'<h2 style="color:{role["accent"]}">{_E(role["name"])}</h2>'
                    f'<p class="lede" style="font-size:16px">{md(role["tagline"])} · '
                    f'<a href="../{role["id"]}/">open the journey</a></p>{"".join(rows)}</section>')
        toc.append(f'<li><a href="#{role["id"]}">{_E(role["name"])}</a></li>')

    body = f"""<div class="cols">
<aside class="rail" aria-label="Roles"><h2>By role</h2><ul class="ticks">{''.join(toc)}</ul></aside>
<main id="main">
  <div class="sec"><div class="kicker">Library</div><h1>{label}</h1>
  <p class="lede">{lede}</p>
  <p><span class="pill acc">{count} {label.lower()}</span>
     <span class="pill">copy button on each</span></p></div>
  {''.join(secs)}
</main>
<aside class="toc" aria-label="On this page"><h2>On this page</h2><ul>{''.join(toc)}</ul></aside>
</div>"""
    return shell(title=f"{label} · The agentic manual",
                 desc=f"{count} copy-paste {label.lower()} for building software with AI, by role.",
                 body=body, depth=1, nav_id=kind, canonical=f"{BASE_URL}{kind}/")


def home_page(roles: list[dict]) -> str:
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

    body = f"""<div class="wrap">
<main id="main" style="padding:44px 0 80px">
  <div class="sec" style="max-width:74ch">
    <div class="kicker">The operating manual for building software that decides</div>
    <h1>Your role, end to end, in the agentic era</h1>
    <p class="lede">Pick your role and walk it from the first discovery conversation to the number you
    report at the end. Every step says what you actually do, where a model helps and where it must not
    be trusted, what artefact you produce, the template to write it, and the prompts to draft it faster.</p>
    <p class="lede" style="font-size:16.5px">One running case throughout: <strong>SkyWays</strong>, an
    airline building a rebooking assistant for disrupted passengers. Each role sees the same ninety days
    from its own angle, so you can switch roles and stay oriented.</p>
  </div>

  <div class="roles">{''.join(cards)}</div>

  <div class="sec" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px">
    <div class="card"><h4>Templates, not theory</h4><p style="font-size:14.5px;color:var(--ink2)">
      Every artefact has a fill-in skeleton with a copy button.
      <a href="templates/">All templates →</a></p></div>
    <div class="card"><h4>Prompts you can paste</h4><p style="font-size:14.5px;color:var(--ink2)">
      Written to be edited: the job, the rules, the output shape.
      <a href="prompts/">All prompts →</a></p></div>
    <div class="card"><h4>The same case, playable</h4><p style="font-size:14.5px;color:var(--ink2)">
      Thirteen dated episodes, nine simulations, seventeen calculators.
      <a href="app/SkyWays-Architect.html">Open the simulator →</a></p></div>
    <div class="card"><h4>The method, written down</h4><p style="font-size:14.5px;color:var(--ink2)">
      Four phases, eight loops, 37 scenarios, every formula.
      <a href="{WIKI}/The-Agentic-PDLC" target="_blank" rel="noopener">The wiki →</a></p></div>
  </div>

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
    <div class="tw"><table><thead><tr><th>You are</th><th>Start here</th><th>Time</th></tr></thead><tbody>
      <tr><td>New to agentic delivery</td><td><a href="product-manager/#qualify">Is this AI at all?</a> — the
        question that saves the most money</td><td>10 min</td></tr>
      <tr><td>About to write a spec</td><td><a href="product-manager/#specify">The eight-field spec</a>, with
        the template</td><td>20 min</td></tr>
      <tr><td>About to launch</td><td><a href="product-manager/#launch">Shadow, then five percent</a></td><td>15 min</td></tr>
      <tr><td>Asked for a business case</td><td><a href="product-manager/#frame">The value line</a>, with the
        arithmetic</td><td>15 min</td></tr>
      <tr><td>Running a workshop</td><td><a href="{WIKI}/Scenario-Library" target="_blank" rel="noopener">37
        scenarios</a> across ten industries</td><td>—</td></tr>
    </tbody></table></div>
  </div>
</main></div>"""
    desc = (f"An operating manual for the agentic era, by role. {total_steps} steps, {total_acts} "
            f"sub-steps, templates and {total_prompts} copy-paste prompts, from discovery to production. "
            f"Built by {AUTHOR}.")
    return shell(title="The agentic manual · your role, end to end", desc=desc, body=body, depth=0,
                 nav_id="home", canonical=BASE_URL)


def load_roles() -> list[dict]:
    out = []
    for rid, *_ in ROLE_ORDER:
        p = CONTENT / f"{rid}.json"
        if p.exists():
            out.append(json.loads(p.read_text(encoding="utf-8")))
    return out


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

    put("index.html", home_page(roles))
    for r in roles:
        put(f"{r['id']}/index.html", role_page(r))
    put("templates/index.html", library_page(roles, "templates"))
    put("prompts/index.html", library_page(roles, "prompts"))
    return written


def urls() -> list[str]:
    u = [BASE_URL, BASE_URL + "templates/", BASE_URL + "prompts/",
         BASE_URL + "app/SkyWays-Architect.html"]
    return u + [f"{BASE_URL}{r['id']}/" for r in load_roles()]
