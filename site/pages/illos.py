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


PICTURES = {"spine": spine, "pdlc_vs": pdlc_vs, "ladder": ladder, "chain": chain, "methods": methods}
