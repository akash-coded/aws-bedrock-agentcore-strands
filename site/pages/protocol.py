"""The agentic operating protocol, the page for whoever owns the P&L.

Every other page on this site is written for someone doing the work. This one is written for the
person funding it, and it answers four questions in order: what actually changes, who does what,
how you will know it is working, and how to roll it out without the organisation rejecting it.

It carries a lens control. The default reading is what a decision means; the second is the
mechanism underneath, for when a claim needs checking rather than accepting.
"""
from __future__ import annotations

from . import _kit as k

E = k.E


def pair(meaning: str, mechanism: str, la: str = "What it means", lb: str = "How it works") -> str:
    """The two readings of a claim, side by side, so neither is hidden behind a toggle."""
    return (f'<div class="pair"><div><b class="pl">{E(la)}</b>{meaning}</div>'
            f'<div><b class="pl">{E(lb)}</b>{mechanism}</div></div>')


def _hero() -> str:
    return f"""<div class="rowh"><div>
<div class="kicker">For leadership</div>
<h1>Organisational DNA for software that decides</h1>
<p class="lede">For executives, leaders, the C-suite, entrepreneurs and business owners: the people who fund
product development and answer for its results.</p>
<p class="allure">If you lead an organisation, large language models have already changed the economics of
building software. <em>Drafting is nearly free, judgement is the bottleneck, and part of every product you ship
is now right only a share of the time.</em> This page shows what that does to your teams, your costs and your
risks, and how to run product development as <em>one operating model, P0 to P3, across the whole organisation</em>,
rather than as five teams each adopting a tool.</p>
</div><div class="rowa"><b>On this page</b><ol>
<li><a href="#why">Why this matters to you now</a></li>
<li><a href="#claims">Five things that change</a></li>
<li><a href="#teams">Your teams, transformed</a></li>
<li><a href="#money">Where the money is</a></li>
<li><a href="#changes">What changes, and what does not</a></li>
<li><a href="#who">Who does what</a></li>
<li><a href="#frameworks">What the frameworks mean for you</a></li>
<li><a href="#decisions">The four decisions only you can make</a></li>
<li><a href="#knowing">How you will know it is working</a></li>
<li><a href="#llms">LLMs across the board, at three levels</a></li>
<li><a href="#rollout">Ninety days, without rejection</a></li>
<li><a href="#escalate">Seven things to escalate on</a></li>
<li><a href="#first30">Your first thirty days</a></li></ol></div></div>
{k.orient(
    "The <strong>sponsor</strong>, the executive, the head of product or engineering: whoever owns the outcome "
    "and the budget rather than the implementation.",
    "See the whole operating model on one screen, and leave with four questions for your next review.",
    ["Read <b>Five things that change</b> and <b>Your teams, transformed</b>.",
     "Take <b>the four decisions</b> to your next review.",
     "Put <b>the first thirty days</b> in your calendar."])}
"""


def _why() -> str:
    cells = [
        ("The economics moved",
         "A model drafts a spec, a test suite or a customer reply in seconds, so the cost of producing "
         "work is close to zero. The cost has moved to judgement: deciding what to build, checking what "
         "was drafted, and proving it works. Organisations that keep paying for production and skimp "
         "on judgement get more output and worse outcomes."),
        ("The risk moved",
         "Part of your product is now probabilistic: right most of the time, wrong fluently, with no "
         "error message. That is survivable when a mistake can be undone and expensive when it cannot. "
         "The control is not more accuracy; it is a person, or a cap in code, on every action that "
         "is a one-way door."),
        ("The organisation has to move with it",
         "Five teams each adopting a tool is not a strategy. One operating model, P0 to P3, gives "
         "every team the same phases, the same gates and the same evidence, so a product manager's "
         "spec, an engineer's slice and QA's proof fit together. It also creates a sixth role, "
         "governance, and that one is yours."),
    ]
    body = "".join(f'<div class="card"><h3 class="h4">{E(t)}</h3><p>{E(b)}</p></div>' for t, b in cells)
    return f"""<div class="sec" id="why">
<h2>Why this matters to you now</h2>
<div class="three">{body}</div>
</div>"""


def _teams() -> str:
    rows = [
        ("Product management", "Frames the work as measured pain and rules on AI fit before anyone builds; "
         "writes specs a machine can build from", "Low effort: a chat assistant with your documents",
         "Fewer wrong bets; a backlog where most items come back as rules, cheaper than agents"),
        ("Engineering", "Builds from story files with coding agents, a shippable slice a day; caps live in "
         "code, not prompts", "High effort: coding agents and agent frameworks, behind a gateway",
         "Cycle time in days, not fortnights; a wrong turn costs a day"),
        ("Quality", "Owns the bar per slice, the golden set and the harness that gates every merge",
         "Mid effort: evaluation tooling wired into CI", "Quality you can quote with a number and a lower bound; "
         "fewer incidents that reach a customer"),
        ("Platform and operations", "Runs one gateway, a per-call log, a trace that redacts, and a rehearsed "
         "rollback", "High effort: the platform under every agent", "A bill attributable per feature; "
         "an incident contained in minutes"),
        ("Customer operations and support", "Lets an assistant draft and propose, and keeps a person on "
         "every action that moves money or cannot be undone", "Mid effort: an agent platform with holds",
         "Handling time falls on the high-volume cases; the risky ones stay human"),
        ("Finance", "Receives two numbers every cycle, the saving and the spend, and can read a bill as "
         "four habits multiplying", "Low effort: the reports, not the tools",
         "No surprise invoice; cost that turns positive from cycle two"),
        ("Legal, risk and compliance", "Signs the authority budget: what the agent may do alone, per action, "
         "and the trace that proves it", "Low effort: the records and the trace", "Auditability by design; "
         "a regulator's question answered from the log"),
        ("Sales, marketing and every other function", "Drafts, summarises and restructures with a chat "
         "assistant, under one rule about what may enter it", "Low effort: a chat surface",
         "Throughput on written work, with no access to systems and no new risk"),
    ]
    body = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>"
                   for a, b, c, d in rows)
    return f"""<div class="sec" id="teams">
<h2>Your teams, transformed</h2>
<p class="wide">The same four phases run through every function. What each team does in them, the level of tooling it
needs, and the gain you should expect to see.</p>
<div class="tw" tabindex="0"><table><thead><tr><th>Team</th><th>What changes in how they work</th><th>What they use</th>
<th>The gain</th></tr></thead><tbody>{body}</tbody></table></div>
<p class="lalt">The effort levels, low, mid and high, are explained in <a href="#llms">LLMs across the board</a>
below, and each role's eight steps are on <a href="#who">its own page</a>.</p>
</div>"""


def _money() -> str:
    rows = [
        ("Drafting time", "Models draft; people check. Review hours are high in cycle one and fall as specs, "
         "bars and context files sharpen.", "Efficiency", "Person-days per story, before and after, with the "
         "review row visible"),
        ("Cycle time", "Work ships in slices of a day, each proven before the next, so a wrong turn costs a "
         "day rather than a fortnight.", "Efficiency", "Something merged most days by day 45"),
        ("Cost of quality", "A bar per slice, derived from what a mistake costs, and a lower bound that must "
         "clear it before traffic widens.", "Both", "Incidents that reached a customer, per quarter"),
        ("Run cost", "Context discipline, routing to cheaper models, a cache that hits, and a retry breaker: "
         "four habits that otherwise multiply into a bill 4.4 times its estimate.", "Cost",
         "Token spend per story, decomposed into its four factors"),
        ("Cost of risk", "Every action that cannot be undone has a person or a cap in code on it, so the "
         "expensive mistake is impossible rather than unlikely.", "Cost", "The authority record, and the cap "
         "shown in code"),
    ]
    body = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>"
                   for a, b, c, d in rows)
    return f"""<div class="sec" id="money">
<h2>Where the money is: efficiency, cost, or both</h2>
<p class="wide">Five levers. Start with efficiency on high-volume, low-damage work, where a first cycle pays for itself in
time; take cost through the gateway, because without a per-call log a bill cannot be diagnosed.</p>
<div class="tw" tabindex="0"><table><thead><tr><th>Lever</th><th>The mechanism</th><th>Gain</th><th>What to ask for</th></tr></thead>
<tbody>{body}</tbody></table></div>
{pair("<p>A first cycle that saves time and costs more is normal and survivable, if the two numbers reach you "
      "from the team. Fund the second cycle on a trajectory: review hours falling, re-runs falling.</p>",
      "<p>The value line nets token cost and review load off the gross saving. Review falls as artefacts "
      "sharpen; if it has not fallen by cycle three the artefacts are the problem, not the model. The "
      "calculator under <a href='#decisions'>decision four</a> lets you drag each term.</p>")}
</div>"""


def _frameworks_exec() -> str:
    cells = [
        ("AI-DLC, from AWS", "Run only the lifecycle stages a change actually needs. The judgement of depth is "
         "made per change, by an architect, which is what stops a one-line fix from costing a programme."),
        ("AIDD", "The daily craft of building with coding agents: context files the agent reads, story files "
         "it builds from, review by risk, and the cost habits that keep the bill flat."),
        ("The BMAD Method", "A pipeline of AI personas, analyst to QA, each handing a versioned artefact to the "
         "next. Right for complex, audited work; twelve personas too many for a small change."),
        ("Spec-driven development", "The specification is the asset you maintain; code is generated from it "
         "and regenerated on change. It is the backbone every other method plugs into."),
    ]
    body = "".join(f'<div class="card"><h3 class="h4">{E(t)}</h3><p>{E(b)}</p></div>' for t, b in cells)
    return f"""<div class="sec" id="frameworks">
<h2>What the frameworks mean for you</h2>
<p class="wide">Four named methods are in the market, and each is right about part of the lifecycle. You do not adopt four.
The SkyWays PDLC takes the part each does best, keeps them in one order with one owner per phase, and adds the
devices none of them carries: one hard gate, a bar per slice, an authority budget and the two-number report.</p>
<div class="four">{body}</div>
<p class="lalt"><a href="../frameworks/">How the four merge into P0 to P3</a>, with the picture.</p>
</div>"""


def _llms() -> str:
    rows = [
        ("Low effort", "Chat assistants: Claude, ChatGPT, Gemini, and the same models inside your office suite",
         "Everyone, any function: drafting, summarising, restructuring, arguing with a plan",
         "No access to systems; the output is a draft by a capable stranger",
         "Nothing enters it that you would not email externally"),
        ("Mid effort", "Agent platforms with your documents and workflows: Copilot Studio, Bedrock Agents, "
         "Dify, n8n and their peers", "Product, analysis, support, operations: proposals grounded in your data",
         "Read-only by default; it proposes and a person decides and signs",
         "Named documents only, never the whole drive"),
        ("High effort", "Agents you build: LangGraph, LangChain, Strands, CrewAI, behind your own gateway",
         "Engineering and platform: the agent inside your product", "Caps and confirmations in tool "
         "signatures; reads open, writes gated; every consequential action leaves a trace",
         "Review by risk band; money paths get two readers, always"),
    ]
    body = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td>"
                   f"<td>{E(e)}</td></tr>" for a, b, c, d, e in rows)
    return f"""<div class="sec" id="llms">
<h2>LLMs across the board, at three levels of effort</h2>
<p class="wide">Most of the value in an organisation comes from the low and mid levels, and most of the risk lives at the
high one. The products change every quarter; the three levels and the control on each do not.</p>
<div class="tw" tabindex="0"><table><thead><tr><th>Level</th><th>What</th><th>Who, for what</th><th>The control on it</th>
<th>The rule</th></tr></thead><tbody>{body}</tbody></table></div>
{pair("<p><strong>The decision to take centrally</strong> is that every model call "
      "in production passes through one layer you own, so routing, budgets and the per-call log exist in one "
      "place. Teams then choose their own editor.</p>",
      "<p>A coding assistant reads a committed context file at session start: <code>CLAUDE.md</code> for Claude "
      "Code, <code>AGENTS.md</code> for Codex, <code>.github/copilot-instructions.md</code> for Copilot. The file "
      "drives autonomous actions, which is why it is committed and reviewed rather than personal.</p>")}
<div class="note"><p><strong>One thing worth funding centrally on day one:</strong> the model gateway. It is
unglamorous, it takes a fortnight, and without it a surprise invoice is a mystery rather than a diagnosis.</p></div>
<p class="lalt">Try it: <a href="../simulator/#/effort">which level fits which task</a>, an exercise per department in the simulator.</p>
</div>"""


def _one_page() -> str:
    points = [
        ("Most of your backlog is not AI work.",
         "Three questions settle it: is there a genuine judgement call, is the volume high enough, "
         "and is a wrong answer recoverable. Expect two or three of your top five to come back as "
         "rules that code does better, cheaper and provably.",
         "A rule with published criteria is a <code>CASE</code> statement. Putting a model on it adds "
         "a token bill, an evaluation harness, gates and a probability of being wrong, and buys "
         "nothing. The AI-fit record is what lets a team decline an agent-first directive with "
         "evidence rather than as an opinion."),
        ("“It works” stops being a yes or a no.",
         "It becomes a number per kind of case, derived from what a mistake costs. You will be asked "
         "to accept 80% on one slice and require a person on another, and both can be correct.",
         "The bar is <code>damage ÷ (damage + saving)</code>, per slice. A human hold on the risky "
         "step lowers the damage and therefore lowers the bar, which is how a feature ships safely "
         "at 71% instead of waiting for a 98% nobody will reach."),
        ("Autonomy is decided per action, and it follows reversibility.",
         "Not per product, and never from what the model is capable of. Showing options and moving "
         "money are different decisions and belong at different levels.",
         "A cap written in a prompt is a request a model can be talked past. A cap written into the "
         "tool's signature raises and cannot be argued with. The difference is invisible on a slide "
         "and total in production."),
        ("A first cycle can save real time and cost more.",
         "That is survivable if it reaches you from the team. It is fatal if it reaches you from "
         "finance. Insist on two numbers from cycle one.",
         "Time saved and money spent, with two rows that keep them honest: review hours added, which "
         "is high early and falls, and re-runs, which is the leak signal. Cost turns positive from "
         "cycle two as the artefacts sharpen."),
        ("Maturity is control, not tool count.",
         "A team with nine AI tools and no gates is less mature, ships less safely and costs more "
         "than a team with one tool and tight control.",
         "Six controls, each present or absent: a context file, a spec with a bar and an owner, a "
         "harness gating the merge per slice, caps in tool signatures, a redacting trace, and "
         "production evidence by segment with drift watched."),
    ]
    rows = "".join(
        f'<div class="card"><h3 class="h4">{E(t)}</h3><p>{b}</p><p class="mech"><b>Why:</b> {w}</p></div>'
        for t, b, w in points)
    return f"""<div class="sec" id="claims">
<h2>Five things that change, in one sentence each</h2>
<div class="claims">{rows}</div>
</div>"""


def _changes() -> str:
    rows = [
        ("Deciding what is worth building", "Unchanged", "The judgement is yours and always was"),
        ("Writing down what it must do", "<b>Changed</b>",
         "A machine now reads it and cannot ask what you meant, so ambiguity becomes defects"),
        ("Knowing when it is finished", "<b>Changed</b>",
         "A measured share per slice, with a confidence bound, replaces a yes or a no"),
        ("Estimating and planning", "Mostly unchanged",
         "The unit shrinks from a two-week sprint to a day, because building is faster than reviewing"),
        ("Reviewing work before it ships", "<b>Changed</b>",
         "Depth follows the risk of the action, not the size of the change. More is produced; the "
         "same people read it"),
        ("Releasing", "<b>Changed</b>",
         "Run beside the humans first, then five percent, then widen on evidence rather than on a date"),
        ("Security", "Mostly unchanged",
         "Least privilege still applies. One genuinely new threat: everything the agent reads can "
         "act as an instruction"),
        ("Knowing it still works next quarter", "<b>Changed</b>",
         "Behaviour drifts with no deploy and no error, so it is watched like a business metric"),
        ("Accountability", "Unchanged",
         "A gate is a person's name against a decision. No model holds one"),
    ]
    body = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f"""<div class="sec" id="changes">
<h2>What changes in your organisation, and what does not</h2>
<p class="wide">Less than the market implies, and in sharper places. The honest list, so nobody has to rebuild a working
discipline to adopt this.</p>
<div class="tw" tabindex="0"><table><thead><tr><th>Activity</th><th>Verdict</th><th>Why</th></tr></thead>
<tbody>{body}</tbody></table></div>
<div class="note"><p><strong>The pattern.</strong> Everything that changed, changed because part of
the product is now probabilistic. Everything that did not, did not. If a proposal in front of you
changes something in the unchanged column, ask what it is actually solving.</p></div>
</div>"""


def _operating_model() -> str:
    roles = [
        ("Product manager", "product-manager", "var(--slate)",
         "Decides what is worth doing and what counts as good enough",
         "Owns the intent and release gates, autonomy per action, and the acceptance bar per slice",
         "Stops approving pull requests. Starts deriving a bar from what a mistake costs."),
        ("Solution architect", "solution-architect", "var(--ochre)",
         "Decides the shape, and which steps may be probabilistic at all",
         "Owns the exact/best-guess map, the authority budget, and the decision records",
         "Stops specifying model settings. Starts specifying behaviours and where the caps live."),
        ("Engineering lead", "engineering", "var(--sage)",
         "Builds it, and makes the boundary real in code",
         "Owns the context file, the harness in CI, and caps inside tool signatures",
         "Stops treating a prompt rule as a control. Starts shipping a slice a day."),
        ("QA lead", "qa", "var(--plum)",
         "Says whether it actually works, with a number",
         "Owns the behaviour and expansion gates, the golden set, and the injection suite",
         "Stops signing off on a demo. Starts reporting a lower bound, not a score."),
        ("DevOps and platform", "devops", "var(--violet)",
         "Makes it repeatable, observable and reversible",
         "Owns the gateway, the per-call log, the trace and the rollback",
         "Stops treating a prompt as config. Starts treating it as a deployable artefact."),
    ]
    cards = []
    for name, slug, colour, one, owns, shift in roles:
        cards.append(
            f'<div class="card" style="--rc:{colour};border-left:3px solid {colour}">'
            f'<h3 class="h4" style="color:{colour}">{E(name)}</h3>'
            f'<p style="font-size:14.5px;margin-bottom:10px">{E(one)}</p>'
            f'<p style="font-size:14px;margin:0 0 6px"><strong>The shift:</strong> {E(shift)}</p>'
            f'<p style="font-size:14px;margin:0 0 10px"><strong>Owns:</strong> {E(owns)}</p>'
            f'<p style="font-size:13.5px;margin:0"><a href="../{slug}/">Their eight steps →</a></p></div>')
    return f"""<div class="sec" id="who">
<h2>Who does what, and the boundary that moves</h2>
<p class="wide">Five roles. None of them is new, and none of them disappears. What moves is the boundary between
them, and the two places it moves are worth knowing: <strong>the product manager stops approving
things they cannot evaluate</strong>, and <strong>QA gains a veto that is arithmetic rather than
opinion</strong>.</p>
<div class="roles" style="grid-template-columns:repeat(auto-fit,minmax(252px,1fr))">{''.join(cards)}</div>
<div class="note"><p><strong>The sixth role is yours.</strong> Governance spans the whole lifecycle
and no delivery role owns it. If nobody is asking the four questions below every cycle, nobody is.</p></div>
</div>"""


def _decisions() -> str:
    from . import calcs
    bar = calcs.render("bar")
    value = calcs.render("value")

    return f"""<div class="sec" id="decisions">
<h2>The four decisions only you can make</h2>
<p class="wide">Delivery decisions belong to delivery. These four do not, because each one trades a business risk
against a business return, and the trade is yours.</p>

<h3>1 · Which work is genuinely AI work</h3>
{pair(
    "<p>Ask it of the roadmap, not of one feature, and expect most of it to come back as rules. A "
    "team under an agent-first directive will build agents for things a rule does better and will "
    "not tell you, because you asked for agents.</p>",
    "<p>Three questions in order, and the first “no” ends it. Is there a genuine judgement "
    "call: could two competent people differ? Is the volume high enough to carry evaluation, gates "
    "and a harness? Is a wrong answer recoverable? Only yes-yes-yes is fully agentic; the rest is "
    "code, a person, or an assisted mix with the unrecoverable steps gated.</p>")}
<p class="wide"><strong>Ask for:</strong> an AI-fit record per candidate, with the rejected alternative and why.
<strong>Healthy answer:</strong> two or three of your top five are rules.</p>

<h3>2 · What the agent may do without a person</h3>
{pair(
    "<p>Per action, never per product, and it follows what a mistake costs and whether you can undo "
    "it. Set it per product and you force everything to the strictness of the riskiest action, or, "
    "worse, to the looseness of the safest.</p>",
    "<p>Five rungs: acts alone, acts monitored, acts inside a veto window, named approver every "
    "time, not delegated at all. Reversibility is the hinge. Levels rise on evidence, one step at a "
    "time, and an incident drops the level of the action involved automatically.</p>")}
<p class="wide"><strong>Ask for:</strong> the autonomy record, and then the follow-up that matters,
<em>show me the cap</em>. If somebody opens a prompt file, you have found a gap.</p>

<h3>3 · What you will accept as evidence</h3>
{pair(
    "<p>This is the decision that most often goes by default. If you accept a demo, you will be "
    "shown demos. If you accept a single accuracy figure, the slice carrying the risk will hide "
    "inside the average.</p>",
    "<p>Accept a score per slice against a derived bar, reported with its lower bound, plus a "
    "shadow-run comparison against the humans doing the work today. Reject any single headline "
    "number, and reject a score quoted without its sample size.</p>")}
{bar}
<p class="wide"><strong>Read it this way:</strong> the bar is not a target somebody chose. It falls out of what a
mistake costs. Push the third slider. That is a person checking the work before it takes effect,
and it is why a gate is a commercial instrument rather than a brake.</p>

<h3>4 · What you will fund past cycle one</h3>
{pair(
    "<p>A first cycle that saves time and costs more is normal. Funding it past that point should "
    "depend on a trajectory, not a promise: the review load falling, and the re-run count falling "
    "with it.</p>",
    "<p>The value line nets the token cost and the review load off the gross saving. Review is high "
    "in cycle one because the artefacts are rough; it falls as specs, bars and context files "
    "sharpen. If it does not fall by cycle three, the artefacts are the problem, not the model.</p>")}
{value}
<p class="wide"><strong>The term to watch is review.</strong> Drag it and you will see why a pilot that worked can
stop working at scale: saving and token cost both scale with volume, and the review load only falls
if somebody is deliberately making it fall.</p>
</div>"""


def _knowing() -> str:
    controls = [
        ("A context file the agent reads",
         "It exists in the repository and was updated this month"),
        ("Every item has a spec, a bar and a named owner",
         "Pick a story at random and look"),
        ("The harness gates the merge, per slice",
         "Ask: what happens if one slice regresses and the average still rises?"),
        ("Caps live in tool signatures, not prompts",
         "Ask to be shown the cap. Somebody opens code, not prose"),
        ("The trace redacts", "Ask whether a passport number could be in a log"),
        ("Production evidence by segment, with drift watched",
         "Ask what automatically re-opens the release gate"),
    ]
    chk = k.check(controls,
                  ["Level 0 (nothing is enforced yet",
                   "Level 1) assisted; one team, no gates",
                   "Level 2 (specified; the work is written down",
                   "Level 3) governed; the gates hold",
                   "Level 4: evidence-led; production proves it"],
                  "Tick only what you could be shown in ten minutes.")
    questions = [
        ("Which of these are rules?", "The roadmap, not one feature",
         "Two or three of the top five come back as rules, on record"),
        ("What may it do without a person, and who decided?", "Per action, with a reversibility column",
         "Someone opens a tool signature when you ask to see the cap"),
        ("What are the two numbers?", "Every cycle, together",
         "Person-days saved and money spent, with review hours and re-runs beside them"),
        ("What level are we, and what is the next control?", "Not how many tools we adopted",
         "A number out of six, and the name of the first missing one"),
    ]
    qrows = "".join(f'<tr><td><strong>{E(q)}</strong></td><td>{E(a)}</td><td>{E(g)}</td></tr>'
                    for q, a, g in questions)
    return f"""<div class="sec" id="knowing">
<h2>How you will know it is working</h2>
<p class="wide">Four questions, asked consistently, and most of the failure modes in this manual cannot survive in
your organisation. They take ten minutes a cycle.</p>
<div class="tw" tabindex="0"><table><thead><tr><th>Ask</th><th>Of what</th><th>A good answer looks like</th></tr></thead>
<tbody>{qrows}</tbody></table></div>

<h3>The maturity check, in ten minutes</h3>
{pair(
    "<p>Tool adoption is the metric that rewards the least mature behaviour available. This is the "
    "replacement: six controls that a team either has or does not, each verifiable by asking to be "
    "shown it.</p>",
    "<p>The level is the count. It is deliberately unweighted, so a team can read as level four with "
    "the two hardest controls missing, read the list, not the number. The next control to build is "
    "always the first unticked one.</p>")}
{chk}

<h3>The report you should receive</h3>
<div class="tw" tabindex="0"><table><thead><tr><th><span class="vh">Measure</span></th><th>Baseline</th><th>Now</th><th>Change</th></tr></thead>
<tbody>
<tr><td>Person-days per story</td><td>8.0</td><td>4.6</td><td><strong>−43%</strong></td></tr>
<tr><td>Token spend per story</td><td>, </td><td>$310</td><td></td></tr>
<tr><td>Review hours added per story</td><td>1.2</td><td>2.0</td><td>+0.8</td></tr>
<tr><td>Re-runs per story</td><td>, </td><td>1.4</td><td></td></tr>
</tbody></table></div>
<p class="wide">Three rules make that table trustworthy. The <strong>baseline is taken before the pilot</strong>,
which costs an afternoon and is unrecoverable afterwards. The <strong>review row stays visible</strong>,
or cycle two reads as a regression when it is the recovery. And the <strong>re-run row stays
visible</strong>, because it is where leaks appear first.</p>
<div class="note warn"><p><strong>The failure mode to name out loud.</strong> Every cycle shows time
saved, none shows spend, and eventually finance computes the token bill independently and arrives at
a review with a number nobody in the programme has seen. The credibility of the first number dies
with the second. This is usually done by people trying to protect the programme.</p></div>
</div>"""


def _rollout() -> str:
    steps = [
        ("Days 1 to 15 · Pick the wrong-looking thing",
         "<p><strong>Choose one feature, and choose it for provability rather than for value.</strong> "
         "The instinct is to start where the prize is largest, which is usually the hardest slice, "
         "the one that cannot clear its bar and cannot be proven inside a quarter.</p>"
         "<ul class='ticks'>"
         "<li>Run the three AI-fit questions across the top ten candidates. Publish the ones that "
         "came back as rules, that list is the most credible thing you will circulate all year</li>"
         "<li>Pick a feature with high volume, low damage per mistake, and an existing human process "
         "to compare against</li>"
         "<li><b>Take the baseline now.</b> Person-days per story, today, before anything changes. "
         "An afternoon, and it cannot be recovered later</li></ul>"
         "<p><strong>The trap:</strong> starting with the flagship. It has the highest bar, the "
         "least tolerance for a first attempt, and the most spectators.</p>"),
        ("Days 15 to 30 · Write the artefacts nobody wants to write",
         "<p><strong>This fortnight produces documents, and it is the fortnight that decides the "
         "outcome.</strong> Teams skip it because it feels like overhead beside a working demo.</p>"
         "<ul class='ticks'>"
         "<li>The eight-field spec. Five of the eight will be undecided, and those five <em>are</em> "
         "the value of the exercise</li>"
         "<li>The acceptance bar per slice, derived from damage and saving</li>"
         "<li>The authority budget: what the agent may do alone, per action</li>"
         "<li>A context file in the repository, so every session starts informed</li></ul>"
         "<p><strong>The trap:</strong> a demo exists by now and it is persuasive. A demo is the easy "
         "20%. What it cannot tell you is how often it is wrong on the cases you did not choose.</p>"),
        ("Days 30 to 60 · Build in slices, prove in CI",
         "<p><strong>A shippable slice a day, each one proven before the next.</strong> The point is "
         "not speed; it is that a wrong turn costs one day instead of a fortnight.</p>"
         "<ul class='ticks'>"
         "<li>Day one is a walking skeleton with no model in it, to prove the pieces connect</li>"
         "<li>Caps move out of prompts and into tool signatures, with two tests each</li>"
         "<li>The golden set reaches fifty real cases, tagged by slice, running in CI</li>"
         "<li>Review routes by risk band, from a path rule rather than from an argument</li></ul>"
         "<p><strong>What you should see:</strong> something merged most days. If the demo is still "
         "the only evidence at day 45, the slices are not slices.</p>"),
        ("Days 60 to 90 · Prove it beside the humans",
         "<p><strong>Run it next to the people doing the work, deciding but never acting.</strong> "
         "You cannot reason your way to knowing whether it agrees with them.</p>"
         "<ul class='ticks'>"
         "<li>Shadow for a fixed window agreed in advance, compared per slice and read daily</li>"
         "<li>Money actions stay gated regardless of what the shadow shows</li>"
         "<li>Rehearse the rollback before the cut-over, not during</li>"
         "<li>Cut over at five percent and widen on live evidence rather than on a date</li></ul>"
         "<p><strong>If it does not match, you learned that for free</strong>, which is the whole "
         "argument for the window.</p>"),
        ("Day 90 onward · Report honestly, and let production set the agenda",
         "<p><strong>Two numbers, both of them, from the first cycle.</strong> Then the loops that "
         "most organisations never close.</p>"
         "<ul class='ticks'>"
         "<li>Cost is a design question, not a finance escalation, a surprise bill closes back into "
         "the design, and the fix order is arithmetic</li>"
         "<li>An incident produces a control, a record and a brief, never a name</li>"
         "<li>Drift is watched weekly like any business metric, and an alert re-opens the release "
         "gate automatically</li>"
         "<li>Re-run the maturity check each quarter and build the first missing control</li></ul>"
         "<p><strong>The signal that it took:</strong> the second feature needs less of your "
         "attention than the first, because the artefacts now exist to copy.</p>"),
    ]
    return f"""<div class="sec" id="rollout">
<h2>Ninety days to a running operating model, without the organisation rejecting it</h2>
<p class="wide">This is the sequence that works, and each phase has one trap that reliably catches capable teams.
It is deliberately unglamorous in the middle.</p>
{k.stepper(steps, "The ninety-day rollout")}

<h3>The resistance you will actually meet</h3>
<div class="tw" tabindex="0"><table><thead><tr><th>What you will hear</th><th>What is underneath</th><th>What answers it</th></tr></thead><tbody>
<tr><td>"This slows us down"</td><td>Usually true for the first feature, and untrue by the third</td>
<td>Show the artefacts being reused. The second spec takes an hour</td></tr>
<tr><td>"The model is good enough already"</td><td>Judged on curated examples</td>
<td>Ask for the score on the slice nobody picked, with its sample size</td></tr>
<tr><td>"We already have gates"</td><td>Approvals, not gates, clicks without evidence</td>
<td>Ask what evidence was in front of the last approver, and what would have made them say no</td></tr>
<tr><td>"Engineering says the cap is handled"</td><td>Handled in a prompt</td>
<td>Ask to be shown it. Prose or code decides the answer</td></tr>
<tr><td>"We cannot measure a baseline, we have started"</td><td>True, and recoverable on the next feature</td>
<td>Say so in the report rather than being caught. Then take one next time</td></tr>
<tr><td>"Our people will resist automation"</td><td>Often the opposite: they resist being measured by it</td>
<td>Put the frontline in discovery first, and credit their requirements by name</td></tr>
</tbody></table></div>

<div class="note"><p><strong>The change-management move that does most work</strong> is unglamorous:
credit every requirement to the person who raised it, in writing, before consolidating any of them.
A voice that felt dropped in week one comes back in week five as a constraint, and it arrives with
the authority of someone who was ignored.</p></div>
</div>"""


def _tooling() -> str:
    rows = [
        ("Everyone, any function", "A chat surface",
         "Drafting, summarising, restructuring, arguing with a plan",
         "No access to systems. Treat output as a draft by a capable stranger",
         "Nothing enters it that you would not email externally"),
        ("Product, architecture, analysis", "A chat surface with your documents",
         "Consolidating discovery, converting prose to testable criteria, building the arithmetic",
         "Read-only. It proposes; a person decides and signs",
         "Named documents only, never the whole drive"),
        ("Engineering", "An editor agent: Claude Code, Codex, Copilot",
         "Multi-file changes, failing-test loops, building from a story file",
         "Reads a committed context file. Changes arrive as reviewable diffs",
         "Review by risk band. Money paths get two readers, always"),
        ("Engineering and platform", "An agent in your product",
         "The thing you are actually building",
         "Caps and confirmations in tool signatures. Reads open, writes gated",
         "Every consequential action leaves a redacted trace row"),
        ("Platform", "A model gateway in front of all of it",
         "Routing, budgets, fallbacks, and one per-call log",
         "Not optional at scale: without the log you cannot diagnose a bill",
         "Cost attributable per feature, not per team"),
    ]
    body = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td><td>{E(c)}</td>"
                   f"<td>{E(d)}</td><td>{E(e)}</td></tr>" for a, b, c, d, e in rows)
    return f"""<div class="sec">
<h2>Tooling, by level</h2>
<p class="wide">The specific products change every quarter and the shape does not. Four levels, each with a
different blast radius, and the governance is what separates them, not the vendor.</p>
<div class="tw" tabindex="0"><table><thead><tr><th>Who</th><th>What</th><th>For</th><th>The control on it</th>
<th>The rule</th></tr></thead><tbody>{body}</tbody></table></div>

{pair(
    "<p><strong>The decision you should take centrally</strong> is that "
    "every model call in production passes through one layer you own, so that routing, budgets and "
    "the per-call log exist in one place. Teams can then choose their own editor.</p>",
    "<p>A coding assistant's configuration file is read at session start: <code>CLAUDE.md</code> for "
    "Claude Code, <code>.github/copilot-instructions.md</code> for Copilot, <code>AGENTS.md</code> "
    "for Codex. Copilot's steers inline suggestions; Claude Code's drives autonomous actions, the "
    "same sentence carries more weight in the second case, which is why the file is committed and "
    "reviewed rather than personal.</p>")}

<div class="note"><p><strong>One thing worth funding centrally on day one:</strong> the model
gateway. It is unglamorous, it takes a fortnight, and without it a surprise invoice is a mystery
rather than a diagnosis. Every cost story in this manual depends on a per-call log existing.</p></div>
</div>"""


def _redflags() -> str:
    flags = [
        ("A single accuracy number in a board pack",
         "The slice carrying the risk is small, and small slices vanish into averages",
         "Ask for the score per slice, with its sample size"),
        ("A cap that lives in a prompt",
         "It is a request, and a model can be talked past a request",
         "Ask to be shown the cap. Prose or code decides it"),
        ("A launch date agreed before a shadow run",
         "The date will win the argument against the evidence, every time",
         "Make the window a condition, not a milestone"),
        ("Tool adoption reported as maturity",
         "It rewards the least mature behaviour available",
         "Replace it with the six controls"),
        ("A postmortem that produced a name",
         "The same class of incident will return, worded differently",
         "Ask which enforced control would have made it impossible"),
        ("A cost number that arrived from finance",
         "The team either did not know or did not say. Both are worse than the number",
         "Two numbers, from the team, from cycle one"),
        ("Boards that stopped moving while submissions continue",
         "Something silently stopped reporting, which is how drift hides",
         "Ask when the last row was written"),
    ]
    body = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td><td>{E(c)}</td></tr>"
                   for a, b, c in flags)
    return f"""<div class="sec" id="escalate">
<h2>Seven things to escalate on</h2>
<p class="wide">None of these is a failure. Each is a signal that a decision is being made by default, somewhere
below the level that should be making it.</p>
<div class="tw" tabindex="0"><table><thead><tr><th>Signal</th><th>Why it matters</th><th>The question</th></tr></thead>
<tbody>{body}</tbody></table></div>
</div>"""


def _first30() -> str:
    return f"""<div class="sec" id="first30">
<h2>Your first thirty days</h2>
<p class="wide">Six actions, in order, none of which needs a budget approval.</p>
<ol class="acts acts2">
<li><b>Ask the four questions at the next review.</b><span>Which of these are rules · what may it do
without a person, and who decided · what are the two numbers · what level are we and what is the
next control. Then say nothing for ten seconds.</span></li>
<li><b>Ask to be shown one cap.</b><span>Pick any limit the team says is enforced. If somebody opens
a prompt file rather than a code file, you have found the gap that produces incidents.</span></li>
<li><b>Take a baseline on whatever starts next.</b><span>Person-days per story, today. An afternoon,
and it is unrecoverable once the pilot begins.</span></li>
<li><b>Run the six-control check yourself</b><span>with the team in the room, ticking only what can
be shown in ten minutes. The number matters less than the argument it starts.</span></li>
<li><b>Name who owns governance.</b><span>It spans the whole lifecycle and no delivery role owns it.
If the answer is "we all do", nobody does.</span></li>
<li><b>Fund the gateway.</b><span>A fortnight of platform work that turns every future cost
conversation from a mystery into a diagnosis.</span></li>
</ol>
<div class="note"><p><strong>What none of this asks for.</strong> No reorganisation, no new function,
no platform migration, no vendor commitment. The whole protocol is a set of artefacts and four
questions, and the artefacts are each about an afternoon's work.</p></div>
</div>"""


def build(shell, urls: dict) -> str:
    body = ("<div class=\"wrap\"><main id=\"main\" style=\"padding:34px 0 28px\">"
            + _hero() + _why() + _one_page() + _teams() + _money() + _changes() + _operating_model()
            + _frameworks_exec() + _decisions() + _knowing() + _llms() + _rollout() + _redflags() + _first30()
            + f"""<div class="sec" style="border-top:1px solid var(--rule);padding-top:26px">
<h2>Where to send people</h2>
<div class="tw" tabindex="0"><table><thead><tr><th>They own</th><th>Send them to</th></tr></thead><tbody>
<tr><td>What gets built and whether it shipped safely</td><td><a href="../product-manager/">The product manager's eight steps</a></td></tr>
<tr><td>The shape of the system and what may be probabilistic</td><td><a href="../solution-architect/">The architect's eight steps</a></td></tr>
<tr><td>Building it, and the boundary in code</td><td><a href="../engineering/">The engineering lead's eight steps</a></td></tr>
<tr><td>Whether it actually works, with a number</td><td><a href="../qa/">The QA lead's eight steps</a></td></tr>
<tr><td>Making it repeatable, observable and reversible</td><td><a href="../devops/">DevOps and platform's eight steps</a></td></tr>
<tr><td>Wanting the artefacts, not the argument</td><td><a href="../templates/">40 templates</a> · <a href="../prompts/">116 prompts</a></td></tr>
<tr><td>Wanting to see it happen to somebody else first</td><td><a href="../simulator/#/story">The simulator's thirteen episodes</a>: the worked case, playable</td></tr>
<tr><td>Chairing a gate, and wanting to know what may halt it</td><td><a href="../simulator/#/governance/gv-gates">The gates, in the simulator</a> · <a href="../simulator/#/evidence">what a complete evidence pack holds</a></td></tr>
<tr><td>Wanting the maturity conversation with a number</td><td><a href="../simulator/#/toolkit/maturity">The maturity self-check</a> · <a href="../simulator/#/toolkit/aifit">is this work for a model at all?</a></td></tr>
</tbody></table></div></div></main></div>""")
    desc = ("For executives and business owners: why agentic product development changes your economics and risk, "
            "how every team is transformed by P0 to P3, where the money is, the four decisions only leadership "
            "makes, LLMs at three levels, and the 90-day rollout.")
    tour = k.tour([
        {"sel": ".claims", "title": "Five things that change", "body": "One sentence each, with the reason underneath. Every claim on this page shows what it means and how it works side by side; nothing is behind a toggle."},
        {"sel": "[data-score]", "title": "The six-control check", "body": "Tick what the team can show in ten minutes. The number is your maturity level; the next unticked box is the next control to fund."},
        {"sel": ".stp", "title": "Ninety days, step by step", "body": "A rollout you can walk: one panel per stage, with the trap each stage sets."},
    ])
    return shell(title="The agentic operating protocol · for whoever owns the P&L",
                 desc=desc, body=body, depth=1, nav_id="protocol",
                 canonical=urls["base"] + "protocol/",
                 crumbs=[("For leadership", "")], tour=tour, kind="protocol", og="protocol")
