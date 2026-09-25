"""The pictures worth carrying in your head, drawn in the explainer-illustration grammar.

Each function returns a figure. Links inside a picture are written as if the picture sat at the
site root (``product-manager/#frame``); the page that embeds it rebases them to its own depth
with :func:`bb.rebase`.

    spine()     the four phases, the hard gate and the loop back, compact — the home page's hero
    pdlc_vs()   traditional PDLC against the agentic one, stacked
    ladder()    R1 to R5: gate by risk, never by size
    chain()     why length is the enemy: six steps at 90% are right 53% of the time
    methods()   SDD, BMAD, AI-DLC and AiDD on one spine, as a plug board
"""
from __future__ import annotations

from . import bb

PHASES = [
    ("g", "P0 · Frame", "flag", "product-manager/#frame"),
    ("b", "P1 · Design & Spec", "spec", "solution-architect/#map"),
    ("p", "P2 · Build & Prove", "bolt", "engineering/#floor"),
    ("o", "P3 · Run & Learn", "chart", "qa/#watch"),
]


# --------------------------------------------------------------------------------------- spine
def spine(caption: bool = True) -> str:
    """The method in one compact picture, for the hero: 640 wide, so it sits beside the words."""
    W, H = 640, 396
    m = bb.title(30, 10, [("The agentic PDLC", "b"), ("in one picture",)], fs=17)
    xs = [16, 164, 344, 492]
    nw, nh, ny = 132, 76, 66
    subs = ["worth doing? AI at all?", "spec, bar, authority", "bolts, harness, shadow", "two numbers, drift"]
    leave = ["an AI-fit verdict", "a signed spec", "a lower bound", "the next P0 brief"]
    for i, ((hue, name, ic, href), x) in enumerate(zip(PHASES, xs)):
        m += bb.node(x, ny, nw, nh, title_=name, sub=subs[i], icon=ic, hue=hue, fs=12.5, href=href)
        m += bb.num(x + 8, ny - 2, i, hue)
        # "you leave with", one chip per phase, in the phase's hue
        pw, ph, pm = bb.pill(0, 0, leave[i], hue, fs=10.5, r=8, hh=24, fill=bb.NODE, c=bb.INK, stroke=bb.solid(hue))
        cx = x + nw / 2 - pw / 2
        m += bb.pill(cx, ny + nh + 34, leave[i], hue, fs=10.5, r=8, hh=24, fill=bb.NODE, c=bb.INK,
                     stroke=bb.solid(hue))[2]
    cy = ny + nh / 2
    m += bb.flow([(xs[0] + nw + 2, cy), (xs[1] - 3, cy)])
    m += bb.flow([(xs[1] + nw + 2, cy), (318, cy)]) + bb.gate(322, ny - 10, nh + 20) + bb.flow([(326, cy), (xs[2] - 3, cy)])
    m += bb.text(322, ny + nh + 24, "hard gate", a="middle", fs=10.5, b=True, c=bb.dark("k"))
    m += bb.flow([(xs[2] + nw + 2, cy), (xs[3] - 3, cy)])
    # "leaves with" arrows, phase to chip
    for x in xs:
        m += bb.flow([(x + nw / 2, ny + nh + 2), (x + nw / 2, ny + nh + 30)], sw=1.6, c=bb.INK2)
    # the loop back: production is where the next frame comes from
    ly = ny + nh + 58
    m += bb.flow([(xs[3] + nw / 2, ly + 2), (xs[3] + nw / 2, ly + 30), (xs[0] + nw / 2, ly + 30), (xs[0] + nw / 2, ly + 4)],
                 c=bb.dark("o"), label="the incident is the next brief", ly=-9)
    m += bb.callout(16, 262, 300, "One hard gate. The spec, the bar and the guardrails are signed before anyone builds.", "k", h=58)
    m += bb.callout(332, 262, 292, "Production is where the next frame comes from: an incident, a drift, a bill.", "o", h=58)
    m += bb.text(16, 348, "Every role page walks these four phases from its own chair: what you do, what a model", fs=11, c=bb.INK2, w=500)
    m += bb.text(16, 363, "drafts, what you check, and the one thing that is never delegated.", fs=11, c=bb.INK2, w=500)
    m += bb.text(16, 386, "Click a phase to open it.", fs=10.5, c=bb.INK2, w=600)
    cap = ("<b>The spine.</b> Four phases, one hard gate between P1 and P2, and a line that comes back from "
           "production to the next frame.") if caption else ""
    return bb.svg(W, H, m, "The agentic PDLC: P0 Frame, P1 Design and Spec, a hard gate, P2 Build and Prove, "
                  "P3 Run and Learn, and a loop from production back to the next frame", caption=cap)


# ------------------------------------------------------------------------------------- pdlc_vs
def pdlc_vs() -> str:
    W, H = 1180, 606
    m = bb.title(34, 12, [("Traditional PDLC", "g"), ("vs",), ("Agentic PDLC", "b")])
    # panel A
    m += bb.panel(20, 70, 1140, 208, "g") + bb.label_col(32, 82, 150, 184, "g", name="Traditional",
                                                            sub="one decision per stage, then build", icon="clipboard")
    A = [("Discovery", "search", "interviews, adjectives"), ("PRD", "doc", "thirty pages, approved"),
         ("Design", "gear", "architecture, once"), ("Build", "code", "two-week sprints"),
         ("Test", "check", "acceptance, at the end"), ("Release", "flag", "then a metric")]
    for i, (t, ic, sub) in enumerate(A):
        x = 205 + i * 156
        m += bb.node(x, 100, 132, 58, title_=t, sub=sub, icon=ic, hue="g", fs=13)
        if i < len(A) - 1:
            m += bb.flow([(x + 134, 129), (x + 154, 129)], sw=1.8)
    m += bb.callout(205, 178, 560, "Every decision is made once, by a person, before the build starts. "
                    "Quality is a demo and a checklist, and both come at the end.", "g", h=62)
    m += bb.callout(785, 178, 362, "Breaks when the product contains something that decides: nobody wrote how "
                    "right it must be, or what it may do alone.", "o", h=62)
    # panel B
    m += bb.panel(20, 296, 1140, 298, "b") + bb.label_col(32, 308, 150, 274, "b", name="Agentic PDLC",
                                                            sub="four phases, one hard gate, one loop back", icon="loop")
    B = [("P0 · Frame", "flag", "the pain in cases, minutes and money", "product-manager/#frame", 205),
         ("P1 · Design & Spec", "spec", "eight fields, a bar per slice", "solution-architect/#map", 412),
         ("P2 · Build & Prove", "bolt", "bolts, a harness in CI, the shadow run", "engineering/#floor", 666),
         ("P3 · Run & Learn", "chart", "two numbers, drift, the incident", "qa/#watch", 873)]
    for i, (t, ic, sub, href, x) in enumerate(B):
        m += bb.node(x, 336, 176, 74, title_=t, sub=sub, icon=ic, hue="b", fs=13.5, href=href) + bb.num(x + 10, 332, i, "b")
        if i in (0, 2):
            m += bb.flow([(x + 178, 373), (B[i + 1][4] - 3, 373)])
    m += bb.flow([(590, 373), (612, 373)]) + bb.gate(632, 326, 94) + bb.flow([(652, 373), (663, 373)])
    m += bb.text(632, 436, "hard gate", a="middle", fs=10.5, b=True, c=bb.dark("k"))
    m += bb.flow([(961, 412), (961, 448), (293, 448), (293, 414)], c=bb.dark("b"), label="the incident is the next brief", ly=-9)
    chips = [("pain register", "AI-fit verdict"), ("eight-field spec", "authority budget"),
             ("golden set", "shadow run"), ("two-number report", "drift readout")]
    for i, pair in enumerate(chips):
        x = B[i][4]
        for t in pair:
            pw, _, pm = bb.pill(x, 462, t, "b", fs=10.5, r=7, hh=24, fill=bb.NODE, c=bb.INK, stroke=bb.border("b"))
            m += pm
            x += pw + 6
    m += bb.callout(205, 504, 470, "The hard gate halts P1 until three things are signed: the spec, the bar "
                    "and the guardrails.", "k", h=52)
    m += bb.callout(693, 504, 454, "The other three crossings are soft: they can cross with a placeholder, "
                    "a named owner and a date.", "o", h=52)
    return bb.svg(W, H, m, "Traditional PDLC, six stages decided once, against the agentic PDLC: four phases, "
                  "a hard gate before the build, and the incident feeding the next frame",
                  caption="<b>What changes.</b> A traditional lifecycle decides everything once, before the build. "
                          "The agentic one adds a bar per slice, an authority budget and one hard gate — and "
                          "brings production back to the next frame.")


# -------------------------------------------------------------------------------------- ladder
def ladder() -> str:
    W = 1180
    rows = [
        ("g", "R1 · Reversible draft", "A draft in a sandbox", "nothing real changes", "pen",
         "Review at the end", "the reader owns the outcome", "eye", "Draft the passenger message", "doc"),
        ("t", "R2 · Reversible change", "Real work, undoable", "a change with an undo", "undo",
         "One reader before merge", "a second pair of eyes", "users", "Search flights, rank options", "search"),
        ("o", "R3 · Hard to reverse", "Small blast radius", "one customer, one booking", "warn",
         "Approve first", "a person before the action", "check", "Rebook onto a new flight", "handoff"),
        ("k", "R4 · Money, identity, policy", "Consequential", "the ledger or the law", "money",
         "A named approver, every time", "and a cap in the tool signature", "lock", "Refund, capped at $400", "bill"),
        ("n", "R5 · Irreversible or safety-critical", "Cannot be undone", "or somebody gets hurt", "stop",
         "Not delegated at all", "a person does it", "person", "Change a passenger's identity", "shield"),
    ]
    m = bb.title(34, 12, [("Gate by risk", "k"), ("never by size",)])
    for x, t in ((205, "What it touches"), (555, "The check"), (855, "At SkyWays")):
        m += bb.text(x + 2, 68, t.upper(), fs=10.5, b=True, c=bb.INK2, ls=".08em")
    y0, rh = 82, 72
    for i, (hue, name, a, asub, aic, b, bsub, bic, c, cic) in enumerate(rows):
        y = y0 + i * rh
        m += bb.panel(20, y, 1140, 64, hue, r=14)
        m += f'<rect x="30" y="{y + 7}" width="150" height="50" rx="11" fill="{bb.solid(hue)}"/>'
        m += bb.lines(40, y + 27, bb.wrap(name, 20)[:2], fs=12.5, b=True, c=bb.ON, lh=14)
        m += bb.node(205, y + 8, 330, 48, title_=a, sub=asub, icon=aic, hue=hue, fs=12.5, r=10)
        m += bb.node(555, y + 8, 280, 48, title_=b, sub=bsub, icon=bic, hue=hue, fs=12.5, r=10)
        m += bb.node(855, y + 8, 290, 48, title_=c, icon=cic, hue=hue, fs=12, r=10)
    yb = y0 + 5 * rh + 4
    m += bb.callout(20, yb, 690, "A change inherits the band of whatever it touches: three lines in a refund cap "
                    "are R4; four hundred lines of help text are R1.", "k", h=56)
    m += bb.callout(730, yb, 430, "Size measures typing. Risk measures what a mistake costs and whether it "
                    "can be undone.", "o", h=56)
    H = yb + 56 + 16
    return bb.svg(W, H, m, "The risk ladder: five bands from a reversible draft reviewed at the end to an "
                  "irreversible action that is not delegated at all, each with its check and a SkyWays example",
                  caption="<b>Gate by risk.</b> The band belongs to what the change touches, and the check follows "
                          "the band: from a review at the end to a named approver every time.")


# --------------------------------------------------------------------------------------- chain
def chain() -> str:
    W, H = 1180, 486
    m = bb.title(34, 12, [("6 steps", "b"), ("at",), ("90% each", "o"), ("=",), ("53% end to end", "k")])
    nw, nh, ny = 150, 64, 74
    base = 300
    for i in range(6):
        x = 34 + i * 186
        p = 0.9 ** (i + 1)
        m += bb.node(x, ny, nw, nh, title_=f"Step {i + 1}", sub="right 90% of the time", icon="gear", hue="b", fs=13)
        if i < 5:
            m += bb.flow([(x + nw + 2, ny + nh / 2), (x + 186 - 3, ny + nh / 2)])
        bh = p * 120
        m += (f'<rect x="{x + nw / 2 - 34}" y="{base - bh:.1f}" width="68" height="{bh:.1f}" rx="7" '
              f'fill="{bb.tint("k")}" stroke="{bb.solid("k")}" stroke-width="1.8"/>')
        m += bb.text(x + nw / 2, base - bh - 9, f"{p * 100:.0f}%", a="middle", fs=17, b=True, c=bb.dark("k"))
        m += bb.text(x + nw / 2, base + 17, "end to end", a="middle", fs=10.5, c=bb.INK2, w=500)
        m += bb.flow([(x + nw / 2, ny + nh + 2), (x + nw / 2, base - bh - 24)], sw=1.4, c=bb.INK2, head=False)
    m += f'<line x1="34" y1="{base}" x2="1146" y2="{base}" stroke="{bb.INK2}" stroke-width="1.2" opacity=".6"/>'
    m += bb.callout(34, 352, 520, "Multiply, never average. Four steps each right 90% of the time are right 66% "
                    "of the time end to end, and they fail fluently: no error, a confident wrong answer.", "k", h=72)
    m += bb.listbox(580, 340, 566, "Best defences, in order", [
        "Keep chains short: fewer probabilistic steps per case",
        "Put an independent checker after the steps that are costly and easy to miss",
        "Make exact steps exact code: a calculator behind an agent is a provable step made probabilistic"], "b")
    return bb.svg(W, H, m, "Six chained steps, each right ninety percent of the time, falling to fifty-three "
                  "percent end to end; multiply, never average",
                  caption="<b>Why length is the enemy.</b> Every probabilistic step multiplies. The bars show "
                          "what survives to the end; the list is what to do about it.")


# ------------------------------------------------------------------------------------- methods
METHODS = [
    ("SDD", "b", "doc", "established", "The spec, not the code, is what you maintain; code is regenerated from it.",
     [("pen", "a spec sketch, lightly: the pain and the ceiling"),
      ("spec", "the spec is the artefact: eight fields, stable IDs"),
      ("code", "code generated from the spec, regenerated on change"),
      ("undo", "lightly: the incident edits the spec first")]),
    ("BMAD Method", "k", "users", "documented", "Named AI personas plan like an agile team; sharded story files carry the context.",
     [("users", "the Analyst writes the project brief"),
      ("doc", "PM and Architect: PRD.md and architecture.md"),
      ("spec", "sharded story files, then the Dev and QA loop"), None]),
    ("AI-DLC (AWS)", "o", "bolt", "documented", "Three phases and bolts of hours or days replace sprints; a person approves every boundary.",
     [("flag", "inception: an intent becomes units of work"),
      ("users", "mob elaboration, NFRs captured"),
      ("bolt", "construction in bolts, mob construction"),
      ("gear", "operations, run adaptively")]),
    ("AiDD, the daily craft", "g", "code", "established", "How an engineer works with a coding agent day to day, whichever method frames it.",
     [None, None, ("code", "context files, story files, a harness in CI, review by risk"), None]),
    ("This manual adds", "n", "target", "working method", "The parts none of the methods decide, on the spine where they belong.",
     [("target", "the AI-fit verdict, the autonomy ceiling, the value line"),
      ("gate", "the hard gate: spec, bar, guardrails; the authority budget"),
      ("ladder", "one unknown per bolt, a lower bound not a score, the shadow run"),
      ("chart", "two numbers, drift, the incident as the next P0")]),
]
CONF_HUE = {"documented": "b", "established": "t", "working method": "o"}


def methods() -> str:
    W, H, LX, CW = 1180, 522, 320, 210
    m = bb.title(34, 12, [("Four methods", "p"), ("on one",), ("spine", "b")])

    def row(r, y):
        name, hue, ic, conf, about, ph = r
        out = (f'<rect x="20" y="{y}" width="1140" height="62" rx="12" fill="{bb.tint(hue)}" '
               f'stroke="{bb.border(hue)}" stroke-width="1.6"/>')
        pw, _, pm = bb.pill(30, y + 8, name, hue, fs=12, r=8, hh=24)
        out += pm
        cw, _, cm = bb.pill(30 + pw + 8, y + 10, conf, CONF_HUE[conf], fs=10, r=7, hh=20, fill=bb.tint(CONF_HUE[conf]),
                            c=bb.INK, stroke=bb.border(CONF_HUE[conf]))
        out += cm
        out += bb.lines(30, y + 44, bb.wrap(about, 50)[:2], fs=10.5, c=bb.INK2, w=500, lh=11.5)
        for i, p in enumerate(ph):
            x, w = LX + i * CW + 4, CW - 8
            if not p:
                out += (f'<rect x="{x}" y="{y + 8}" width="{w}" height="46" rx="9" fill="none" '
                        f'stroke="{bb.border(hue)}" stroke-width="1.2" stroke-dasharray="4 4"/>'
                        + bb.text(x + w / 2, y + 35, "silent", a="middle", fs=10.5, c=bb.INK2, w=500))
                continue
            out += (f'<rect x="{x}" y="{y + 8}" width="{w}" height="46" rx="9" fill="{bb.NODE}" '
                    f'stroke="{bb.solid(hue)}" stroke-width="1.8"/>')
            out += bb.icon(p[0], x + 22, y + 16, 26, c=bb.solid(hue), ink=bb.INK, fill=bb.tint(hue))
            L = bb.wrap(p[1], 29)[:3]
            out += bb.lines(x + 42, y + 31 - (len(L) - 1) * 5.5, L, fs=10, b=True, lh=11.5)
        return out

    for k, r in enumerate(METHODS[:2]):
        m += row(r, 64 + k * 70)
    SY = 204
    m += (f'<rect x="20" y="{SY}" width="1140" height="48" rx="24" fill="{bb.solid("n")}"/>'
          + bb.text(40, SY + 29, "Agentic PDLC · the spine", fs=13, b=True, c=bb.ON)
          + f'<path d="M{LX + 10} {SY + 24}H1140" fill="none" stroke="{bb.ON}" stroke-opacity=".45" '
            f'stroke-width="2" stroke-dasharray="7 5" class="bb-flow"/>')
    for i, (hue, name, _ic, _h) in enumerate(PHASES):
        pw, _, _ = bb.pill(0, 0, name, hue, fs=12.5, r=14, hh=28)
        m += bb.pill(LX + i * CW + CW / 2 - pw / 2, SY + 10, name, hue, fs=12.5, r=14, hh=28)[2]
    m += bb.gate(LX + 2 * CW, SY - 6, 60)
    for k, r in enumerate(METHODS[2:]):
        m += row(r, 270 + k * 70)
    m += bb.text(34, 502, "A filled cell is where the method says something about that phase; a dashed cell is where a team "
                 "has to bring its own answer. The last row is where this manual's own devices sit.", fs=11, c=bb.INK2, w=500)
    return bb.svg(W, H, m, "Four methods on one spine: spec-driven development, the BMAD Method, AWS AI-DLC and "
                  "AiDD, each filled where it speaks to a phase and dashed where it is silent, with the "
                  "devices this manual adds",
                  caption="<b>Not competitors.</b> Each method speaks to part of the lifecycle. The decision that "
                          "matters is not which method but how deep to go on this change.")



# --------------------------------------------------------------------------------------- tower
LOOP = "M215 167 H425 A88 88 0 0 1 425 343 H215 A88 88 0 0 1 215 167 Z"   # the runway loop, clockwise

PLANE = ('<path d="M-14 0 H-30" stroke="var(--ink2)" stroke-width="1.2" stroke-dasharray="3 3" opacity=".55"/>'
         '<path d="M-12 0 L-6 -2.6 L7 -2.6 Q12.5 -2.6 12.5 0 Q12.5 2.6 7 2.6 L-6 2.6 Z" fill="var(--paper)" '
         'stroke="var(--ink)" stroke-width="1.4"/>'
         '<path d="M-1 -2.6 L-7 -10 L-3 -10 L3.5 -2.6 Z M-1 2.6 L-7 10 L-3 10 L3.5 2.6 Z M-10 -1.8 L-14 -6 L-12 -6 '
         'L-7.5 -1.8 Z M-10 1.8 L-14 6 L-12 6 L-7.5 1.8 Z" fill="var(--ink)"/>')

# every rule is prefixed: a style element inside an inline SVG applies to the whole document
TOWER_CSS = """
.twr-lane{stroke-dasharray:12 10;animation:twr-march 1.6s linear infinite}
@keyframes twr-march{to{stroke-dashoffset:-22}}
.twr-plane{offset-path:path("%s");offset-rotate:auto;animation:twr-fly 26s linear infinite}
.twr-plane.a{offset-distance:6%%;animation-delay:0s}
.twr-plane.b{offset-distance:31%%;animation-delay:-6.5s}
.twr-plane.c{offset-distance:56%%;animation-delay:-13s}
.twr-plane.d{offset-distance:81%%;animation-delay:-19.5s}
@keyframes twr-fly{from{offset-distance:0%%}to{offset-distance:100%%}}
.twr-radar{transform-box:view-box;transform-origin:320px 229px;animation:twr-spin 9s linear infinite}
@keyframes twr-spin{to{transform:rotate(360deg)}}
.twr-beacon{animation:twr-blink 1.8s ease-in-out infinite}
@keyframes twr-blink{0%%,100%%{opacity:1}50%%{opacity:.25}}
.twr-cloud{animation:twr-drift 40s linear infinite alternate}
@keyframes twr-drift{to{transform:translateX(26px)}}
@media (prefers-reduced-motion:reduce){.twr-lane,.twr-plane,.twr-beacon,.twr-cloud{animation:none}.twr-radar{display:none}}
@supports not (offset-path:path("M0 0h1")){.twr-plane{display:none}}
""" % LOOP


def _twr_label(x: float, y: float, key: str, name: str, hue: str, a: str = "middle") -> str:
    c = f"color-mix(in oklab,var(--dg-{hue}) 72%,var(--ink))"
    return (f'<text x="{x}" y="{y}" text-anchor="{a}" font-family="{bb.FONT}" fill="{c}">'
            f'<tspan font-size="14" font-weight="800">{key}</tspan>'
            f'<tspan font-size="11.5" font-weight="600" dx="5">{name}</tspan></text>')


def tower() -> str:
    """The hook band's scene: the lifecycle flown as a loop, controlled from a tower.

    Motion is direction only: the lane's dashes march, the planes follow the loop, the
    radar sweeps. Reduced motion stops all of it and the planes keep their places; a
    browser without motion paths hides the planes rather than piling them in a corner."""
    sky = ('<defs><linearGradient id="twr-sky" x1="0" y1="0" x2="0" y2="1">'
           '<stop offset="0" style="stop-color:color-mix(in oklab,var(--dg-slate) 26%,var(--paper))"/>'
           '<stop offset="1" style="stop-color:var(--paper)"/></linearGradient></defs>'
           '<rect width="640" height="400" fill="url(#twr-sky)"/>')
    clouds = ('<g class="twr-cloud" fill="var(--paper)" opacity=".85">'
              '<ellipse cx="86" cy="62" rx="34" ry="12"/><ellipse cx="108" cy="54" rx="24" ry="14"/>'
              '<ellipse cx="548" cy="88" rx="30" ry="11"/><ellipse cx="566" cy="80" rx="20" ry="12"/></g>')
    lane = f'<path d="{LOOP}" fill="none" stroke="var(--rule2)" stroke-width="18" stroke-linejoin="round"/>'

    def seg(d: str, hue: str) -> str:
        return (f'<path d="{d}" fill="none" stroke="color-mix(in oklab,var(--dg-{hue}) 58%,var(--paper))" '
                f'stroke-width="18"/>')
    segs = (seg("M215 167 H425", "slate") + seg("M425 167 A88 88 0 0 1 425 343", "indigo")
            + seg("M425 343 H215", "teal") + seg("M215 343 A88 88 0 0 1 215 167", "amber"))
    centre = f'<path class="twr-lane" d="{LOOP}" fill="none" stroke="var(--paper)" stroke-width="2"/>'
    # the one hard gate, where P1 hands to P2
    gate = ('<g transform="translate(425 343)">'
            '<rect x="-13" y="-16" width="26" height="32" rx="7" fill="var(--dg-teal)"/>'
            '<rect x="-6.5" y="-2" width="13" height="10" rx="2" fill="none" stroke="var(--dg-on)" stroke-width="1.8"/>'
            '<path d="M-3.5 -2V-5.5a3.5 3.5 0 0 1 7 0V-2" fill="none" stroke="var(--dg-on)" stroke-width="1.8" '
            'stroke-linecap="round"/></g>'
            + bb.text(446, 371, "hard gate", fs=11, b=True, c="color-mix(in oklab,var(--dg-teal) 78%,var(--ink))"))
    ret = bb.text(196, 151, "production feeds the next frame", fs=10.5, w=600, c="var(--ink2)", a="end")
    labels = (_twr_label(320, 151, "P0", "Frame", "slate")
              + _twr_label(528, 250, "P1", "Design &amp; Spec", "indigo", a="start")
              + _twr_label(320, 383, "P2", "Build &amp; Prove", "teal")
              + _twr_label(112, 250, "P3", "Run &amp; Learn", "amber", a="end"))
    radar = ('<path class="twr-radar" d="M320 229 L320 99 A130 130 0 0 1 385 116 Z" fill="var(--dg-slate)" '
             'opacity=".16"/>')
    tower_ = ('<g><path d="M306 246 H334 L331 322 H309 Z" fill="var(--ink2)"/>'
              '<rect x="294" y="318" width="52" height="9" rx="3" fill="var(--ink)"/>'
              '<rect x="282" y="212" width="76" height="36" rx="9" fill="var(--ink)"/>'
              '<rect x="289" y="220" width="62" height="13" rx="3" fill="var(--paper)" opacity=".92"/>'
              '<path d="M304 220v13M320 220v13M336 220v13" stroke="var(--ink)" stroke-width="1.6"/>'
              '<path d="M320 212V194" stroke="var(--ink)" stroke-width="2"/>'
              '<circle class="twr-beacon" cx="320" cy="192" r="3.5" fill="var(--dg-rose)"/></g>'
              + bb.text(296, 296, "control:", fs=10, w=700, c="var(--ink2)", a="end")
              + bb.text(296, 310, "gates, loops, the sponsor", fs=10, w=600, c="var(--ink2)", a="end"))
    planes = "".join(f'<g class="twr-plane {k}">{PLANE}</g>' for k in "abcd")
    inner = sky + clouds + radar + lane + segs + centre + gate + ret + labels + tower_ + planes
    return ('<svg class="twr" viewBox="0 0 640 400" role="img" aria-label="Four planes fly a loop of four runway '
            'segments, P0 Frame, P1 Design and Spec, P2 Build and Prove and P3 Run and Learn, past one hard gate, '
            f'under a control tower with a radar sweep"><style>{TOWER_CSS}</style>{inner}</svg>')


_METHOD_HUES = [('SDD', 'b'), ('BMAD', 'k'), ('AI-DLC', 'o'), ('AiDD', 'g')]   # (short name, hue) as METHODS names them


# --------------------------------------------------------------------------------------- merge
def merge() -> str:
    """How the four methods merge into the SkyWays PDLC: each part lands in the phase it serves.

    Four phase columns hold the parts each phase takes, every part in its method's hue with the
    method named under it; the columns flow into the spine; the row beneath is what the SkyWays
    PDLC adds and none of the methods carries."""
    W, H, CW, GAP = 1180, 486, 270, 20
    hue_of = {}
    for name, hue in [(n, h) for n, h in _METHOD_HUES]:
        hue_of[name] = hue
    PARTS = {
        0: [("The brief and the PRD", "BMAD", "analyst and PM personas"),
            ("Depth judged per change", "AI-DLC", "adaptive: only the stages this change needs"),
            ("Intent written before code", "SDD", "the spec starts here, lightly")],
        1: [("The spec is what you maintain", "SDD", "code is generated from it"),
            ("Architecture and stories", "BMAD", "the architect persona's artefacts"),
            ("Only the stages that are needed", "AI-DLC", "the architect judges depth")],
        2: [("Code regenerated from the spec", "SDD", "on every change, not patched"),
            ("Dev and QA personas, story by story", "BMAD", "each hands a versioned artefact on"),
            ("Context files and editor agents", "AiDD", "the day-to-day craft"),
            ("Review by risk, cost habits", "AiDD", "who signs, what it costs")],
        3: [("Operate, then re-enter at depth", "AI-DLC", "the next change picks its own stages"),
            ("Cache, route, trace", "AiDD", "cost habits that survive launch"),
            ("The spec learns from production", "SDD", "updated, then regenerated")],
    }
    ADDS = ["The autonomy ceiling, decided before anything is built",
            "A bar per slice and an authority budget, signed at the hard gate",
            "Prove the bar first: a lower bound, never a score, before traffic",
            "The two-number report that starts the next P0"]
    m = bb.title(34, 12, [("Four methods", "p"), ("merge into",), ("one loop", "n")])
    # legend: one hue per method, top right
    lx = W - 20
    for name, hue in reversed(_METHOD_HUES):
        pw, _, pm = bb.pill(0, 0, name, hue, fs=11, r=9, hh=24)
        lx -= pw
        m += bb.pill(lx, 14, name, hue, fs=11, r=9, hh=24)[2]
        lx -= 8
    TY = 56
    for i, (phue, pname, _ic, _href) in enumerate(PHASES):
        x = 20 + i * (CW + GAP)
        parts = PARTS[i]
        ph = 14 + max(len(v) for v in PARTS.values()) * 52   # parallel slots: every column ends on the same row
        m += bb.panel(x, TY, CW, ph, phue, r=14)
        for k, (title_, meth, sub) in enumerate(parts):
            m += bb.node(x + 10, TY + 10 + k * 52, CW - 20, 44, title_=title_, sub=f"{meth} · {sub}",
                         hue=hue_of[meth], fs=11.5)
        cx = x + CW / 2
        m += bb.flow([(cx, TY + ph + 2), (cx, 314)], sw=2)
    SY = 318
    m += (f'<rect x="20" y="{SY}" width="{W - 40}" height="48" rx="24" fill="{bb.solid("n")}"/>'
          + f'<path d="M40 {SY + 24}H{W - 40}" fill="none" stroke="{bb.ON}" stroke-opacity=".45" '
            f'stroke-width="2" stroke-dasharray="7 5" class="bb-flow"/>')
    for i, (phue, pname, _ic, _href) in enumerate(PHASES):
        x = 20 + i * (CW + GAP)
        pw, _, _ = bb.pill(0, 0, pname, phue, fs=12.5, r=14, hh=28)
        m += bb.pill(x + CW / 2 - pw / 2, SY + 10, pname, phue, fs=12.5, r=14, hh=28)[2]
    m += bb.gate(20 + 2 * (CW + GAP) - GAP / 2, SY - 8, 64)
    m += bb.text(20 + 2 * (CW + GAP) - GAP / 2, SY + 74, "hard gate", a="middle", fs=10.5, b=True, c=bb.dark("k"))
    AY = 392
    for i, txt in enumerate(ADDS):
        x = 20 + i * (CW + GAP)
        m += bb.callout(x, AY, CW, txt, "n", h=54, fs=11)
    m += bb.text(20, AY - 8, "What the SkyWays PDLC adds, and none of the four carries", fs=11, b=True, c=bb.dark("n"))
    m += bb.text(34, 474, "One order, one owner per phase, one hard gate. The parts keep their names; the spine keeps them honest.",
                 fs=11.5, w=600, c=bb.INK2)
    return bb.svg(W, H, m, "How the four methods merge into the SkyWays PDLC: the parts of spec-driven development, "
                  "the BMAD Method, AI-DLC and AiDD placed in the phase each serves, flowing into the four-phase "
                  "spine with its hard gate, and the row of devices the SkyWays PDLC adds",
                  caption="<b>Merged, not stacked.</b> Each method keeps the part it does best; the spine gives the "
                          "parts one order, one owner per phase and one hard gate.")


PICTURES = {"spine": spine, "pdlc_vs": pdlc_vs, "ladder": ladder, "chain": chain, "methods": methods,
            "merge": merge}
