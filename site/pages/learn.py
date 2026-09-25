"""The tutorial: lessons written once in markdown, published twice.

Source lives in ``site/content/learn/``: ``curriculum.py`` fixes the order, ``lessons/*.md`` hold
the words. This module renders them as indexed pages under ``/learn/`` on the site, where the
boards are the live ones. ``site/learn_export.py`` puts the tutorial's index and track pages on the
wiki, linking back here for the lessons themselves. The wiki is not indexed by search engines (GitHub only indexes wikis with
500+ stars and closed editing), so the site copy is the canonical one and both say so.

The markdown is a deliberate subset (headings, paragraphs, lists, tables, fences, blockquotes and
GitHub alerts, links, images, raw ``<details>``/``<picture>`` lines) because a subset can be
validated. Anything outside it is a build error rather than a silent mis-render.

Five link schemes resolve per target, so one source works in both places:

    [text](lesson:slug#anchor)   another lesson
    [text](wiki:Page#anchor)     an existing wiki page
    [text](site:path/#anchor)    a page on the site
    [text](repo:path)            a file in the repository (``path/`` for a directory)
    [text](sim:#/toolkit/aifit)  the simulator

and one directive embeds a visual on a line of its own:

    {{board:pdlc}}   {{figure:bar_sheet}}   {{model:g_decay}}   {{frameworks:ring}}
"""
from __future__ import annotations

import html
import importlib.util
import json
import math
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
LEARN = SITE / "content" / "learn"
LESSONS = LEARN / "lessons"
WIKI_DIR = SITE.parent / "wiki"
BASE_URL = "https://akash-coded.github.io/aws-bedrock-agentcore-strands/"
REPO = "https://github.com/akash-coded/aws-bedrock-agentcore-strands"
WIKI = REPO + "/wiki"
AUTHOR = "Akash Das"
AUTHOR_URL = "https://github.com/akash-coded"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.esm.min.mjs"
SHOTS = BASE_URL + "assets/learn/"

# Reading speed for English non-fiction, from a meta-analysis of 190 studies: Brysbaert (2019),
# Journal of Memory and Language 109. Pictures are timed the way Medium times them: 12 seconds for
# the first, one second less for each after it, never less than 3.
WPM = 238
LEVELS = ("Beginner", "Intermediate", "Advanced")
REQUIRED_H2 = ("Key takeaways", "Apply it in your role", "Sources and credits")

_E = html.escape


# ---------------------------------------------------------------------------------------- model
@dataclass
class Lesson:
    slug: str
    title: str
    short: str
    description: str
    wiki: str
    level: str
    updated: str
    dek: str = ""
    keywords: list[str] = field(default_factory=list)
    body: str = ""
    track: "Track | None" = None
    n: int = 0
    prev: "Lesson | None" = None
    next: "Lesson | None" = None

    @property
    def url(self) -> str:
        return f"{BASE_URL}learn/{self.slug}/"


@dataclass
class Track:
    id: str
    title: str
    short: str
    wiki: str
    blurb: str
    promise: str
    lessons: list[Lesson] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"{BASE_URL}learn/{self.id}/"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _front(text: str, where: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise SystemExit(f"{where}: missing front matter")
    head, _, body = text[4:].partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        if not line.strip():
            continue
        k, sep, v = line.partition(":")
        if not sep:
            raise SystemExit(f"{where}: bad front-matter line {line!r}")
        meta[k.strip()] = v.strip()
    return meta, body.lstrip("\n")


def load() -> tuple[dict, list[Track], dict[str, Lesson]]:
    """Read the curriculum and every lesson, and wire order, prev and next."""
    cur = _load_module(LEARN / "curriculum.py", "learn_curriculum")
    lessons: dict[str, Lesson] = {}
    for p in sorted(LESSONS.glob("*.md")):
        meta, body = _front(p.read_text(encoding="utf-8"), p.name)
        missing = [k for k in ("title", "short", "description", "wiki", "level", "updated") if not meta.get(k)]
        if missing:
            raise SystemExit(f"{p.name}: front matter missing {', '.join(missing)}")
        lessons[p.stem] = Lesson(
            slug=p.stem, title=meta["title"], short=meta["short"], description=meta["description"],
            wiki=meta["wiki"], level=meta["level"], updated=meta["updated"], dek=meta.get("dek", ""),
            keywords=[k.strip() for k in meta.get("keywords", "").split(",") if k.strip()], body=body)
    tracks = []
    for t in cur.TRACKS:
        tr = Track(id=t["id"], title=t["title"], short=t["short"], wiki=t["wiki"], blurb=t["blurb"],
                   promise=t["promise"])
        for i, slug in enumerate(t["lessons"], 1):
            if slug not in lessons:
                raise SystemExit(f"curriculum: track {t['id']} lists {slug}, which has no lessons/{slug}.md")
            les = lessons[slug]
            if les.track is not None:
                raise SystemExit(f"curriculum: {slug} is listed in two tracks")
            les.track, les.n = tr, i
            tr.lessons.append(les)
        tracks.append(tr)
    orphans = [s for s, l in lessons.items() if l.track is None]
    if orphans:
        raise SystemExit(f"curriculum: lessons not in any track: {', '.join(orphans)}")
    flat = [l for t in tracks for l in t.lessons]
    for a, b in zip(flat, flat[1:]):
        a.next, b.prev = b, a
    return {"start": cur.START}, tracks, lessons


# ---------------------------------------------------------------------------------------- slugs
def slug(text: str) -> str:
    """GitHub's anchor rule, so an anchor is the same on the wiki and on the site."""
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"[`*_]", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[^a-z0-9 -]", "", s.lower()).strip()
    return s.replace(" ", "-")


def headings(md: str) -> list[tuple[int, str, str]]:
    """(level, text, anchor) for every heading outside a fence, with GitHub's duplicate suffixes."""
    out, seen, fence = [], {}, None
    for line in md.splitlines():
        f = re.match(r"^(`{3,}|~{3,})", line)
        if f:
            fence = None if fence and line.startswith(fence) else (fence or f.group(1))
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            a = slug(m.group(2))
            n = seen.get(a, 0)
            seen[a] = n + 1
            out.append((len(m.group(1)), m.group(2), a if n == 0 else f"{a}-{n}"))
    return out


# ---------------------------------------------------------------------------------------- links
class Links:
    """Resolve the five schemes for one target: ``site`` (a page at /learn/<x>/) or ``wiki``."""

    def __init__(self, target: str, lessons: dict[str, Lesson], tracks: list[Track]):
        self.target, self.lessons = target, lessons
        self.tracks = {t.id: t for t in tracks}
        self.problems: list[str] = []

    def __call__(self, href: str) -> str:
        scheme, _, rest = href.partition(":")
        if scheme not in ("lesson", "track", "wiki", "site", "repo", "sim") or href.startswith(("http:", "https:")):
            return href
        path, _, frag = rest.partition("#")
        frag = f"#{frag}" if frag else ""
        if scheme == "lesson":
            les = self.lessons.get(path)
            if les is None:
                self.problems.append(f"unknown lesson {path!r}")
                return href
            # the wiki no longer mirrors the lessons (2026-09-24): a lesson link from a wiki page goes to the site
            return f"{les.url}{frag}" if self.target == "wiki" else f"../{les.slug}/{frag}"
        if scheme == "track":
            tr = self.tracks.get(path)
            if tr is None:
                self.problems.append(f"unknown track {path!r}")
                return href
            return f"{tr.wiki}{frag}" if self.target == "wiki" else f"../{tr.id}/{frag}"
        if scheme == "wiki":
            if not (WIKI_DIR / f"{path}.md").exists() and path not in ("Scoreboard",):
                self.problems.append(f"unknown wiki page {path!r}")
            return f"{path}{frag}" if self.target == "wiki" else f"{WIKI}/{path}{frag}"
        if scheme == "site":
            return f"{BASE_URL}{path}{frag}" if self.target == "wiki" else f"../../{path}{frag}"
        if scheme == "repo":
            kind = "tree" if path.endswith("/") or not path else "blob"
            return f"{REPO}/{kind}/main/{path.rstrip('/')}{frag}"
        return f"{BASE_URL}simulator/{rest}"


# ---------------------------------------------------------------------------------------- visuals
def _visuals() -> dict[str, dict]:
    """Every picture a lesson may embed: how to draw it live, what it says, where it lives."""
    from pages import boards, figures, models, illos, maps, wikimaps

    def m(fn, label):
        return lambda: f'<figure class="lmodel" aria-label="{_E(label, quote=True)}">{fn()}</figure>'

    v = {
        "board:pdlc": (boards.pdlc, "The agentic PDLC: four phases, one hard gate between P1 and P2, and a "
                       "line from P3 back to the next P0", "#pdlc"),
        "board:loops": (boards.loops, "Eight loops that run every team's workflow: five carry work forward, "
                        "three run backwards and need a named owner", "#loops"),
        "board:by_role": (boards.by_role, "Each role across the four phases, including the cells that should "
                          "stay empty", "#by-role"),
        "board:delegation": (boards.delegation, "Where the model helps and where it must not: the model drafts, "
                             "you check, and one thing per step is never delegated", "#delegation"),
        "figure:bar_sheet": (figures.bar_sheet, "The acceptance bar rises with the damage a mistake does",
                             "qa/"),
        "figure:chain": (figures.chain, "Chained steps multiply: four steps at 90% each are right 66% of the "
                         "time end to end", "solution-architect/"),
        "figure:cache_prefix": (figures.cache_prefix, "A cache matches an exact prefix: stable blocks first, then "
                                "the cache marker, then the request that changes", "devops/"),
        "figure:bolt_days": (figures.bolt_days, "A bolt plan: one risk per bolt, the walking skeleton first",
                             "engineering/"),
        "figure:shadow_widen": (figures.shadow_widen, "Shadow first, then widen the live share step by step",
                                "qa/"),
        "figure:bill_factors": (figures.bill_factors, "Four ordinary habits multiply into a bill 4.4 times its "
                                "estimate", "devops/"),
        "figure:authority_ladder": (figures.authority_ladder, "The authority ladder: every tool gets a band, from "
                                    "read-only to not delegated, and the band belongs to the tool", "solution-architect/"),
        "figure:two_numbers": (figures.two_numbers, "The two numbers a sponsor reports together: the saving and "
                               "the spend", "protocol/"),
        "frameworks:spine": (illos.spine, "The agentic PDLC in one picture: four phases, one hard gate, and "
                             "production feeding the next frame", "frameworks/"),
        "frameworks:pdlc_vs": (illos.pdlc_vs, "Traditional PDLC against the agentic PDLC: six stages decided once, "
                               "against four phases, a hard gate and the incident as the next brief", "frameworks/"),
        "frameworks:ladder": (illos.ladder, "The risk ladder: a change inherits the band of whatever it touches, "
                              "from R1 reviewed at the end to R5 not delegated", "frameworks/"),
        "frameworks:chain": (illos.chain, "Chained steps multiply: each right 90% of the time, six steps are right "
                             "53% of the time", "frameworks/"),
        "frameworks:methods": (illos.methods, "Four methods on one spine: SDD, BMAD, AI-DLC and AiDD, filled where "
                               "each speaks to a phase and dashed where it is silent", "frameworks/"),
        "frameworks:merge": (illos.merge, "How the four methods merge into the SkyWays PDLC: the parts of SDD, BMAD, "
                             "AI-DLC and AiDD placed in the phase each serves, flowing into the spine, and the row "
                             "of devices the SkyWays PDLC adds", "frameworks/"),
        "home:tower": (illos.tower, "The lifecycle flown as a loop: four runway segments P0 Frame, P1 Design and "
                       "Spec, P2 Build and Prove and P3 Run and Learn, one hard gate, four planes and the control "
                       "tower they answer to", ""),
    }
    for slug in maps.slugs():
        v[f"map:{slug}"] = (lambda s=slug: maps.draw(s), maps.alt(slug), f"learn/{slug}/")
    for slug in wikimaps.keys():
        v[f"wikimap:{slug}"] = (lambda s=slug: wikimaps.draw(s), wikimaps.alt(slug), "")
    from pages import posters
    for pid, (fn, alt, live) in posters.POSTERS.items():
        v[f"poster:{pid}"] = (fn, alt, live)
    for g, label in (("g_decay", "Length is the enemy"), ("g_doors", "Reversibility is the hinge"),
                     ("g_lever", "A hold is a lever, not a brake"), ("g_wall", "A prompt is a request; a signature is a boundary"),
                     ("g_average", "The average hides the slice that matters"), ("g_bound", "A score is not proof"),
                     ("g_funnel", "Evidence arrives at the speed of traffic"), ("g_multiply", "Cost is a product of habits"),
                     ("g_fanout", "Parallelism is a property of a tool"), ("g_dial", "Depth is a dial, not a constant"),
                     ("g_baton", "A phase ends on an artefact, not a date"), ("g_drift", "Drift is the defect with no error message")):
        v[f"model:{g}"] = (m(getattr(models, g), label), label, "models/")
    return {k: {"draw": d, "alt": a, "live": l} for k, (d, a, l) in v.items()}


VISUAL_KEYS = None


def visual_keys() -> set[str]:
    global VISUAL_KEYS
    if VISUAL_KEYS is None:
        VISUAL_KEYS = set(_visuals())
    return VISUAL_KEYS


def shot_name(key: str) -> str:
    return key.replace(":", "-").replace("_", "-")


DIRECTIVE = re.compile(r"^\{\{(board|figure|model|frameworks|map):([a-z0-9_-]+)\}\}\s*$")


# ---------------------------------------------------------------------------------------- inline
INLINE_TAG = re.compile(r"</?(?:b|i|em|strong|br|kbd|sub|sup|small|mark|abbr|span|u)(?:\s[^<>]*)?/?>", re.I)


ASSETS = Path(__file__).resolve().parents[1] / "assets"


def image_size(href: str) -> tuple[int, int] | None:
    """CSS size of a ``site:assets/…`` WebP, read from its header. Every picture the tutorial ships
    is captured at 2x (site/tools/shoot.mjs, simshots.mjs), so the CSS size is half the pixels,
    declaring it keeps a narrow screenshot at its own size and stops the page shifting as it loads."""
    if not (href.startswith("site:assets/") and href.endswith(".webp")):
        return None
    f = ASSETS / href[len("site:assets/"):]
    if not f.exists():
        return None
    b = f.read_bytes()[:40]
    if b[:4] != b"RIFF" or b[8:12] != b"WEBP":
        return None
    kind = b[12:16]
    if kind == b"VP8X":
        w, h = 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
    elif kind == b"VP8 ":
        w, h = int.from_bytes(b[26:28], "little") & 0x3FFF, int.from_bytes(b[28:30], "little") & 0x3FFF
    elif kind == b"VP8L":
        v = int.from_bytes(b[21:25], "little")
        w, h = (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
    else:
        return None
    return w // 2, h // 2


def inline(s: str, link) -> str:
    codes, tags = [], []

    def keep_code(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    def keep_tag(m):
        tags.append(m.group(0))
        return f"\x01{len(tags) - 1}\x01"

    s = re.sub(r"`([^`]+)`", keep_code, s)
    s = INLINE_TAG.sub(keep_tag, s)
    s = html.escape(s, quote=False)
    s = re.sub(r"&amp;(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]{2,8});", r"&\1;", s)

    def img(m):
        size = image_size(m.group(2))
        dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
        return f'<img src="{_E(link(m.group(2)), quote=True)}" alt="{m.group(1)}"{dims} loading="lazy">'

    def lnk(m):
        href = link(m.group(2))
        ext = href.startswith("http") and not href.startswith(BASE_URL)
        attr = ' rel="noopener"' if ext else ""
        return f'<a href="{_E(href, quote=True)}"{attr}>{m.group(1)}</a>'

    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", img, s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lnk, s)
    s = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub("\x01(\\d+)\x01", lambda m: tags[int(m.group(1))], s)
    s = re.sub("\x00(\\d+)\x00", lambda m: "<code>" + html.escape(codes[int(m.group(1))]) + "</code>", s)
    return s


# ---------------------------------------------------------------------------------------- blocks
FENCE = re.compile(r"^(`{3,}|~{3,})\s*([\w+-]*)\s*$")
LIST = re.compile(r"^(\s*)([-*]|\d+[.)])\s+(.*)$")
SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
RAW = re.compile(r"^\s*</?(details|summary|picture|source|img|div|figure|figcaption|p|br)\b[^>]*>", re.I)
ALERT = re.compile(r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$")
ALERT_LABEL = {"NOTE": "Note", "TIP": "In short", "IMPORTANT": "Important", "WARNING": "Watch out",
               "CAUTION": "Caution"}


def _cells(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, tick, k = [], "", False, 0
    while k < len(s):
        c = s[k]
        if c == "\\" and k + 1 < len(s) and s[k + 1] == "|":
            cur += "|"
            k += 2
            continue
        if c == "`":
            tick = not tick
        if c == "|" and not tick:
            cells.append(cur.strip())
            cur = ""
        else:
            cur += c
        k += 1
    cells.append(cur.strip())
    return cells


def _starts_block(line: str) -> bool:
    return bool(FENCE.match(line) or re.match(r"^#{1,6}\s", line) or LIST.match(line)
                or line.lstrip().startswith(">") or line.lstrip().startswith("|")
                or RAW.match(line) or DIRECTIVE.match(line.strip())
                or re.match(r"^\s*(-{3,}|\*{3,})\s*$", line))


class Html:
    """Markdown subset to HTML for the site. ``visual`` draws a directive; ``link`` resolves hrefs."""

    def __init__(self, link, visual):
        self.link, self.visual = link, visual
        self.anchors: dict[str, int] = {}
        self.mermaid = 0

    def _id(self, text: str) -> str:
        a = slug(text)
        n = self.anchors.get(a, 0)
        self.anchors[a] = n + 1
        return a if n == 0 else f"{a}-{n}"

    def render(self, md: str) -> str:
        return self._blocks(md.split("\n"))

    def _blocks(self, lines: list[str]) -> str:
        out, i = [], 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            f = FENCE.match(line)
            if f:
                fence, lang, body = f.group(1), f.group(2).lower(), []
                i += 1
                while i < len(lines) and not lines[i].startswith(fence):
                    body.append(lines[i])
                    i += 1
                i += 1
                src = "\n".join(body)
                if lang == "mermaid":
                    self.mermaid += 1
                    out.append(f'<figure class="mmd"><pre class="mermaid">{_E(src)}</pre></figure>')
                else:
                    cls = f' class="language-{lang}"' if lang else ""
                    self._cb = getattr(self, "_cb", 0) + 1
                    out.append(f'<div class="codebox"><button type="button" class="cp" data-copy="cb-{self._cb}" '
                               f'aria-label="Copy this block">Copy</button>'
                               f'<pre id="cb-{self._cb}" tabindex="0"><code{cls}>{_E(src)}</code></pre></div>')
                continue
            d = DIRECTIVE.match(line.strip())
            if d:
                out.append(self.visual(f"{d.group(1)}:{d.group(2)}"))
                i += 1
                continue
            h = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
            if h:
                lvl, text = len(h.group(1)), h.group(2)
                hid = self._id(text)
                out.append(f'<h{lvl} id="{hid}">{inline(text, self.link)}'
                           f'<a class="hl" href="#{hid}" aria-label="Link to this section">#</a></h{lvl}>')
                i += 1
                continue
            if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
                out.append("<hr>")
                i += 1
                continue
            if line.lstrip().startswith("|") and i + 1 < len(lines) and SEP.match(lines[i + 1]):
                head = _cells(line)
                i += 2
                rows = []
                while i < len(lines) and lines[i].lstrip().startswith("|"):
                    rows.append(_cells(lines[i]))
                    i += 1
                th = "".join(f"<th>{inline(c, self.link)}</th>" for c in head)
                tb = "".join("<tr>" + "".join(f"<td>{inline(c, self.link)}</td>" for c in r) + "</tr>" for r in rows)
                out.append(f'<div class="tw" tabindex="0"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
                continue
            if line.lstrip().startswith(">"):
                inner = []
                while i < len(lines) and lines[i].lstrip().startswith(">"):
                    inner.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                a = ALERT.match(inner[0].strip()) if inner else None
                if a:
                    kind = a.group(1)
                    body = self._blocks(inner[1:])
                    out.append(f'<div class="callout {kind.lower()}" role="note"><p class="ct">'
                               f'{ALERT_LABEL[kind]}</p>{body}</div>')
                else:
                    out.append(f"<blockquote>{self._blocks(inner)}</blockquote>")
                continue
            if LIST.match(line):
                html_, i = self._list(lines, i, len(LIST.match(line).group(1)))
                out.append(html_)
                continue
            if RAW.match(line):
                out.append(line.strip())
                i += 1
                continue
            para = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not _starts_block(lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(para), self.link)}</p>")
        return "\n".join(out)

    def _list(self, lines: list[str], i: int, indent: int) -> tuple[str, int]:
        ordered = bool(re.match(r"^\s*\d+[.)]\s", lines[i]))
        start = re.match(r"^\s*(\d+)", lines[i])
        items = []
        while i < len(lines):
            m = LIST.match(lines[i])
            if not m:
                if not lines[i].strip():
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    nxt = LIST.match(lines[j]) if j < len(lines) else None
                    if nxt and len(nxt.group(1)) == indent:
                        i = j
                        continue
                break
            if len(m.group(1)) < indent:
                break
            if len(m.group(1)) > indent:
                sub, i = self._list(lines, i, len(m.group(1)))
                items[-1] = items[-1][:-5] + sub + "</li>" if items else sub
                continue
            content = [m.group(3)]
            i += 1
            while (i < len(lines) and lines[i].strip() and not LIST.match(lines[i])
                   and lines[i].startswith(" " * (indent + 2))):
                content.append(lines[i].strip())
                i += 1
            items.append(f"<li>{inline(' '.join(content), self.link)}</li>")
        tag = "ol" if ordered else "ul"
        st = f' start="{start.group(1)}"' if ordered and start and start.group(1) != "1" else ""
        return f"<{tag}{st}>{''.join(items)}</{tag}>", i


# ---------------------------------------------------------------------------------------- measures
def plain_words(md: str) -> int:
    text = re.sub(r"(`{3,}|~{3,})[\s\S]*?\1", " ", md)
    text = DIRECTIVE.sub(" ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"[#>*_`|\[\]-]", " ", text)
    return len(re.findall(r"[A-Za-z0-9][\w'’.%×÷−-]*", text))


def visuals_in(md: str) -> int:
    fences = len(re.findall(r"^```mermaid\s*$", md, re.M))
    dirs = sum(1 for line in md.splitlines() if DIRECTIVE.match(line.strip()))
    imgs = len(re.findall(r"!\[[^\]]*\]\(", md)) + len(re.findall(r"<picture\b", md))
    return fences + dirs + imgs


def minutes(md: str) -> int:
    secs = plain_words(md) / WPM * 60
    secs += sum(max(12 - k, 3) for k in range(visuals_in(md)))
    return max(1, round(secs / 60))


def faq(md: str) -> list[tuple[str, str]]:
    """Question and plain-text answer pairs from a ``## FAQ`` section."""
    m = re.search(r"^## FAQ\s*$([\s\S]*?)(?=^## |\Z)", md, re.M)
    if not m:
        return []
    out = []
    for q in re.finditer(r"^### (.+?)\s*$([\s\S]*?)(?=^### |\Z)", m.group(1), re.M):
        ans = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", q.group(2))
        ans = re.sub(r"[*`>]", "", ans)
        ans = " ".join(ans.split())
        if ans:
            out.append((q.group(1).strip(), ans))
    return out


def fmt_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b')} {d.year}"


# ---------------------------------------------------------------------------------------- checks
def validate(meta: dict, tracks: list[Track], lessons: dict[str, Lesson]) -> tuple[list[str], list[str]]:
    """Errors stop the build; warnings are printed. Every rule here encodes a way a lesson went wrong."""
    err, warn = [], []
    keys = visual_keys()
    seen_wiki = {}
    wiki_pages = {p.stem for p in WIKI_DIR.glob("*.md")}
    for t in tracks:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", t.id):
            err.append(f"track {t.id}: id must be lowercase-hyphenated")
        if t.id in lessons:
            err.append(f"track {t.id}: collides with a lesson slug")
        if not t.lessons:
            err.append(f"track {t.id}: has no lessons")
    for les in lessons.values():
        w = f"lessons/{les.slug}.md"
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", les.slug):
            err.append(f"{w}: slug must be lowercase-hyphenated")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", les.wiki):
            err.append(f"{w}: wiki name {les.wiki!r} may only use letters, digits and hyphens")
        if les.wiki in seen_wiki:
            err.append(f"{w}: wiki name {les.wiki!r} also used by {seen_wiki[les.wiki]}")
        seen_wiki[les.wiki] = les.slug
        if len(les.title) > 72:
            err.append(f"{w}: title is {len(les.title)} characters; keep it under 72 or search engines cut it")
        elif len(les.title) > 62:
            warn.append(f"{w}: title is {len(les.title)} characters; 60 or fewer shows in full on most results")
        dl = len(les.description)
        if not 90 <= dl <= 175:
            err.append(f"{w}: description is {dl} characters; aim for 120 to 160")
        elif not 115 <= dl <= 162:
            warn.append(f"{w}: description is {dl} characters; 120 to 160 shows in full")
        if les.level not in LEVELS:
            err.append(f"{w}: level must be one of {', '.join(LEVELS)}")
        try:
            date.fromisoformat(les.updated)
        except ValueError:
            err.append(f"{w}: updated must be an ISO date")
        hs = headings(les.body)
        if any(h[0] == 1 for h in hs):
            err.append(f"{w}: the body must not have an H1; the title is the H1")
        h2 = [h[1] for h in hs if h[0] == 2]
        for need in REQUIRED_H2:
            if need not in h2:
                err.append(f"{w}: missing the '## {need}' section")
        if visuals_in(les.body) < 1:
            err.append(f"{w}: every lesson carries at least one picture, a board, a figure or a diagram")
        for line in les.body.splitlines():
            d = DIRECTIVE.match(line.strip())
            if d and f"{d.group(1)}:{d.group(2)}" not in keys:
                err.append(f"{w}: unknown visual {{{{{d.group(1)}:{d.group(2)}}}}}")
            if re.match(r"^\s*\{\{", line) and not d:
                err.append(f"{w}: malformed directive {line.strip()!r}")
        own = {h[2] for h in hs}
        for m in re.finditer(r"\]\((lesson|track|wiki|#)([^)]*)\)", les.body):
            kind, rest = m.group(1), m.group(2)
            if kind == "#":
                if rest and rest not in own:
                    err.append(f"{w}: anchor #{rest} is not a heading on this page")
                continue
            target, _, frag = rest.lstrip(":").partition("#")
            if kind == "lesson":
                if target not in lessons:
                    err.append(f"{w}: links to unknown lesson {target!r}")
                elif frag and frag not in {h[2] for h in headings(lessons[target].body)}:
                    err.append(f"{w}: lesson {target} has no heading #{frag}")
            elif kind == "track" and target not in {t.id for t in tracks}:
                err.append(f"{w}: links to unknown track {target!r}")
            elif kind == "wiki" and target not in wiki_pages | {"Scoreboard"}:
                err.append(f"{w}: links to unknown wiki page {target!r}")
        first = next((p for p in re.split(r"\n\s*\n", les.body) if p.strip()), "")
        if not first.lstrip().startswith(">"):
            warn.append(f"{w}: open with the answer, in a '> [!TIP]' block, before anything else")
        if minutes(les.body) > 14:
            warn.append(f"{w}: {minutes(les.body)} minutes is long for one sitting; consider splitting")
        if not faq(les.body):
            warn.append(f"{w}: no FAQ section")
    start = LEARN / "start-here.md"
    if start.exists():
        smeta, sbody = _front(start.read_text(encoding="utf-8"), "start-here.md")
        for m in re.finditer(r"\]\((lesson|track):([^)#]*)(?:#([^)]*))?\)", sbody):
            kind, target, frag = m.group(1), m.group(2), m.group(3)
            if kind == "lesson" and target not in lessons:
                err.append(f"start-here.md: links to unknown lesson {target!r}")
            elif kind == "lesson" and frag and frag not in {h[2] for h in headings(lessons[target].body)}:
                err.append(f"start-here.md: lesson {target} has no heading #{frag}")
            elif kind == "track" and target not in {t.id for t in tracks}:
                err.append(f"start-here.md: links to unknown track {target!r}")
        if not 90 <= len(smeta.get("description", "")) <= 175:
            err.append("start-here.md: description should be 120 to 160 characters")
    return err, warn


# ---------------------------------------------------------------------------------------- pages
def _rail(tracks: list[Track], here: str) -> str:
    groups = []
    for t in tracks:
        items = "".join(
            f'<li><a class="ll" href="../{l.slug}/"{" aria-current=page" if l.slug == here else ""}>'
            f"{_E(l.short)}</a></li>" for l in t.lessons)
        on = " on" if here == t.id or any(l.slug == here for l in t.lessons) else ""
        groups.append(f'<section class="lt{on}"><h3><a href="../{t.id}/">{_E(t.title)}</a></h3>'
                      f"<ol>{items}</ol></section>")
    cur = " aria-current=page" if here == "start" else ""
    return (f'<aside class="rail lrail" aria-label="All lessons"><details class="lnav" open>'
            f"<summary>All lessons</summary>"
            f'<a class="lstart" href="../"{cur}>Start here</a>{"".join(groups)}</details></aside>')


def _toc(md: str) -> str:
    """Inline contents, under the lesson header. A right-hand rail would cost the boards 248px."""
    items = "".join(f'<li><a href="#{a}">{_E(re.sub(r"[`*]", "", t))}</a></li>'
                    for lvl, t, a in headings(md) if lvl == 2)
    return f'<details class="otp" open><summary>On this page</summary><ol>{items}</ol></details>'


def _ld_org() -> dict:
    return {"@type": "Organization", "@id": BASE_URL + "#org", "name": "SkyWays Consultancy", "url": BASE_URL}


def _og_for(slug: str) -> str:
    p = Path(__file__).resolve().parents[1] / "assets" / "og" / f"learn-{slug}.jpg"
    return f"{BASE_URL}assets/og/learn-{slug}.jpg" if p.exists() else BASE_URL + "assets/og.png"


def _ld_person() -> dict:
    return {"@type": "Person", "name": AUTHOR, "url": AUTHOR_URL, "sameAs": [AUTHOR_URL],
            "jobTitle": "Solution architect and trainer, agentic AI on AWS"}


def _graph(nodes: list[dict]) -> str:
    return json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False)


def lesson_page(les: Lesson, tracks, lessons, shell, visual) -> str:
    link = Links("site", lessons, tracks)
    body = Html(link, visual).render(les.body)
    t = les.track
    mins = minutes(les.body)
    crumbs = [("Tutorial", f"{BASE_URL}learn/"), (t.title, t.url), (les.short, les.url)]
    pn = []
    if les.prev:
        pn.append(f'<a class="pv" href="../{les.prev.slug}/"><span class="k">Previous</span>'
                  f"<b>{_E(les.prev.short)}</b></a>")
    else:
        pn.append('<a class="pv" href="../"><span class="k">Previous</span><b>Start here</b></a>')
    if les.next:
        nt = "" if les.next.track is t else f"<small>{_E(les.next.track.title)}</small>"
        pn.append(f'<a class="nx" href="../{les.next.slug}/"><span class="k">Next</span>'
                  f"<b>{_E(les.next.short)}</b>{nt}</a>")
    else:
        pn.append('<a class="nx" href="../"><span class="k">Next</span><b>Back to the start</b></a>')
    nodes = [{
        "@type": "TechArticle", "@id": les.url + "#article", "headline": les.title,
        "description": les.description, "url": les.url, "mainEntityOfPage": les.url,
        "datePublished": les.updated, "dateModified": les.updated, "inLanguage": "en",
        "author": _ld_person(), "publisher": _ld_org(), "image": _og_for(les.slug),
        "keywords": ", ".join(les.keywords), "educationalLevel": les.level,
        "timeRequired": f"PT{mins}M", "wordCount": plain_words(les.body),
        "isPartOf": {"@type": "Course", "name": t.title, "url": t.url,
                     "provider": _ld_person(), "description": t.blurb},
        "license": REPO + "/blob/main/LICENSE", "isAccessibleForFree": True,
    }, {
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": k, "name": n, "item": u}
                            for k, (n, u) in enumerate(crumbs, 1)],
    }]
    qa = faq(les.body)
    if qa:
        nodes.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]})
    head = (f'<meta property="article:modified_time" content="{les.updated}">'
            f'<link rel="alternate" type="text/markdown" href="index.md" title="This lesson as markdown">'
            f'<script type="application/ld+json">{_graph(nodes)}</script>')
    html_ = f"""<div class="cols lcols">
{_rail(tracks, les.slug)}
<main id="main" class="lesson">
  <h1>{_E(les.title)}</h1>
  {f'<p class="lede">{inline(les.dek, link)}</p>' if les.dek else ''}
  <p class="lmeta"><span><b>{mins} min</b> read</span><span>{les.level}</span><span>Lesson {les.n} of {len(t.lessons)}</span><span>Updated <time datetime="{les.updated}">{fmt_date(les.updated)}</time></span><span>By <a href="{AUTHOR_URL}" rel="author">{AUTHOR}</a></span></p>
  {_toc(les.body)}
  <article class="prose">
{body}
  </article>
  <nav class="pn" aria-label="Lesson navigation">{''.join(pn)}</nav>
  <p class="lalt">Prefer GitHub? This track is <a href="{WIKI}/{t.wiki}">on the wiki</a>, and this lesson is <a href="index.md">markdown</a>. Found a mistake? <a href="{REPO}/edit/main/site/content/learn/lessons/{les.slug}.md">Edit this lesson</a>, or <a href="{REPO}/discussions/101">say so</a>.</p>
</main>
</div>"""
    if link.problems:
        raise SystemExit(f"lessons/{les.slug}.md: " + "; ".join(sorted(set(link.problems))))
    tour = [
        {"sel": ".lrail", "title": "Every lesson, in order", "body": f"Eight tracks. You are in <b>{_E(t.title)}</b>, lesson {les.n} of {len(t.lessons)}. Read a track top to bottom, or jump to the one your role needs."},
        {"sel": ".otp", "title": "On this page", "body": "Every lesson has the same shape: the answer in one sentence, a picture, the sound-familiar symptoms, the how-to, where you'll use it, a try-it exercise, takeaways, an FAQ and <b>how to apply it in your role</b>."},
        {"sel": ".prose .callout", "title": "The answer first", "body": "The green box is the whole lesson in one sentence. If it is enough, move on; the rest is the argument and the practice."},
        {"sel": "#apply-it-in-your-role", "title": "Apply it in your role", "body": "Near the end: what to do as a forward-deployed engineer, a product manager or an engineer, an AI-augmented shortcut for each, how it runs across an enterprise, and a ten-minute workflow with a prompt to paste."},
        {"sel": ".pn", "title": "Next lesson", "body": "Lessons chain in order. Previous and next are always at the bottom."},
    ]
    return shell(title=les.title, desc=les.description, body=html_, depth=2, nav_id="learn", modified=les.updated,
                 canonical=les.url, head_extra=head + MERMAID_HEAD, own_ld=True,
                 crumbs=[("Tutorial", "../"), (t.title, f"../{t.id}/"), (les.short, "")], tour=tour, kind="lesson", og=f"learn-{les.slug}")


MERMAID_HEAD = f'<script type="module" src="../../theme/learn.js" data-mermaid="{MERMAID}"></script>'


def _cards(t: Track) -> str:
    return "".join(
        f'<li><a class="lc" href="../{l.slug}/"><span class="lcn">{l.n}</span><span class="lcb">'
        f"<b>{_E(l.title)}</b><span>{_E(l.description)}</span>"
        f'<small>{minutes(l.body)} min · {l.level}</small></span></a></li>' for l in t.lessons)


def track_page(t: Track, tracks, lessons, shell) -> str:
    total = sum(minutes(l.body) for l in t.lessons)
    html_ = f"""<div class="cols lcols">
{_rail(tracks, t.id)}
<main id="main" class="lesson">
  <h1>{_E(t.title)}</h1>
  <p class="lede">{_E(t.blurb)}</p>
  <p class="lmeta"><span><b>{len(t.lessons)} lessons</b></span><span>about {total} minutes</span><span>{_E(t.promise)}</span></p>
  <ol class="lcards">{_cards(t)}</ol>
  <p class="lalt">Also <a href="{WIKI}/{t.wiki}">on the wiki</a>.</p>
</main>
</div>"""
    ld = [{"@type": "Course", "@id": t.url + "#course", "name": t.title, "description": t.blurb,
           "url": t.url, "provider": _ld_person(), "inLanguage": "en", "isAccessibleForFree": True,
           "hasPart": [{"@type": "TechArticle", "name": l.title, "url": l.url} for l in t.lessons]},
          {"@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Tutorial", "item": f"{BASE_URL}learn/"},
              {"@type": "ListItem", "position": 2, "name": t.title, "item": t.url}]}]
    head = f'<script type="application/ld+json">{_graph(ld)}</script>'
    desc = f"{t.title}: {t.blurb}"[:160]
    return shell(title=f"{t.title} · Agentic PDLC tutorial", desc=desc, body=html_, depth=2, nav_id="learn",
                 canonical=t.url, head_extra=head, own_ld=True,
                 crumbs=[("Tutorial", "../"), (t.title, "")], kind="track", og=f"learn-{t.id}")


def start_page(meta, tracks, lessons, shell, visual) -> str:
    from pages import _kit as kit
    src = (LEARN / "start-here.md").read_text(encoding="utf-8")
    smeta, sbody = _front(src, "start-here.md")
    link = Links("site", lessons, tracks)
    # the start page sits at /learn/, one level shallower than a lesson
    body = Html(lambda h: re.sub(r"^\.\./", "", link(h)) if h.startswith("lesson:") or h.startswith("track:")
                else re.sub(r"^\.\./\.\./", "../", link(h)), visual).render(sbody)
    groups = []
    for k, t in enumerate(tracks, 1):
        total = sum(minutes(l.body) for l in t.lessons)
        first = t.lessons[0]
        groups.append(
            f'<li><a class="lk" href="{t.id}/"><span class="lkn">{k}</span><span class="lkb"><b>{_E(t.title)}</b>'
            f"<span>{_E(t.blurb)}</span><small>{len(t.lessons)} lessons · about {total} min · "
            f"starts with “{_E(first.short)}”</small></span></a></li>")
    rail = _rail(tracks, "start").replace('href="../', 'href="').replace('href="">', 'href="./">')
    rail = rail.replace('class="lstart" href=""', 'class="lstart" href="./"')
    html_ = f"""<div class="cols lcols">
{rail}
<main id="main" class="lesson">
  <p class="kicker">A free tutorial in {sum(len(t.lessons) for t in tracks)} lessons</p>
  <h1>{_E(smeta['title'])}</h1>
  <p class="lede">{inline(smeta.get('dek', ''), link)}</p>
  {kit.orient(
      "Anyone running, building, testing, operating or funding software where a model does part of the work. "
      "and anyone preparing for an interview for such a job.",
      "Learn the agentic PDLC in five-to-ten-minute lessons, in order, then apply each one in your own role "
      "with the shortcut and the ten-minute workflow at the end of every lesson.",
      ["New? Read <b>Getting started</b>, then <b>Fundamentals</b>, top to bottom.",
       "In a hurry? Use <b>Start where you are</b> below to jump to your role's lesson.",
       "Every lesson ends with <b>Apply it in your role</b> and a prompt to paste; every diagram is drawn live."])}
  <article class="prose">
{body}
  </article>
  <h2 id="the-tracks" style="margin-top:36px">The tracks</h2>
  <ol class="lkeys">{''.join(groups)}</ol>
  <p class="lalt">Also <a href="{WIKI}/Start-Here">on the wiki</a>, and as <a href="../llms.txt">llms.txt</a> for AI assistants.</p>
</main>
</div>"""
    ld = [{"@type": "CollectionPage", "@id": f"{BASE_URL}learn/#page", "name": smeta["title"],
           "description": smeta["description"], "url": f"{BASE_URL}learn/", "inLanguage": "en",
           "author": _ld_person(), "hasPart": [{"@type": "Course", "name": t.title, "url": t.url} for t in tracks]}]
    head = f'<script type="application/ld+json">{_graph(ld)}</script>' + MERMAID_HEAD.replace("../../", "../")
    tour = [
        {"sel": ".lrail", "title": "Every lesson, in order", "body": "Eight tracks, top to bottom: getting started, fundamentals, methods decoded, running delivery, by role, teams and organisation, the case study, interviews and careers."},
        {"sel": ".orient", "title": "How to use the tutorial", "body": "Read in order if you are new; jump by role if you are not. Each lesson is five to ten minutes and ends with how to apply it in your role."},
        {"sel": "#by-role", "title": "Your role across the phases", "body": "One row per role, one column per phase. Hover a cell to light its row and column; click one to open that step of the role's page."},
        {"sel": "#the-tracks", "title": "The tracks", "body": "Each card is a track with its lesson count and reading time. Start with the first; the interview banks are last."},
    ]
    return shell(title=smeta["title"], desc=smeta["description"], body=html_, depth=1, nav_id="learn",
                 canonical=f"{BASE_URL}learn/", head_extra=head, own_ld=True,
                 crumbs=[("Tutorial", "")], tour=tour, kind="learn", og="learn")


def site_markdown(les: Lesson, lessons, tracks) -> str:
    """The lesson as plain markdown with absolute links, for readers and tools that prefer it."""
    link = Links("wiki", lessons, tracks)
    body = re.sub(r"\]\(([^)\s]+)\)", lambda m: "](" + _absolute(link(m.group(1))) + ")", les.body)
    body = "\n".join(f"![{_visuals()[k]['alt']}]({SHOTS}{shot_name(k)}.light.webp)"
                     if (d := DIRECTIVE.match(line.strip())) and (k := f"{d.group(1)}:{d.group(2)}") else line
                     for line in body.splitlines())
    return (f"# {les.title}\n\n{les.dek}\n\n{minutes(les.body)} min read · {les.level} · "
            f"Lesson {les.n} of {len(les.track.lessons)} in {les.track.title} · Updated {les.updated} · "
            f"By {AUTHOR}\n\nCanonical: {les.url}\n\n{body}\n")


def _absolute(href: str) -> str:
    if href.startswith(("http:", "https:", "#", "mailto:")):
        return href
    return f"{WIKI}/{href}"


def _rebase(fragment: str, prefix: str) -> str:
    """Boards link to site pages as if drawn at the site root; move those links to the page's depth."""
    return re.sub(r'\b(href|src)="(?![a-zA-Z][a-zA-Z0-9+.-]*:|/|#|\.)([^"]+)"',
                  lambda m: f'{m.group(1)}="{prefix}{m.group(2)}"', fragment)


def render(out: Path, shell) -> list[str]:
    meta, tracks, lessons = load()
    errors, warnings = validate(meta, tracks, lessons)
    for w in warnings:
        print("  learn: warning:", w)
    if errors:
        raise SystemExit("learn: " + "\n  learn: ".join([""] + errors))
    reg = _visuals()

    def visual(key: str) -> str:
        return reg[key]["draw"]()

    written = []

    def put(rel: str, text: str) -> None:
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        written.append(rel)

    put("learn/index.html", start_page(meta, tracks, lessons, shell, lambda k: _rebase(visual(k), "../")))
    for t in tracks:
        put(f"learn/{t.id}/index.html", track_page(t, tracks, lessons, shell))
        for les in t.lessons:
            put(f"learn/{les.slug}/index.html",
                lesson_page(les, tracks, lessons, shell, lambda k: _rebase(visual(k), "../../")))
            put(f"learn/{les.slug}/index.md", site_markdown(les, lessons, tracks))
    put("llms.txt", llms_txt(tracks))
    put("llms-full.txt", llms_full(tracks, lessons))
    put("feed.xml", feed_xml(lessons))
    return written


def used_visuals() -> list[str]:
    """Registry keys that some lesson or the start page actually embeds, in first-use order."""
    seen: list[str] = []
    sources = [p.read_text(encoding="utf-8") for p in sorted(LESSONS.glob("*.md"))]
    sources.append((LEARN / "start-here.md").read_text(encoding="utf-8"))
    for text in sources:
        for line in text.splitlines():
            d = DIRECTIVE.match(line.strip())
            if d and (k := f"{d.group(1)}:{d.group(2)}") not in seen:
                seen.append(k)
    return seen


def shots_page(out: Path, shell) -> str:
    """The visuals the lessons embed, one per cell, for site/tools/shoot.mjs. Built only with --shots.

    Boards are captured at the width they were drawn for; figures and models at a reading width, so
    a screenshot on the wiki is the size it would be in the lesson."""
    reg = _visuals()
    import wiki_pictures
    wanted = list(reg)  # every picture, so the picture pack has all of them
    cells = "".join(
        f'<div class="shot {"wide" if k.startswith(("board:", "frameworks:", "map:", "wikimap:", "poster:")) else "model" if k.startswith("model:") else "narrow"}" data-shot="{shot_name(k)}">'
        f'{reg[k]["draw"]()}</div>' for k in wanted)
    body = f'<main id="main" class="shots">{cells}</main>'
    html_ = shell(title="shots", desc="Screenshot sheet. Not for readers.", body=body, depth=2, nav_id="",
                  canonical=f"{BASE_URL}learn/", head_extra='<meta name="robots" content="noindex">', own_ld=True)
    p = out / "learn" / "_shots" / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html_, encoding="utf-8")
    return str(p)


def urls() -> list[tuple[str, str]]:
    meta, tracks, lessons = load()
    newest = max(l.updated for l in lessons.values())
    out = [(f"{BASE_URL}learn/", newest)]
    for t in tracks:
        out.append((t.url, max(l.updated for l in t.lessons)))
        out += [(l.url, l.updated) for l in t.lessons]
    return out


def feed_xml(lessons: dict[str, Lesson]) -> str:
    """An Atom feed of the lessons, newest update first, for readers and crawlers that follow feeds."""
    from xml.sax.saxutils import escape as X
    items = sorted(lessons.values(), key=lambda x: (x.updated, x.slug), reverse=True)
    newest = items[0].updated if items else "2026-01-01"
    entries = "".join(
        f"  <entry>\n    <title>{X(x.title)}</title>\n    <link href=\"{x.url}\"/>\n    <id>{x.url}</id>\n"
        f"    <updated>{x.updated}T00:00:00Z</updated>\n    <summary>{X(x.description)}</summary>\n"
        f"    <author><name>Akash Das</name></author>\n  </entry>\n" for x in items)
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">\n'
            f"  <title>The agentic manual: lessons</title>\n  <subtitle>New and updated lessons on the agentic PDLC, "
            f"by SkyWays Consultancy</subtitle>\n  <link href=\"{BASE_URL}learn/\"/>\n"
            f"  <link rel=\"self\" href=\"{BASE_URL}feed.xml\"/>\n  <id>{BASE_URL}feed.xml</id>\n"
            f"  <updated>{newest}T00:00:00Z</updated>\n{entries}</feed>\n")


def llms_txt(tracks: list[Track]) -> str:
    """The llms.txt proposal (llmstxt.org, Howard 2024): a markdown index an assistant can read."""
    lines = ["# The agentic manual. Agentic PDLC tutorial", "",
             "> A free, method-agnostic tutorial for running software projects where an AI model does the "
             "work: the four-phase agentic PDLC (P0 Frame, P1 Design & Spec, P2 Build & Prove, P3 Run & "
             "Learn), how AWS AI-DLC, AIDD, the BMAD Method and spec-driven development fit onto it, and what "
             "each role does. By Akash Das. MIT licence.", "",
             "Each lesson is also available as markdown at the same URL with index.md appended. The full text "
             f"of every lesson is at {BASE_URL}llms-full.txt. Every diagram, with its caption, is listed at "
             f"{BASE_URL}pictures/.", ""]
    for t in tracks:
        lines.append(f"## {t.title}")
        lines.append("")
        lines += [f"- [{l.title}]({l.url}): {l.description}" for l in t.lessons]
        lines.append("")
    lines += ["## The manual, by role", "",
              f"- [Product manager]({BASE_URL}product-manager/): eight steps from a vibe to a number you can defend "
              f"(markdown: {WIKI}/Journey-Product-Manager)",
              f"- [Solution architect]({BASE_URL}solution-architect/): from requirements to a system that holds "
              f"(markdown: {WIKI}/Journey-Solution-Architect)",
              f"- [Engineering lead]({BASE_URL}engineering/): from a story file to a shipped bolt "
              f"(markdown: {WIKI}/Journey-Engineering-Lead)",
              f"- [QA lead]({BASE_URL}qa/): from 'it works' to a number you can defend (markdown: {WIKI}/Journey-QA-Lead)",
              f"- [DevOps and platform]({BASE_URL}devops/): from a laptop to production, repeatably "
              f"(markdown: {WIKI}/Journey-DevOps)", "",
              "## Reference", "",
              f"- [The operating protocol]({BASE_URL}protocol/): for whoever funds the work; the four decisions only leadership can make",
              f"- [Twelve mental models]({BASE_URL}models/): what each predicts, the mistake it prevents, and a test for whether it landed",
              f"- [Frameworks, acronyms and the pictures]({BASE_URL}frameworks/): AI-DLC, AIDD, BMAD and SDD placed on one spine",
              f"- [Templates]({BASE_URL}templates/) and [prompts]({BASE_URL}prompts/): every artefact skeleton and every prompt, copyable",
              f"- [The wiki]({WIKI}): the method written down, with decision trees, formulas, scenarios and exercises", "",
              "## Optional", "",
              f"- [Home]({BASE_URL}): the method drawn as four boards, by role",
              f"- [The SkyWays playbook]({BASE_URL}simulator/): ninety days of one airline's agentic build, playable",
              f"- [Source repository]({REPO}): curriculum, labs and this tutorial's source", ""]
    return "\n".join(lines)


def llms_full(tracks: list[Track], lessons: dict[str, Lesson]) -> str:
    parts = [f"# The agentic manual, every lesson, in order\n\nSource: {BASE_URL}learn/\n"]
    for t in tracks:
        parts.append(f"\n\n# Track: {t.title}\n\n{t.blurb}\n")
        parts += ["\n\n" + site_markdown(l, lessons, tracks) for l in t.lessons]
    return "".join(parts)
