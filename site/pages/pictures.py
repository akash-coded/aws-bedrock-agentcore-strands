"""The picture pack: every diagram on the site and in the simulator as an image with a title, a caption,
alt text, the page it comes from and a download, plus the structured data and sitemap entries that let
image search find them.

Sources
  - the lesson visuals registry (boards, figures, frameworks pictures, lesson maps, wiki-only pictures,
    posters): captured by site/tools/shoot.mjs into assets/learn/<name>.<light|dark>.webp
  - the simulator's pictures: captured by site/tools/simshots.mjs into assets/pictures/<name>.webp
"""
from __future__ import annotations

import json
from html import escape as E
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
LEARN_DIR = SITE / "assets" / "learn"
SIM_DIR = SITE / "assets" / "pictures"

GROUPS = [
    ("method", "The method", "The spine, the gates, the loops and the pictures every lesson returns to."),
    ("roles", "Roles", "Who does what, what arrives on each desk, and what leaves it."),
    ("decide", "Decisions and how-tos", "Decision trees and step sequences for the calls the method asks you to make."),
    ("lessons", "Lesson maps", "The picture that opens each lesson of the tutorial."),
    ("simulator", "From the simulator", "The flight plan, the loop, the three efforts and the concept map."),
    ("posters", "Posters and cheat sheets", "Drawn to be shared: one page each."),
]

# Titles for the pictures whose registry entry only carries alt text.
TITLES = {
    "board:pdlc": "The agentic PDLC", "board:loops": "Eight loops", "board:by_role": "Your role, across the four phases",
    "board:delegation": "Where the model helps, and where it must not",
    "figure:bar_sheet": "The acceptance bar sheet", "figure:chain": "Chained steps multiply",
    "figure:cache_prefix": "How a prompt cache matches", "figure:bolt_days": "A bolt plan",
    "figure:shadow_widen": "Shadow first, then widen", "figure:bill_factors": "Four habits, one bill",
    "figure:authority_ladder": "The authority ladder", "figure:two_numbers": "The two-number report",
    "frameworks:spine": "The agentic PDLC in one picture", "frameworks:pdlc_vs": "Traditional PDLC vs agentic PDLC",
    "frameworks:ladder": "The risk ladder", "frameworks:chain": "Six steps at ninety percent",
    "frameworks:methods": "Four methods on one spine", "frameworks:merge": "How the four methods merge into one loop",
    "home:tower": "The tower: the lifecycle flown as a loop",
    "wikimap:anti-patterns": "Eighteen anti-patterns", "wikimap:depth-of-change": "Depth of change",
    "wikimap:eight-loops-workshop": "The requirements loop", "wikimap:eight-loops-proof": "The trust loop",
    "wikimap:formulas": "Fourteen formulas on four phases", "wikimap:mental-models": "Twelve mental models on one page",
    "wikimap:dt-exact": "Exact, consequential or best-guess?", "wikimap:dt-autonomy": "How much autonomy?",
    "wikimap:dt-agents": "One agent, or several?", "wikimap:dt-prompt-or-signature": "Prompt, or tool signature?",
    "wikimap:dt-review-band": "Which review band?", "wikimap:dt-cache": "Cache it, and for how long?",
    "wikimap:dt-tier": "Which model tier?", "wikimap:dt-ship": "Ready to ship to five percent?",
    "wikimap:choose": "Build, buy or borrow", "wikimap:control-bill": "Control the token bill",
    "wikimap:cut-sprints": "Cut sprints into bolts", "wikimap:design-agent": "Design an agent on paper",
    "wikimap:review-band": "Review by risk band", "wikimap:nfr-workshop": "The NFR workshop",
    "wikimap:prove-bar": "Prove the bar", "wikimap:postmortem": "The missing-control postmortem",
    "wikimap:hold-boundary": "Hold the security boundary", "wikimap:agent-topology": "An agent's topology",
    "wikimap:role-product-manager": "The product manager's desk", "wikimap:role-solution-architect": "The solution architect's desk",
    "wikimap:role-engineering-lead": "The engineering lead's desk", "wikimap:role-qa-lead": "The QA lead's desk",
    "wikimap:role-devops": "The platform's desk", "wikimap:role-sponsor": "The sponsor's desk",
    "wikimap:scenario-library": "Five kinds of failure, rehearsed", "wikimap:where-do-i-find-it": "Six symptoms, six how-tos",
    "wikimap:error-index": "Seven kinds of error string", "wikimap:study-plans": "Six study plans",
    "wikimap:sources": "How a default becomes evidence",
    "wikimap:journey-product-manager": "The product manager's journey", "wikimap:journey-solution-architect": "The solution architect's journey",
    "wikimap:journey-engineering": "The engineering lead's journey", "wikimap:journey-qa": "The QA lead's journey",
    "wikimap:journey-devops": "The platform team's journey",
    "poster:prompt_anatomy": "The anatomy of a prompt template", "poster:prompts_by_role": "Prompt templates by role",
}

POSTER_KEYS = {"wikimap:mental-models", "wikimap:formulas", "poster:prompt_anatomy", "poster:prompts_by_role",
               "wikimap:anti-patterns", "wikimap:scenario-library"}
ROLE_KEYS_PREFIX = ("wikimap:role-", "wikimap:journey-")
DECIDE_KEYS_PREFIX = ("wikimap:dt-",)
DECIDE_KEYS = {"wikimap:choose", "wikimap:control-bill", "wikimap:cut-sprints", "wikimap:design-agent",
               "wikimap:review-band", "wikimap:nfr-workshop", "wikimap:prove-bar", "wikimap:postmortem",
               "wikimap:hold-boundary", "wikimap:agent-topology", "wikimap:where-do-i-find-it",
               "wikimap:error-index", "wikimap:study-plans", "wikimap:sources", "wikimap:depth-of-change"}

# The simulator's pictures: name, title, alt, the route they come from. Captured by site/tools/simshots.mjs.
SIM = [
    ("sim-flight-plan", "The flight plan", "The SkyWays PDLC as one route: four legs from P0 to P3 under the sky, "
     "thirteen stops, the gates between legs, and the control tower at Day 90", "simulator/#/quest"),
    ("sim-line-vs-loop", "A line, or a loop", "A traditional lifecycle as six stages in a line beside the SkyWays PDLC "
     "as a loop of four phases, with the five published methods plugging into the loop", "simulator/#/start"),
    ("sim-spine", "Four phases on one spine", "P0 Frame, P1 Specify, P2 Build and prove, P3 Run and learn, with the "
     "soft and hard gates between them and what each phase leaves you with", "simulator/#/start"),
    ("sim-methods", "Where each method plugs in", "Spec Kit, Kiro, BMAD, AI-DLC and AiDD on the spine, and what the "
     "SkyWays PDLC adds where they are silent", "simulator/#/start"),
    ("sim-roles", "Who does what, when", "Six roles along the four phases, each step named", "simulator/#/start"),
    ("sim-three-efforts", "Three efforts, one method", "Low effort in a chat, mid effort on a platform, high effort in "
     "code: who builds, how long, what it fits and how much of the method applies", "simulator/#/effort"),
    ("sim-same-task", "The same task at three efforts", "Answering customers' booking questions built as a chat, "
     "as a platform flow and as a product feature", "simulator/#/effort"),
    ("sim-concept-map", "The concept map", "Fifty-five concepts placed by loop, phase and role, as one map",
     "simulator/#/concepts"),
    ("sim-loop-map", "The Loop Map", "Four phases on a spine and eight loops that open in one phase and close in "
     "another, with the hard gate between P1 and P2", "simulator/#/loopmap"),
    ("sim-gates", "Hard gates and soft gates", "The spine with its gates: the hard gate between P1 and P2, the soft "
     "gates that run alongside the build", "simulator/#/governance"),
]


def webp_size(p: Path) -> tuple[int, int] | None:
    """Width and height from a WebP header (lossy, lossless or extended), without an image library."""
    try:
        b = p.read_bytes()[:40]
    except OSError:
        return None
    if b[:4] != b"RIFF" or b[8:12] != b"WEBP":
        return None
    chunk = b[12:16]
    if chunk == b"VP8X":
        return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
    if chunk == b"VP8L":
        bits = int.from_bytes(b[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if chunk == b"VP8 ":
        return int.from_bytes(b[26:28], "little") & 0x3FFF, int.from_bytes(b[28:30], "little") & 0x3FFF
    return None


def _group_of(key: str) -> str:
    if key in POSTER_KEYS or key.startswith("poster:"):
        return "posters"
    if key.startswith("map:"):
        return "lessons"
    if key.startswith(ROLE_KEYS_PREFIX) or key in ("board:by_role", "board:delegation"):
        return "roles"
    if key.startswith(DECIDE_KEYS_PREFIX) or key in DECIDE_KEYS:
        return "decide"
    return "method"


def catalogue() -> list[dict]:
    """Every picture with a file on disk, in gallery order."""
    from pages import learn
    reg = learn._visuals()
    _meta, _tracks, lessons = learn.load()
    items = []
    for key, v in reg.items():
        if key.startswith("model:"):
            continue  # the twelve glyphs are small; the poster holds them all
        name = learn.shot_name(key)
        light = LEARN_DIR / f"{name}.light.webp"
        if not light.exists():
            continue
        dark = LEARN_DIR / f"{name}.dark.webp"
        size = webp_size(light)
        if not size or not size[0] or not size[1]:
            continue
        if key.startswith("map:"):
            slug = key.split(":", 1)[1]
            title = lessons[slug].title if slug in lessons else slug.replace("-", " ")
        else:
            title = TITLES.get(key, key.split(":", 1)[1].replace("-", " ").replace("_", " ").capitalize())
        used = v["live"] or ""  # "#pdlc" is a home-page anchor; "qa/" a page
        items.append({"id": name, "key": key, "group": _group_of(key), "title": title, "alt": v["alt"],
                      "light": f"assets/learn/{name}.light.webp",
                      "dark": f"assets/learn/{name}.dark.webp" if dark.exists() else None,
                      "w": size[0], "h": size[1], "used": used})
    for name, title, alt, route in SIM:
        f = SIM_DIR / f"{name}.webp"
        size = webp_size(f) if f.exists() else None
        if not size or not size[0] or not size[1]:
            continue
        items.append({"id": name, "key": "sim:" + name, "group": "simulator", "title": title, "alt": alt,
                      "light": f"assets/pictures/{name}.webp", "dark": None, "w": size[0], "h": size[1], "used": route})
    order = {g: i for i, (g, *_r) in enumerate(GROUPS)}
    items.sort(key=lambda x: (order[x["group"]], x["title"].lower()))
    return items


def _used_href(used: str, base: str) -> str:
    if not used:
        return base
    if used.startswith("#"):
        return base + used
    return base + used


def _card(it: dict, base: str) -> str:
    light = "../" + it["light"]
    dark = ("../" + it["dark"]) if it["dark"] else None
    imgs = (f'<img class="light" src="{light}" width="{it["w"]}" height="{it["h"]}" alt="{E(it["alt"], quote=True)}" '
            f'loading="lazy" decoding="async">')
    if dark:
        imgs += (f'<img class="dark" src="{dark}" width="{it["w"]}" height="{it["h"]}" alt="" aria-hidden="true" '
                 f'loading="lazy" decoding="async">')
    used = _used_href(it["used"], base)
    dl = it["light"].rsplit("/", 1)[-1].replace(".light.webp", ".webp")
    return (f'<figure class="pic" data-group="{it["group"]}" id="pic-{it["id"]}">'
            f'<a class="pic-a" href="{light}" target="_blank" rel="noopener" aria-label="{E(it["title"], quote=True)}, full size">{imgs}</a>'
            f'<figcaption><b>{E(it["title"])}</b><span>{E(it["alt"])}</span>'
            f'<small><a href="{used}">Where it is used</a> · <a href="{light}" download="{dl}">Download</a> · '
            f'{it["w"]}×{it["h"]}</small></figcaption></figure>')


def image_entries(base: str) -> list[dict]:
    """For the sitemap: every picture's URL, title and caption."""
    return [{"loc": base + it["light"], "title": it["title"], "caption": it["alt"]} for it in catalogue()]


def build(shell, urls: dict) -> str:
    from pages import _kit as k
    base = urls["base"]
    items = catalogue()
    counts = {g: sum(1 for it in items if it["group"] == g) for g, *_r in GROUPS}
    chips = '<button type="button" class="chip on" data-pick="all" aria-pressed="true">All <b>%d</b></button>' % len(items)
    chips += "".join(f'<button type="button" class="chip" data-pick="{g}" aria-pressed="false">{E(label)} <b>{counts[g]}</b></button>'
                     for g, label, _d in GROUPS if counts[g])
    sections = []
    for g, label, blurb in GROUPS:
        cards = [_card(it, base) for it in items if it["group"] == g]
        if not cards:
            continue
        sections.append(f'<section class="picsec" id="pics-{g}" data-group="{g}"><h2>{E(label)} <span class="cnt">{len(cards)}</span></h2>'
                        f'<p class="lede" style="font-size:15.5px">{E(blurb)}</p><div class="pics">{"".join(cards)}</div></section>')
    orient = k.orient(
        "Anyone who has to <strong>explain this to someone else</strong>: a deck, a wiki page, a workshop, a post. "
        "And anyone who found one of these in an image search and wants the page behind it.",
        "Find the picture, open it full size or download it, and put it where it helps. Every picture links to "
        "the page that explains it, and reads in dark mode too.",
        ["Filter by what you need: the method, a role, a decision, a lesson, the simulator, a poster.",
         "Open a picture full size; <b>Download</b> saves the file.",
         "Reuse freely under the site's MIT licence; credit <b>Akash Das, SkyWays Consultancy</b> and link the page."])
    tour = k.tour([
        {"sel": ".picks", "title": "Filter", "body": "Six groups. The counts say how many pictures each holds."},
        {"sel": ".pic", "title": "A picture", "body": "Title, what it shows, the page it comes from, and a download. Click the picture for full size."},
    ])
    body = f"""<div class="wrap"><main id="main" class="picpage">
  <div class="rowh"><div><div class="kicker">The picture pack</div><h1>Every picture in the manual and the simulator, ready to share</h1><p class="lede">{len(items)} diagrams, boards, decision trees and posters, each with a title, a caption and the page
  that explains it. The same pictures that teach the SkyWays PDLC here, drawn to be put in a deck, a wiki or a post.</p></div><div class="rowa"><b>On this page</b><p><span class="pill acc">{len(items)} pictures</span> <span class="pill">light and dark</span>
     <span class="pill">MIT licence, credit the author</span></p><p style="margin:10px 0 0;font-size:13.5px">Six groups, each picture with a title, a caption, the page it comes from, and a download in light and dark.</p></div></div>
  {orient}
  <div class="picks" role="group" aria-label="Show a group">{chips}</div>
  {"".join(sections)}
  <div class="sec" style="max-width:74ch;margin-top:36px"><div class="note"><p><strong>Reuse.</strong> The pictures are part of
  <a href="{urls["repo"]}">the repository</a> and share its MIT licence: use them, adapt them, teach with them, and keep the
  credit <em>Akash Das, SkyWays Consultancy</em> with a link to the page each one comes from. The ones marked as a
  working method are this manual's own construction; the ones drawn from a published method or vendor documentation say so
  on their page.</p></div></div>
</main></div>"""
    gallery_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": base + "pictures/", "url": base + "pictures/",
         "name": "The picture pack: every diagram of the agentic PDLC",
         "description": f"{len(items)} diagrams, boards, decision trees and posters on the agentic PDLC, each with a caption and the page behind it.",
         "isPartOf": {"@type": "WebSite", "name": "The agentic manual", "url": base},
         "publisher": {"@type": "Organization", "name": "SkyWays Consultancy", "url": base},
         "license": urls["repo"] + "/blob/main/LICENSE", "inLanguage": "en",
         "mainEntity": {"@type": "ImageGallery", "name": "The picture pack", "image": [
             {"@type": "ImageObject", "contentUrl": base + it["light"], "url": base + "pictures/#pic-" + it["id"],
              "name": it["title"], "description": it["alt"], "caption": it["alt"], "width": it["w"], "height": it["h"],
              "encodingFormat": "image/webp", "license": urls["repo"] + "/blob/main/LICENSE",
              "acquireLicensePage": base + "pictures/", "creditText": "Akash Das, SkyWays Consultancy",
              "creator": {"@type": "Person", "name": "Akash Das"},
              "copyrightNotice": "Akash Das, SkyWays Consultancy. MIT licence."} for it in items]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": base},
            {"@type": "ListItem", "position": 2, "name": "Libraries", "item": base + "pictures/"},
            {"@type": "ListItem", "position": 3, "name": "The picture pack", "item": base + "pictures/"}]}]}
    return shell(title="The picture pack · every diagram of the agentic PDLC, ready to share",
                 desc=f"{len(items)} diagrams, boards, decision trees and posters on the agentic PDLC: the spine, the gates, "
                      "the eight loops, every role, every lesson. Each with a caption, light and dark, free to reuse.",
                 body=body, depth=1, nav_id="pictures", canonical=base + "pictures/", own_ld=True,
                 head_extra='<script type="application/ld+json">' + json.dumps(gallery_ld, ensure_ascii=False) + "</script>",
                 crumbs=[("Libraries", ""), ("The picture pack", "")], tour=tour, kind="pictures", og="pictures")
