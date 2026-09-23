# Exercises and answers

<!-- tutorial:lesson -->*Twelve more, three per phase, are in the lesson **[Twelve exercises](Agentic-PDLC-Exercises-with-Answers)**, each with its working.*<!-- /tutorial:lesson -->

Thirty-one exercises across the playbook, with worked answers. Use them to test yourself, to run a
session, or to prepare for an interview where someone asks how you would actually do this.

Every answer is worked, not asserted. Where there is a formula, it is applied.

| Set | What it tests | Go to |
| --- | --- | --- |
| A | Framing: is this even AI? | [below](#set-a--framing) |
| B | Arithmetic: bars, chains, bounds | [below](#set-b--arithmetic) |
| C | Design: shape, authority, checkers | [below](#set-c--design) |
| D | Delivery: bolts, queues, cost | [below](#set-d--delivery) |
| E | Running: drift, incidents, reporting | [below](#set-e--running) |
| F | Interview questions | [below](#set-f--interview-questions) |
| G | Reading a symptom | [below](#set-g--reading-a-symptom) |

### Find one

Difficulty is about how much of the method a full answer has to touch. The three-dot ones are not
harder arithmetic; they are the ones where the defensible answer is the unwelcome one.

| | It tests | Stresses | The method lives in | Difficulty |
| --- | --- | --- | --- | --- |
| **A1** | Is this AI at all? | Product manager | [Decision Trees](Decision-Trees) | ●○○ |
| **A2** | Defending an AI-fit verdict upwards | Sponsor | [Role Sponsor](Role-Sponsor) | ●●○ |
| **A3** | The value line, with run and review in it | Product manager | [Formulas and Calculators](Formulas-and-Calculators) | ●○○ |
| **B1** | Deriving a bar from damage and saving | Product manager | [Formulas and Calculators](Formulas-and-Calculators) | ●○○ |
| **B2** | Chained probability | Solution architect | [Formulas and Calculators](Formulas-and-Calculators) | ●○○ |
| **B3** | Lower bound, adequate sample | QA lead | [How to Prove the Bar](How-to-Prove-the-Bar) | ●●○ |
| **B4** | Lower bound, thin sample | QA lead | [How to Prove the Bar](How-to-Prove-the-Bar) | ●●○ |
| **B5** | Queue arithmetic under a review policy | Engineering lead | [How to Review by Risk Band](How-to-Review-by-Risk-Band) | ●●○ |
| **B6** | Cache break-even | Engineering lead | [How to Control the Token Bill](How-to-Control-the-Token-Bill) | ●●○ |
| **C1** | How many agents is too many | Solution architect | [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper) | ●○○ |
| **C2** | Where a boundary is enforced | Solution architect | [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary) | ●●○ |
| **C3** | Why a checker must be independent | QA lead | [How to Prove the Bar](How-to-Prove-the-Bar) | ●●● |
| **C4** | Turning a policy into an authority budget | Solution architect | [Gates and Governance](Gates-and-Governance) | ●●○ |
| **D1** | Ordering bolts by dependency | Engineering lead | [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts) | ●○○ |
| **D2** | Diagnosing a bill with four flat factors | Engineering lead | [How to Control the Token Bill](How-to-Control-the-Token-Bill) | ●●● |
| **D3** | Which factor to fix first | Engineering lead | [Formulas and Calculators](Formulas-and-Calculators) | ●●○ |
| **D4** | A bolt that cannot be built alone | Engineering lead | [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts) | ●○○ |
| **E1** | Behaviour changing with no code change | DevOps | [How to Run a Missing Control Postmortem](How-to-Run-a-Missing-Control-Postmortem) | ●●○ |
| **E2** | A postmortem that names a string, not a control | QA lead | [How to Run a Missing Control Postmortem](How-to-Run-a-Missing-Control-Postmortem) | ●●● |
| **E3** | Defending the two-number report | Product manager | [The Evidence Pack](The-Evidence-Pack) | ●●○ |
| **E4** | Replacing an adoption metric | Sponsor | [Role Sponsor](Role-Sponsor) | ●●● |
| **F1** | "How accurate does it need to be?" | Any | [How to Prove the Bar](How-to-Prove-the-Bar) | ●●○ |
| **F2** | "How do you know it works?" | Any | [The Evidence Pack](The-Evidence-Pack) | ●●○ |
| **F3** | "What is new about securing an agent?" | Any | [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary) | ●●● |
| **F4** | "Five agents — what do you ask?" | Any | [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper) | ●●○ |
| **F5** | "How do you report on this?" | Any | [The Evidence Pack](The-Evidence-Pack) | ●●○ |
| **G1** | A hit ratio near zero with caching on | Engineering lead | [How to Control the Token Bill](How-to-Control-the-Token-Bill) | ●●○ |
| **G2** | A set that passes while production degrades | QA lead | [How to Prove the Bar](How-to-Prove-the-Bar) | ●●● |
| **G3** | A flat median and a six-times tail | DevOps | [How to Control the Token Bill](How-to-Control-the-Token-Bill) | ●●● |
| **G4** | A gate cleared in aggregate | Product manager | [How to Prove the Bar](How-to-Prove-the-Bar) | ●●○ |
| **G5** | A cap that is not a control | Solution architect | [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary) | ●●● |

### How to mark one

Mark on structure, not on fluency. A full answer has four parts, and a confident answer missing two
of them is worth less than a hesitant answer with all four.

| | What you are looking for | A zero looks like |
| --- | --- | --- |
| **The call** | One sentence, with *because* in it | A survey of considerations with no verdict |
| **The artefact** | Named — a record, a register, an ADR, a bar sheet | "We'd document it" |
| **The number** | The arithmetic shown, not the result asserted | A figure with no derivation |
| **The owner** | A person, not a team | "The team would decide" |

Two answers deserve full marks and look nothing alike, because several of these have more than one
defensible reading. What is not defensible is an answer that cannot say what would change its mind.
Ask that question when a room agrees too quickly.

---

## Set A · framing

**A1.** A logistics team asks for an agent to check whether a shipment qualifies for expedited
handling. The criteria are published and unambiguous. Verdict?

<details><summary>Answer</summary>

**Not AI.** The first AI-fit question fails: there is no genuine judgement call. Published, unambiguous
criteria are a rule, and code does rules perfectly, cheaply and provably.

The model's legitimate job is nearby: reading unstructured evidence to *extract* the inputs the rule
needs. That is best-guess work feeding an exact determination — which is the standard shape, and it is
not the same as letting the model decide.
</details>

**A2.** Your top five requests come back from the AI-fit check as four rules and one agentic. Your VP
says the assessment is "not ambitious enough". Respond.

<details><summary>Answer</summary>

Four out of five is the **normal, healthy** result. Most of a backlog is deterministic.

The argument to make is not about ambition, it is about where ambition pays. Agentic ceremony on a
rule costs the token bill, the review load, the evaluation harness and the gates, and buys a
probabilistic answer to a question that had a certain one. The one genuinely agentic request is where
that spend earns something.

Bring the record, not the opinion. Each verdict has three answers and a build shape written down —
that is what makes this a decision rather than a preference.
</details>

**A3.** A feature saves 5 minutes on each of 1,200 cases a day. A minute costs $0.90. It costs $0.35 a
case to run, and 20% of cases need 2 minutes of review. Net value per day?

<details><summary>Answer</summary>

Saving: 1,200 × 5 × $0.90 = **$5,400**
Run cost: 1,200 × $0.35 = **$420**
Review: 1,200 × 20% × 2 × $0.90 = **$432**

**Net = $4,548 a day.**

Note that the two terms people omit — run and review — total $852, about 16% of the gross. They do not
change the answer here, and on a thinner feature they are the whole answer. Keep the review row
visible; it is high in cycle one and falls.
</details>

---

## Set B · arithmetic

**B1.** A wrong answer costs $250. A right one saves $10. What is the bar, and what do you do about it?

<details><summary>Answer</summary>

N = 250 ÷ 10 = **25**. bar = 25 ÷ 26 = **96.2%**.

That is almost certainly unreachable for a best-guess step, and the right response is not to try
harder. It is to **lower the damage**: put a human hold on the action so a wrong answer costs a
correction rather than $250.

Drop the damage to $20 and N = 2, so the bar falls to **67%** — shippable. The hold is the lever, and
it belongs in the spec as a documented decision.
</details>

**B2.** Five chained best-guess steps, each 95%. End-to-end?

<details><summary>Answer</summary>

0.95⁵ = **0.774**. Wrong roughly one time in four.

Each step looks excellent and the chain does not. Multiply, never average — and note that removing a
single step takes you to 0.95⁴ = 0.815, which is usually cheaper than trying to move any individual
step from 95% to 99%.
</details>

**B3.** A slice scores 78% on 200 cases against a 75% bar. Proven?

<details><summary>Answer</summary>

Margin = 1.96 × √(0.78 × 0.22 ÷ 200) = 1.96 × 0.0293 ≈ **5.7 points**. Lower bound ≈ **72.3%**, below
the 75% bar. **Not proven.**

Cases needed = 1.96² × 0.78 × 0.22 ÷ (0.03)² ≈ **733**. You have 200.

The shape of that answer matters more than the number: three points above the bar costs you hundreds
of cases, because the denominator is squared.
</details>

**B4.** A slice scores 95% on 80 cases against a 90% bar. Proven?

<details><summary>Answer</summary>

Lower bound ≈ **90.2%**, just above the bar. **Proven — barely.**

Cases needed ≈ **73**, and you have 80. This is the pleasant case: a score comfortably above the bar
needs far fewer cases than one hugging it.

With n this small, quote the **Wilson** bound rather than the normal approximation; near 0.95 the
normal approximation is optimistic.
</details>

**B5.** Twelve changes wait for review. Policy is two senior reviewers on everything; capacity is 3
review slots a day. After routing, 1 change needs two readers, 4 need one, and 7 can go to the
harness alone. Before and after?

<details><summary>Answer</summary>

Before: 12 × 2 = 24 slots ÷ 3 = **8.0 days**.
After: (1 × 2) + (4 × 1) + (7 × 0) = 6 slots ÷ 3 = **2.0 days**.

Same people, same capacity. **Slots needed is the only variable you control**, and it is a policy
choice rather than a hiring problem.
</details>

**B6.** A 6,000-token prefix will be used three times. Five-minute cache. Does caching pay?

<details><summary>Answer</summary>

With cache: (1.25 + 0.1 × 2) = **1.45** prefix-equivalents.
Without: **3.0**.

**Yes — it more than halves it.** At N = 1 it is 1.25 against 1.0, so caching *costs* money on a
single use. Break-even is the second use, and the saving approaches 90% as N grows.
</details>

---

## Set C · design

**C1.** An engineer proposes: a planner agent, a retriever agent, a calculator agent, a writer agent
and a critic agent. Which survive?

<details><summary>Answer</summary>

**One agent and one checker.**

The *calculator* is exact work — a function, and putting it behind an agent makes a provable step
probabilistic, which is the worst trade in the playbook. The *retriever* is a tool. The *planner* is
what the single agent already does. The *writer* is the same agent's output.

The **critic survives**, because independence is the entire point of a checker — a different model,
or a fresh context with an adversarial brief.

Five agents is ten possible hand-offs, n(n−1)/2. One agent, one function, one tool and one checker is
zero.
</details>

**C2.** Where does "never book a flight departing within 45 minutes" belong?

<details><summary>Answer</summary>

**Both places, doing different jobs.**

In the **tool signature**, as a validated parameter that raises — because booking an unmakeable
connection is consequential and hard to reverse for the passenger.

In the **prompt**, as an explanation — so the agent reasons about it and does not propose options it
will then be refused.

The prompt makes it behave well by default. The signature makes bad behaviour impossible when the
prompt has been talked past. Saying "put it in the tool, not the prompt" is half right and loses
something real.
</details>

**C3.** Your team wants to pass the drafter's reasoning to the checker "so it has full context". Why
not?

<details><summary>Answer</summary>

Because the reasoning is exactly what you are trying to check. A checker given the drafter's chain of
thought is strongly anchored by it and will tend to confirm it — you have rebuilt the drafter with
extra steps.

Pass the **constraints and the output only**. The checker's job is "does this output satisfy these
constraints", answered fresh.

And cap the re-draft loop at two rounds before escalating, or a stubborn disagreement becomes a spend
loop.
</details>

**C4.** A compliance officer says every refund over $400 needs a named approver. Where does that
requirement travel?

<details><summary>Answer</summary>

Through four artefacts, and you should be able to trace it in all four:

1. **Constraints by type** — regulatory, captured before any NFR is ratified.
2. **Ratified NFRs** — it reshapes the autonomy NFR from an adjective into a number.
3. **The authority budget** — `issue_refund` becomes R4 with a $400 cap and a named approver.
4. **The tool signature** — a typed bounded parameter and a confirmation token, with two tests.

If it exists in the first three and not the fourth, you have the $2,000 refund waiting to happen. If
it exists only in the fourth, nobody knows why the number is 400 and someone will "improve" it.
</details>

---

## Set D · delivery

**D1.** Your ten bolts are ordered by business priority. What goes wrong?

<details><summary>Answer</summary>

Business priority ignores dependency, so at least one bolt cannot be built when its day arrives —
classically a gated write scheduled before the plug it needs.

Re-order by dependency: **walking skeleton first** (it proves the pieces connect), then pure exact
code (it stands alone and never blocks), then checkers, then the plug, then gated writes, then the
proof.

Business priority still decides *which* slices are in the plan at all. It just does not decide the
order they can be built in.
</details>

**D2.** The bill doubled. Tokens per call are flat, the tier mix is unchanged, retries are unchanged,
and the cache hit ratio fell from 80% to 5%. What happened, and what is the fix?

<details><summary>Answer</summary>

Three of the four signatures are flat, so the cache is the whole story. Something broke the **exact
prefix match**, and there are only a few candidates:

- A **model switch mid-task** — the cache is model-scoped
- Something **volatile inside the cached block** — a timestamp, a request id, a session id
- The prompt was **reordered**, putting variable content before the marker
- The prefix fell below the ~1,024-token minimum

The most common in practice is the reorder, and it usually arrives as a small readability improvement
by someone new. Which is the argument for keeping the caching layout in **one configuration file,
reviewed like code**, with the hit ratio as a monitored number.
</details>

**D3.** Which do you fix first: a factor of 2.0 that takes 4 days, or a factor of 1.25 that takes half
a day?

<details><summary>Answer</summary>

Priority = (factor − 1) ÷ days.

- 2.0 over 4 days → (1.0) ÷ 4 = **0.25**
- 1.25 over 0.5 days → (0.25) ÷ 0.5 = **0.50**

**The small one first.** It removes twice the multiplier per day of work, and the bill starts falling
tomorrow rather than next week. Then do the large one.

The instinct to attack the biggest factor first is the same instinct that attacks the biggest ratio
change first, and both cost you days at the full bill.
</details>

**D4.** A bolt turns out to need a component scheduled three days later. What do you do?

<details><summary>Answer</summary>

**Stop and say so, before starting it.** A bolt that cannot be built alone was cut wrong, and the fix
belongs with the architect's dependency order — not with the engineer who discovered it at 2pm and is
now improvising a stub nobody agreed.

Then pick up a bolt that *can* stand alone — usually a piece of exact code, which is why exact code
is scheduled early.

The failure to avoid is the heroic one: building half of it, mocking the rest, and creating an
integration problem for the day the real component lands.
</details>

---

## Set E · running

**E1.** Three months in, no code has changed and a customer complains about behaviour nobody
recognises. What failed?

<details><summary>Answer</summary>

**Drift**, and the absence of a drift KPI.

A probabilistic system changes behaviour when the world shifts under it: a supplier changes a format,
an upstream field starts arriving empty, the mix of incoming cases moves. No deploy, no error, no
alert.

The control is an output-mix chart, weekly, with a threshold — 5% week over week is a working default
— and the rule that **a drift alert re-opens the release gate**. It belongs on the product dashboard
next to conversion, because the question is "is it still doing what we launched?"
</details>

**E2.** Your postmortem concludes: "the passenger used a known jailbreak string; we will add it to the
blocklist." Critique.

<details><summary>Answer</summary>

It names the **input**, not the missing control, so it prevents exactly one string. The next attack is
worded differently and works.

Re-ask the question: *which enforced control, if present, would have made this impossible?* Almost
certainly a cap in the tool signature, a confirmation token, or both.

A blocklist is a **probability reducer**, which has a place. It is not a boundary, and writing it in
the fix column of a postmortem is how a team believes the class of incident is closed when only one
instance is.
</details>

**E3.** Your two-number report shows 43% fewer person-days and $310 a story in tokens. The sponsor
asks whether this is good. Answer.

<details><summary>Answer</summary>

Convert both to the same unit and give a net, then a trajectory.

43% of 8 person-days is 3.4 days saved. At a loaded day rate, that is comfortably more than $310 — so
the cycle pays, even before the review hours are counted against it.

Then the honest part: review hours are **up** 0.8 a story, which is normal in cycle one and falls as
the artefacts sharpen, and re-runs are at 1.4, which is the leak signal to watch.

The answer the sponsor needs is "yes, and here is the trajectory", not a percentage.
</details>

**E4.** The VP wants an AI maturity metric. They propose counting tools adopted per team. Offer an
alternative in one minute.

<details><summary>Answer</summary>

"Tool count rewards adopting tools, which is the thing we least need to encourage. Six controls, each
present or absent: a context file the agent reads; every item with a spec, a bar and an owner; the
harness gating merges per slice; caps in tool signatures; a redacting trace; production evidence by
segment with drift watched.

Your level is how many you have. Your next step is the first one you do not. A team with nine tools
and none of these is level one — and I can show you that team."

It fits on a slide, it is auditable in an afternoon, and it names the next action instead of just
scoring the past.
</details>

---

## Set F · interview questions

Questions worth being able to answer, whichever side of the table you are on.

**F1.** *"How accurate does your agent need to be?"*

<details><summary>What a strong answer sounds like</summary>

"It depends on the slice, and it is derived rather than chosen. The bar is damage divided by damage
plus saving, per slice. On our codeshare slice a wrong answer costs about four times what a right one
saves, so the bar is 80%. On refunds, unheld, it would be 98% — so we put a human hold on the charge,
which drops the damage and the bar to about 70%, and that is why we could ship it."

The tells of a weak answer: a single number for the whole product, a number with no derivation, or
"as accurate as possible".
</details>

**F2.** *"How do you know it works?"*

<details><summary>What a strong answer sounds like</summary>

"A golden set of real historical cases, tagged by slice, scored on every change in CI. Exact checks
first, then an independent judge. We gate on the **lower bound** of the score per slice, not the point
estimate, because 82% on forty cases does not prove an 80% bar. Then a shadow run beside the human
desk before any traffic, and a cut-over at five percent that widens on live evidence."

The distinguishing detail is the lower bound. Most candidates stop at "we have an eval set".
</details>

**F3.** *"What is genuinely new about securing an agent?"*

<details><summary>What a strong answer sounds like</summary>

"Almost nothing, and one thing. Least authority, bounded tools, gates on money, traceability — all
old, all applicable.

The genuinely new threat is **prompt injection**: every piece of text the agent reads is a possible
instruction, including partner API responses and uploaded documents, not just user input. The
consequence is architectural rather than tactical: a rule in a prompt is a request, and a request can
be talked past, so anything consequential has to be enforced in the tool contract."
</details>

**F4.** *"Your team wants to use five agents. What do you ask?"*

<details><summary>What a strong answer sounds like</summary>

"What named limit justifies each hand-off? Five agents is ten possible hand-offs, and coordination
cost grows faster than the work.

I would start single and escalate on a written condition — a context that genuinely overloads, or
parallel sub-tasks a fan-out tool cannot express. Parallelism is a property of a tool, not of an agent
count. And I would put the escalation condition in the record, because otherwise the swarm comes back
by default at the next design review."
</details>

**F5.** *"How do you report on an AI programme?"*

<details><summary>What a strong answer sounds like</summary>

"Two numbers, always together: person-days saved and money spent. Plus two rows that keep them honest
— review hours added, which is high in the first cycle and falls, and re-runs, which is the leak
signal.

A first cycle can genuinely save time and cost more. That is survivable if it comes from the team and
fatal if it comes from finance. The programme gets cancelled on the number you hid, not the one you
showed."
</details>

---

## Set G · reading a symptom

The other sets give you a question. These give you what you would actually have: a number that moved,
a log line, a report that reads fine. Name the cause, then name the control that would have made it
impossible.

**G1.** The caching line item on your bill says caching is on. Your gateway reports a hit ratio of 4%.
No prompt text changed this week, but on Monday a per-customer context block was added at the top of
the system message. What happened, and what is the fix?

<details><summary>Answer</summary>

**The prefix moved.** A cache matches an *exact* prefix. Putting something that differs per customer
at the top means no two calls share a prefix, so every call is a miss — while the line item goes on
saying caching is enabled, because it is.

The fix is ordering, not configuration: stable first (tools, system instructions, shared context),
then the cache marker, then everything that changes. The tell is the shape of the symptom — a hit
ratio near zero *with caching on* is almost never a config bug and almost always a prefix-ordering
bug. See [How to Control the Token Bill](How-to-Control-the-Token-Bill).

The control: the ordering is part of the prompt's structure, so it belongs in review. A diff that
inserts anything above the marker is a cost change and should be read as one.
</details>

**G2.** Your golden set has passed at 88% against an 85% bar for six weeks. This week it passes at
87%. Production complaints have tripled. Where do you look?

<details><summary>Answer</summary>

**At the denominator, not the score.** The golden set is fixed; production is not. A set that still
passes while production degrades is a set that no longer represents traffic.

Compare the *slice mix* at launch with the mix now. The usual finding is that a slice which was 5% of
traffic is now 30% — and that slice has its own bar, usually a higher one, because its damage per
case is higher. The aggregate score barely moves because the set's composition never moved.

This is why the bar is per slice and why the set is tagged by slice. An untagged golden set cannot
show you this at all. See [How to Prove the Bar](How-to-Prove-the-Bar).

The control: a monthly comparison of the traffic mix against the set's mix, with a named owner. It
takes ten minutes and it is the cheapest drift detector there is.
</details>

**G3.** Median cost per call is flat. The p99 is up six times. Total spend is up 40%. What is
happening?

<details><summary>Answer</summary>

**A tail, not a shift.** Flat median means the common path is unchanged, so this is not a bigger
prompt or a different tier — both of those move the middle.

A p99 up six times with spend up 40% means a small share of calls is doing far more work than it
used to. That is attempts. Check **attempts per case**, not retries: the bill factor is
`(1 + r) / (1 + r₀)` on attempts, and a small rise in the tail moves the total a long way.

The usual cause is a loop with no cap — often two components politely handing work back to each
other. A runaway does not need a bug; it needs no breaker. See scenario 19 in the
[Scenario Library](Scenario-Library).

The control: a per-case attempt cap and an alarm on attempts, not on spend. Spend tells you after the
month; attempts tell you in the hour.
</details>

**G4.** A shadow run agrees with the desk on 91% of cases. Your expansion gate is 90%. Two of your
five slices were left out of the comparison because their volume was "too low to be meaningful". Do
you widen?

<details><summary>Answer</summary>

**No, and the exclusion is the finding.**

The threshold was always per slice. An aggregate that clears it tells you the *large* slices are
fine, which you mostly already knew. Worse, low-volume slices are usually the ones with the highest
damage per case — the unusual situations are exactly the ones people escalate.

Low volume is a reason to gather more evidence, or to keep the slice held while the others widen. It
is not a reason to leave it out of the gate. And note who made the call: excluding a slice from
gating is the product manager's decision, not the analyst's, because it changes what the gate means.

This is scenario 17 with the numbers changed, and it is one of the two most common ways a gate gets
passed without being met.
</details>

**G5.** A trace shows `issue_refund` called with $380 on a case where the policy cap is $400. The fare
was $220. Nothing errored. What is missing?

<details><summary>Answer</summary>

**The cap is not the control.** A cap bounds the worst case; it does not make the amount correct. A
tool that accepts any value at or under the cap has delegated the *amount* to the model.

What is missing is the relation: the refund is bounded by the fare, not only by the policy ceiling.
That boundary belongs in the tool signature, where it is enforced, rather than in the prompt, where
it is requested. `issue_refund(amount)` with a cap is one control; `issue_refund(booking_id)` that
derives the amount is a different and much stronger one.

The wider lesson is the shape of the day-82 incident: several layers each *claimed* the constraint
and none enforced it. Ask of every stated limit — which line of code refuses? If the answer is a
sentence in a prompt, there is no control. See
[How to Run a Missing-Control Postmortem](How-to-Run-a-Missing-Control-Postmortem).
</details>

---

## Running these as a session

| Format | Sets | Time |
| --- | --- | --- |
| Stand-up warm-up | One question | 5 min |
| Team workshop | A and B | 45 min |
| Design review practice | C and D | 60 min |
| Incident-review practice | G, then E | 50 min |
| Interview preparation | F, then B | 45 min |
| Full session | All, with the [simulations](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/simulations/master) between sets | Half a day |

**Three sessions that are worth running as written.**

*Ninety minutes, a team that has never done this.* A1 and A2 to establish that most of a backlog is
not AI — this is the single most useful thing a new team learns, and it lands better as an exercise
than as an assertion. Then B1 and B2, because the bar and the chain are the two pieces of arithmetic
everything else depends on. Then C1. Stop there. Do not add D; a team that has just learned the bar
is not ready to argue about bolt order, and trying makes both worse.

*Fifty minutes, after an incident.* G5 first, whatever the incident was, because "which line of code
refuses?" is the question that generalises. Then the G exercise nearest the symptom you actually saw.
Then E2. The point of ending on E2 is that it is about the *postmortem*, not the incident — and a
team that has just been through one will recognise its own draft in it.

*Forty-five minutes, an interview loop.* F1 and F3, then one of B3, B4 or G2 to see whether the
answers to F have arithmetic underneath them. Someone who answers F1 well and cannot do B3 has read
about this. That is worth knowing, and it is not disqualifying — but it is a different hire.

**Where these come from.** Every exercise is a compression of something on another page; the finder
above says which. If an answer here seems to skip a step, the page named in the table has the long
form, and the [Formulas](Formulas-and-Calculators) page has every calculation with its derivation.

Want these graded automatically? The repository's
[L.A.B. Simulator](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs) runs
code drills in the
[Arena](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/75) — post a comment
and a bot grades it.

---

**Next:** [Formulas and Calculators](Formulas-and-Calculators) · [Scenario Library](Scenario-Library)
· [Decision Trees](Decision-Trees) · [Anti-Patterns](Anti-Patterns)
