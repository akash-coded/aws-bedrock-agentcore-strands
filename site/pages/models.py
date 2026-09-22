"""Mental models — the twelve shapes that make the rest of the manual predictable.

A procedure tells you what to do on Tuesday. A mental model tells you what to expect before you
start, which is what lets somebody make a good call on a case this manual never covered. Each entry
is a picture, the thing it predicts, the mistake it prevents, and a test for whether it has actually
landed.

The drawings are deliberately schematic and all the same size. They are mnemonics, not data.
"""
from __future__ import annotations

from . import _kit as k

E = k.E
W, H = 260, 130  # every glyph shares a frame so the page reads as one set


def _svg(inner: str, label: str) -> str:
    return (f'<svg viewBox="0 0 {W} {H}" class="mg" role="img" aria-label="{E(label)}">'
            f"{inner}</svg>")


# --------------------------------------------------------------------- glyphs
def g_decay() -> str:
    bars = []
    for i in range(6):
        p = 0.9 ** (i + 1)
        h = 88 * p
        x = 18 + i * 40
        bars.append(f'<rect x="{x}" y="{104-h:.0f}" width="26" height="{h:.0f}" rx="3" '
                    f'fill="var(--accent)" opacity="{0.95 - i*0.12:.2f}"/>')
        bars.append(f'<text x="{x+13}" y="{100-h:.0f}" text-anchor="middle" font-size="9.5" '
                    f'fill="currentColor" opacity=".65">{p*100:.0f}</text>')
    return _svg("".join(bars) + '<line x1="10" y1="104" x2="250" y2="104" stroke="currentColor" opacity=".28"/>',
                "Six bars falling from 90 to 53 as steps are chained")


def g_doors() -> str:
    return _svg(
        '<rect x="20" y="26" width="86" height="76" rx="5" fill="none" stroke="var(--sage)" stroke-width="2"/>'
        '<path d="M42 64 H86 M78 56 l8 8 -8 8" stroke="var(--sage)" stroke-width="2" fill="none"/>'
        '<path d="M84 46 H40 M48 38 l-8 8 8 8" stroke="var(--sage)" stroke-width="2" fill="none"/>'
        '<text x="63" y="118" text-anchor="middle" font-size="10" fill="var(--sage)" font-weight="600">two-way</text>'
        '<rect x="154" y="26" width="86" height="76" rx="5" fill="none" stroke="var(--stop)" stroke-width="2"/>'
        '<path d="M176 64 H220 M212 56 l8 8 -8 8" stroke="var(--stop)" stroke-width="2" fill="none"/>'
        '<path d="M218 46 H174" stroke="var(--stop)" stroke-width="2" stroke-dasharray="3 3" opacity=".5"/>'
        '<path d="M190 38 l14 14 M204 38 l-14 14" stroke="var(--stop)" stroke-width="2"/>'
        '<text x="197" y="118" text-anchor="middle" font-size="10" fill="var(--stop)" font-weight="600">one-way</text>',
        "A two-way door with arrows both ways, and a one-way door with the return crossed out")


def g_lever() -> str:
    return _svg(
        '<path d="M22 86 L238 44" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M150 52 l12 22 -24 0 z" fill="var(--accent)"/>'
        '<rect x="14" y="60" width="34" height="26" rx="4" fill="var(--stop)" opacity=".85"/>'
        '<text x="31" y="78" text-anchor="middle" font-size="11" fill="#fff" font-weight="700">$$$</text>'
        '<circle cx="228" cy="42" r="11" fill="var(--sage)"/>'
        '<path d="M224 42 l3 4 6 -8" stroke="#fff" stroke-width="2" fill="none"/>'
        '<text x="31" y="106" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">damage</text>'
        '<text x="228" y="70" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">one person</text>',
        "A lever: one person at the long end lifts the damage at the short end")


def g_wall() -> str:
    return _svg(
        '<text x="62" y="22" text-anchor="middle" font-size="10" fill="var(--warn)" font-weight="700">PROMPT</text>'
        + "".join(f'<rect x="{22+i*22}" y="34" width="14" height="58" rx="2" fill="none" '
                  f'stroke="var(--warn)" stroke-width="2" stroke-dasharray="4 4"/>' for i in range(4))
        + '<path d="M28 62 H112" stroke="var(--stop)" stroke-width="2.5" marker-end="url(#mk)"/>'
        '<text x="62" y="110" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">gets through</text>'
        '<text x="196" y="22" text-anchor="middle" font-size="10" fill="var(--ok)" font-weight="700">SIGNATURE</text>'
        '<rect x="158" y="34" width="76" height="58" rx="3" fill="var(--ok)" opacity=".16" stroke="var(--ok)" stroke-width="2"/>'
        '<path d="M140 62 H156" stroke="var(--stop)" stroke-width="2.5"/>'
        '<path d="M150 54 l10 8 -10 8" fill="none" stroke="var(--stop)" stroke-width="2.5" opacity=".35"/>'
        '<text x="196" y="110" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">raises</text>'
        '<defs><marker id="mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">'
        '<path d="M0 0 L7 3.5 L0 7 z" fill="var(--stop)"/></marker></defs>',
        "A dashed fence a line passes through, beside a solid wall that stops it")


def g_average() -> str:
    return _svg(
        '<rect x="18" y="30" width="150" height="34" rx="4" fill="var(--accent)" opacity=".28"/>'
        '<text x="93" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent)">overall 84%</text>'
        '<rect x="18" y="74" width="118" height="17" rx="3" fill="var(--sage)" opacity=".7"/>'
        '<text x="142" y="87" font-size="9.5" fill="currentColor" opacity=".75">easy, 89%</text>'
        '<rect x="18" y="96" width="26" height="17" rx="3" fill="var(--stop)"/>'
        '<text x="50" y="109" font-size="9.5" fill="var(--stop)" font-weight="600">the risky one, 77%</text>'
        '<line x1="18" y1="22" x2="18" y2="118" stroke="currentColor" opacity=".2"/>',
        "A wide average bar above a large passing slice and a small failing one")


def g_bound() -> str:
    return _svg(
        '<line x1="30" y1="84" x2="244" y2="84" stroke="currentColor" opacity=".25"/>'
        '<line x1="150" y1="20" x2="150" y2="100" stroke="var(--ink2)" stroke-width="2" stroke-dasharray="4 3"/>'
        '<text x="150" y="114" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">the bar</text>'
        '<line x1="96" y1="44" x2="206" y2="44" stroke="var(--stop)" stroke-width="2"/>'
        '<line x1="96" y1="38" x2="96" y2="50" stroke="var(--stop)" stroke-width="2"/>'
        '<line x1="206" y1="38" x2="206" y2="50" stroke="var(--stop)" stroke-width="2"/>'
        '<circle cx="172" cy="44" r="5" fill="var(--stop)"/>'
        '<text x="222" y="40" font-size="9.5" fill="var(--stop)" font-weight="600">n=40</text>'
        '<line x1="158" y1="72" x2="196" y2="72" stroke="var(--ok)" stroke-width="2"/>'
        '<line x1="158" y1="66" x2="158" y2="78" stroke="var(--ok)" stroke-width="2"/>'
        '<line x1="196" y1="66" x2="196" y2="78" stroke="var(--ok)" stroke-width="2"/>'
        '<circle cx="177" cy="72" r="5" fill="var(--ok)"/>'
        '<text x="212" y="76" font-size="9.5" fill="var(--ok)" font-weight="600">n=500</text>',
        "Two point estimates with error bars: the wide one crosses the bar, the narrow one clears it")


def g_funnel() -> str:
    drops = "".join(f'<circle cx="{132+((i*37)%56)-28}" cy="{34+i*11}" r="2.6" fill="var(--accent)" opacity=".7"/>'
                    for i in range(6))
    return _svg(
        '<path d="M44 24 H216 L164 72 V104 H96 V72 Z" fill="none" stroke="currentColor" stroke-width="2" opacity=".55"/>'
        + drops +
        '<text x="130" y="122" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">'
        '5% of traffic = 12 cases a day</text>',
        "A funnel with a narrow neck and a slow trickle of cases")


def g_multiply() -> str:
    xs = [18, 78, 138, 198]
    vals = ["1.6", "1.5", "1.3", "1.4"]
    out = []
    for x, v in zip(xs, vals):
        out.append(f'<rect x="{x}" y="34" width="44" height="40" rx="5" fill="var(--warn)" opacity=".2" '
                   f'stroke="var(--warn)"/>')
        out.append(f'<text x="{x+22}" y="59" text-anchor="middle" font-size="13" font-weight="700" '
                   f'fill="var(--warn)">{v}</text>')
    for x in xs[:-1]:
        out.append(f'<text x="{x+52}" y="59" text-anchor="middle" font-size="12" fill="currentColor" '
                   f'opacity=".5">×</text>')
    out.append('<text x="130" y="100" text-anchor="middle" font-size="15" font-weight="700" '
               'fill="var(--stop)">= 4.4× the estimate</text>')
    return _svg("".join(out), "Four ordinary factors multiplied together giving 4.4 times")


def g_fanout() -> str:
    lines = []
    pts = [(176, 34), (216, 52), (226, 88), (190, 106), (154, 74)]
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            lines.append(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" y2="{pts[j][1]}" '
                         f'stroke="var(--stop)" stroke-width="1" opacity=".45"/>')
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="var(--stop)" opacity=".8"/>' for x, y in pts)
    fan = "".join(f'<line x1="56" y1="66" x2="104" y2="{34+i*16}" stroke="var(--sage)" stroke-width="1.6"/>'
                  f'<circle cx="104" cy="{34+i*16}" r="4" fill="var(--sage)"/>' for i in range(5))
    return _svg(
        '<circle cx="42" cy="66" r="13" fill="var(--sage)"/>' + fan +
        '<text x="62" y="120" text-anchor="middle" font-size="9.5" fill="var(--sage)" font-weight="600">one agent, 0 hand-offs</text>'
        + "".join(lines) + dots +
        '<text x="192" y="120" text-anchor="middle" font-size="9.5" fill="var(--stop)" font-weight="600">five agents, 10</text>',
        "One agent fanning out to five tools, beside five agents joined by ten lines")


def g_dial() -> str:
    return _svg(
        '<path d="M46 96 A56 56 0 0 1 158 96" fill="none" stroke="currentColor" stroke-width="7" opacity=".18"/>'
        '<path d="M46 96 A56 56 0 0 1 72 49" fill="none" stroke="var(--sage)" stroke-width="7"/>'
        '<line x1="102" y1="96" x2="72" y2="52" stroke="var(--ink)" stroke-width="2.5" stroke-linecap="round"/>'
        '<circle cx="102" cy="96" r="5" fill="var(--ink)"/>'
        '<text x="46" y="114" text-anchor="middle" font-size="9" fill="currentColor" opacity=".7">a fix</text>'
        '<text x="158" y="114" text-anchor="middle" font-size="9" fill="currentColor" opacity=".7">a new system</text>'
        '<text x="212" y="62" text-anchor="middle" font-size="10" fill="currentColor" opacity=".75">depth is</text>'
        '<text x="212" y="76" text-anchor="middle" font-size="10" fill="currentColor" opacity=".75">per change</text>',
        "A dial turned low, running from a fix to a new system")


def g_baton() -> str:
    return _svg(
        '<circle cx="48" cy="58" r="15" fill="var(--accent)" opacity=".85"/>'
        '<circle cx="200" cy="58" r="15" fill="var(--accent)" opacity=".5"/>'
        '<rect x="88" y="48" width="72" height="22" rx="4" fill="var(--ochre)" opacity=".3" stroke="var(--ochre)"/>'
        '<text x="124" y="63" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ochre)">artefact</text>'
        '<path d="M66 58 H86" stroke="currentColor" stroke-width="2" opacity=".5"/>'
        '<path d="M162 58 H182" stroke="currentColor" stroke-width="2" opacity=".5"/>'
        '<text x="124" y="102" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">'
        'the phase ends when this crosses</text>'
        '<text x="124" y="116" text-anchor="middle" font-size="9.5" fill="var(--stop)" opacity=".8">not on Friday</text>',
        "Two runners passing an artefact rather than a baton")


def g_drift() -> str:
    flat = " ".join(f"{20+i*10},{52+(i % 2)}" for i in range(11))
    slide = " ".join(f"{130+i*11},{52+i*3.6:.0f}" for i in range(11))
    return _svg(
        f'<polyline points="{flat}" fill="none" stroke="var(--sage)" stroke-width="2.5"/>'
        f'<polyline points="{slide}" fill="none" stroke="var(--stop)" stroke-width="2.5"/>'
        '<line x1="130" y1="22" x2="130" y2="100" stroke="currentColor" opacity=".25" stroke-dasharray="3 3"/>'
        '<text x="74" y="110" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">no deploy</text>'
        '<text x="186" y="110" text-anchor="middle" font-size="9.5" fill="currentColor" opacity=".7">no error</text>'
        '<text x="196" y="34" text-anchor="middle" font-size="9.5" fill="var(--stop)" font-weight="600">still no alarm</text>',
        "A flat line that begins sliding downwards with no marker for the change")


# --------------------------------------------------------------------- models
MODELS = [
    dict(
        id="length", name="Length is the enemy", glyph=g_decay,
        one="Chained probabilistic steps multiply. They do not average.",
        predicts="Four steps each right 90% of the time are right 66% of the time end to end, and "
                 "they fail fluently — no exception, no red test, a confident wrong answer. Every "
                 "step you add is a tax on every step before it.",
        prevents="Judging a pipeline by its weakest step, or by the mean of its steps. Both readings "
                 "are optimistic, and the second is the one that gets written in a status report.",
        subtle="It is the <em>optimistic</em> bound, because real steps correlate: a bad retrieval "
               "makes the next three worse. If your measured end-to-end rate is below p to the n, "
               "correlation is why, and the fix is upstream of the step you were blaming.",
        landed="You reach for a multiplication before you reach for an average, and your first "
               "instinct on a long chain is to remove a step rather than improve one.",
        where=[("The arithmetic", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Formulas-and-Calculators"),
               ("Where the checkers go", "../solution-architect/#detail")]),
    dict(
        id="doors", name="Reversibility is the hinge", glyph=g_doors,
        one="What a mistake costs matters less than whether you can undo it.",
        predicts="Two actions with the same expected loss need different controls if one can be "
                 "withdrawn and the other cannot. A proposal can be retracted; a cash refund cannot. "
                 "The second needs a person regardless of how accurate the model becomes.",
        prevents="Setting autonomy from model capability, and setting it per product. Both produce "
                 "a level that is simultaneously too loose for the money action and too strict for "
                 "the harmless one.",
        subtle="Reversibility is a property of your business, not of the software. The same refund "
               "is a two-way door at a company that can claw back and a one-way door at one that "
               "cannot, and no amount of engineering changes which you are.",
        landed="Your first question about a new action is “can we undo it, and how fast”, "
               "before anyone has mentioned accuracy.",
        where=[("Autonomy, per action", "../product-manager/#frame"),
               ("The risk ladder", "../frameworks/")]),
    dict(
        id="lever", name="A hold is a lever, not a brake", glyph=g_lever,
        one="Putting a person in the loop lowers the damage, and therefore lowers the accuracy you "
            "need.",
        predicts="A refund with $600 of damage needs 98% accuracy to break even. Put a person on the "
                 "charge, drop the damage to $30, and the same step needs 71%. Nothing about the "
                 "model changed; the arithmetic did.",
        prevents="Treating a human check as friction to be removed, and treating an unreachable bar "
                 "as a reason not to build. Both follow from reading the hold as a brake.",
        subtle="This is why a gate is a commercial instrument. It is the cheapest way to make a "
               "feature shippable, and the case for removing one is an argument about damage, never "
               "about speed.",
        landed="When somebody says the accuracy is not good enough, you ask what a mistake costs "
               "before you ask how to improve the model.",
        where=[("Derive the bar", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Prove-the-Bar"),
               ("Try the arithmetic", "../protocol/#")]),
    dict(
        id="boundary", name="A prompt is a request; a signature is a boundary", glyph=g_wall,
        one="A rule the model reads lowers a probability. A rule the code enforces closes a path.",
        predicts="Every limit written in prose will eventually be crossed, because a model can be "
                 "talked past a request and text arriving from anywhere can do the talking. A typed "
                 "parameter that raises cannot be argued with.",
        prevents="The most expensive sentence in agentic software: “we have a cap”, said "
                 "about a cap that lives in a prompt. Nothing in a code review flags it, because it "
                 "reads exactly like a rule.",
        subtle="Both belong. The prompt explains the rule so the agent behaves well by default; the "
               "signature makes bad behaviour impossible when the prompt has been talked past. "
               "“Put it in the tool, not the prompt” is half right and throws away the "
               "half that makes the agent cooperative.",
        landed="When told a control exists, you ask to be shown it, and you notice whether somebody "
               "opens prose or code.",
        where=[("The six controls", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Hold-the-Security-Boundary"),
               ("In code", "../engineering/#gate")]),
    dict(
        id="average", name="The average hides the slice that matters", glyph=g_average,
        one="Aggregate quality is dominated by the easy, high-volume cases.",
        predicts="An overall score can rise while the slice carrying all the risk falls below its "
                 "bar. It happened at SkyWays: 79% to 84% overall, and codeshare down from 81% to "
                 "77% against a bar of 80.",
        prevents="Shipping a regression that the headline number endorses, and setting one bar for "
                 "a whole feature so the hard slice ships broken while the easy one waits.",
        subtle="The same trap runs through sampling. A sample representative of <em>traffic</em> is "
               "not representative of <em>risk</em>, so the rare costly slice needs deliberate "
               "oversampling rather than a bigger random draw.",
        landed="You ask “per slice?” before you read any quality number, and a single "
               "percentage in a deck makes you suspicious rather than reassured.",
        where=[("Per-slice readouts", "../qa/#measure"),
               ("Rare slices", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scenario-Library")]),
    dict(
        id="bound", name="A score is not proof", glyph=g_bound,
        one="A measurement from a sample is an estimate with a width, and the width is the argument.",
        predicts="82% on forty cases and 82% on five hundred are different claims. The first has a "
                 "lower bound near 70%, the second near 79%. Against an 80% bar, neither is proven — "
                 "and no realistic sample will prove it, because the estimate sits too close.",
        prevents="Shipping on a point estimate, and rejecting a slice that is merely unproven. The "
                 "second matters: “not proven” with a cases-owed number is a plan, where "
                 "“it failed” is an argument.",
        subtle="The cost of proving grows <em>quadratically</em> as your score approaches the bar. "
               "Halve the gap and you quadruple the cases. A score a whisker above the bar is the "
               "most expensive result you can get.",
        landed="You never quote a score without its sample size, and you hear “94% accurate” "
               "as an incomplete sentence.",
        where=[("Lower bounds", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Prove-the-Bar"),
               ("The calculator", "../simulator/#/toolkit/confidence")]),
]

MODELS += [
    dict(
        id="speed", name="Evidence arrives at the speed of traffic", glyph=g_funnel,
        one="You cannot learn faster than your sample accumulates.",
        predicts="At 240 cases a day and five percent of traffic you see twelve cases a day, so five "
                 "hundred cases takes forty-two days. That number is fixed by arithmetic, not by "
                 "effort, and no amount of urgency moves it.",
        prevents="Promising a cut-over date before anyone has divided cases-needed by cases-per-day, "
                 "and sitting at five percent indefinitely because it feels safe.",
        subtle="The safe share is the slow one, which is the whole reason a cut-over <em>widens</em> "
               "rather than holding. And the sample is biased by time: at five percent for six weeks "
               "you meet a normal Tuesday many times and a storm day perhaps once, so widen across "
               "conditions rather than only across volume.",
        landed="When asked for a launch date you reach for a division, and you can say what the "
               "window buys as well as what it costs.",
        where=[("Cut over and widen", "../qa/#shadow"),
               ("The arithmetic", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Formulas-and-Calculators")]),
    dict(
        id="habits", name="Cost is a product of habits", glyph=g_multiply,
        one="A bill is four ordinary behaviours multiplying, not one runaway.",
        predicts="Context bloat 1.6, no routing 1.5, a discarded cache 1.3, extra attempts 1.4 — and "
                 "the invoice is 4.4 times its estimate on flat traffic. Each decision was sensible "
                 "and made by a careful person.",
        prevents="Hunting for the one thing that broke, and fixing the biggest <em>ratio change</em> "
                 "first. Attempts rose more than five-fold in relative terms and contribute the "
                 "smallest factor of the four.",
        subtle="Because they multiply, the right fix order is what removes the most multiplier per "
               "day of work — <code>(factor − 1) ÷ days</code> — which is usually not the fix that "
               "feels most urgent. The retry breaker is the right fix in the wrong position.",
        landed="A surprise invoice makes you open the per-call log rather than the price list, and "
               "you expect to find four things rather than one.",
        where=[("Decompose a bill", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Control-the-Token-Bill"),
               ("In the platform", "../devops/#observe")]),
    dict(
        id="fanout", name="Parallelism is a property of a tool, not a headcount", glyph=g_fanout,
        one="Things happening at once does not mean several agents.",
        predicts="Five agents have ten possible hand-offs, and coordination cost grows faster than "
                 "the work. One agent with a fan-out tool searches four partners in parallel with "
                 "zero hand-offs and nothing to get wrong between them.",
        prevents="The reflex that turns “these run concurrently” into “these need "
                 "separate agents”, which is how a swarm arrives without anyone choosing one.",
        subtle="The rule is start single and escalate on a <em>named limit</em> written into the "
               "record — a context that genuinely overloads, or parallel sub-tasks a tool cannot "
               "express. Without the written limit the swarm returns by default at the next design "
               "review, because nobody can point at what was decided.",
        landed="You ask what limit justifies each hand-off, and you notice that a calculator behind "
               "an agent is a provable step made probabilistic.",
        where=[("How many agents", "../solution-architect/#shape"),
               ("On paper", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Design-an-Agent-on-Paper")]),
    dict(
        id="depth", name="Depth is a dial, not a constant", glyph=g_dial,
        one="Run only the lifecycle stages this particular change actually needs.",
        predicts="One process for everything over-serves the one-line fix and under-serves the new "
                 "subsystem. Both failures are expensive, and the first is the one that gives the "
                 "method a reputation for slowing teams down.",
        prevents="Eleven gates on a printer-helpdesk question — and the reputation that earns, which "
                 "is then used to skip the gates on the refund tool, where they mattered.",
        subtle="The spec stays everywhere; it is the backbone. What flexes is everything around it: "
               "the persona trail, the depth of discovery, the number of records. And the judgement "
               "is per change, made by the architect, not per programme set by a policy.",
        landed="You classify a change before you choose a process for it, and you are comfortable "
               "saying that a piece of work deserves almost none of this.",
        where=[("Depth per change", "../solution-architect/#shape"),
               ("The helpdesk case", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scenario-Library")]),
    dict(
        id="artefact", name="A phase ends on an artefact, not a date", glyph=g_baton,
        one="A hand-off happens when the next person has what they cannot start without.",
        predicts="Phases that end on dates hand over nothing, and the receiving team rediscovers the "
                 "missing decision three weeks later — usually the one nobody wanted to make.",
        prevents="A spec signed off in a meeting with five of its eight fields undecided, which the "
                 "engineer then decides by default because the code has to do something.",
        subtle="Only one of the four hand-offs is a hard gate. The other three can cross with a "
               "placeholder, a named owner and a date, which is what keeps velocity while the "
               "decision is still being measured. Treating all four as hard is its own failure.",
        landed="You ask what crossed rather than whether the phase finished, and an empty evidence "
               "line reads to you as a blocked merge.",
        where=[("What crosses each hand-off", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/The-Evidence-Pack"),
               ("Hard and soft gates", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Gates-and-Governance")]),
    dict(
        id="drift", name="Drift is the defect with no error message", glyph=g_drift,
        one="A probabilistic system changes behaviour when the world moves, with no deploy.",
        predicts="No code changed, nothing threw, no alert fired, and three months later a customer "
                 "notices the assistant offers credits where it used to offer refunds. Your existing "
                 "monitoring was never looking for this.",
        prevents="Believing that “nothing changed” means nothing changed, and treating "
                 "post-launch quality as a testing problem rather than an operational one.",
        subtle="Watch the <em>output mix</em>, not the accuracy — accuracy needs labels and arrives "
               "late. And watch two thresholds: the week-on-week step, and the level against a "
               "frozen baseline, because a slide of two points a week never trips a five percent "
               "rule and still moves you thirty points in a quarter.",
        landed="You treat an output distribution as a business metric, and you know what "
               "automatically re-opens your release gate.",
        where=[("Watch for drift", "../qa/#watch"),
               ("As a KPI", "../product-manager/#learn")]),
]


def _card(m: dict) -> str:
    where = " · ".join(
        f'<a href="{E(h)}"{" target=_blank rel=noopener" if h.startswith("http") else ""}>{E(l)}</a>'
        for l, h in m["where"])
    return f"""<section class="mm" id="{E(m['id'])}">
  <div class="mmg">{m['glyph']()}</div>
  <div class="mmb">
    <h3>{E(m['name'])}</h3>
    <p class="mo">{m['one']}</p>
    {k.lens(
      f'<p><strong>What it predicts.</strong> {m["predicts"]}</p>'
      f'<p><strong>The mistake it prevents.</strong> {m["prevents"]}</p>',
      f'<p><strong>The part that is easy to miss.</strong> {m["subtle"]}</p>',
      "The model", "The subtlety")}
    <p class="ml"><span>Landed when</span> {m['landed']}</p>
    <p class="mw">{where}</p>
  </div>
</section>"""


def build(shell, urls: dict) -> str:
    cards = "".join(_card(m) for m in MODELS)
    index = "".join(
        f'<li><a href="#{E(m["id"])}"><b>{E(m["name"])}</b><span>{m["one"]}</span></a></li>'
        for m in MODELS)
    body = f"""<div class="wrap"><main id="main" style="padding:40px 0 84px">
<div class="sec" style="max-width:74ch">
  <div class="kicker">Intuition</div>
  <h1>Twelve shapes that make the rest predictable</h1>
  <p class="lede">A procedure tells you what to do on Tuesday. A model tells you what to expect
  before you start, which is what lets somebody make a good call on a case this manual never
  covered. These twelve are the ones that keep paying.</p>
  <p>Each one is a picture, what it predicts, the mistake it prevents, and a test for whether it has
  actually landed. The test is the useful part: a model you can recite and do not use is a slogan.</p>
  <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:18px">
  {k.lens_toggle("The model", "The subtlety")}
  <span style="font-size:13px;color:var(--soft);flex:1 1 300px;min-width:240px">Read the models
  first. The second view holds the qualification each one needs before you apply it somewhere it
  does not fit.</span></div>
</div>

<div class="sec"><ol class="mix">{index}</ol></div>

{cards}

<div class="sec" style="border-top:1px solid var(--rule);padding-top:28px;max-width:74ch">
<h2>How to use these</h2>
<ol class="acts">
<li><b>Teach one a week, not twelve at once.</b><span>A model lands when somebody uses it unprompted
in an argument. That takes a fortnight of the same idea being available, not an hour of all of
them.</span></li>
<li><b>Use the landed-when line as the test.</b><span>Not whether the team can define it. Whether
the question it implies has started showing up in reviews.</span></li>
<li><b>Expect three to be resisted.</b><span>Usually the hold as a lever, the average hiding the
slice, and depth as a dial — because each one contradicts something a competent person currently
believes is good practice.</span></li>
<li><b>Pair each with its arithmetic once.</b><span>The intuition is what you carry; the formula is
what settles the argument. A model without its number loses to a confident opinion.</span></li>
<li><b>Keep the subtlety visible.</b><span>Every one of these has a boundary, and a model applied
past its boundary does more damage than no model, because it comes with confidence.</span></li>
</ol>
<div class="note"><p><strong>Where they came from.</strong> Some are established ideas applied to a
new setting — one-way doors, least privilege, Little's law. Some are this manual's own constructions
and are defaults to argue with rather than findings. Which is which is recorded on
<a href="{urls['wiki']}/Sources-and-Confidence" target="_blank" rel="noopener">Sources and
confidence</a>.</p></div>
</div>
</main></div>"""
    return shell(title="Mental models · The agentic manual",
                 desc="Twelve mental models for building software that decides: chained probability, "
                      "reversibility, the hold as a lever, requests versus boundaries, and the eight "
                      "others that keep paying.",
                 body=body, depth=1, nav_id="models",
                 canonical=urls["base"] + "models/")
