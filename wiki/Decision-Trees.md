# Decision trees

Eleven decisions this playbook makes the same way every time, each drawn as a tree. Print the ones you
use; they are meant to be settled in minutes, not debated in meetings.

A tree is thinking that was already done, recorded so the same question stops costing a meeting. The
questions come in a fixed order, each "no" ends the exercise, and the leaf is written down with a
date. Each carries what is decided and who decides it, the diagram, the running case walked to a
leaf, the cost of the wrong leaf, and the honest boundary. Six end in a record you can paste in.

**The running case.** **SkyWays** is an airline rebooking assistant for disrupted passengers: **240
cases a day**, three slices — same-day, codeshare, refund. The
[Scenario Library](Scenario-Library) has the episodes; this page has the branches.

---

## 1 · Is this AI at all?

### The decision

Whether a request becomes a probabilistic system at all, or a function, or a person, or an assisted
workflow with a person on the end of it. The product manager owns the verdict and the architect owns
the evidence under it. It is asked before the word *agent* enters any document, because every other
tree assumes this one came back agentic. The questions are ordered by cost: each is cheaper to answer
than the next, and each "no" ends the exercise before you have spent anything.

```mermaid
flowchart TD
  A["A request"] --> Q1{"Genuine judgement call?"}
  Q1 -->|no| R1["<b>A rule.</b> Code does it."]
  Q1 -->|yes| Q2{"Volume high enough to be worth<br/>a probabilistic system?"}
  Q2 -->|no| R2["<b>A person is cheaper.</b>"]
  Q2 -->|yes| Q3{"Is a wrong answer recoverable?"}
  Q3 -->|no| R3["<b>A person in the loop.</b><br/>Assisted, gated."]
  Q3 -->|yes| R4["<b>Agentic</b> — with the<br/>unrecoverable steps gated."]
```

Expect two or three of your top five requests to come back as rules. That is the healthy answer.

### Worked

- **Judgement call?** Yes. Which alternative suits this passenger depends on the visa, the onward
  booking and how they travel. Two experienced desk agents differ about the case, not the procedure.
- **Volume high enough?** Yes. 240 disrupted cases a day carries a golden set, a harness, five gates
  and a per-call bill. Eleven a week would not.
- **Recoverable?** **Partly.** A proposed rebooking can be withdrawn before it is confirmed; a refund
  that has left the account cannot.
- **Leaf: agentic, with the unrecoverable steps gated.** That one word *partly* is why the design has
  a named approver on money and nothing else. The scope in which the verdict flips, written the same
  day: same-route, same-day moves only.

### What it costs to get wrong

Answer yes at question one when the criteria sit in a published table, and you have built a harness,
a golden set and a per-call bill to reproduce a lookup — **$144 a day** of run cost at $0.60 a case
before a minute is saved. The reverse error is dearer: a "no" on recoverability recorded as "yes,
eventually" ships an unheld money action, which runs straight to day 82.

### When this tree does not apply

Question two assumes you can estimate volume. With no ticket history the honest answer is a range,
and a range straddling the fixed cost of a harness means the tree cannot decide — run a manual month
and count. It also says nothing about whether the work is *worth* doing; that is the
[value line](Formulas-and-Calculators), and a request can clear all three questions and lose money.

<details><summary><b>Template · AI-fit verdict</b></summary>

```markdown
# AI-fit · <request> · <date>
Verdict owner: <name>   Evidence owner: <name>   Status: accepted / superseded by <ADR-n>

| # | Question | Answer | The evidence, not the opinion |
|---|----------|--------|-------------------------------|
| 1 | Genuine judgement call? | yes / no | <what two competent people would differ about> |
| 2 | Volume worth a probabilistic system? | yes / no | <n> cases/day, from <source, dated> |
| 3 | Wrong answer recoverable? | yes / no / partly | <what can be undone; what cannot> |

Leaf: <a rule | a person is cheaper | assisted and gated | agentic, unrecoverable steps
gated>. Reached <date>, in front of <who was present>.
The scope in which this is a rule: <e.g. same-route, same-day moves only>.

## Steps gated whatever the model quality becomes
| Step | Why it is unrecoverable | The gate |
|------|-------------------------|----------|
| <issue_refund> | <money leaves the account> | <named approver above $400> |

Rejected, with the number that rejected it: <a rule in code — cannot express the
judgement; <n>% of cases fall outside it> · <a person — <n>/day x <n> min x $<n>>
Revisit when: <named trigger, never a date>
```
</details>

---

## 2 · What kind of step is this?

### The decision

For one step inside a feature, which of three kinds it is, and therefore what builds it and what
proves it. The architect owns the map and the engineering lead builds from it. This is where the
arithmetic lives, and it is answered per step — a feature of nine steps is answered nine times.

```mermaid
flowchart TD
  A["One step of the feature"] --> Q1{"Must it be right<br/><b>every single time?</b>"}
  Q1 -->|yes| E["<b>EXACT</b><br/>a function · proven by a unit test"]
  Q1 -->|no| Q2{"Does it change<br/>something real?"}
  Q2 -->|yes| C["<b>CONSEQUENTIAL</b><br/>a tool + a gate · proven by a confirmation"]
  Q2 -->|no| B["<b>BEST-GUESS</b><br/>a model call · proven by a measured share"]
```

**The rule that never breaks: the best-guess machine never does the exact math.** The model may call
the function and read the result; it never computes the value.

### Worked

- **"Rank the alternatives for this passenger."** Right every time? No. Changes something real? No. →
  **best-guess**, proven by the codeshare slice at an 80% bar.
- **"What is the fare difference?"** Right every time? Yes — a passenger charged $80 where the rules
  say $62 is a complaint and a refund. → **exact**, a function with a unit test, called and read back.
- **"Issue the refund."** Not exact arithmetic, but it changes something real and irreversibly. →
  **consequential**, a tool with a typed cap and a confirmation token.
- **The second leaf is the one that gets missed.** Written as one step it becomes one prompt
  containing the word *exactly*, which returns a confident wrong number with no error and no red test.

### What it costs to get wrong

An exact step built as a best-guess step fails fluently: no exception, no failed assertion, and the
first person to notice is the passenger reading the invoice. Four steps at 90% chain to **65.6%**, so
turning one exact step into a model call does not lose ten points — it loses the multiplication.

### When this tree does not apply

The first question assumes "right" is well defined for the step. For a summary, a tone or a ranked
list there is no single right answer, and best-guess is the correct leaf. The trap is a step where
"right" *is* well defined and nobody wrote the definition down — it reads as judgement because the
rule is undocumented. Ask who would arbitrate a dispute; if the answer is a document, it is exact.

---

## 3 · How much autonomy?

### The decision

What a single action may do without a person. The product manager owns the record, compliance signs
the rows that move money, and the architect turns each leaf into a tool signature. It is answered per
**action**, which is why one feature holds three different leaves at once.

```mermaid
flowchart TD
  A["One action"] --> Q1{"Cost of one<br/>wrong action?"}
  Q1 -->|"~nothing"| Q2{"Reversible?"}
  Q1 -->|"real money,<br/>identity or policy"| R4["<b>Named approver,<br/>every time</b>"]
  Q1 -->|"irreversible or<br/>safety-critical"| R5["<b>Not delegated</b>"]
  Q2 -->|yes| R1["<b>Acts alone</b>"]
  Q2 -->|"with effort"| R2["<b>Acts, monitored</b><br/>or with a veto window"]
```

Per **action**, never per product. **Reversibility is the hinge**, and it is the column that ends most
arguments. Levels rise only on evidence; an incident usually drops one.

### Worked

- **`search_flights`.** Cost of one wrong action: about nothing, a bad option a human ignores.
  Reversible: yes. → **acts alone.**
- **`rebook_passenger`.** No money, but undoing it means a second seat movement and a second
  notification. Reversible with effort. → **acts, monitored**, with a veto window until reissue.
- **`issue_refund`.** Real money leaving the account. → **named approver, every time**, above the
  $400 line compliance set on day six. **`change_identity`** is irreversible in the audit trail, so
  it reaches the last branch: **not delegated.**
- **Day 82 tested the third leaf and it was not there.** The cap and the approver lived in a document
  and in a prompt, and $2,000 left the account.

### What it costs to get wrong

One leaf recorded and not enforced is the whole of day 82: **five claimed layers, none enforced**, and
a **$2,000** refund that was not owed. The opposite error has a price too — an approver on
`search_flights` puts a person in front of 240 lookups a day and removes the saving entirely.

### When this tree does not apply

The first branch assumes damage can be priced. A wrong clinical summary, a wrongly refused benefit or
a mis-stated legal position has no dollar figure, and inventing one is worse than admitting you
cannot — where damage resists pricing, the action needs a hold regardless of any number. The tree
also ignores **frequency**: something cheap to get wrong once and done 240 times a day is not cheap.

<details><summary><b>Template · Autonomy record, per action</b></summary>

```markdown
# Autonomy · <feature> · v<n> · <date>
Owner: <PM name>   Money rows signed by: <compliance name>, <date>

| Action | Cost of one wrong one | Reversible? | Level | Enforced where |
|--------|----------------------|-------------|-------|----------------|
| <search_flights> | <~nothing> | yes | acts alone | — |
| <rebook_passenger> | <a second seat movement> | with effort | monitored, <n>-min veto | <path> |
| <issue_refund> | <$<n>, irreversibly> | no | **named approver** | <signature + test> |
| <change_identity> | <unbounded> | no | **not delegated** | <permission set> |

## For every gated row: what enforces it, and the test that was red first
| Action | The limit | File and line | Test that proves it raises |
|--------|----------|---------------|----------------------------|
| <issue_refund> | <$400, config/caps.yaml> | <src/tools/refund/issue.py:41> | <test name> |

Who may mint the confirmation token: <the approver's screen, signed, scoped to one
booking and one amount, expiry <n> min>. The agent cannot construct it because: <why>.

## Level changes
| Date | Action | Was | Now | Why | Evidence that restores it |
|------|--------|-----|-----|-----|---------------------------|
| <date> | <issue_refund> | <approver> | <not delegated> | <incident <id>> | <n> clean weeks |
```
</details>

---

## 4 · Hard gate or soft gate?

### The decision

Whether an open decision halts a phase or runs alongside the build behind a placeholder. The
architect classifies and the delivery lead holds the register. Every open decision goes through it at
the start of the phase and again at each weekly review, because evidence is allowed to change the
answer in either direction.

```mermaid
flowchart TD
  A["An open decision"] --> Q1{"Reversible cheaply once<br/>the build has started?"}
  Q1 -->|no| H["<b>HARD</b><br/>settle before the phase closes"]
  Q1 -->|yes| Q2{"Can the build proceed<br/>behind a placeholder?"}
  Q2 -->|no| H
  Q2 -->|yes| Q3{"Named owner and a date?"}
  Q3 -->|no| H
  Q3 -->|yes| Q4{"Does everything downstream survive<br/>if the answer changes?"}
  Q4 -->|no| H
  Q4 -->|yes| S["<b>SOFT</b><br/>runs alongside, behind a stub"]
```

**A single no makes it hard.** For SkyWays, three of eleven are hard and eight run in parallel. Treat
all eleven as hard and the build waits behind every one.

### Worked

- **Model tier per slice.** Reversible cheaply? Yes, it is a routing table. Placeholder? Yes,
  everything on the mid tier behind the gateway. Owner and date? Yes. Downstream survives? Yes. →
  **soft**, settled by the shadow run.
- **The framework choice.** Four yeses, behind an interface layer. → **soft**, an ADR on day 20.
- **The autonomy level on money.** Reversible cheaply once the build has started? **No** — a regulator
  has a rule about it and the tool contract is built against it. → **hard** at the first question, and
  the other three are not asked.
- **The AI-fit verdict and the spec, bar and guardrails** fail that same first question.
- **Three hard, eight soft**, and every soft one names a placeholder you can open in the repository.

### What it costs to get wrong

Classify all eleven as hard and the build waits behind a framework choice an interface layer would
have deferred entirely — three weeks for a decision that was reversible all along. Classify the money
one as soft and its placeholder is *the model behaves sensibly*, which cost **$2,000** on day 82.

### When this tree does not apply

Question two assumes a placeholder can be built, and a decision that shapes the data model rather
than a call site may have nothing to stub. Question three is the one answered generously: a named
owner is a person who knows they own it, and a date is in a calendar rather than "before P2". The
tree classifies a list rather than producing one, and an unnoticed open decision is on no list.

<details><summary><b>Template · Gate classification, one row per open decision</b></summary>

```markdown
# Gate classification · <feature> · <phase> · <date>
Classified by: <architect>. Re-checked at every weekly review. ONE "no" makes it HARD.

| # | Open decision | Q1 reversible | Q2 placeholder | Q3 owner+date | Q4 downstream | Verdict |
|---|---------------|---------------|----------------|---------------|---------------|---------|
| 1 | <model tier per slice> | yes | yes | yes | yes | soft |
| 2 | <autonomy on money> | **no** | — | — | — | **HARD** |

## Hard — what is blocked until each is settled
| # | Decision | The question that made it hard | Blocked | Settle by |
|---|----------|-------------------------------|---------|-----------|
| <n> | | <Q1: not reversible> | <what cannot start> | <date> |

## Soft — the placeholder you can open in the repository
| # | Decision | Placeholder today | Path | Owner | Settled by | Due |
|---|----------|-------------------|------|-------|------------|-----|
| <n> | | <stub / interface / flag> | <src/...> | <name> | <the evidence> | <date> |

Re-classified this cycle: <#n, soft -> HARD, because a slice now needs it and nothing
downstream survives a change>
Hard count: <n>. More than three is a classification failure, not a careful team.
```
</details>

---

## 5 · How many agents?

### The decision

The topology: one agent with tools, an orchestrator with workers, or a full team. The architect
decides and writes the hand-off count beside the diagram. The default is not a preference — it is
where the tree returns unless a named condition moves it.

```mermaid
flowchart TD
  A["A feature"] --> B["<b>Start single.</b><br/>One agent with its tools"]
  B --> Q1{"Does one context<br/>genuinely overload?"}
  Q1 -->|yes| C["Orchestrator + workers"]
  Q1 -->|no| Q2{"Parallel sub-tasks that a<br/>fan-out tool cannot express?"}
  Q2 -->|yes| C
  Q2 -->|no| Q3{"Complex, multi-team<br/>and audited?"}
  Q3 -->|yes| D["A full agent team"]
  Q3 -->|no| B
```

Five agents have **ten** possible hand-offs. Parallelism is a property of a **tool**, not of an agent
count. Write the escalation condition down, or the swarm returns by default.

### Worked

- **Start single.** One agent, four tools: search, rebook, refund, notify.
- **Does one context genuinely overload?** No. A disruption is one passenger, one itinerary and one
  fare-rule set — 2,100 tokens a call at the day-30 baseline.
- **Parallel sub-tasks a fan-out tool cannot express?** No. Searching six partner airlines at once is
  fan-out *inside* `search_flights`: one tool, one call, no hand-off.
- **Complex, multi-team and audited?** No. One team, one repository.
- **Leaf: stay single**, with the escalation condition in the record — if a case needs a visa
  determination and a fare re-computation in the same turn and the context exceeds the budget,
  escalate to orchestrator plus workers and record the case that triggered it.

### What it costs to get wrong

Five agents create **ten** possible hand-offs, and each is a place a field is dropped, re-serialised
or silently defaulted; the debugging cost is not linear in the agent count because the failure lives
in the edges. The other direction is cheap and loud — an overloaded single agent truncates context
and produces obvious nonsense.

### When this tree does not apply

It assumes hand-offs are the dominant cost, which holds while the work sits inside one trust
boundary. Where sub-tasks have genuinely different boundaries — data residency, regulator, tenant,
credentials — separation is a security requirement and the hand-off count is a price you pay. It
also assumes one delivery team; two teams that must ship independently already have a boundary, and
pretending otherwise produces one agent with two owners.

---

## 6 · Where does this rule live?

### The decision

Whether a rule is written in the prompt or enforced in a tool signature. The engineering lead decides
and the authority budget supplies the input. It is the shortest tree here because the consequence is
binary: one branch produces something a model can be talked past, the other produces something it
cannot.

```mermaid
flowchart TD
  A["A rule"] --> Q1{"If the model were talked<br/>past it, would it cost money,<br/>expose data or be irreversible?"}
  Q1 -->|yes| T["<b>The tool signature.</b><br/>Typed, bounded, raises.<br/>Keep the sentence in the prompt as policy."]
  Q1 -->|no| P["<b>The prompt.</b><br/>It is policy, and policy is fine there."]
```

> A prompt is a **request**. A tool contract is a **boundary**.

### Worked

- **"Never refund more than $400 without a named approver."** Talked past, it costs money — on day 82
  it cost **$2,000**. → **the tool signature**: a typed, bounded parameter that raises rather than
  clamps, plus a confirmation token minted on the approver's screen.
- **The prompt sentence stays**, with a comment naming the file that enforces it. That comment stops
  the next engineer deleting the signature check because the prompt covers it.
- **"Prefer the earliest arrival when two options are within thirty minutes."** Talked past, it costs
  a slightly worse itinerary. → **the prompt**, proven by the golden set rather than by a test.
- **The two tests that are the step:** an over-cap call raises, a call with no confirmation token
  raises. Both were red before they were green.

### What it costs to get wrong

A cap in a prompt reads exactly like a cap and nothing in code review flags it, which is why five
people in the SkyWays design review believed the $400 limit existed and the ledger disagreed. One
wrong leaf produced a **$2,000** unowed refund, a postmortem, an amended ADR and an autonomy level
dropped by one. The other direction is mild: a preference hard-coded makes the agent rigid.

### When this tree does not apply

It assumes the rule is expressible as a boundary — a parameter, a type, a range, a token. Rules about
tone, ordering, disclosure or what to say when the answer is unknown have no violation detectable in
a signature, and they belong in the prompt with a golden-set case behind them. It also assumes a tool
exists to carry the signature; where the step is still a paragraph of prompt with no call site, turn
it into a tool first and run this tree second.

<details><summary><b>Template · The policy pair, one per rule</b></summary>

```markdown
# Policy pair · <rule, in one sentence> · <date>
Source: <authority budget v<n> / constraint C-R<n> / <name>, <document §>>

Talked past, would it cost money, expose data, or be irreversible? <yes / no>
Worst case, concretely: <what actually happens>.   Leaf: <tool signature | prompt only>

## The request — what stays in the prompt, labelled
> <the sentence, verbatim as it appears in the prompt file>
File: <prompts/...>   Labelled: "policy, not enforcement — the boundary is in <file>"

## The boundary — only if the leaf is "tool signature"
| | |
|---|---|
| Tool and parameter | <issue_refund(amount: Decimal, 0 < amount <= cap)> |
| Cap comes from | <config/caps.yaml, reviewed like code> |
| On breach | **raises** <RefundCapExceeded> — not clamps, not logs, not warns |
| Confirmation | <token minted on the approver's screen; scoped, signed, expires> |

## The two tests, which were red first
| Test | Asserts | File | Red on |
|------|---------|------|--------|
| <test_over_cap_raises> | <a $5,000 attempt raises> | <tests/...> | <date> |
| <test_no_token_raises> | <a call with no token raises> | <tests/...> | <date> |

The grep that would have found this rule sooner: <never | always | do not | ask before
| $ | limit | maximum> over <prompts/**>
```
</details>

---

## 7 · Which review band?

### The decision

How many people read a change before it merges, and which people. The engineering lead owns the
ladder, the architect maps tools to bands from the authority budget, and a path rule in the
repository applies it. The interesting property is that nobody answers this one by hand.

```mermaid
flowchart TD
  A["A change"] --> Q["<b>What is the most dangerous<br/>tool it touches?</b><br/><i>not: how large is it</i>"]
  Q --> R1["reads only → <b>R1</b><br/>harness, review at end"]
  Q --> R2["reversible write → <b>R2</b><br/>one reader before merge"]
  Q --> R3["hard to reverse → <b>R3</b><br/>approve first"]
  Q --> R4["money · identity · policy → <b>R4</b><br/><b>two readers, every time</b>"]
  Q --> R5["irreversible → <b>R5</b><br/>not delegated"]
```

A change **inherits the band of whatever it touches**. Three lines in a refund cap is R4; four hundred
lines of help text is R1. The band comes from a path rule in the repository, never from the author.

### Worked

- **Day 60, nine pull requests, a four-day queue.** Three lines in the refund tool's cap check touch
  `issue_refund` → money → **R4**, two named readers.
- **Four hundred lines rewriting the help text** touch nothing that acts → **R1**. A read-only search
  filter → **R2**, one reader.
- **Shared code takes the band of its most dangerous caller**, so the formatting helper used by both
  search and refund is R4 — the rule teams most often omit.
- **The arithmetic:** 2×2 + 3×1 + 4×0 = **7 slots** against 18. At 4.5 slots a day that is **1.6
  days** against **4.0**. Nobody read faster and nobody was hired.

### What it costs to get wrong

Band by size and the help-text rewrite gets two senior readers while three lines in a refund cap get
a quick approval — a money path unread on the day it changes. Band everything at the top instead and
the queue stays at **18 slots and 4.0 days**, caution paid for on the changes that never needed it.

### When this tree does not apply

It assumes reviewers are interchangeable. If one person is the only one who can review the payment
path, that lane has a capacity of one whatever the headline slots-per-day says, and the average hides
it — compute the queue per band. It also assumes the map is complete: a path in a diff and not in the
map is a **gap**, never an R1, and treating unbanded as low is the commonest way an escape happens.

<details><summary><b>Template · Band record for a change</b></summary>

```markdown
# Band · <change / PR reference> · <date>
Assigned by: <the path rule, .github/review-bands.yml v<n>>. Not by the author.

| Path touched | Band from the map | Set by |
|--------------|-------------------|--------|
| <src/tools/refund/cap.py> | **R4** | <R4 glob> |
| <docs/help/*.md> | R1 | <R1 glob> |

**Band of the change: <R4>** — the highest band of any path it touches, set by <path>.
Lines changed: <n>. That number is not an input to the band.
What a wrong version would do at its worst: <one sentence — the band, restated>.

Unbanded paths are gaps, never R1: <path — serves <tool> — map fix owned by <name>>

## Readers and queue effect
| Band | Readers required | Named | Read on |
|------|------------------|-------|---------|
| <R4> | 2, named | <name>, <name> | <date> |

Slots consumed: <n>. Queue: <slots needed> / <slots per day> = <n> days.
```
</details>

---

## 8 · Does caching pay here?

### The decision

Whether to cache a prompt prefix and, if so, which window. The engineering lead decides per prompt
from three facts rather than from instinct: how often the prefix repeats, how large it is, and how
long the gap is between calls. It is one of the four factors that multiply into a surprise bill.

```mermaid
flowchart TD
  A["A prompt prefix"] --> Q1{"Will it be reused<br/><b>more than once?</b>"}
  Q1 -->|no| N["<b>No.</b> A write costs more than the call"]
  Q1 -->|yes| Q2{"At least ~1,024<br/>cacheable tokens?"}
  Q2 -->|no| N
  Q2 -->|yes| Q3{"Gap between calls?"}
  Q3 -->|"seconds to minutes"| F["<b>Five-minute cache</b><br/>write 1.25×, refreshes free on each hit"]
  Q3 -->|"longer than five minutes"| H["<b>One-hour cache</b><br/>write 2× once, beats paying 1.25× every call"]
```

And check the layout: **tools → system → stable context → marker → the request.** One model per task;
no timestamps inside the cached block.

### Worked

- **The live passenger path.** Reused more than once? Yes, every turn. Above 1,024 cacheable tokens?
  Yes, once tools, system and the fare-rules context sit above the marker. Gap? Seconds. →
  **five-minute cache**. Twenty calls cost 1.25 + 19 × 0.1 = **3.15 units** against 20 uncached,
  about **84% saved**.
- **The overnight re-scoring job**, one call every twelve minutes, reaches the other leaf. Five calls
  in an hour cost 5 × 1.25 = **6.25** on the five-minute window, or 2 + 4 × 0.1 = **2.40** on the
  one-hour window. The cheaper write, paid every call, is the dearer option.
- **Day 75 is the counter-example.** An engineer moved the passenger's request to the front of the
  prompt for clarity. Caching stayed switched on and the hit ratio fell from 71% to **9%**.

### What it costs to get wrong

That reordering contributed a **1.30** cache factor to a bill that landed at **4.4×** its estimate on
flat traffic. Caching a prefix used once costs 1.25 units against 1.00 — a 25% surcharge on calls
that were already cheap. Only the measured hit ratio distinguishes a working cache from a dead one.

### When this tree does not apply

The arithmetic assumes the prefix above the marker is **byte-identical** across calls, which is
stronger than "roughly the same". One timestamp, request id or session id inside the block takes the
hit ratio to zero while every branch still reads yes. The cache is also model-scoped, so a task that
switches model mid-flight pays the write twice. Hash the prefix across a hundred consecutive calls
before trusting any leaf here.

---

## 9 · Which model tier?

### The decision

Which tier serves a class of request. The engineering lead owns the routing table, the architect owns
the classes, and the shadow run settles the boundaries. It is decided per request class, and it is
one of the eight soft gates — "everything on the mid tier behind the gateway" is a legitimate start.

```mermaid
flowchart TD
  A["A request"] --> Q1{"Reasoning it<br/>actually needs?"}
  Q1 -->|"a lookup"| C["<b>Cheap tier</b>"]
  Q1 -->|"a policy question"| M["<b>Mid tier</b>"]
  Q1 -->|"genuinely multi-constraint"| F["<b>Frontier</b>"]
  C --> W["Every loop gets<br/><b>MAX_LOOPS = 5</b><br/>and a per-transaction token cap"]
  M --> W
  F --> W
```

Right-sized, not over- or under-routed. **A model too weak produces wrong answers that get re-run,
which costs more than the right model once.**

### Worked

- **"Is there a later flight on this route today?"** A lookup against a structured answer. →
  **cheap tier.** **"Does this fare rule permit a change without a fee?"** One document, one
  determination. → **mid tier.**
- **A codeshare rebooking with a visa, an onward booking and a partner fare rule** — three
  constraints that interact. → **frontier.**
- **All three leaves get the same guard:** `MAX_LOOPS = 5` and a per-transaction token cap, in the
  harness rather than in the prompt.
- **Day 75 shows the drift.** The frontier share was **100%** against a 50% baseline — a factor of
  **1.5** — built from six temporary escalations after hard cases, none carrying an expiry.

### What it costs to get wrong

Over-routing is the quiet one: a 1.5 tier factor multiplied by three other habits produced a bill at
**4.4×** estimate on flat traffic, and no decision in that chain looked wrong on the day it was
taken. Under-routing costs more than it looks — a cheap call that fails twice and then escalates has
paid three times for one answer.

### When this tree does not apply

It assumes the three tiers are a real choice. A request class with a hard latency ceiling may have
only one tier that meets it, and then the NFR answers the tree. It also assumes you can tell what
reasoning a request needs *before* routing it; where that judgement is itself a model call, its cost
and its error rate belong in the sum, and a classifier that mis-routes a tenth of frontier work into
the cheap tier can cost more in re-runs than routing everything to mid.

---

## 10 · How deep a process for this change?

### The decision

How much ceremony this change gets: which artefacts are produced, which gates are walked, and whether
the persona trail runs. The architect decides per change, in ten lines or fewer. Depth belongs to the
change rather than the team, and a depth decision that takes an hour is its own overhead.

```mermaid
flowchart TD
  A["A change"] --> B["One-line fix"]
  A --> C["A feature"]
  A --> D["Audited, multi-team"]
  A --> E["Depth unknown"]
  B --> B1["Spec + a single agent.<br/>Skip discovery and most design"]
  C --> C1["SDD + the five gates"]
  D --> D1["SDD + the BMAD persona trail"]
  E --> E1["AI-DLC: start shallow,<br/>escalate on evidence"]
```

**SDD is the backbone everywhere.** BMAD is layered on only where the work is audited and multi-team —
on a small feature it is twelve personas between you and a one-line change.

### Worked

- **Codeshare rebooking**, the first real slice: a feature, one team, a bar and a golden set. →
  **SDD plus the five gates.**
- **A 900-line refactor of the read-only reporting view:** large and shallow. → **spec plus a single
  agent**, and the size of the diff is not what put it there.
- **The one-line change to the refund cap after day 82:** tiny and deep. A regulator reads the result,
  so it enters at **audited** and keeps the versioned trail however small the diff is.
- **The retrieval design on day 20**, where nobody could say how deep it went. → **AI-DLC: start
  shallow, escalate on evidence**, and it escalated in week three when a slice needed cross-session
  state.

### What it costs to get wrong

Run the persona trail on a typo fix and six artefacts are generated for one line; within a month the
team is quietly skipping the trail on everything, including the audited work it exists for. The
mirror error is the same mistake upside down — an editor agent and R1 ceremony on a refund cap, which
is how three lines that move money reach production on one quick approval.

### When this tree does not apply

It assumes somebody can classify the change before it starts, which is false often enough that the
fourth branch exists. Treat "depth unknown" as a real answer rather than an admission; the failure is
picking a branch to look decisive and never re-opening it. The tree also chooses only what is
*added* — SDD runs on every branch, and a change with no spec change is one nobody can review.

---

## 11 · Ship it, or not?

### The decision

Whether a change goes live. The QA lead brings the readout, the product manager owns the bars, and a
person signs the release gate. Four questions in a fixed order: the cheap deterministic check comes
first, and the question about money comes last because it is the one that is never waived.

```mermaid
flowchart TD
  A["A change"] --> Q1{"Exact checks green?"}
  Q1 -->|no| N["<b>Reject</b>"]
  Q1 -->|yes| Q2{"<b>Every</b> slice at or above its bar?"}
  Q2 -->|no| N
  Q2 -->|yes| Q3{"Lower bound clears the bar,<br/>not just the estimate?"}
  Q3 -->|no| M["<b>Cases owed.</b> Not a rejection"]
  Q3 -->|yes| Q4{"Money actions still gated?"}
  Q4 -->|no| N
  Q4 -->|yes| S["<b>Ship to 5%</b>,<br/>widen on live evidence"]
```

The second box is the one that catches the real regressions: an overall score can rise while the
slice that carries the risk falls below its bar.

### Worked

- **Day 45. Exact checks green?** Yes — fare arithmetic, cap arithmetic, schema validation.
- **Every slice at or above its bar?** Same-day 96% against 50%, codeshare 82.4% against 80%, refund
  held 74% against 71%. Yes, on the point estimates.
- **Lower bound clears the bar?** Codeshare is 412 right of 500; the 95% lower bound is **79.1%**
  against a bar of 80. **No.**
- **Leaf: cases owed, which is not a rejection.** Proving 82.4% against 80 needs **968** cases, the
  set holds 500, so the team owes **468** — about eighteen days of codeshare history to curate, or 81
  days at 5% of live traffic.
- **The third lever nobody had listed:** a hold on codeshare lowers the damage and brings the bar
  down to the number, the same lever that takes refunds from 98% to 71%.

### What it costs to get wrong

Read the point estimate as a pass and you ship a slice that has not been proven: 82% on forty cases
has a lower bound of **70%**, and every dashboard in the building shows the 82. Skip the last box and
the release leaves a money action ungated — on day 82 that answer was no and nobody had been asked.

### When this tree does not apply

It assumes every slice has a bar and a curated set behind it. A slice with no bar is not a pass; it is
**unmeasured**, and this tree cannot tell the two apart, so the first move on a new slice is a bar
rather than a run. The last box asks whether money actions are *gated* — day 82 is what happens when
that answer comes from the design document instead of from a test that was red an hour ago.

<details><summary><b>Template · Ship decision</b></summary>

```markdown
# Ship decision · <change> · run <date> · commit <sha>
Readout by: <QA lead>   Bars owned by: <PM>   Gate signed by: <name>

| # | Question | Answer | Evidence |
|---|----------|--------|----------|
| 1 | Exact checks green? | yes / no | <CI run link> |
| 2 | Every slice at or above its bar? | yes / no | <the table below> |
| 3 | Lower bound clears the bar? | yes / no | <the table below> |
| 4 | Money actions still gated? | yes / no | <test names that were red first> |

| Slice | Score | n | 95% lower bound | Method | Bar | Verdict | Cases owed |
|-------|-------|---|-----------------|--------|-----|---------|-----------|
| <same-day> | <n>% | <n> | <n>% | normal | <n>% | PASS | — |
| <codeshare> | <n>% | <n> | <n>% | normal | <n>% | **UNPROVEN** | <n> |

Method: Wilson below 100 cases, normal above. Stated per row.
Leaf: <reject | cases owed: <n> | ship to 5%>. Reached <date>.

## If "cases owed", the three levers, priced
| Lever | Cost | Days | Chosen? |
|-------|------|------|---------|
| Collect <n> more cases | <curation effort> | <n> | |
| Raise the score | <what would change> | <n> | |
| Lower the damage with a hold | <the hold> | <n> | |

Rollback rehearsed by <name> on <date>, took <n> min. It is a <flag / config change>.
```
</details>

---

## Where a model helps across these

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Run one tree across a backlog in bulk — ten items, the answer at each branch, the leaf, one line of justification. It is generous at the first branch of trees 1 and 2, so re-read every leaf that comes back *agentic* or *best-guess* |
| **Chat LLM, adversarially** | "Argue the other branch, as strongly as you can." One prompt per contested question. The strongest case against your leaf is the cheapest review of it you will get |
| **Claude Code** | Fetch the inputs these trees need out of the repository rather than out of memory: cases a day from the ticket export, cacheable tokens above the marker, which files each tool reaches, the reviewers on last quarter's merges |
| **Claude Code** | Turn a settled leaf into the thing that enforces it — the path rule from a band, the typed signature and its two tests from an autonomy level, the routing config from a tier decision |
| **Do not delegate** | The leaf on any tree whose branches mention money, identity or irreversibility. A model returns a plausible branch, and plausible is the precise failure trees 3, 6 and 11 exist to prevent |

---

## How to use a tree in a room

1. **Read the tree aloud before anyone answers anything** — questions and leaves, in order. Thirty
   seconds. People who have seen where the branches end argue about the evidence rather than about
   the destination they fear.
2. **Answer in the order drawn.** The order is cost: each question is cheaper than the next.
   Answering volume before judgement costs a system nobody has established needs to exist.
3. **Stop at the first stop.** A "no" that ends the exercise has ended it. Continuing "to be
   thorough" invites somebody to re-open the answered question using the later ones as an argument.
4. **Answer with evidence, or write UNKNOWN.** A branch taken on a number nobody can source is a
   branch taken on a preference. `UNKNOWN` names the follow-up call and whose it is.
5. **Record the leaf and the date on the screen, in the room.** Ambiguity re-enters between agreement
   and minutes. Fill in the template under that tree while people are still present.
6. **Name what would re-open it before anyone leaves** — a trigger, never a date. "Revisit in a
   quarter" means the argument returns in a quarter; "revisit when a slice needs cross-session state"
   means it returns when something has changed.

---

## Try it

Take the decision your team argued about most recently. Find it on this page. Walk it to a leaf out
loud, fill in the template beneath that tree, and write the one sentence that would re-open it. If a
branch stalls because nobody has the number, that gap is the reason the argument recurred.

<details>
<summary>If it is not here</summary>

Two possibilities, and they are worth telling apart.

**It is a genuine trade-off point** — two quality attributes pulling against each other, with no
general right answer. That is what a decision record is *for*. Write the ADR, name what you rejected,
and stop re-litigating it.

**Or it is a decision this playbook makes the same way every time, and your team has not adopted the
rule yet.** Autonomy arguments, agent-count arguments and review-depth arguments are almost always
this. Adopt the tree, and the argument becomes a two-minute lookup.

The tell: if the argument recurs every few weeks with the same people on the same sides, it is the
second kind.

A third case turns up less often. The tree covers the argument and keeps returning a leaf the team
will not accept — usually tree 3 or tree 11. That is an input nobody believes: a damage figure
somebody invented, or a bar never derived from one. Fix the input and the leaf stops being contested.
</details>

---

**Next:** [Formulas and Calculators](Formulas-and-Calculators) · [The Agentic PDLC](The-Agentic-PDLC)
· [Exercises and Answers](Exercises-and-Answers) · [Anti-Patterns](Anti-Patterns) ·
[Gates and Governance](Gates-and-Governance) · [The Eight Loops](The-Eight-Loops) ·
[How to Review by Risk Band](How-to-Review-by-Risk-Band) · [Scenario Library](Scenario-Library)
