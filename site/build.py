#!/usr/bin/env python3
"""Build the GitHub Pages site: the role manual, plus the SkyWays tool published unchanged.

Two things are published and they are kept strictly apart.

**The manual** — ``content/roles/*.json`` rendered to static HTML by :mod:`render`. Home page, one
page per role, and the template and prompt libraries.

**The tool** — ``app/SkyWays-Architect.html``, which is never edited. It is copied byte-for-byte to
``app/SkyWays-Architect.html``, and a second copy at ``simulator/index.html`` carries the site frame
(attribution, licence, contact) injected only at the document boundaries. The build refuses to
continue if the tool's own bytes changed.

    python site/build.py            # writes site/_site/
    python -m http.server -d site/_site 8000

Updating the tool is a file copy. Updating the manual is
``python site/content/roles/_src/build_content.py`` then this.
"""
from __future__ import annotations

import argparse
import json
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
TITLE = "SkyWays · the agentic PDLC operating playbook"
DESCRIPTION = ("Ninety days of one airline's agentic build, in thirteen episodes: eight loops, nine simulations, "
               "seventeen calculators and fifty-four role steps from frame to run. Built by Akash Das.")

JSON_LD = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "SkyWays · the agentic PDLC operating playbook",
    "alternateName": "SkyWays Architect",
    "url": BASE_URL,
    "description": DESCRIPTION,
    "image": BASE_URL + "assets/og.png",
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

# The framed copy is served from /simulator/, so its links climb one level to the site's shared files,
# and it is canonical for itself — pointing it at the home page told search engines it was a duplicate.
HEAD = f"""
<!-- site frame: injected at build time by site/build.py. The tool itself is untouched. -->
<meta name="description" content="{DESCRIPTION}">
<meta name="author" content="{AUTHOR}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BASE_URL}simulator/">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F7F6F2">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SkyWays Architect">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{BASE_URL}simulator/">
<meta property="og:image" content="{BASE_URL}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="{BASE_URL}assets/og.png">
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


def sitemap(today: str) -> str:
    # The tutorial carries its own dates; a page that did not change should not claim it did.
    urls = render.dated_urls() + [(BASE_URL + "simulator/", None)]
    body = "".join(f"  <url><loc>{u}</loc><lastmod>{d or today}</lastmod></url>\n" for u, d in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


def inject(html: str) -> str:
    for marker in ("</head>", "</body>"):
        if html.count(marker) != 1:
            sys.exit(f"expected exactly one {marker} in {SRC.name}, found {html.count(marker)}")
    html = html.replace("</head>", HEAD + "</head>", 1)
    return html.replace("</body>", BODY + "</body>", 1)


def build(out: Path, shots: bool = False) -> None:
    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # 1 · the manual
    pages = render.render(out)

    # 2 · the tool, pristine, and a framed copy at /simulator/
    original = SRC.read_text(encoding="utf-8")
    (out / "app").mkdir(parents=True, exist_ok=True)
    (out / "app" / SRC.name).write_text(original, encoding="utf-8")
    (out / "simulator").mkdir(parents=True, exist_ok=True)
    (out / "simulator" / "index.html").write_text(inject(original), encoding="utf-8")

    # 3 · static assets
    for folder in ("frame", "assets", "theme"):
        shutil.copytree(SITE / folder, out / folder)
    shutil.copy2(SITE / "404.html", out / "404.html")
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
    framed = (out / "simulator" / "index.html").read_text(encoding="utf-8")
    if framed.replace(HEAD, "", 1).replace(BODY, "", 1) != original:
        sys.exit("the build changed the tool itself; refusing to continue")

    files = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    total = sum((out / f).stat().st_size for f in files)
    print(f"built {out.relative_to(SITE.parent)} — {len(files)} files, {total / 1e6:.1f} MB")
    learn_pages = [p for p in pages if p.startswith("learn/") or p.startswith("llms")]
    print(f"  manual: {len(pages) - len(learn_pages)} pages")
    for p in pages:
        if p not in learn_pages:
            print(f"    {p} ({(out / p).stat().st_size:,} bytes)")
    print(f"  learn:  {len(learn_pages)} files (lessons, tracks, markdown twins, llms.txt)")
    print(f"  tool:   app/{SRC.name} (pristine) + simulator/index.html (framed)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=str(SITE / "_site"), help="output directory (default: site/_site)")
    ap.add_argument("--shots", action="store_true", help="also write learn/_shots/ for the screenshot tool")
    a = ap.parse_args()
    build(Path(a.out).resolve(), shots=a.shots)
