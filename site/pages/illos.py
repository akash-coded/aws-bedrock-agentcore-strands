"""The pictures worth carrying in your head, drawn in the explainer-illustration grammar.

Each function returns a figure. Links inside a picture are written as if the picture sat at the
site root (``product-manager/#frame``); the page that embeds it rebases them to its own depth
with :func:`bb.rebase`.

    spine()     the four phases, the sign-off and the loop back, in one compact picture
    pdlc_vs()   traditional PDLC against the agentic one, stacked
    ladder()    R1 to R5: gate by risk, never by size
    chain()     why length is the enemy: six steps at 90% are right 53% of the time
    methods()   SDD, BMAD, AI-DLC and AIDD on the four phases, as a plug board
    merge()     the parts of the four methods, in the phase each one serves
    tower()     the lifecycle flown as a loop, for the head of the method page

Hue means phase in every one of them: P0 slate, P1 indigo, P2 teal, P3 amber, the sign-off rose.
A method, a role or a risk band never borrows a phase's hue in a picture that also shows phases.
Every drawing carries the same content as wrapping HTML for a narrow column (see ``bb.svg``).
"""
from __future__ import annotations

from . import bb
from .bb import INK, INK2, MIN, NODE, ON

PHASES = [
    ("g", "P0 · Frame", "flag", "product-manager/#frame"),
    ("b", "P1 · Design & Spec", "spec", "solution-architect/#map"),
    ("p", "P2 · Build & Prove", "bolt", "engineering/#floor"),
    ("o", "P3 · Run & Learn", "chart", "qa/#watch"),
]
LH = 17


def _chip(cx: float, y: float, s: str, hue: str) -> str:
    """A small outlined chip, centred on ``cx``."""
    pw = bb.width(s, MIN)
    return bb.pill(cx - pw / 2, y, s, hue, fs=MIN, r=8, hh=26, fill=NODE, c=INK, stroke=bb.solid(hue))[2]


# --------------------------------------------------------------------------------------- spine
def spine(caption: bool = True) -> str:
    """The lifecycle in one compact picture: four phases, what you leave each with, the sign-off,
    and the line that comes back from production."""
    W, PX, PW, GAP, GW = 880, 24, 832, 32, 30
    title = [("The agentic PDLC", "n"), ("in one picture",)]
    m, y = bb.title(PX + 2, 14, title, maxw=PW - 4)
    subs = ["worth doing? AI at all?", "spec, bar, authority", "bolts, harness, shadow", "two numbers, drift"]
    leave = ["an AI-fit verdict", "a signed spec", "a lower bound", "the next P0 brief"]
    nw = (PW - 3 * GAP - GW) / 4
    xs = [PX, PX + nw + GAP, PX + 2 * nw + 2 * GAP + GW, PX + 3 * nw + 3 * GAP + GW]
    ny = y + 46
    nh = max(bb.node_h(nw, name, subs[i], ic) for i, (_h, name, ic, _u) in enumerate(PHASES))
    cy = ny + nh / 2
    fol = []
    for i, ((hue, name, ic, href), x) in enumerate(zip(PHASES, xs)):
        m += bb.node(x, ny, nw, nh, title_=name, sub=subs[i], icon=ic, hue=hue, href=href)
        # what you leave the phase with, one chip each, in the phase's hue
        m += bb.flow([(x + nw / 2, ny + nh + 3), (x + nw / 2, ny + nh + 27)], sw=1.6, c=INK2)
        m += _chip(x + nw / 2, ny + nh + 30, leave[i], hue)
        fol.append(bb.h_cell(name, subs[i], ic, hue, href=href))
        if i < 3:
            fol.append(bb.h_gate(f"{bb.SIGN_OFF}: you leave with {leave[i]}", el="li") if i == 1
                       else bb.h_arrow(f"you leave with {leave[i]}", el="li"))
    gx = xs[1] + nw + (GAP + GW) / 2
    m += bb.flow([(xs[0] + nw + 2, cy), (xs[1] - 3, cy)])
    m += bb.flow([(xs[1] + nw + 2, cy), (gx - 7, cy)]) + bb.gate(gx, ny - 12, nh + 24) + bb.flow([(gx + 7, cy), (xs[2] - 3, cy)])
    m += bb.text(gx, ny - 20, bb.SIGN_OFF, a="middle", fs=MIN, b=True, c=bb.dark("k"))
    m += bb.flow([(xs[2] + nw + 2, cy), (xs[3] - 3, cy)])
    # the line that comes back: production is where the next frame comes from
    ly = ny + nh + 56
    back = "the incident is the next brief"
    m += bb.flow([(xs[3] + nw / 2, ly + 3), (xs[3] + nw / 2, ly + 28), (xs[0] + nw / 2, ly + 28), (xs[0] + nw / 2, ly + 5)],
                 c=bb.dark("o"), label=back)
    fol.append(f'<li class="bbn-e" style="--c:var(--bb-o)"><b>{back}</b><small>back to P0 · Frame</small></li>')
    c1 = "One sign-off. The spec, the bar and the guardrails are signed before anyone builds."
    c2 = "Production is where the next frame comes from: an incident, a drift, a bill."
    cw = (PW - 20) / 2
    cyy = ly + 52
    ch = max(bb.callout_h(cw, c1), bb.callout_h(cw, c2))
    m += bb.callout(PX, cyy, cw, c1, "k", h=ch) + bb.callout(PX + cw + 20, cyy, cw, c2, "o", h=ch)
    html = (bb.h_title(title) + f'<ol class="bbn-f">{"".join(fol)}</ol>' + bb.h_call(c1, "k") + bb.h_call(c2, "o"))
    cap = ("<b>One loop.</b> Four phases, one sign-off between P1 and P2 (the lessons call it the hard gate), "
           "and a line that comes back from production to the next frame.") if caption else ""
    return bb.svg(W, cyy + ch + 14, m, "The agentic PDLC: P0 Frame, P1 Design and Spec, the sign-off, P2 Build and "
                  "Prove, P3 Run and Learn, and a loop from production back to the next frame", caption=cap, narrow=html)


# ------------------------------------------------------------------------------------- pdlc_vs
def pdlc_vs() -> str:
    W, PX, PW, LC = 1100, 20, 1060, 150
    title = [("Traditional PDLC", "s"), ("vs",), ("Agentic PDLC", "n")]
    m, y = bb.title(PX + 14, 14, title, maxw=PW - 28)
    IX = PX + 12 + LC + 16            # where a panel's content begins
    IW = PX + PW - 12 - IX
    # panel A: six stages, decided once
    A = [("Discovery", "interviews, adjectives"), ("PRD", "thirty pages, approved"),
         ("Design", "architecture, once"), ("Build", "two-week sprints"),
         ("Test", "acceptance, at the end"), ("Release", "then a metric")]
    a1 = ("Every decision is made once, by a person, before the build starts. Quality is a demo and a "
          "checklist, and both come at the end.")
    a2 = ("Breaks when the product contains something that decides: nobody wrote how right it must be, or "
          "what it may do alone.")
    ay = y + 18
    g = 18
    nw = (IW - 5 * g) / 6
    nh = max(bb.node_h(nw, t, sub) for t, sub in A)
    cw1 = IW * 0.56
    cw2 = IW - cw1 - 16
    ch = max(bb.callout_h(cw1, a1), bb.callout_h(cw2, a2))
    ah = 14 + nh + 14 + ch + 14
    m += bb.panel(PX, ay, PW, ah, "s") + bb.label_col(PX + 12, ay + 12, LC, ah - 24, "s", name="Traditional",
                                                       sub="one decision per stage, then build")
    for i, (t, sub) in enumerate(A):
        x = IX + i * (nw + g)
        m += bb.node(x, ay + 14, nw, nh, title_=t, sub=sub, hue="s")
        if i < len(A) - 1:
            m += bb.flow([(x + nw + 2, ay + 14 + nh / 2), (x + nw + g - 3, ay + 14 + nh / 2)], sw=1.8)
    m += bb.callout(IX, ay + 28 + nh, cw1, a1, "s", h=ch) + bb.callout(IX + cw1 + 16, ay + 28 + nh, cw2, a2, "o", h=ch)
    # panel B: four phases, one sign-off, one loop back
    B = [("the pain in cases, minutes and money", ("pain register", "AI-fit verdict")),
         ("eight fields, a bar per slice", ("eight-field spec", "authority budget")),
         ("bolts, a harness in CI, the shadow run", ("golden set", "shadow run")),
         ("two numbers, drift, the incident", ("two-number report", "drift readout"))]
    b1 = "The sign-off halts P1 until three things are signed: the spec, the bar and the guardrails."
    b2 = "The other three crossings are soft: they can cross with a placeholder, a named owner and a date."
    by = ay + ah + 18
    GAP, GW = 30, 30
    pw_ = (IW - 3 * GAP - GW) / 4
    xs = [IX, IX + pw_ + GAP, IX + 2 * pw_ + 2 * GAP + GW, IX + 3 * pw_ + 3 * GAP + GW]
    ph = max(bb.node_h(pw_, name, B[i][0], ic, 15) for i, (_h, name, ic, _u) in enumerate(PHASES))
    ny = by + 14 + 26                  # room above the row for the sign-off's name
    cyy = ny + ph / 2
    chips_y = ny + ph + 46
    cwb = (IW - 16) / 2
    chb = max(bb.callout_h(cwb, b1), bb.callout_h(cwb, b2))
    bh = (chips_y + 2 * 32 + 10 + chb + 14) - by
    m += bb.panel(PX, by, PW, bh, "n") + bb.label_col(PX + 12, by + 12, LC, bh - 24, "n", name="Agentic PDLC",
                                                       sub="four phases, one sign-off, one loop back")
    cells = []
    for i, ((hue, name, ic, href), x) in enumerate(zip(PHASES, xs)):
        m += bb.node(x, ny, pw_, ph, title_=name, sub=B[i][0], icon=ic, hue=hue, fs=15, href=href)
        for k, t in enumerate(B[i][1]):
            m += bb.pill(x, chips_y + k * 32, t, hue, fs=MIN, r=7, hh=26, fill=NODE, c=INK, stroke=bb.border(hue))[2]
        cells.append(bb.h_cell(name, f"{B[i][0]} · {B[i][1][0]}, {B[i][1][1]}", ic, hue, href=href))
        if i == 1:
            cells.append(bb.h_gate(el="li"))
    gx = xs[1] + pw_ + (GAP + GW) / 2
    m += bb.flow([(xs[0] + pw_ + 2, cyy), (xs[1] - 3, cyy)])
    m += bb.flow([(xs[1] + pw_ + 2, cyy), (gx - 7, cyy)]) + bb.gate(gx, ny - 12, ph + 24) + bb.flow([(gx + 7, cyy), (xs[2] - 3, cyy)])
    m += bb.text(gx, ny - 20, bb.SIGN_OFF, a="middle", fs=MIN, b=True, c=bb.dark("k"))
    m += bb.flow([(xs[2] + pw_ + 2, cyy), (xs[3] - 3, cyy)])
    back = "the incident is the next brief"
    m += bb.flow([(xs[3] + pw_ / 2, ny + ph + 3), (xs[3] + pw_ / 2, ny + ph + 24), (xs[0] + pw_ / 2, ny + ph + 24),
                  (xs[0] + pw_ / 2, ny + ph + 5)], c=bb.dark("o"), label=back)
    cells.append(f'<li class="bbn-e" style="--c:var(--bb-o)"><b>{back}</b><small>back to P0 · Frame</small></li>')
    m += bb.callout(IX, chips_y + 2 * 32 + 10, cwb, b1, "k", h=chb) + bb.callout(IX + cwb + 16, chips_y + 2 * 32 + 10, cwb, b2, "o", h=chb)
    html = (bb.h_title(title)
            + bb.h_block("s", "Traditional", "".join(bb.h_cell(t, sub, hue="s", n=i + 1) for i, (t, sub) in enumerate(A)),
                         sub="one decision per stage, then build",
                         foot=f'<div class="bbn-in">{bb.h_call(a1, "s")}{bb.h_call(a2, "o")}</div>')
            + bb.h_block("n", "Agentic PDLC", "".join(cells), sub="four phases, one sign-off, one loop back", one=True,
                         foot=f'<div class="bbn-in">{bb.h_call(b1, "k")}{bb.h_call(b2, "o")}</div>'))
    return bb.svg(W, by + bh + 14, m, "Traditional PDLC, six stages decided once, against the agentic PDLC: four phases, "
                  "a sign-off before the build, and the incident feeding the next frame", cls="bbw-w", narrow=html,
                  caption="<b>What changes.</b> A traditional lifecycle decides everything once, before the build. "
                          "The agentic one adds a bar per slice, an authority budget and one sign-off (the hard gate), "
                          "and brings production back to the next frame.")


# -------------------------------------------------------------------------------------- ladder
def ladder() -> str:
    W, PX, PW = 1100, 20, 1060
    # a ramp of risk, none of it a phase: grey, sky, amber, rose, ink
    rows = [
        ("s", "R1 · Reversible draft", "A draft in a sandbox", "nothing real changes", "pen",
         "Review at the end", "the reader owns the outcome", "eye", "Draft the passenger message", "doc"),
        ("u", "R2 · Reversible change", "Real work, undoable", "a change with an undo", "undo",
         "One reader before merge", "a second pair of eyes", "users", "Search flights, rank options", "search"),
        ("o", "R3 · Hard to reverse", "Small blast radius", "one customer, one booking", "warn",
         "Approve first", "a person before the action", "check", "Rebook onto a new flight", "handoff"),
        ("k", "R4 · Money, identity, policy", "Consequential", "the ledger or the law", "money",
         "A named approver, every time", "and a cap in the tool signature", "lock", "Refund, capped at $400", "bill"),
        ("n", "R5 · Irreversible or safety-critical", "Cannot be undone", "or somebody gets hurt", "stop",
         "Not delegated at all", "a person does it", "person", "Change a passenger's identity", "shield"),
    ]
    title = [("Gate by risk", "k"), ("never by size",)]
    heads = ("What it touches", "The check", "At the airline")
    m, y = bb.title(PX + 14, 14, title, maxw=PW - 28)
    LX, LW = PX + 10, 178
    cols = [(LX + LW + 14, 292), (LX + LW + 14 + 292 + 12, 268), (LX + LW + 14 + 292 + 12 + 268 + 12, 0)]
    cols[2] = (cols[2][0], PX + PW - 10 - cols[2][0])
    y += 30
    for (x, _w), t in zip(cols, heads):
        m += bb.text(x + 2, y, t, fs=MIN, b=True, c=INK2)
    y += 12
    html = bb.h_title(title)
    for hue, name, a, asub, aic, b, bsub, bic, c, cic in rows:
        nl = bb.fit(name, LW - 24, 14.5, 700)
        rh = max(bb.node_h(cols[0][1], a, asub, aic), bb.node_h(cols[1][1], b, bsub, bic),
                 bb.node_h(cols[2][1], c, "", cic), len(nl) * 18 + 16)
        m += bb.panel(PX, y, PW, rh + 16, hue, r=14)
        m += f'<rect x="{LX}" y="{y + 8}" width="{LW}" height="{rh}" rx="11" fill="{bb.solid(hue)}"/>'
        m += bb.lines(LX + 12, y + 8 + (rh - len(nl) * 18) / 2 + 13.5, nl, fs=14.5, b=True, c=ON, lh=18)
        m += bb.node(cols[0][0], y + 8, cols[0][1], rh, title_=a, sub=asub, icon=aic, hue=hue, r=10)
        m += bb.node(cols[1][0], y + 8, cols[1][1], rh, title_=b, sub=bsub, icon=bic, hue=hue, r=10)
        m += bb.node(cols[2][0], y + 8, cols[2][1], rh, title_=c, icon=cic, hue=hue, r=10)
        html += bb.h_block(hue, name, bb.h_cell(a, asub, aic, hue, via=heads[0]) + bb.h_cell(b, bsub, bic, hue, via=heads[1])
                           + bb.h_cell(c, "", cic, hue, via=heads[2]))
        y += rh + 16 + 8
    c1 = ("A change inherits the band of whatever it touches: three lines in a refund cap are R4; four hundred "
          "lines of help text are R1.")
    c2 = "Size measures typing. Risk measures what a mistake costs and whether it can be undone."
    w1 = PW * 0.6
    w2 = PW - w1 - 20
    ch = max(bb.callout_h(w1, c1), bb.callout_h(w2, c2))
    m += bb.callout(PX, y + 6, w1, c1, "k", h=ch) + bb.callout(PX + w1 + 20, y + 6, w2, c2, "o", h=ch)
    html += bb.h_call(c1, "k") + bb.h_call(c2, "o")
    return bb.svg(W, y + 6 + ch + 14, m, "The risk ladder: five bands from a reversible draft reviewed at the end to an "
                  "irreversible action that is not delegated at all, each with its check and an example from the airline",
                  cls="bbw-w", narrow=html,
                  caption="<b>Gate by risk.</b> The band belongs to what the change touches, and the check follows "
                          "the band: from a review at the end to a named approver every time.")


# --------------------------------------------------------------------------------------- chain
def chain() -> str:
    W, PX, PW = 1100, 20, 1060
    title = [("6 steps", "s"), ("at",), ("90% each", "s"), ("=",), ("53% end to end", "k")]
    m, y = bb.title(PX + 14, 14, title, maxw=PW - 28)
    g = 22
    nw = (PW - 5 * g) / 6
    ny = y + 20
    nh = bb.node_h(nw, "Step 1", "right 90% of the time", "gear")
    base = ny + nh + 44 + 126
    fol = []
    for i in range(6):
        x = PX + i * (nw + g)
        p = 0.9 ** (i + 1)
        m += bb.node(x, ny, nw, nh, title_=f"Step {i + 1}", sub="right 90% of the time", icon="gear", hue="s")
        if i < 5:
            m += bb.flow([(x + nw + 2, ny + nh / 2), (x + nw + g - 3, ny + nh / 2)])
        bh = p * 120
        m += (f'<rect x="{x + nw / 2 - 36:.1f}" y="{base - bh:.1f}" width="72" height="{bh:.1f}" rx="7" '
              f'fill="{bb.tint("k")}" stroke="{bb.solid("k")}" stroke-width="1.8"/>')
        m += bb.text(x + nw / 2, base - bh - 9, f"{p * 100:.0f}%", a="middle", fs=18, b=True, c=bb.dark("k"))
        m += bb.text(x + nw / 2, base + 20, "end to end", a="middle", fs=MIN, c=INK2, w=500)
        m += bb.flow([(x + nw / 2, ny + nh + 3), (x + nw / 2, base - bh - 30)], sw=1.4, c=INK2, head=False)
        fol.append(bb.h_cell(f"Step {i + 1}: right 90% of the time", f"{p * 100:.0f}% right end to end", hue="k" if i == 5 else "s", n=i + 1))
    m += f'<line x1="{PX}" y1="{base}" x2="{PX + PW}" y2="{base}" stroke="{INK2}" stroke-width="1.2" opacity=".6"/>'
    c1 = ("Multiply, never average. Four steps each right 90% of the time are right 66% of the time end to end, "
          "and they fail fluently: no error, a confident wrong answer.")
    best = ("Best defences, in order", [
        "Keep chains short: fewer probabilistic steps per case",
        "Put an independent checker after the steps that are costly and easy to miss",
        "Make exact steps exact code: a calculator behind an agent is a provable step made probabilistic"], "s")
    fy = base + 44
    cw = 440
    lw = PW - cw - 20
    h = max(bb.callout_h(cw, c1) + 12, bb.listbox_h(lw, best[1]))
    m += bb.callout(PX, fy + 12, cw, c1, "k", h=h - 12) + bb.listbox(PX + cw + 20, fy, lw, best[0], best[1], best[2], h=h)
    html = bb.h_title(title) + f'<ol class="bbn-f">{"".join(fol)}</ol>' + bb.h_call(c1, "k") + bb.h_list(*best)
    return bb.svg(W, fy + h + 14, m, "Six chained steps, each right ninety percent of the time, falling to fifty-three "
                  "percent end to end; multiply, never average", cls="bbw-w", narrow=html,
                  caption="<b>Why length is the enemy.</b> Every probabilistic step multiplies. The bars show "
                          "what survives to the end; the list is what to do about it.")


# ------------------------------------------------------------------------------------- methods
# (name, icon, how sure, what it is, what it says in each phase; None where it is silent)
METHODS = [
    ("SDD", "doc", "established", "The spec, not the code, is what you maintain; code is regenerated from it.",
     [("pen", "a spec sketch, lightly: the pain and the ceiling"),
      ("spec", "the spec is the artefact: eight fields, stable IDs"),
      ("code", "code generated from the spec, regenerated on change"),
      ("undo", "lightly: the incident edits the spec first")]),
    ("BMAD Method", "users", "documented", "Named AI personas plan like an agile team; sharded story files carry the context.",
     [("users", "the Analyst writes the project brief"),
      ("doc", "PM and Architect: PRD.md and architecture.md"),
      ("spec", "sharded story files, then the Dev and QA loop"),
      ("loop", "extended here: learn and adjust, into the next brief")]),
    ("AI-DLC (AWS)", "bolt", "documented", "Three phases and bolts of hours or days replace sprints; a person approves every boundary.",
     [("flag", "inception: an intent becomes units of work"),
      ("users", "mob elaboration, NFRs captured"),
      ("bolt", "construction in bolts, mob construction"),
      ("gear", "operations, run adaptively")]),
    ("AIDD, the daily craft", "code", "established", "How an engineer works with a coding agent day to day, whichever method frames it.",
     [None, None, ("code", "context files, story files, a harness in CI, review by risk"), None]),
    ("This manual adds", "target", "working method", "The parts none of the methods decide, in the phase where each belongs.",
     [("target", "the AI-fit verdict, the autonomy ceiling, the value line"),
      ("gate", "what the sign-off needs: spec, bar, guardrails, and the authority budget"),
      ("ladder", "one unknown per bolt, a lower bound not a score, the shadow run"),
      ("chart", "two numbers, drift, the incident as the next P0")]),
]


def _plug(x: float, y: float, w: float, h: float, icon: str, s: str, hue: str) -> str:
    """A filled cell of the plug board: an icon and a sentence, in the phase's hue."""
    ls = bb.fit(s, w - 52, MIN, 600)
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" fill="{NODE}" '
            f'stroke="{bb.solid(hue)}" stroke-width="1.8"/>'
            + bb.icon(icon, x + 24, y + h / 2 - 13, 26, c=bb.solid(hue), ink=INK, fill=bb.tint(hue))
            + bb.lines(x + 44, y + (h - len(ls) * LH) / 2 + 12.5, ls, fs=MIN, w=600, lh=LH))


def _plug_h(w: float, s: str) -> float:
    return max(46, len(bb.fit(s, w - 52, MIN, 600)) * LH + 18)


def methods() -> str:
    W, PX, PW, LW, G = 1100, 20, 1060, 300, 8
    title = [("Four methods", "s"), ("on",), ("the four phases", "n")]
    m, y = bb.title(PX + 14, 14, title, maxw=PW - 28)
    LX = PX + LW + 10
    CW = (PX + PW - 8 - LX - 3 * G) / 4
    cx = [LX + i * (CW + G) for i in range(4)]
    # the phases, as the head of the board
    hy = y + 44
    m += (f'<rect x="{PX}" y="{hy}" width="{PW}" height="46" rx="23" fill="{bb.solid("n")}"/>'
          + bb.text(PX + 22, hy + 28, "The SkyWays PDLC", fs=14.5, b=True, c=ON))
    for i, (hue, name, _ic, _h) in enumerate(PHASES):
        pw = bb.width(name, 14)
        m += bb.pill(cx[i] + CW / 2 - pw / 2, hy + 8, name, hue, fs=14, r=15, hh=30, stroke=bb.solid("n"))[2]
    gx = cx[2] - G / 2
    top = hy + 46 + 10
    yy = top
    html = bb.h_title(title)
    for name, _ic, conf, about, ph in METHODS:
        mine = name.startswith("This manual")
        hue = "n" if mine else "s"
        al = bb.fit(about, LW - 24, MIN, 500)
        pw = bb.width(name, 14)
        cw_ = bb.width(conf, MIN)
        inline = pw + 8 + cw_ <= LW - 20
        left_h = 10 + 28 + (0 if inline else 30) + 8 + len(al) * LH + 8
        rh = max([left_h] + [_plug_h(CW, p[1]) + 16 for p in ph if p])
        m += (f'<rect x="{PX}" y="{yy:.1f}" width="{PW}" height="{rh:.1f}" rx="12" fill="{bb.tint(hue)}" '
              f'stroke="{bb.border(hue)}" stroke-width="1.6"/>')
        m += bb.pill(PX + 10, yy + 10, name, hue, fs=14, r=8, hh=28)[2]
        chip_at = (PX + 10 + pw + 8, yy + 11) if inline else (PX + 10, yy + 42)
        m += bb.pill(chip_at[0], chip_at[1], conf, "s", fs=MIN, r=7, hh=26, fill=NODE, c=INK, stroke=bb.border("s"))[2]
        m += bb.lines(PX + 12, yy + 10 + 28 + (0 if inline else 30) + 8 + 12.5, al, fs=MIN, c=INK2, w=500, lh=LH)
        cells, silent = [], []
        for i, p in enumerate(ph):
            phue, pname = PHASES[i][0], PHASES[i][1]
            if not p:
                m += (f'<rect x="{cx[i]:.1f}" y="{yy + 8:.1f}" width="{CW:.1f}" height="{rh - 16:.1f}" rx="10" fill="none" '
                      f'stroke="{bb.border(phue)}" stroke-width="1.3" stroke-dasharray="5 4"/>'
                      + bb.text(cx[i] + CW / 2, yy + rh / 2 + 4.7, "silent", a="middle", fs=MIN, c=INK2, w=500))
                silent.append(pname.split(" · ")[0])
                continue
            m += _plug(cx[i], yy + 8, CW, rh - 16, p[0], p[1], phue)
            cells.append(bb.h_cell(pname, p[1], p[0], phue))
        if silent:
            cells.append(bb.h_cell("Silent in " + ", ".join(silent[:-1]) + (" and " if len(silent) > 1 else "") + silent[-1],
                                   hue=hue, is_quiet=True))
        html += bb.h_block(hue, name, "".join(cells), key=conf, sub=about)
        yy += rh + 8
    # the sign-off, between P1 and P2, down through every row
    m += bb.gate(gx, hy - 10, yy - 8 - (hy - 10), at=hy + 23)
    m += bb.text(gx, hy - 18, bb.SIGN_OFF, a="middle", fs=MIN, b=True, c=bb.dark("k"))
    note = ("A filled cell is where the method says something about that phase; a dashed cell is where a team has to "
            "bring its own answer. The last row is where this manual's own devices sit.")
    pm, ph_ = bb.para(PX + 6, yy + 8, note, PW - 12)
    m += pm
    html += bb.h_note(note)
    return bb.svg(W, yy + 8 + ph_ + 12, m, "Four methods on the four phases: spec-driven development, the BMAD Method, AWS "
                  "AI-DLC and AIDD, each filled where it speaks to a phase and dashed where it is silent, with the "
                  "devices this manual adds", cls="bbw-w", narrow=html,
                  caption="<b>Not competitors.</b> Each method speaks to part of the lifecycle. The decision that "
                          "matters is not which method but how deep to go on this change.")


# --------------------------------------------------------------------------------------- tower
LOOP = "M215 167 H425 A88 88 0 0 1 425 343 H215 A88 88 0 0 1 215 167 Z"   # the runway loop, clockwise

PLANE = ('<path d="M-14 0 H-30" stroke="var(--ink2)" stroke-width="1.2" stroke-dasharray="3 3" opacity=".55"/>'
         '<path d="M-12 0 L-6 -2.6 L7 -2.6 Q12.5 -2.6 12.5 0 Q12.5 2.6 7 2.6 L-6 2.6 Z" fill="var(--paper)" '
         'stroke="var(--ink)" stroke-width="1.4"/>'
         '<path d="M-1 -2.6 L-7 -10 L-3 -10 L3.5 -2.6 Z M-1 2.6 L-7 10 L-3 10 L3.5 2.6 Z M-10 -1.8 L-14 -6 L-12 -6 '
         'L-7.5 -1.8 Z M-10 1.8 L-14 6 L-12 6 L-7.5 1.8 Z" fill="var(--ink)"/>')

# every rule is prefixed: a style element inside an inline SVG applies to the whole document.
# Each plane starts where it would stand still (6%, 31%, 56%, 81% of the loop), so none begins
# on the sign-off, which is at half way.
TOWER_CSS = """
.twr-lane{stroke-dasharray:12 10;animation:twr-march 1.6s linear infinite}
@keyframes twr-march{to{stroke-dashoffset:-22}}
.twr-plane{offset-path:path("%s");offset-rotate:auto;animation:twr-fly 26s linear infinite}
.twr-plane.a{offset-distance:6%%;animation-delay:-1.56s}
.twr-plane.b{offset-distance:31%%;animation-delay:-8.06s}
.twr-plane.c{offset-distance:56%%;animation-delay:-14.56s}
.twr-plane.d{offset-distance:81%%;animation-delay:-21.06s}
@keyframes twr-fly{from{offset-distance:0%%}to{offset-distance:100%%}}
.twr-radar{transform-box:view-box;transform-origin:320px 229px;animation:twr-spin 9s linear infinite}
@keyframes twr-spin{to{transform:rotate(360deg)}}
.twr-beacon{animation:twr-blink 1.8s ease-in-out infinite}
@keyframes twr-blink{0%%,100%%{opacity:1}50%%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.twr-lane,.twr-plane,.twr-beacon{animation:none}.twr-radar{display:none}}
@supports not (offset-path:path("M0 0h1")){.twr-plane{display:none}}
""" % LOOP

# what the picture's four keys and its lock stand for, set as text under it so it can be read at
# any width: (hue, key, name)
TOWER_KEY = [("slate", "P0", "Frame"), ("indigo", "P1", "Design & Spec"), ("rose", "", "Sign-off (the hard gate)"),
             ("teal", "P2", "Build & Prove"), ("amber", "P3", "Run & Learn")]


def _twr_key(x: float, y: float, key: str, hue: str, a: str = "middle") -> str:
    """A phase's key on the picture. 24 units, so it is 11px or more even on a 320px phone."""
    c = f"color-mix(in oklab,var(--dg-{hue}) 72%,var(--ink))"
    return (f'<text x="{x}" y="{y}" text-anchor="{a}" font-family="{bb.FONT}" font-size="24" font-weight="700" '
            f'fill="{c}">{key}</text>')


def tower() -> str:
    """The method page's scene: the lifecycle flown as a loop, controlled from a tower.

    Motion is direction only: the lane's dashes march, the planes follow the loop, the
    radar sweeps. Reduced motion stops all of it and the planes keep their places; a
    browser without motion paths hides the planes rather than piling them in a corner.

    The drawing carries four keys and nothing smaller; what they stand for is the line of
    text under it. The sign-off is a bar across the lane with its lock beside it, so an
    aircraft crosses the bar and never sits on the lock."""
    sky = ('<defs><linearGradient id="twr-sky" x1="0" y1="0" x2="0" y2="1">'
           '<stop offset="0" style="stop-color:color-mix(in oklab,var(--dg-slate) 26%,var(--paper))"/>'
           '<stop offset="1" style="stop-color:var(--paper)"/></linearGradient></defs>'
           '<rect x="40" y="92" width="560" height="318" fill="url(#twr-sky)"/>')
    lane = f'<path d="{LOOP}" fill="none" stroke="var(--rule2)" stroke-width="18" stroke-linejoin="round"/>'

    def seg(d: str, hue: str) -> str:
        return (f'<path d="{d}" fill="none" stroke="color-mix(in oklab,var(--dg-{hue}) 58%,var(--paper))" '
                f'stroke-width="18"/>')
    segs = (seg("M215 167 H425", "slate") + seg("M425 167 A88 88 0 0 1 425 343", "indigo")
            + seg("M425 343 H215", "teal") + seg("M215 343 A88 88 0 0 1 215 167", "amber"))
    centre = f'<path class="twr-lane" d="{LOOP}" fill="none" stroke="var(--paper)" stroke-width="2"/>'
    # the one sign-off, where P1 hands to P2: a bar across the lane, and its lock below the lane
    gate = ('<path d="M425 329 V372" stroke="var(--dg-rose)" stroke-width="4" stroke-linecap="round"/>'
            '<g transform="translate(425 384)">'
            '<rect x="-13" y="-15" width="26" height="30" rx="7" fill="var(--dg-rose)"/>'
            '<rect x="-6.5" y="-2" width="13" height="10" rx="2" fill="none" stroke="var(--dg-on)" stroke-width="1.8"/>'
            '<path d="M-3.5 -2V-5.5a3.5 3.5 0 0 1 7 0V-2" fill="none" stroke="var(--dg-on)" stroke-width="1.8" '
            'stroke-linecap="round"/></g>')
    keys = (_twr_key(320, 146, "P0", "slate") + _twr_key(532, 264, "P1", "indigo", a="start")
            + _twr_key(320, 384, "P2", "teal") + _twr_key(108, 264, "P3", "amber", a="end"))
    radar = ('<path class="twr-radar" d="M320 229 L320 99 A130 130 0 0 1 385 116 Z" fill="var(--dg-slate)" '
             'opacity=".16"/>')
    tower_ = ('<g><path d="M306 246 H334 L331 322 H309 Z" fill="var(--ink2)"/>'
              '<rect x="294" y="318" width="52" height="9" rx="3" fill="var(--ink)"/>'
              '<rect x="282" y="212" width="76" height="36" rx="9" fill="var(--ink)"/>'
              '<rect x="289" y="220" width="62" height="13" rx="3" fill="var(--paper)" opacity=".92"/>'
              '<path d="M304 220v13M320 220v13M336 220v13" stroke="var(--ink)" stroke-width="1.6"/>'
              '<path d="M320 212V194" stroke="var(--ink)" stroke-width="2"/>'
              '<circle class="twr-beacon" cx="320" cy="192" r="3.5" fill="var(--dg-rose)"/></g>')
    planes = "".join(f'<g class="twr-plane {k}">{PLANE}</g>' for k in "abcd")
    inner = sky + radar + lane + segs + centre + gate + keys + tower_ + planes
    lock = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/>'
            '<path d="M8.5 10.5V7.5a3.5 3.5 0 0 1 7 0v3"/></svg>')
    key = "".join(f'<li style="--c:var(--dg-{hue})">{f"<b>{k}</b>" if k else lock}{bb.E(name)}</li>'
                  for hue, k, name in TOWER_KEY)
    return ('<svg class="twr" viewBox="40 92 560 318" role="img" aria-label="Four planes fly a loop of four runway '
            'segments, P0 Frame, P1 Design and Spec, P2 Build and Prove and P3 Run and Learn, across one sign-off, '
            f'round a control tower with a radar sweep"><style>{TOWER_CSS}</style>{inner}</svg>'
            f'<ul class="twr-key">{key}</ul>')


# --------------------------------------------------------------------------------------- merge
# What the SkyWays PDLC adds in each phase and none of the four methods carries. The home page's table
# ends on the same four lines.
ADDS = ["The autonomy ceiling, decided before anything is built",
        "A bar per slice and an authority budget, signed before the build",
        "Prove the bar first: a lower bound, never a score, before traffic",
        "The two-number report that starts the next P0"]


def merge() -> str:
    """How the four methods merge into the SkyWays PDLC: each part lands in the phase it serves.

    Four phase columns, each in its phase's hue, hold the parts that phase takes, with the method
    named under each part; the sign-off stands between P1 and P2; the row beneath is what the
    SkyWays PDLC adds and none of the methods carries."""
    W, PX, CW, GAP = 1100, 20, 250, 20
    PARTS = {
        0: [("The brief and the PRD", "BMAD", "analyst and PM personas"),
            ("Depth judged per change", "AI-DLC", "adaptive: only the stages this change needs"),
            ("Intent written before code", "SDD", "the spec starts here, lightly")],
        1: [("The spec is what you maintain", "SDD", "code is generated from it"),
            ("Architecture and stories", "BMAD", "the architect persona's artefacts"),
            ("Only the stages that are needed", "AI-DLC", "the architect judges depth")],
        2: [("Code regenerated from the spec", "SDD", "on every change, not patched"),
            ("Dev and QA personas, story by story", "BMAD", "each hands a versioned artefact on"),
            ("Context files and editor agents", "AIDD", "the day-to-day craft"),
            ("Review by risk, cost habits", "AIDD", "who signs, what it costs")],
        3: [("Operate, then re-enter at depth", "AI-DLC", "the next change picks its own stages"),
            ("Learn and adjust, into the next brief", "BMAD", "extended: the trail runs one hand-off further"),
            ("Cache, route, trace", "AIDD", "cost habits that survive launch"),
            ("The spec learns from production", "SDD", "updated, then regenerated")],
    }
    title = [("Four methods", "s"), ("merge into",), ("one loop", "n")]
    m, y = bb.title(PX + 14, 14, title, maxw=1032)
    TY = y + 44                         # room above the columns for the sign-off's name
    NW = CW - 20
    slots = max(len(v) for v in PARTS.values())
    sh = [max(bb.node_h(NW, v[k][0], f"{v[k][1]} · {v[k][2]}") for v in PARTS.values() if k < len(v)) for k in range(slots)]
    ph = 10 + 30 + 8 + sum(sh) + (slots - 1) * 8 + 10     # parallel slots: every column ends on the same row
    head = "What the SkyWays PDLC adds, and none of the four carries"
    AY = TY + ph + 42
    ah = max(bb.callout_h(CW, t) for t in ADDS)
    html = bb.h_title(title)
    for i, (phue, pname, _ic, _href) in enumerate(PHASES):
        x = PX + i * (CW + GAP)
        m += bb.panel(x, TY, CW, ph, phue, r=14)
        m += bb.pill(x + 10, TY + 10, pname, phue, fs=14, r=8, hh=30)[2]
        yy = TY + 48
        cells = []
        for k, (t, meth, sub) in enumerate(PARTS[i]):
            m += bb.node(x + 10, yy, NW, sh[k], title_=t, sub=f"{meth} · {sub}", hue=phue)
            cells.append(bb.h_cell(t, f"{meth} · {sub}", hue=phue))
            yy += sh[k] + 8
        m += bb.callout(x, AY, CW, ADDS[i], "n", h=ah)
        key, _, nm = pname.partition(" · ")
        html += bb.h_block(phue, nm, "".join(cells), key=key,
                           foot=f'<div class="bbn-in">{bb.h_call("The SkyWays PDLC adds: " + ADDS[i][0].lower() + ADDS[i][1:], "n")}</div>')
        if i == 1:
            html += bb.h_gate()
    gx = PX + 2 * (CW + GAP) - GAP / 2
    m += bb.gate(gx, TY - 10, ph + 20)
    m += bb.text(gx, TY - 18, bb.SIGN_OFF, a="middle", fs=MIN, b=True, c=bb.dark("k"))
    m += bb.text(PX + 4, TY + ph + 30, head, fs=14, b=True)
    foot = "One order, one owner per phase, one sign-off. The parts keep their names; the four phases keep them in order."
    pm, fh = bb.para(PX + 6, AY + ah + 12, foot, 1048, w=600)
    m += pm
    html += bb.h_note(foot)
    return bb.svg(W, AY + ah + 12 + fh + 12, m, "How the four methods merge into the SkyWays PDLC: the parts of spec-driven "
                  "development, the BMAD Method, AI-DLC and AIDD placed in the phase each serves, with the sign-off "
                  "between P1 and P2, and the row of devices the SkyWays PDLC adds", cls="bbw-w", narrow=html,
                  caption="<b>Merged, not stacked.</b> Each method keeps the part it does best; the SkyWays PDLC gives the "
                          "parts one order, one owner per phase and one sign-off.")


PICTURES = {"spine": spine, "pdlc_vs": pdlc_vs, "ladder": ladder, "chain": chain, "methods": methods,
            "merge": merge}
