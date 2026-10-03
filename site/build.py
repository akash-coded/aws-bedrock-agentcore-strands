#!/usr/bin/env python3
"""Build the GitHub Pages site: the role manual, plus the SkyWays tool published unchanged.

Two things are published and they are kept strictly apart.

**The manual** — ``content/roles/*.json`` rendered to static HTML by :mod:`render`. Home page, one
page per role, and the template and prompt libraries.

**The tool** — ``app/SkyWays-Architect.html``, the workbench: calculators, playbooks and the case in
depth. The build never edits it. It is copied byte-for-byte to ``app/SkyWays-Architect.html``, and a
second copy at ``workbench/index.html`` carries the site frame (attribution, licence, contact) injected
only at the document boundaries. The build refuses to continue if the tool's own bytes changed.

**The simulator** — ``simulator/index.html`` is the game, Ninety Days, rendered by :mod:`pages.play`
from ``play/``. The workbench used to live at that address, so the game's first script forwards any
old ``#/…`` route to ``/workbench/``.

    python site/build.py            # writes site/_site/
    python -m http.server -d site/_site 8000

Updating the tool is a file copy. Updating the manual is
``python site/content/roles/_src/build_content.py`` then this.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

if sys.version_info < (3, 9):
    sys.exit(f"site/build.py needs Python 3.9 or newer; this is {sys.version.split()[0]}")
import render

SITE = Path(__file__).resolve().parent
SRC = SITE / "app" / "SkyWays-Architect.html"
BASE_URL = "https://akash-coded.github.io/aws-bedrock-agentcore-strands/"
REPO_URL = "https://github.com/akash-coded/aws-bedrock-agentcore-strands"
AUTHOR = "Akash Das"
TITLE = "The SkyWays workbench · calculators, playbooks and the case in depth"
DESCRIPTION = ("The workbench behind the agentic manual and its game: seventeen calculators, a playbook for each role, "
               "and ninety days of one fictional airline's agentic build in thirteen episodes. Built by Akash Das.")
WB_IMG = render.og_image("workbench")   # the workbench's own social card, once it has been shot

JSON_LD = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "The SkyWays workbench",
    "alternateName": "SkyWays workbench",
    "url": BASE_URL,
    "description": DESCRIPTION,
    "image": WB_IMG,
    "applicationCategory": "EducationalApplication",
    "operatingSystem": "Any",
    "browserRequirements": "Requires JavaScript",
    "isAccessibleForFree": True,
    "author": {"@type": "Person", "name": AUTHOR, "url": "https://github.com/akash-coded"},
    "copyrightHolder": {"@type": "Person", "name": AUTHOR},
    "copyrightYear": 2026,
    "license": REPO_URL + "/blob/main/LICENSE",
    "isPartOf": {"@type": "CreativeWork", "name": "Agentic AI on AWS", "url": REPO_URL},
}

# The framed copy is served from /workbench/, so its links climb one level to the site's shared files,
# and it is canonical for itself — pointing it at the home page told search engines it was a duplicate.
HEAD = f"""
<!-- site frame: injected at build time by site/build.py. The tool itself is untouched. -->
<meta name="description" content="{DESCRIPTION}">
<meta name="author" content="{AUTHOR}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BASE_URL}workbench/">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#121316">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The agentic manual">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{BASE_URL}workbench/">
<meta property="og:image" content="{WB_IMG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="{WB_IMG}">
<script type="application/ld+json">{json.dumps(JSON_LD, ensure_ascii=False)}</script>
<link rel="stylesheet" href="../frame/frame.css">
"""

BODY = """
<!-- site frame: attribution, licence, invitation and contact form. See site/frame/. -->
<script src="../frame/config.js"></script>
<script src="../frame/frame.js"></script>
"""

ROBOTS = ("User-agent: *\nAllow: /\n\n"
          "# AI assistants are welcome to read and cite this site; llms.txt is the index for them.\n"
          + "".join(f"User-agent: {b}\nAllow: /\n" for b in
                    ("GPTBot", "ChatGPT-User", "ClaudeBot", "anthropic-ai", "PerplexityBot", "Google-Extended", "Bingbot"))
          + f"\nSitemap: {BASE_URL}sitemap.xml\n")


# What each undated page is built from, so its lastmod is the date the sources last changed rather than
# the date of the build. Lessons carry their own dates. The Pages workflow fetches full history for this.
SOURCES = {
    "": ["site/render.py", "site/pages/globe.py", "site/theme/hero.js"],
    "method/": ["site/render.py", "site/pages/boards.py", "site/pages/illos.py", "site/pages/dg.py"],
    "protocol/": ["site/pages/protocol.py"],
    "models/": ["site/pages/models.py"],
    "templates/": ["site/content/roles"],
    "prompts/": ["site/content/roles", "site/pages/posters.py"],
    "frameworks/": ["site/content/library/frameworks.json", "site/pages/illos.py"],
    "pictures/": ["site/pages/pictures.py", "site/assets/pictures", "site/assets/learn"],
    "app/SkyWays-Architect.html": ["site/app/SkyWays-Architect.html"],
    "workbench/": ["site/app/SkyWays-Architect.html", "site/frame"],
    "simulator/": ["site/play", "site/pages/play.py"],
    "labs/": ["site/content/labs", "site/pages/labs.py", "site/labs"],
    "tools/": ["site/content/tools", "site/pages/tools.py"],
    "tools/claude-at-the-desk/": ["site/content/tools", "site/pages/tools.py"],
    "tools/claude-in-the-repo/": ["site/content/tools", "site/pages/tools.py"],
    "tools/chatgpt-and-codex/": ["site/content/tools", "site/pages/tools.py"],
    "tools/google-ai-studio-and-jules/": ["site/content/tools", "site/pages/tools.py"],
    # The FDE guide: its hub's words and its dated sources live beside the role's JSON, so a page's date follows them too.
    "forward-deployed-engineer/": ["site/content/roles/forward-deployed-engineer.json", "site/content/roles/_src/fde_hub.py",
                                   "site/content/roles/_src/fde_sources.py", "site/pages/fde.py"],
    "forward-deployed-engineer/frame/": ["site/content/roles/forward-deployed-engineer.json", "site/content/roles/_src/fde_sources.py",
                                         "site/pages/fde.py"],
    "forward-deployed-engineer/deliver/": ["site/content/roles/forward-deployed-engineer.json", "site/content/roles/_src/fde_sources.py",
                                           "site/pages/fde.py"],
    "forward-deployed-engineer/evolve/": ["site/content/roles/forward-deployed-engineer.json", "site/content/roles/_src/fde_sources.py",
                                          "site/pages/fde.py"],
}


def git_date(paths: list[str]) -> str | None:
    """The commit date of the newest change under any of the paths, or None outside a git checkout."""
    import subprocess
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", *paths], cwd=SITE.parent,
                             capture_output=True, text=True, timeout=30).stdout.strip()
        return out or None
    except (OSError, subprocess.SubprocessError):
        return None


def sitemap(today: str) -> str:
    # The tutorial carries its own dates; a page that did not change should not claim it did.
    urls = render.dated_urls() + [(BASE_URL + "simulator/", None), (BASE_URL + "workbench/", None)]
    dated = []
    for u, d in urls:
        rel = u[len(BASE_URL):]
        if not d:
            src = SOURCES.get(rel) or (["site/content/roles/" + rel.rstrip("/") + ".json"] if rel.endswith("/") else None)
            d = git_date(src) if src else None
        dated.append((u, d or today))
    from pages import pictures
    imgs = pictures.image_entries(BASE_URL)
    lines = []
    for u, d in dated:
        if u == BASE_URL + "pictures/" and imgs:
            inner = "".join(f"    <image:image><image:loc>{i['loc']}</image:loc></image:image>\n" for i in imgs)
            lines.append(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod>\n{inner}  </url>\n")
        else:
            lines.append(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n")
    body = "".join(lines)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            f'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n{body}</urlset>\n')


def inject(html: str) -> str:
    for marker in ("</head>", "</body>"):
        if html.count(marker) != 1:
            sys.exit(f"expected exactly one {marker} in {SRC.name}, found {html.count(marker)}")
    html = html.replace("</head>", HEAD + "</head>", 1)
    return html.replace("</body>", BODY + "</body>", 1)


def lean(css: str) -> str:
    """A stylesheet without its comments, which stay in the source for the next person to edit it.

    The comments were a quarter of base.css, and every page loads base.css. A comment inside a string is left
    alone; one between two words becomes a space, as CSS reads it; a line left empty goes."""
    out, i, n, q = [], 0, len(css), ""
    while i < n:
        c = css[i]
        if q:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(css[i + 1])
                i += 1
            elif c == q:
                q = ""
        elif c in "'\"":
            q = c
            out.append(c)
        elif css.startswith("/*", i):
            end = css.find("*/", i + 2)
            if end < 0:
                sys.exit("a stylesheet has a comment that never closes; refusing to ship it")
            i = end + 2
            if out and i < n and (out[-1].isalnum() or out[-1] in "-_") and (css[i].isalnum() or css[i] in "-_"):
                out.append(" ")
            continue
        else:
            out.append(c)
        i += 1
    return re.sub(r"\n[ \t]*(?=\n)", "", "".join(out)).strip() + "\n"


_ASSET = re.compile(r'\b(href|src)="([^"?#:]+\.(?:css|js))"')


def stamp(out: Path) -> int:
    """Give every local stylesheet and script a ``?v=`` taken from its content.

    GitHub Pages lets a browser keep a file for ten minutes. Without this, a reader who arrives just after
    a release gets the new page with the old stylesheet, and the page looks broken. With it, a changed file
    has a new address, so the page and its files always match. The pristine tool in ``app/`` is left alone."""
    import hashlib
    seen: dict[Path, str] = {}
    n = 0
    for page in out.rglob("*.html"):
        if page.parent.name == "app":
            continue

        def v(m: re.Match) -> str:
            f = (page.parent / m.group(2)).resolve()
            if not f.is_file():
                return m.group(0)
            if f not in seen:
                seen[f] = hashlib.sha1(f.read_bytes()).hexdigest()[:10]
            return f'{m.group(1)}="{m.group(2)}?v={seen[f]}"'

        html = page.read_text(encoding="utf-8")
        new = _ASSET.sub(v, html)
        if new != html:
            page.write_text(new, encoding="utf-8")
            n += 1
    return n


def build(out: Path, shots: bool = False) -> None:
    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # 1 · the manual
    pages = render.render(out)

    # 2 · the tool, pristine, and a framed copy at /workbench/
    original = SRC.read_text(encoding="utf-8")
    (out / "app").mkdir(parents=True, exist_ok=True)
    (out / "app" / SRC.name).write_text(original, encoding="utf-8")
    (out / "workbench").mkdir(parents=True, exist_ok=True)
    (out / "workbench" / "index.html").write_text(inject(original), encoding="utf-8")

    # 3 · static assets
    for folder in ("frame", "assets", "theme", "play"):
        shutil.copytree(SITE / folder, out / folder)
    for f in (SITE / "labs").iterdir():                      # the labs' engine, beside the lab pages render wrote
        if f.suffix in (".js", ".css"):
            shutil.copy2(f, out / "labs" / f.name)
    shutil.copy2(SITE / "404.html", out / "404.html")
    for f in out.rglob("*.css"):                             # every stylesheet ships without its comments
        f.write_text(lean(f.read_text(encoding="utf-8")), encoding="utf-8")
    (out / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (out / "sitemap.xml").write_text(sitemap(date.today().isoformat()), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")

    if shots:
        # Local-only sheets: every embeddable visual for site/tools/shoot.mjs, and every page's social
        # card for site/tools/ogshots.mjs. Neither is deployed.
        from pages import learn, ogcards
        print("  shots:", learn.shots_page(out, render.shell))
        print("  og cards:", ogcards.sheet(out, ogcards.all_cards(render.load_roles())))

    # The tool must survive the build untouched, in both copies.
    if (out / "app" / SRC.name).read_text(encoding="utf-8") != original:
        sys.exit("the pristine copy of the tool differs from the source; refusing to continue")
    framed = (out / "workbench" / "index.html").read_text(encoding="utf-8")
    if framed.replace(HEAD, "", 1).replace(BODY, "", 1) != original:
        sys.exit("the build changed the tool itself; refusing to continue")

    stamped = stamp(out)

    files = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    total = sum((out / f).stat().st_size for f in files)
    where = out.relative_to(SITE.parent) if out.is_relative_to(SITE.parent) else out
    print(f"built {where} — {len(files)} files, {total / 1e6:.1f} MB")
    learn_pages = [p for p in pages if p.startswith("learn/") or p.startswith("llms")]
    print(f"  manual: {len(pages) - len(learn_pages)} pages")
    for p in pages:
        if p not in learn_pages:
            print(f"    {p} ({(out / p).stat().st_size:,} bytes)")
    print(f"  learn:  {len(learn_pages)} files (lessons, tracks, markdown twins, llms.txt)")
    print(f"  tool:   app/{SRC.name} (pristine) + workbench/index.html (framed)")
    print(f"  game:   simulator/index.html + play/")
    print(f"  labs:   labs/index.html + {len([p for p in pages if p.startswith('labs/') and p != 'labs/index.html'])} lab pages + labs/lab.js, lab.css")
    print(f"  tools:  tools/index.html + {len([p for p in pages if p.startswith('tools/') and p != 'tools/index.html'])} manuals, from content/tools/tools.json")
    print(f"  files:  stylesheets and scripts carry a content version in {stamped} pages")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=str(SITE / "_site"), help="output directory (default: site/_site)")
    ap.add_argument("--shots", action="store_true", help="also write learn/_shots/ for the screenshot tool")
    a = ap.parse_args()
    build(Path(a.out).resolve(), shots=a.shots)
