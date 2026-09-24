# Playbook glossary

Terms as this playbook uses them, with a confidence mark on each:
**documented** (from a vendor's published documentation, read on a date) ·
**established** (a named, published practice with an author and a year) ·
**working method** (this playbook's construction — a default to tune).

A glossary earns its place through its **distinctions**, not its definitions. Nobody misuses a word
they have never heard. The expensive mistakes come from two words a room treats as one — a request
and an enforced control, a score and a lower bound, a gate and an approval — and the cost lands
weeks later, in a postmortem, in an invoice, or in a release that was never actually proven.

So the terms that appear in a formula, a gate or a control get a full entry: the definition
tightened to one line, the confusion named, one link into the page where you meet the term, and a
pair of sentences showing the term said wrongly and said rightly. The remaining terms keep their
one-line definition in [a table at the end](#everything-else-briefly).

Where the industry definition is contested, the contested part is said out loud.

The curriculum's wider glossary is
[docs/concepts/glossary.md](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/concepts/glossary.md);
this page is the playbook's own vocabulary.

---

## The distinctions that cost the most

| The confusion | What it costs | Entry |
| --- | --- | --- |
| A **request** read as an **enforced control** | Four layers claimed in the postmortem, one of them real | [Enforced control](#enforced-control--working-method) |
| A **score** read as a **lower bound** | A bar declared proven on forty cases | [Lower bound](#lower-bound--established) |
| A **gate** treated as an **approval** | A signature with no evidence in front of it | [Gate](#gate--established) |
| **Exact** used to mean **deterministic** | A best-guess step gets a unit test and no measured share | [Deterministic (exact)](#deterministic-exact--established) |
| A **slice** treated as a **segment** | One average hides the slice that is failing | [Slice](#slice--working-method) |
| **Drift** reported as a **regression** | A rollback that restores nothing, because nothing was deployed | [Drift](#drift--established) |
| An **agent** built where a **workflow** was wanted | Hand-offs, loops and a bill, for a decision an `if` could make | [Agentic](#agentic--established) |
| **Retries** counted as **attempts** | The bill model misses a whole pass per conversation | [Circuit breaker](#circuit-breaker--established) |
| A **bar** negotiated like a **target** | The refund slice ships at 85% | [Acceptance bar](#acceptance-bar--working-method) |
| A **trace** assumed to be a **log** | An audit question nobody can answer from what was kept | [Trace](#trace--established) |
| A **golden set** run as a **test suite** | Green means the cases ran, not that the bar held | [Golden set](#golden-set--established) |
| **Cost per case** quoted as **cost per call** | A three-call case looks a third of its price | [Cost per case](#cost-per-case--working-method) |

---

## A–C

### Acceptance bar · **working method**

**In one line** — the success rate a best-guess step must clear to be worth running unaided:
`N = damage ÷ saving`, then `bar = N ÷ (N + 1)`, set per slice and never per feature.

**The distinction that matters** — a bar is not a **target** and not an SLA. A target is something
you would like to reach and may miss without consequence; a bar is the line below which the step is
not worth running at all, and it is *derived* from money rather than chosen. The confusion is
expensive because a target gets negotiated down in a Friday release meeting, whereas a bar moves
only by changing the damage.

**Where you meet it** — [How to Prove the Bar](How-to-Prove-the-Bar), move 1 ·
[the bar calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/bar)

> **Said wrongly** — "Let's set the accuracy target at 90% and see how close we get."
>
> **Said rightly** — "Refunds carry $600 of damage against $12 of saving, so the bar is 98%. That is
> a design signal, not a goal: put a hold on it and the bar becomes 71%."

### ADR (architecture decision record) · **established**

**In one line** — one decision with its context, its consequences and what it rejected, numbered and
versioned next to the code, written only at a trade-off point. Nygard, 2011.

**The distinction that matters** — a record is not the **decision**, and it is not minutes. Minutes
say what was said; a record says what was chosen, what was given up, and what would re-open it. The
expensive habit is one for every decision: forty records in a week buries the three that mattered.
The opposite habit costs more — the model-tier question re-opened in week three with no record.

**Where you meet it** — [How to Choose Build, Buy or Borrow](How-to-Choose-Build-Buy-or-Borrow),
move 5

> **Said wrongly** — "We should have an ADR for each ticket so the decisions are traceable."
>
> **Said rightly** — "Three sensitivity points came out of the workshop, so there are three records,
> and each one names the condition that re-opens it."

### Agentic · **established**

**In one line** — software that decides and acts rather than following fixed steps; the word that
separates a rule-based system from one with a model in the loop.

**The distinction that matters** — an **agent** is not a **workflow**. A workflow has its path
decided at design time and a model may write text at one of its nodes; an agent chooses the next
step at run time, which is what makes it useful and what makes it expensive to prove. Building one
where a workflow was wanted buys hand-offs, loops and a bill for a decision an `if` could make.

**Where you meet it** — [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper), move 1 ·
[the AI-fit check](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/aifit)

> **Said wrongly** — "We are building an agent that validates the form and posts it to the queue."
>
> **Said rightly** — "That path is fixed and every branch is knowable, so it is a workflow with one
> model call inside it. We are not paying for an agent to do it."

### Authority budget · **working method**

**In one line** — what the agent may change, touch or commit, decided before what it may spend.

**The distinction that matters** — authority is not **cost**. A cheap task with broad authority is
more dangerous than an expensive one with none, and the two are owned by different people: finance
owns the spend, the accountable engineer owns the authority. Conflate them and you cap tokens, feel
governed, and leave an agent able to write to production.

**Where you meet it** — [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary),
move 1

> **Said wrongly** — "It is a small job, so we gave it the same credentials as the service."
>
> **Said rightly** — "It reads three tables and writes one, and the write needs a confirmation
> token. Spend is a separate limit and a separate owner."

### Best-guess (probabilistic) · **established**

**In one line** — work a model does that is right a share of the time and never every time, proven
by measuring the share on real cases.

**The distinction that matters** — best-guess is not **broken**, and it is not **nearly exact**.
A step right 88% of the time is working as designed, and the question is whether 88% clears the bar
for that slice. Read it as broken and you spend a quarter chasing determinism; read it as nearly
exact and you ship with a unit test and no measured share.

**Where you meet it** — [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper), move 2

> **Said wrongly** — "It failed on three of the demo cases, so it is not ready."
>
> **Said rightly** — "Three failures in forty is a 92.5% point estimate; the lower bound is 80.5%,
> which does not yet prove the 85% bar."

### Bolt · **working method**

**In one line** — a thin, shippable slice reviewed and integrated the same day, carrying exactly one
unknown. The term comes from AWS's AI-DLC; **one unknown per bolt** is this playbook's rule.

**The distinction that matters** — a bolt is not a **small story**. A story is cut by priority and
sized by effort; a bolt is cut by **dependency** and sized by what can be integrated before the day
ends. Cutting the sprint's stories smaller and calling them bolts produces the same integration
cliff a week later, because the ordering was never changed. The test is not "is this small" but
"can this be built today without waiting for anything, and what one thing will it tell us?"

**Where you meet it** — [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts), move 2 ·
[the bolt planner](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/bolts)

> **Said wrongly** — "We have broken the sprint into fourteen bolts, ordered by business value."
>
> **Said rightly** — "Ordered by dependency: the skeleton first because it retires the largest
> unknown, then the two that unblock everything else."

### Cache (prompt cache) · **documented**

**In one line** — reusing the processed prefix of a prompt instead of re-paying for it; an exact
prefix match in the order tools → system → messages, up to a marked block, model-scoped, with
break-even at the second use.

**The distinction that matters** — a prompt cache is not a **response cache** and not a semantic
one. Nothing is remembered and no answer is reused: the only saving is re-reading an identical
prefix. One volatile token in the cached block — a timestamp, a session id, a shuffled tool list —
invalidates everything after it and turns the saving into a 1.25× surcharge, and because the cache
is model-scoped, switching model mid-task starts from cold.

**Where you meet it** — [How to Control the Token Bill](How-to-Control-the-Token-Bill), move 4 ·
[the cache calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/cache)

> **Said wrongly** — "Caching is on, so the repeat questions are basically free."
>
> **Said rightly** — "The prefix is stable and hit 71% last week. The answers are recomputed every
> time — what we stopped paying for is re-reading the 9,000-token preamble."

### Checker (inspector) · **established**

**In one line** — an independent model, or the same model in a fresh context with an adversarial
brief, placed after a generating step. Never the drafter grading itself.

**The distinction that matters** — a checker is not a **second opinion from the same context**.
A model asked "is that right?" in the conversation that produced the answer agrees with itself at a
rate that tells you nothing, and the independence is cheap to lose by accident. Nor is it a
[judge](#judge-llm-as-a-judge--established): a checker hunts one failure, a judge scores a rubric.

**Where you meet it** — [How to Prove the Bar](How-to-Prove-the-Bar), move 3

> **Said wrongly** — "We ask it to double-check its own answer before returning it."
>
> **Said rightly** — "A fresh context gets the output and the policy, with no sight of the
> reasoning, and its brief is to find the violation rather than to confirm."

### Circuit breaker · **established**

**In one line** — a maximum number of agent reasoning loops, then a hard stop and a hand-off to a
person. Five is a common working value.

**The distinction that matters** — a breaker counts **loops**, not seconds, and this is where
**retries** and **attempts** part company. Cost models work on attempts — `1 + retries` — because a
conversation with no retries still costs one pass, so "three retries" permits four. A timeout is a
different control: a loop that spins fast stays inside it and burns the budget anyway.

**Where you meet it** — [How to Control the Token Bill](How-to-Control-the-Token-Bill), move 5

> **Said wrongly** — "We allow three retries, so worst case it costs three times a normal call."
>
> **Said rightly** — "Three retries is four attempts, so the worst case is 4×, and `MAX_LOOPS = 5`
> stops the loop rather than the clock."

### Compounding (pⁿ) · **established**

**In one line** — chained steps multiply rather than average: four steps at 90% is 66% end to end.

**The distinction that matters** — the arithmetic everyone reaches for is the **average**, and the
average of four 90% steps is 90%, which is wrong by twenty-four points. `pⁿ` is also the
**optimistic** bound, because real steps correlate, so a measured rate below it is correlation
rather than a mystery. Removing a step buys more than improving one.

**Where you meet it** — [Formulas and Calculators](Formulas-and-Calculators) ·
[Journey: Solution architect](Journey-Solution-Architect)

> **Said wrongly** — "Every step is at least 90%, so the pipeline is about 90% accurate."
>
> **Said rightly** — "Six steps at 90% is 53% end to end, and that is the generous reading. We are
> shortening the chain before we tune anything."

### Consequential step · **working method**

**In one line** — a step that changes something real, built as a tool plus a gate and proven by a
required confirmation.

**The distinction that matters** — consequential is not **important**. Importance is how much the
business cares; consequence is whether the world changes and whether it changes back cheaply. A
board summary is important and reversible; a $40 fee waiver is unglamorous and irreversible.
Classifying by importance guards the visible work and leaves the money path unheld.

**Where you meet it** — [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper), move 2

> **Said wrongly** — "The refund tool is low risk — it is only small amounts."
>
> **Said rightly** — "It moves money and it cannot be undone without a customer conversation, so it
> is consequential at any amount and the cap lives in the signature."

### Context file · **documented**

**In one line** — the markdown a coding tool reads at session start: `CLAUDE.md` (Claude Code),
`.github/copilot-instructions.md` (Copilot), `AGENTS.md` (Codex CLI), `.cursor/rules/*.mdc` (Cursor).

**The distinction that matters** — a context file is not **documentation**. Documentation is written
for people and may be aspirational; a context file is read by a machine on every session, and
Copilot's steers inline suggestions while Claude Code's drives autonomous actions — so a wrong line
runs a command rather than offering a completion. Nothing in it is enforcement; it is all request.

**Where you meet it** — [Journey: Engineering lead](Journey-Engineering-Lead) ·
[The Evidence Pack](The-Evidence-Pack)

> **Said wrongly** — "The standards are in the context file, so the agent will follow them."
>
> **Said rightly** — "The context file raises the odds; the two rules that must hold are in the
> linter and the tool signature."

### Cost per case · **working method**

**In one line** — the running cost of one handled case, end to end, ratified as an NFR and monitored
like latency.

**The distinction that matters** — a case is not a **call**. One case may be four calls, a retry, a
checker and a judge, so a per-call figure quoted as a per-case figure is out by a factor of five,
always flatteringly. The second half is temporal: this is a *monitored* number with an alert, and
the programmes that meet their token bill in month three ratified an estimate and measured nothing.

**Where you meet it** — [How to Control the Token Bill](How-to-Control-the-Token-Bill), move 1 ·
[the leak finder](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/leaks)

> **Said wrongly** — "It is about two cents a call, so the running cost is negligible."
>
> **Said rightly** — "Six cents a case at P95, measured weekly from the per-call log, with an alert
> at 3× the ratified figure."

---

## D–G

### Deterministic (exact) · **established**

**In one line** — work that must be right every single time, done by code and proven by a unit test,
with the model handing it numbers and reading the result.

**The distinction that matters** — **exact** is a statement about the *requirement*; **deterministic**
is a statement about the *mechanism*. A model at temperature zero is close to deterministic and still
not exact: it returns the same wrong answer reliably. That is why "we set temperature to zero" is
proof of repeatability offered as proof of correctness. Arithmetic, eligibility and totals are
exact work, and they belong in code.

**Where you meet it** — [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper), move 2

> **Said wrongly** — "Temperature is zero, so the fare calculation is deterministic and safe."
>
> **Said rightly** — "The fare calculation is exact work, so code does it and a unit test proves it.
> The model reads the number out."

### Door (one-way / two-way) · **established**

**In one line** — a decision is a two-way door if it can be reversed cheaply and a one-way door if it
cannot. Bezos, 2015 letter to shareholders.

**The distinction that matters** — a door is not a **big decision**. Size is what is spent; the door
is what reversal costs once you are wrong, and the two come apart constantly. A vendor choice is
expensive and often two-way; a data model is cheap this week and one-way for three years. A two-way
door deserves a quick choice and a review date; a one-way door deserves the exit priced first.

**Where you meet it** — [How to Choose Build, Buy or Borrow](How-to-Choose-Build-Buy-or-Borrow),
move 4

> **Said wrongly** — "It is a big commitment, so let's take another two weeks on the analysis."
>
> **Said rightly** — "Reversing it costs six weeks of migration and a contract exit, so it is a
> one-way door. Price the exit first."

### Drift · **established**

**In one line** — a probabilistic system changing behaviour because the world shifted under it, with
no deploy and no error; watched as an output-mix KPI, and a drift alert re-opens the release gate.

**The distinction that matters** — drift is not a **regression**. A regression is caused by a change
you made, is visible in a diff, and is fixed by reverting. Drift is caused by a change somebody else
made — a new fare class, a new phrasing, a partner's schedule — and there is nothing to revert. The
confusion costs a day of bisecting commits that cannot contain the cause, and it hides the real
response: re-open the gate, re-score the affected slice, and add the new condition to the golden set.

**Where you meet it** — [The Eight Loops](The-Eight-Loops) · [Journey: DevOps](Journey-DevOps)

> **Said wrongly** — "Quality dropped on Tuesday — find the commit and roll it back."
>
> **Said rightly** — "Nothing shipped for eleven days. The refund share of the output mix moved
> nine points, so this is drift and the release gate is open again."

### EARS · **established**

**In one line** — Easy Approach to Requirements Syntax: `WHEN` a condition `THE SYSTEM SHALL` a
behaviour, plus a boundary and a number. Mavin, Wilkinson, Harwood and Novak, Rolls-Royce, 2009.

**The distinction that matters** — an EARS line is not a **user story**. A story carries motivation
and deliberately leaves the behaviour open; an EARS line closes it so that two engineers cannot read
it two ways, which is what spec-driven tooling consumes. Nor is it a six-part scenario: the scenario
carries the environment and the measure, the EARS line carries the rule.

**Where you meet it** — [How to Run an NFR Workshop](How-to-Run-an-NFR-Workshop), move 5 ·
[How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper)

> **Said wrongly** — "As a passenger, I want fast rebooking options so that I can get home."
>
> **Said rightly** — "WHEN a codeshare segment is cancelled, THE SYSTEM SHALL return at most three
> ranked alternatives within 30 seconds at P95."

### Eight-field spec · **working method**

**In one line** — title, value, acceptance, the model's role, autonomy, the bar, the fallback, the
records: the smallest spec a coding agent can build from.

**The distinction that matters** — it is not a **longer ticket**. Three fields are familiar and five
are the decisions nobody had made: what the model is for, what it may do alone, what rate counts as
working, what happens when it does not, and what evidence gets written. Each is a question otherwise
answered by whoever writes the code that afternoon.

**Where you meet it** — [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper), move 3

> **Said wrongly** — "The ticket has acceptance criteria, so the agent has what it needs."
>
> **Said rightly** — "Acceptance is there; autonomy, the bar and the fallback are blank, and those
> three are the ones that decide what it may do at two in the morning."

### Enforced control · **working method**

**In one line** — a limit written into the tool's own signature — a cap, a required confirmation
token, a separated credential — which holds whatever the model is convinced of.

**The distinction that matters** — the pair that costs the most on this page: an enforced control
against a [request](#request-a-rule-in-a-prompt--working-method). A prompt rule lowers a probability;
a signature removes a path. Both are said the same way in a review — "we prevent refunds over $400" —
so every layer owes one honest word: **enforced**, **a request**, or **absent**.

**Where you meet it** — [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary),
move 2

> **Said wrongly** — "The system prompt tells it never to refund above four hundred."
>
> **Said rightly** — "The tool signature rejects any amount above $400 without an approver token.
> The prompt also says it, which lowers how often we see the rejection."

### Gate · **established**

**In one line** — a decision with evidence in front of a named person and their name on it. Five
here: intent, plan, behaviour, release, expansion.

**The distinction that matters** — a gate is not an **approval**, and it is not a meeting. An
approval is a signature; a gate is a *question with named evidence attached*, and the signature is
the last thing that happens. So a gate leaves a record of what was in front of the signer and what
would have made them say no; one passed without evidence protects nobody, least of all the signer.

**Where you meet it** — [Gates and Governance](Gates-and-Governance)

> **Said wrongly** — "The release gate is approved — I signed it off this morning."
>
> **Said rightly** — "The gate has the per-slice lower bounds, the shadow agreement and the open
> conditions in front of it. On that evidence, it is a pass with two conditions."

### Golden set · **established**

**In one line** — real historical cases with the expected outcome, one per line, run on every change:
the acceptance bar made executable, where a slice below its bar rejects the change.

**The distinction that matters** — a golden set is not a **test suite**, though it runs in the same
place. A suite answers yes/no and green means every assertion held; a golden set answers *what
share*, per slice, and a green run can sit below the bar. The cases must also be **real**, and a
stale set is worse than a small one because it is trusted.

**Where you meet it** — [How to Prove the Bar](How-to-Prove-the-Bar), move 2 ·
[The Evidence Pack](The-Evidence-Pack)

> **Said wrongly** — "The golden set passes, so we are good to ship."
>
> **Said rightly** — "It scores 86% overall, but the codeshare slice is at 79% against an 80% bar,
> and one slice below its bar rejects the change."

---

## H–P

### Hard gate / soft gate · **working method**

**In one line** — a hard gate halts the phase until it is signed; a soft gate lets the phase close
behind a placeholder with a named owner and a date. Four questions classify any decision, and one
"no" makes it hard.

**The distinction that matters** — hardness is not **importance**. Every gate feels important to its
owner, and making them all hard stops the programme within a fortnight, after which the team routes
around all of them including the three that mattered. The four questions ask about reversibility,
blast radius, evidence and who is blocked; everything else closes behind a named, dated placeholder.

**Where you meet it** — [Gates and Governance](Gates-and-Governance) ·
[The Agentic PDLC](The-Agentic-PDLC)

> **Said wrongly** — "Security is important, so every security item is a hard gate."
>
> **Said rightly** — "The authority budget is hard because it is irreversible once credentials are
> issued. The threat-model refresh is soft, owned by Priya, due on the 14th."

### Injection (prompt injection) · **established**

**In one line** — text that arrives as data and is read by the model as an instruction; the one
genuinely new threat, where every ingested text is untrusted, including partner API responses.

**The distinction that matters** — injection is not a **jailbreak**. A jailbreak is the user talking
the model out of its rules, with the attacker in front of you; injection arrives inside content the
model was asked to read — a PDF, a ticket body, a partner's JSON. So the defence sits at the
**ingest layer**, and it belongs in the regression suite rather than in a launch checklist.

**Where you meet it** — [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary),
move 4 ·
[the injection drill](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/inject)

> **Said wrongly** — "Only our own staff use it, so injection is not really our threat model."
>
> **Said rightly** — "It reads partner responses and uploaded documents, so the untrusted text is
> already inside the prompt. The suite runs on every change."

### Judge (LLM-as-a-judge) · **established**

**In one line** — an independent model scoring a best-guess output against a rubric for tone, policy
and false claims, after the exact checks have run.

**The distinction that matters** — a judge is not a **measurement**; it is an instrument that needs
calibrating. Run it first and you pay to grade outputs a cheap exact check would have rejected. Quote
its score without comparing it against human labels on the same cases and you have reported the
judge's opinion as the system's accuracy.

**Where you meet it** — [How to Prove the Bar](How-to-Prove-the-Bar), move 3

> **Said wrongly** — "The judge gives it 4.6 out of 5, so quality is good."
>
> **Said rightly** — "The judge agrees with our reviewers on 88% of a 60-case calibration sample,
> and on that basis its score is worth quoting — after the exact checks."

### Least authority (least privilege) · **established**

**In one line** — the narrowest permissions that still let the agent work, with read separated from
write. Saltzer and Schroeder, 1975.

**The distinction that matters** — least authority is about what the credential **can** do, not what
the agent is **asked** to do. A broad role plus a careful prompt is a request with a large blast
radius behind it. The useful audit is what was granted and never called: the list of permissions you
can remove this week with no argument.

**Where you meet it** — [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary),
move 1

> **Said wrongly** — "It uses the existing service account, but it only ever reads."
>
> **Said rightly** — "It has a read role for three tables and a separate write role for one, and the
> write role is not in the session that reads untrusted text."

### Little's law · **established**

**In one line** — time in a queue equals work waiting divided by the rate served. Little, 1961.
Capacity is fixed by people; **slots needed is a policy variable**.

**The distinction that matters** — a queue is not a **capacity problem** until you have checked the
policy. Both terms are movable, but hiring takes a quarter and changing who must read what takes an
afternoon, and review queues are almost always the second problem wearing the first one's clothes.
The second trap is the average: the law assumes reviewers are interchangeable, so if only one person
can review the payment path, that lane has a capacity of one however healthy the headline looks.
Compute the queue per band.

**Where you meet it** — [How to Review by Risk Band](How-to-Review-by-Risk-Band), move 1 ·
[the queue calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/queue)

> **Said wrongly** — "Reviews take four days because we are two engineers short."
>
> **Said rightly** — "Two readers on all nine changes is eighteen slots against 4.5 a day. Routed by
> band it is seven slots, which is 1.6 days with the same people."

### Lower bound · **established**

**In one line** — the lowest value a true score could plausibly have given the sample size. The bar
is proven only when the lower bound clears it. Wilson, 1927.

**The distinction that matters** — a **score** is what you observed; a **lower bound** is what you
are entitled to claim, and the gap is entirely about n. 82% on forty cases has a Wilson lower bound
of 67.5%, so it does not prove an 80% bar. And "not proven" is not a rejection but a **cases-owed
number** — "we owe 331 more codeshare cases" is a plan where "it failed" is an argument.

**Where you meet it** — [How to Prove the Bar](How-to-Prove-the-Bar), move 4 ·
[the confidence calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/confidence)

> **Said wrongly** — "We are at 82% against an 80% bar, so that one is cleared."
>
> **Said rightly** — "82% on 150 cases has a lower bound of 75.1%, so the bar is unproven and we owe
> about another 800 cases — or we accept the slice stays gated."

### MCP (Model Context Protocol) · **documented**

**In one line** — one plug so any compliant AI client can use your tools and data, turning M apps ×
N systems into M + N. A server exposes **tools** (actions), **resources** (read-only data) and
**prompts** (templates).

**The distinction that matters** — exposing a **tool** is not exposing a **resource**. A resource is
read-only, a prompt is a template, and a tool *acts*, so the read/write split is a decision made at
the server rather than a convention followed by the client. Publishing an internal API through MCP
grants the model everything that API can do, and the narrowing happens in the tool signatures.

**Where you meet it** — [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper) ·
[Journey: Solution architect](Journey-Solution-Architect)

> **Said wrongly** — "We put the booking API behind MCP, so the agent can use it safely."
>
> **Said rightly** — "Reads are resources, the two writes are tools with caps and a confirmation
> token, and the refund path is not exposed at all."

---

## R–Z

### Request (a rule in a prompt) · **working method**

**In one line** — a model can be talked past anything in its prompt, so a prompt rule lowers a
probability and never removes a path.

**The distinction that matters** — the counterpart of an
[enforced control](#enforced-control--working-method), and worth its own entry because the word
"rule" hides it. A request moves the rate, costs nothing, and is the right instrument for tone,
format and preference; it is the wrong instrument for money, identity and policy, where the failure
is silent — nothing errors and nothing logs.

**Where you meet it** —
[How to Run a Missing Control Postmortem](How-to-Run-a-Missing-Control-Postmortem), move 2

> **Said wrongly** — "We have a rule that it must not quote prices it has not verified."
>
> **Said rightly** — "That is a request. It holds most of the time; the price comes from the tool
> and the response is rejected if it contains a figure the tool did not return."

### Risk ladder (R1–R5) · **working method**

**In one line** — reversible draft → reversible change → hard to reverse → money, identity or policy
→ irreversible. The check grows with the band, and **a change inherits the band of whatever it
touches**.

**The distinction that matters** — a band is a property of what the change **touches**, not of how
**big** it is. Three lines in the refund tool is R4; 900 lines of report template is R1. The
inheritance rule is the part teams forget: shared code takes the band of its most dangerous caller,
and configuration is behaviour without code, so it is banded like code.

**Where you meet it** — [How to Review by Risk Band](How-to-Review-by-Risk-Band), move 2

> **Said wrongly** — "It is a one-line change, so a quick review is fine."
>
> **Said rightly** — "One line, but it is in the fee-waiver path, so it is R4: two named readers and
> the harness green on the refund slice."

### Sensitivity point · **established**

**In one line** — an NFR rated high for both importance and difficulty, where one design decision
changes the outcome. ATAM. **Sensitivity points, and only they, earn an ADR.**

**The distinction that matters** — a sensitivity point is not a **risk**. A risk is something that
might happen to you; a sensitivity point is where a *choice you are about to make* swings the result,
so it is actionable today and it has an owner. Nor is it a disagreement: two stakeholders far apart
on the tree may hold different information, which a fact settles rather than a trade-off.

**Where you meet it** — [How to Run an NFR Workshop](How-to-Run-an-NFR-Workshop), move 8 ·
[the utility tree builder](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/utree)

> **Said wrongly** — "Cost is a risk on this programme, so let's add it to the register."
>
> **Said rightly** — "Cost per case is high value and high difficulty, and the model-tier decision
> moves it. That is a sensitivity point: ADR-001, owned by the architect, due Day 12."

### Shadow deployment · **established**

**In one line** — run the agent beside the live process, deciding but never acting, for a fixed
window; compare, then cut over a slice on evidence. Also called dark launching.

**The distinction that matters** — a shadow run is not a **canary**. A canary is live for a share of
real traffic and its mistakes reach customers; a shadow run touches nobody, which is what lets it see
the full distribution rather than an easy slice. A disagreement is also not automatically the agent
being wrong — the cases where the desk was wrong are among the window's best output.

**Where you meet it** — [How to Prove the Bar](How-to-Prove-the-Bar), move 5 ·
[the cut-over planner](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/cutover)

> **Said wrongly** — "We will run it in shadow for a while and see how it does."
>
> **Said rightly** — "Fourteen days, agreement measured nightly per slice, money actions excluded,
> and the cut-over at 5% happens on the 15th if the refund slice holds."

### Slice · **working method**

**In one line** — one kind of case with its own difficulty — same-day lookups, codeshare tickets,
refunds. **Bars, scores and gates are all per slice.**

**The distinction that matters** — a slice is not a **segment**. A segment is who the customer is —
region, tier, channel — and it is a reporting cut; a slice is what makes the work *hard*, and it is a
measurement cut. Reporting by segment produces an average true of nobody, and because bars come from
damage, two slices inside one segment routinely carry bars twenty points apart.

**Where you meet it** — [How to Prove the Bar](How-to-Prove-the-Bar), move 1 ·
[Scenario Library](Scenario-Library)

> **Said wrongly** — "Accuracy is 86% across the board, and it is consistent between regions."
>
> **Said rightly** — "Same-day lookups are at 94% against a 50% bar, codeshare at 79% against 80%.
> The 86% is an average of two different problems."

### Trace · **established**

**In one line** — one row per consequential action: input (redacted), tools called, the decision,
model version, approver, cost. Replayable, auditable, and not a breach target.

**The distinction that matters** — a trace is not a **log**. A log serves the engineer debugging
tonight and may be verbose, partial and full of raw payloads; a trace answers the question asked in
six months — *why did it do that, on whose authority, at what cost* — and is designed around
**redaction**. Redact at write time, because redacting later means it was stored.

**Where you meet it** — [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary),
move 5

> **Said wrongly** — "Everything is in the application logs, so we can reconstruct it if we need
> to."
>
> **Said rightly** — "One row per consequential action, with the model version and the approver, PII
> redacted at write time, replayable from the row alone."

### Two numbers · **working method**

**In one line** — time saved **and** money spent, reported together, always.

**The distinction that matters** — this is not a **dashboard**, and adding numbers makes it worse.
The pairing is the mechanism: the second number is chosen because pushing the first moves it. A cycle
that saves time and costs more is a normal result — the programme is cancelled on the number you hid,
not on the one that looked bad. Two rows keep it honest: review hours added, and re-runs.

**Where you meet it** — [Gates and Governance](Gates-and-Governance) ·
[the two-number report](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/report)

> **Said wrongly** — "Cycle one saved 40% of the handling time — we will get to the cost side later."
>
> **Said rightly** — "40% fewer person-days, $4,100 of tokens, 60 review hours added. The review
> hours are the number I expect to fall, and it is the one to hold me to."

### Walking skeleton · **established**

**In one line** — a thin end-to-end slice that works, proving the pieces connect before you add more.
Cockburn, *Crystal Clear*, 2004. Day one of a bolt plan.

**The distinction that matters** — a skeleton is not an **MVP** and not a **spike**. An MVP is the
smallest thing a *customer* finds useful; a skeleton is the smallest thing that proves the *system*
connects, and it may be worthless to a customer. A spike is thrown away; a skeleton is the first
thing you keep, and it goes first because it retires the largest unknown for half a day's work.

**Where you meet it** — [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts), move 2

> **Said wrongly** — "The skeleton is not worth demoing — it does not do anything useful yet."
>
> **Said rightly** — "It returns one hard-coded rebooking through the real gateway, the real tool
> and the real trace. Everything after this is a change to a system that already works."

---

## Everything else, briefly

The terms that do not sit in a formula, a gate or a control, with their one-line definition and mark.

| Term | Mark | In one line |
| --- | --- | --- |
| **AI-DLC** | *established* | AI-Driven Development Life Cycle (AWS). Adaptive: run only the lifecycle stages a given change actually needs. Here, the architect's judgement of **depth per change** |
| **AiDD** | *established* | AI-driven development: the day-to-day craft of building with coding agents. Context files, story files, editor agents, review by risk, cost habits |
| **Batch pricing** | *documented* | Work that can wait, such as re-scoring the golden set overnight, runs at about half the on-demand price |
| **BMAD** | *established* | Breakthrough Method for Agile AI-Driven Development. A pipeline of AI personas — analyst, PM, architect, dev, QA — each handing a versioned artefact to the next. For complex, multi-team, audited work |
| **Context layers (onion)** | *working method* | Shared → domain → product → task, each versioned. A new product writes only its own layers and inherits the rest. Built on DRY and layered architecture, not a named standard |
| **Exact / best-guess map** | *working method* | Every step of a feature tagged exact, best-guess or consequential, with the proof each kind owes. Drawn before any framework is chosen |
| **Layered defences** | *established* | Several imperfect layers in a row; harm gets through only if every layer fails at once. Reason, 1990. The discipline is classifying each layer honestly as enforced, a request, or absent |
| **Model gateway** | *documented* | One layer every model call passes through, giving routing, budgets, fallbacks and a per-call log in one place. LiteLLM is the named example |
| **P0 · P1 · P2 · P3** | *established* | Frame, Design & Spec, Build & Prove, Run & Learn. The spine |
| **Paired indicators** | *established* | Every measure reported beside the one that shows its side effect, so neither can be pushed alone. Grove, 1983; Goodhart's law, 1975 |
| **Rule sheet** | *established* | Business rules extracted from legacy code into condition, action, source line and confidence, so the agent reads rules instead of thousands of lines. Everything below 0.9 confidence gets a human check |
| **SDD (spec-driven development)** | *established* | The spec, not the code, is what you maintain; code is generated from it and regenerated on change. **The backbone. Use it always** |
| **Story file (agent-ready)** | *working method* | One self-contained file the agent builds from: context by reference, spec in EARS, tools, tests, done-when, cost. BMAD's shard and SDD's unit at once. Reviewable as a diff |
| **Strangler Fig** | *established* | Wrap the legacy system, route a slice to the new one, grow the new, retire the old. Fowler, 2004 |
| **Unknown-days** | *working method* | The sum, over every day, of the unknowns still open. The measure that explains why the walking skeleton goes first |

---

## How to use this page in a review

Five moves for catching an expensive confusion while it is still cheap — in the room, out loud,
without turning the review into a seminar.

1. **Listen for the passive voice around a control.** "Refunds over $400 are approved" names no
   approver and no enforcement point. Ask the one question that separates the two categories: *is
   that enforced, or is it a request — and which line holds it?* Nobody is put on the spot by a
   question about a file path.
2. **Ask for the denominator every time a percentage is spoken.** "It is at 86%" is not yet a claim.
   *On how many cases, and per slice?* converts an argument about confidence into arithmetic, and
   the arithmetic usually answers itself before anyone has to disagree.
3. **When someone says it got worse, ask what was deployed.** If the answer is nothing, the word is
   [drift](#drift--established) and the response is to re-open the gate and re-score the slice —
   not to bisect commits that cannot contain the cause.
4. **Repeat the sentence back with the precise word substituted.** "So the model is *asked* not to,
   and nothing stops it." The room hears the difference immediately, the correction lands on the
   sentence rather than on the person, and it takes four seconds.
5. **Write the corrected sentence into the artefact before the meeting ends.** A distinction agreed
   aloud and never written is re-lost by the next review, and the person who corrected it looks
   pedantic the second time. The sheet below exists so the correction has somewhere to land.

<details><summary><b>Template · Team vocabulary sheet</b></summary>

```markdown
# Vocabulary sheet · <team> · <date> · Owner: <name>

One page, pinned where the standup happens. Ten distinctions, plus the words this team
invented for itself without noticing.

## The ten that cost the most
| We say | We mean | NOT to be confused with | Because the difference is |
|--------|---------|------------------------|---------------------------|
| enforced control | a limit in the tool signature | a request in the prompt | one removes a path, one lowers a probability |
| request | a rule in a prompt | an enforced control | it holds most of the time, and fails silently |
| lower bound | what we may claim | the score | the gap between them is entirely n |
| bar | derived from damage / saving | a target | a target is negotiable, a bar is arithmetic |
| gate | evidence in front of a named person | an approval | an approval is the signature, not the question |
| slice | a kind of case, by difficulty | a segment | a segment is who; a slice is what is hard |
| drift | behaviour moved, nothing deployed | a regression | there is no commit to revert |
| exact | must be right every time | deterministic | temperature zero repeats, it does not verify |
| consequential | changes something real | important | importance is attention; consequence is blast radius |
| attempts | 1 + retries | retries | every cost model works on attempts |

## Our house terms — the words only this team uses
| Our word | What we mean by it | What an outsider would assume | Agreed by | Date |
|----------|--------------------|------------------------------|-----------|------|
| <e.g. "the harness"> | <the golden-set run wired as a required check> | <any CI job> | <name> | |
| | | | | |
| | | | | |

## Words we have retired, and what we say instead
| Retired | Say instead | Why |
|---------|-------------|-----|
| "the AI decided" | "<the model proposed X; the gate passed it>" | it hides who is accountable |
| "we prevent <X>" | "enforced in <file:line>" OR "requested in the prompt" | the sentence that starts postmortems |
| | | |

## Review
Re-read at the start of each quarter, and whenever a postmortem turns on a word. A term
nobody argued about all quarter is either settled or unused — find out which.
```
</details>

---

## The concept map

The playbook teaches **55 concepts**, grouped by the loop they belong to. Browse them with their
worked example and the episode each first appears in:
[the concept map](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/concepts).

| Group | Concepts |
| --- | --- |
| **Requirements** | pain as a measurement · AI-fit · credited requirements · constraints by type · six-part scenario · utility tree · sensitivity point |
| **Decision** | record only at the trade-off point · ADR · exact/best-guess map · three-year cost · doors · decision sheet · flip test · model gateway · context layers · MCP |
| **Spec** | slice · EARS · bar per slice · autonomy level · eight-field spec · authority budget and bands |
| **Delivery** | walking skeleton · bolt · unknown-days · harness before review · Little's law · review by risk band |
| **Trust** | golden set · lower bound · a sample per slice · checker matched to the work · shadow run · cut-over on evidence |
| **Cost** | cost per case · routing by slice · prompt caching · batch pricing · breaker and loop cap · the four bill signatures |
| **Incident** | a rule in a prompt is a request · enforced control · injection · trace · layered defences · missing-control postmortem |
| **Governance** | P0–P3 · the eight loops · traditional track and agentic delta · hard and soft gates · minimum artefact set · paired indicators · two-number report · maturity |

---

## Where a model helps

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Reading a spec, an ADR or a postmortem back and flagging every sentence where a control is stated as a request — "the prompt says", "the agent should", "we prevent" — with the sentence quoted. It is literal about this, which is the quality wanted |
| **Claude Code** | Checking the vocabulary against the code: grep the tool signatures for each cap a document claims, and list the claims with no enforcement point. A distinction that exists only in prose is the one that fails |
| **Chat LLM** | Drafting the house-term column of the sheet above from a month of standup notes and pull request titles — the words a team has invented without noticing, and what an outsider would assume they meant |
| **Do not delegate** | Correcting a person in a review. The words are cheap to fix and the correction is a social act; a model can find the confusion, and only a person can make the room comfortable with having been wrong |

---

**Next:** [Formulas and Calculators](Formulas-and-Calculators) · [Decision Trees](Decision-Trees) ·
[Sources and Confidence](Sources-and-Confidence) · [The Agentic PDLC](The-Agentic-PDLC)
