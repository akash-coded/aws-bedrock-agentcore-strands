# Gates and governance

<!-- tutorial:lesson -->*New to this? Start with the lesson **[The five governance gates](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-governance-gates/)** — the idea step by step, with a worked problem. This page is the reference.*<!-- /tutorial:lesson -->

A gate is **a decision, with evidence in front of a named person, and their name on it.** It is not a
click, not a status column, and not a meeting that happens to end in "fine".

This page holds the five gates, the hard-and-soft split, the R1–R5 risk ladder, and the two-number
report. Live version:
[Governance](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/governance/gv-gates).

---

## The five gates

| # | Gate | The question | Owner | The evidence |
| --- | --- | --- | --- | --- |
| 1 | **Intent** | Is this worth doing at all? | Product manager | Pain register, AI-fit verdict, value line |
| 2 | **Plan** | Is this the right slice at the right control level? | PM **and** architect | Bolt cut, authority budget, gate map |
| 3 | **Behaviour** | Does it meet the spec? | QA lead | Golden-set score per slice, with its lower bound |
| 4 | **Release** | Is it safe to show a few real users? | Product manager | Shadow-run comparison, rollback rehearsed |
| 5 | **Expansion** | Have we earned wider use? | QA lead | Live evidence by slice, drift inside threshold |

**The most common failure is a product manager approving a pull request.** Strike every approval you
cannot evaluate, and insist on being asked the ones you can. Behaviour and expansion belong to QA.

<!-- picture:map:ai-governance-gates -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-governance-gates/"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/map-ai-governance-gates.dark.webp"><img alt="The five governance gates in order, each with its owner, and the drift alert that re-opens release" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/map-ai-governance-gates.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-governance-gates/">Open the live, interactive version</a></sub>
<!-- /picture -->

That dotted line is a rule, not a nicety: **a drift alert re-opens the release gate automatically.**

### How it actually goes wrong

A gate becomes a status column. The card moves to "approved" because the stand-up did not object, and
six weeks later nobody can say who decided or what they saw. The second shape is worse because it
looks like diligence: the gate has a named approver, the approver is senior, and the evidence in front
of them is a demo. A demo is the one thing a best-guess system is guaranteed to pass, because the
cases were chosen by the person showing it.

The third is the approval nobody can evaluate. A product manager clicking approve on a pull request
adds a name to an audit trail and nothing to the decision — and it costs more than it looks, because
it means the person who *could* have evaluated it has stopped being asked.

### What good looks like

| Sign | The test |
| --- | --- |
| Each gate names **one** person, and that person can explain the evidence | Ask them what they would have needed to see to say no |
| The evidence is a number with a denominator, not a demonstration | "82% on 40 cases, lower bound 68%" beats any walkthrough |
| At least one gate has been **refused** this quarter | A gate that has never stopped anything is a status column |
| A drift alert re-opened the release gate without anyone deciding to | It is wired, not remembered |
| Nobody approves something they could not evaluate | Count the approvals each role gives; strike the ones they cannot read |

<details><summary><b>Template · Gate decision record</b></summary>

```markdown
# Gate decision · <intent | plan | behaviour | release | expansion> · <feature>
Decision: <PASS | REFUSE | PASS WITH CONDITIONS>
Decided by: <one name, one role>   Date: <date>   Gate type: <hard | soft>

## The question this gate asks
<copied from the gate table — not reworded>

## The evidence that was actually in front of me
| Evidence | Link | Dated | Who produced it | Did I read it? |
|----------|------|-------|-----------------|----------------|
| <golden-set score per slice, with lower bound> | <link> | <date> | <QA lead> | yes |
| <shadow-run comparison over <n> days> | <link> | <date> | <QA lead> | yes |

## The numbers, with denominators
| Slice | Bar | Score | n | Lower bound | At bar? |
|-------|-----|-------|---|-------------|---------|
| <codeshare> | <80%> | <82%> | <40> | <68%> | **no** |
| <simple reroute> | <90%> | <94%> | <220> | <90%> | yes |

## What would have made me say no
<write this BEFORE looking at the numbers if you can. It is the only defence against a gate
that passes because it was scheduled to.>

## Conditions, if PASS WITH CONDITIONS
| Condition | Owner | Due | What happens if it is missed |
|-----------|-------|-----|-------------------------------|
| <120 more codeshare cases before widening past 5%> | <QA> | <date> | <traffic share stays at 5%> |

## What I could not evaluate, and who should have
| Item | Why not me | Who | Asked? |
|------|-----------|-----|--------|
| <the checker implementation> | <I cannot read the harness> | <eng lead> | yes |

## Signed
<name>, <role>, <date>. This decision is recorded whether it passed or not.
```
</details>

---

## Hard gates and soft gates

An agentic build creates more decisions than a traditional one, and most of them do not need to halt
anything. Treating them all as hard is how a build ends up waiting behind eleven open questions.

Four questions classify any open decision. **One "no" makes it hard.**

<!-- picture:map:the-hard-gate -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/the-hard-gate/"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/map-the-hard-gate.dark.webp"><img alt="Four questions decide whether an open decision is a hard gate or a soft one" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/map-the-hard-gate.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/the-hard-gate/">Open the live, interactive version</a></sub>
<!-- /picture -->

### The three that are hard

| Decision | Why it halts |
| --- | --- |
| The AI-fit verdict | It fixes the shape of the product; changing it later means starting again |
| The autonomy level on money actions | It moves money, and a regulator has a rule about it |
| The spec, the bar and the guardrails | Everything downstream is built and measured against them |

### The eight that are soft

Each runs behind a placeholder, with an owner and a date.

| Decision | The placeholder it runs behind | Settled by |
| --- | --- | --- |
| Model tier per slice | Everything on the mid tier, behind the gateway | The shadow run |
| Model family | Whichever the gateway points at today | When the golden set exists |
| Framework | An interface layer in front of it | Day 20, as an ADR |
| Cloud service and region | Any in-region option, since data must stay in-region | Before P2 hardening |
| Retrieval design | A stub that returns the fare-rules file | During P2 |
| Memory | None; the first slice does not need it | When a slice needs it |
| Judge rubric | Rubric v0, three criteria | During the shadow run |
| Dashboard cuts | The default trace view | In P3 |

**A placeholder behind every soft gate** is the practice that makes this work. An interface layer or a
stub lets the build proceed while the decision is being measured.

### How it actually goes wrong

Teams fail in one direction and they fail in it consistently. The careful team makes everything hard:
eleven open questions, each with a meeting, and a build that waits three weeks for a framework choice
that an interface layer would have deferred entirely. The fast team makes everything soft, which is
fine until one of the soft ones was the autonomy level on a money action, and the placeholder that
was standing in for it was *the model behaves sensibly*.

The subtler failure is a soft gate with no placeholder. The decision is declared soft, the build
proceeds, and because there is no stub the team simply writes the first plausible implementation —
which becomes the decision, taken by whoever was on that ticket, never recorded. Soft means
*deferred behind something*, not *not yet thought about*.

### What good looks like

| Sign | The test |
| --- | --- |
| Every soft gate has a **named placeholder** you can point at in the repo | A stub, an interface, a flag. Not "we will decide later" |
| Every soft gate has an owner and a date | Question three of the four. No date makes it hard |
| Hard gates are countable on one hand | Eleven hard gates is a classification failure, not a careful team |
| A soft gate was settled on evidence, not on the calendar | The shadow run chose the tier; nobody voted |
| A soft gate was **re-classified as hard** at least once | Evidence is allowed to change the classification |

<details><summary><b>Template · Soft-gate placeholder register</b></summary>

```markdown
# Soft-gate register · <feature>
Every open decision that is NOT halting the build. Reviewed weekly, out loud, in ten minutes.
Owner of this register: <architect name>   Last review: <date>

| # | Open decision | Placeholder in place today | Where it lives | Owner | Settled by | Due |
|---|---------------|-----------------------------|----------------|-------|------------|-----|
| 1 | <model tier per slice> | <everything on the mid tier> | <gateway config, link> | <name> | <the shadow run> | <date> |
| 2 | <framework> | <an interface layer in front of it> | <src/ports/agent.py> | <name> | <ADR, day 20> | <date> |
| 3 | <retrieval design> | <stub returning the fare-rules file> | <src/stubs/retrieval.py> | <name> | <during P2> | <date> |

## The four questions, answered for each — re-checked at every review
| # | Reversible cheaply? | Placeholder exists? | Owner and date? | Downstream survives a change? | Still soft? |
|---|---------------------|---------------------|-----------------|-------------------------------|-------------|
| 1 | yes | yes | yes | yes | soft |
| 2 | yes | yes | yes | yes | soft |

<Any row with a "no" is HARD from this review onward. Move it out of this register and stop the
work that depends on it.>

## Re-classified this cycle
| # | Decision | Was | Now | What changed |
|---|----------|-----|-----|--------------|
| <n> | <memory> | soft | HARD | <a slice now needs cross-session state, so nothing downstream survives> |

## Overdue
| # | Decision | Due | Days late | What it is now silently deciding for us |
|---|----------|-----|-----------|------------------------------------------|
| <n> | | <date> | <n> | <the first plausible implementation, chosen by whoever had the ticket> |

## Placeholders with no owner
<There should be none. Each one is a decision being taken by default.>
```
</details>

<details><summary><b>Prompt · Classify an open decision hard or soft</b></summary>

```text
You are classifying open decisions on a build as HARD (must be settled before the phase closes)
or SOFT (runs alongside the build, behind a placeholder).

Apply exactly these four questions. ONE "no" makes it HARD.
1. Can it be reversed cheaply once the build has started?
2. Can the build proceed behind a placeholder?
3. Is there a named owner and a date?
4. Does everything downstream survive if the answer changes?

For each decision below, produce:
| Decision | Q1 | Q2 | Q3 | Q4 | Verdict | The placeholder, if SOFT | Who owns it |

Then, separately:
- For every SOFT verdict, name the SPECIFIC placeholder: a stub, an interface, a flag, a config
  default. "Decide later" is not a placeholder; if you cannot name one, the answer to Q2 is no.
- For every HARD verdict, name the single question that made it hard and what is blocked until
  it is answered.
- List any decision where the honest answer to Q3 is "no owner" — those are HARD today and
  become SOFT the moment somebody's name goes on them.

RULES:
- Anything that moves money, changes identity, or a regulator has a rule about, is HARD.
  Say which of the three.
- Do not use effort or urgency as an input. A decision is not soft because the team is busy.
- Do not classify more than three as HARD unless you can defend each one against all four
  questions in a sentence.

OPEN DECISIONS:
<paste the list, with what each one affects>
```
</details>

---

## The risk ladder: gate by risk, never by size

The single most expensive review habit is sizing the check to the diff. A one-line change to a refund
cap is tiny and belongs in the highest band there is.

| Band | The action | The check |
| --- | --- | --- |
| **R1** | Reversible draft, sandbox | Review at the end |
| **R2** | Reversible change to real work | Review before merge |
| **R3** | Hard to reverse, small blast radius | Approve first |
| **R4** | Money, identity, policy | A **named** approver, every time |
| **R5** | Irreversible or safety-critical | Not delegated at all |

> **The trap.** "Small changes don't need a gate." A one-line refund-cap change is R4.

The band belongs to the **tool**, assigned once in the authority budget, and a path rule in the
repository routes the review. It is never argued per pull request. See
[How to Review by Risk Band](How-to-Review-by-Risk-Band) and
[Journey: Engineering lead](Journey-Engineering-Lead).

### How it actually goes wrong

The bands are written down and the routing is not, so the band becomes an argument held once per pull
request — usually by the person who wants it merged, usually at 5pm. Within a month the ladder is a
diagram on a wiki page and review depth is back to being a function of diff size and mood.

The other failure is banding the *change* rather than the *tool*. SkyWays' refund tool is R4 because
of what it does, not because of what a given commit touches. A two-character change to its cap is
R4; a 400-line refactor of the itinerary formatter is R2. Band the tool once, in the authority
budget, and the routing follows automatically.

### What good looks like

| Sign | The test |
| --- | --- |
| The band is recorded against the **tool**, once | Open the authority budget and read a band per tool |
| A path rule routes the review automatically | Nobody has argued about review depth on a pull request this month |
| R4 approvers are named people, not a group | A group alias is nobody at 5pm on a Friday |
| R5 tools do not exist in the codebase | The strongest control is the tool you did not build |
| A tiny diff has been deeply reviewed recently | The ladder is beating the diff-size instinct |

<details><summary><b>Template · Review-lane path rule</b></summary>

```markdown
# Review lanes · <repo>
The band belongs to the TOOL, from the authority budget. This file turns bands into routing so
nobody argues about depth on a pull request. Owner: <engineering lead>.

## Bands, from the authority budget
| Tool / path | Band | Why | Approver | Extra required check |
|-------------|------|-----|----------|----------------------|
| <src/tools/search.py> | R1 | <read-only, sandboxed> | <any reviewer> | – |
| <src/tools/draft.py> | R2 | <reversible, touches real work> | <any reviewer> | – |
| <src/tools/hold_cancel.py> | R3 | <hard to reverse, one passenger> | <named on the rota> | – |
| <src/tools/refund.py> | **R4** | <moves money, regulator rule at $400> | <named person, not a group> | <cap + approver tests> |
| <identity change> | **R5** | <irreversible> | none — **no tool exists** | – |

## CODEOWNERS entries this produces
<paste the actual lines, so the file and the table cannot drift apart>

## Rules that live in branch protection, not here
- <the eval harness is a REQUIRED check, not advisory>
- <bar files are owned by QA and changed in their own commit>
- <R4 paths require review from a named owner and dismiss stale approvals>

## What is explicitly NOT a factor
Diff size. Urgency. Who wrote it. Whether an agent or a person wrote it.

## Exceptions granted this quarter
| Date | Path | Band waived to | Who approved | Why | Reverted on |
|------|------|----------------|--------------|-----|-------------|
| | | | | | |

<An empty table is the healthy state. Three entries is a band that is wrong.>
```
</details>

<details><summary><b>Prompt · Assign risk bands to a tool list</b></summary>

```text
You are assigning risk bands to the tools an agent can call. Band the TOOL, never the change.

The ladder:
R1 reversible draft or sandbox — review at the end
R2 reversible change to real work — review before merge
R3 hard to reverse, small blast radius — approve first
R4 money, identity or policy — a NAMED approver, every time
R5 irreversible or safety-critical — not delegated at all; the tool should not exist

For each tool below, produce:
| Tool | What it changes | Reversible? By whom, in how long? | Blast radius | Band | Why, in one clause |

Then:
1. Every R4 and R5 tool, with the cap or limit that must be a TYPED PARAMETER in its signature,
   and the test that fails if the cap is absent.
2. Every R5 tool, with the sentence "this tool should not exist" and what replaces it.
3. Any tool whose band you would change if it were called by a different caller — those need
   splitting into two tools.

RULES:
- Reversible means reversible by us, cheaply, without asking the customer. A cash refund is not
  reversible. A draft itinerary is.
- A cap described in a prompt does not exist. Only a typed parameter or a policy counts.
- Never use expected call volume or implementation effort as an input.
- If a tool does two things at different bands, say so and split it.

TOOLS:
<paste each tool's name, signature and one line on what it does>
```
</details>

---

## Who signs what

One accountable name per artefact. Not a committee, not a team.

| Artefact | PM | Architect | Engineering | QA | Sponsor |
| --- | :---: | :---: | :---: | :---: | :---: |
| Pain register, AI-fit verdict | **A** | C | I | I | I |
| Ratified NFRs, sensitivity points | C | **A** | C | C | I |
| Eight-field spec, acceptance bar | **A** | C | I | C | I |
| Authority budget and gate map | C | **A** | R | C | I |
| Decision records (ADRs) | I | **A** | C | I | I |
| Bolt cut, dependency order | C | **A** | R | I | – |
| Golden set, checkers | I | C | R | **A** | – |
| Shadow-run comparison, cut-over | **A** | C | R | C | I |
| Trace, redaction, drift alert | I | **A** | R | C | I |
| Two-number report | R | C | R | C | **A** |

*A = accountable, R = responsible, C = consulted, I = informed.*

### How it actually goes wrong

The table is filled in and then quietly contradicted by the tooling. CODEOWNERS says the whole
`eval/` directory belongs to engineering, so the bar file — QA's accountability on paper — is
changed by whoever is fixing the build. Nothing in the RACI is wrong; it simply has no teeth,
because the enforcement lives in a different file that nobody read it against.

The other pattern is the shared A. Two names in the accountable cell reads as thoroughness and
behaves as nobody, and it shows up at exactly the moment you needed one person: a Friday evening,
one of them on leave, and a decision that waits until Monday because neither can take it alone. Plan
is the only shared cell here, and it is shared deliberately between PM and architect, which is why
it needs its own convention for who breaks a tie.

### What good looks like

| Sign | The test |
| --- | --- |
| Exactly one **A** per row | Read the column. Two As is a row you have not finished |
| The RACI and CODEOWNERS agree | Diff them. They drift silently and always in the same direction |
| The shared plan gate has a stated tie-breaker | Write down who decides when PM and architect disagree, before they do |
| Each accountable person has **refused** something | Accountability that has never said no is a signature, not a decision |

---

## Paired indicators and the two-number report

Every measure is reported beside the one that shows its side effect, so neither can be pushed alone.
Push throughput without quality and you get merged pull requests nobody read. Push cost down without
the bar and you get a cheap model failing fluently.

**The report carries two numbers and never one:**

```
CYCLE 3                      baseline      now       change
person-days per story            8.0        4.6      −43%
token spend per story              –      $310            
review hours added per story     1.2        2.0       +0.8
re-runs per story                  –        1.4            
────────────────────────────────────────────────────────────
net                        saved 3.4 person-days, spent $310 + 0.8 review hours
```

Three rules that keep it honest:

1. **Take the baseline before the pilot.** After the pilot it is a guess, and everyone knows it.
2. **Keep the review-hours row.** It is high in cycle one and falls as the artefacts sharpen. Hiding
   it makes cycle two look like a regression.
3. **Keep the re-run row.** It is the leak signal — where model switching and vague asks show up first.

> The programme is cancelled on the number you hid, never on the one you showed.

### How it actually goes wrong

Nobody lies. Each cycle reports the saving because the saving is what was asked for, the spend goes
to a finance dashboard because that is where spend goes, and the two never appear in the same
document. Then somebody outside the programme assembles both, at a budget review, from sources the
team has not seen. SkyWays reported 40–45% fewer person-days **and** $4,200 of tokens on day 90, on
one line, with the review hours beside them. The review row was up. The programme continued, and it
continued because both numbers came from the team.

The other failure is a baseline taken after the pilot started. Everyone in the room knows it is a
reconstruction, so the saving is discounted to roughly zero however real it was — which is the
expensive part, because you then have no way to argue for the thing that actually worked.

### What good looks like

| Sign | The test |
| --- | --- |
| Both numbers on **one line**, in one document, every cycle | Not two dashboards, not an appendix |
| The baseline predates the first agent commit | Check its date against the git log |
| The review-hours row appears in a cycle where it went up | It is being reported, not curated |
| The report is sent before it is requested | A number produced on demand is a number somebody else is already assembling |
| Every headline number has its paired indicator beside it | Throughput with quality, cost with the bar, speed with re-runs |

<details><summary><b>Template · The two-number cycle report</b></summary>

```markdown
# Cycle report · <programme> · cycle <n> · <date>
Accountable: <sponsor name>. One page. Sent on <day> whether or not anybody asked.

## The two numbers
> This cycle we saved <n> person-days and spent $<n> plus <n> review hours.

| Measure | Baseline (<date, before the pilot>) | This cycle | Change | Paired with |
|---------|--------------------------------------|------------|--------|-------------|
| Person-days per story | <8.0> | <4.6> | <−43%> | token spend |
| Token spend per story | – | <$310> | – | person-days |
| Review hours added per story | <1.2> | <2.0> | <+0.8> | quality at bar |
| Re-runs per story | – | <1.4> | – | cost |
| Stories at bar on first pass | <n%> | <n%> | | throughput |

## Where the baseline came from
<source, date, and who produced it. If it was reconstructed after the pilot began, say so here
in plain words rather than letting somebody discover it.>

## What moved, and why
| Number | Direction | Cause we can evidence | Expected next cycle |
|--------|-----------|------------------------|---------------------|
| <review hours> | up | <cycle-one artefacts are thin; reviewers are writing the spec back> | <down to <n>> |

## The number that looks bad, stated first
<name it, with the reason and the expected trajectory. A report where nothing looks bad is a
report nobody believes twice.>

## Quality, so the savings cannot be read alone
| Slice | Bar | Score | n | Lower bound | Drift since last cycle |
|-------|-----|-------|---|-------------|------------------------|
| <codeshare> | <80%> | <82%> | <n> | <n%> | <+1.2 pts> |

## Decisions I am asking for
| Ask | Why now | What happens if the answer is no |
|-----|---------|-----------------------------------|
| | | |
```
</details>

<details><summary><b>Prompt · Find the unpaired number</b></summary>

```text
Below is a report, dashboard extract or steering-committee slide from a delivery programme.

Every measure in it should be reported beside the measure that shows its side effect, so that
neither can be improved by damaging the other.

Produce:
1. | Number reported | What it can be improved by damaging | Is the paired number present? |
2. Every number that appears ALONE, ranked by how badly it could mislead a reader who has no
   other source. For each, name the paired number that is missing and where it would come from.
3. Any number with no denominator, no date, or no baseline. List these separately; they are not
   yet numbers.
4. The single sentence a sceptical reader outside the programme would use to attack this
   document, and the one row that would answer it.

RULES:
- Treat a number in a different document or dashboard as ABSENT. The pairing has to be visible
  on the same page to do its job.
- Do not suggest new metrics. Work only with what the report already claims.
- Do not soften. If the report shows savings and no spend, say that in one sentence.
- Say nothing about presentation, layout or wording.

REPORT:
<paste>
```
</details>

Build it: [Two-number report builder](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/report)
· [Formulas and Calculators](Formulas-and-Calculators) · [Role: Sponsor](Role-Sponsor)

---

## Maturity: control, not tool count

A team with ten AI tools and no gates is **less** mature than a team with one tool and tight control.
Six controls, each either present or absent. Your level is how many you have; your next step is the
first one you do not.

| # | Control | The test |
| --- | --- | --- |
| 1 | A context file the agent reads | It exists in the repo and is current |
| 2 | Every item has a spec with a bar and an owner | Pick a story at random and look |
| 3 | The harness gates the merge, per slice | A slice below its bar blocks the merge |
| 4 | Caps live in tool signatures | Grep the prompts; find none |
| 5 | The trace redacts | A passport number never reaches a row |
| 6 | Production evidence by segment, with drift watched | The alert re-opens the release gate |

### How it actually goes wrong

The self-check is scored on intent. Control 4 is marked present because the cap was decided, written
into the autonomy record and repeated in the system prompt — and on day 82 a $2,000 refund goes out
that was not owed, because the refund tool's signature accepted any amount. Five layers were claimed
in SkyWays' design review and none was enforced; two of the five existed only in the prompt. Each
control has a **test** for exactly this reason, and every test is something you run rather than
something you recall.

The other failure is scoring the controls as a ladder to be climbed in order. They are not staged.
Control 4 is an afternoon's work and control 6 takes a quarter, so a team that "isn't ready for
level 4 yet" is usually a team that has not read what level 4 is.

### What good looks like

| Sign | The test |
| --- | --- |
| Each control was scored by **running its test**, this week | Present the grep output, the red harness run, the redacted row |
| A control is marked absent even though the decision was made | Decided is not enforced, and the self-check says so |
| The next control is being built, and only that one | Six actions produce none |
| The score went **down** once | Controls decay; a score that only rises is not being measured |

<details><summary><b>Template · Maturity self-check</b></summary>

```markdown
# Maturity self-check · <team> · <date>
Score by RUNNING each test, not by remembering. Previous score: <n>/6 on <date>.

| # | Control | Test I ran | Output | Present? |
|---|---------|-----------|--------|----------|
| 1 | Context file the agent reads | <opened it; checked last commit date> | <current as of <date>> | yes |
| 2 | Spec with a bar and an owner on every item | <picked 3 stories at random> | <2 of 3 had a bar> | **no** |
| 3 | Harness gates the merge, per slice | <lowered a bar and pushed> | <merge blocked> | yes |
| 4 | Caps live in tool signatures | <grep the prompts for the cap; grep the signatures> | <found in prompt, NOT in signature> | **no** |
| 5 | The trace redacts | <searched a week of rows for a passport pattern> | <0 hits> | yes |
| 6 | Production evidence by segment, drift watched | <checked the alert fired and re-opened the gate> | <alert exists, does not re-open> | **no** |

**Score: <3>/6.**

## Anything marked present on a decision rather than a test
| Control | What we decided | Where it is actually enforced | Honest verdict |
|---------|-----------------|--------------------------------|----------------|
| <4> | <$400 cap, day 12> | <the system prompt> | absent |

## Change since last time
| Control | Was | Now | What moved it, or what decayed |
|---------|-----|-----|---------------------------------|
| | | | |

## The ONE control we build next
<the cheapest absent control, not the most impressive one>
Owner: <name>   Due: <date>   Its test, which we will run on that date: <the test>
```
</details>

Run it: [Maturity self-check](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/maturity)

---

## Where a model helps across this page

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Running the four classification questions over a list of open decisions. It is literal about "is there a named owner", which is the question teams answer generously |
| **Claude Code** | Scoring the maturity self-check by running its tests: grep the prompts for caps, grep the signatures, diff the RACI against CODEOWNERS, check the harness is a required check |
| **Chat LLM** | Reading a cycle report back as a hostile outsider and naming every number that appears without its pair |
| **Claude Code** | Generating the CODEOWNERS lines from the authority budget, so the bands and the routing cannot drift apart |
| **Do not delegate** | Saying no at a gate. The model can tell you the lower bound misses the bar; refusing a release in front of the people who want it is the entire content of the role |

---

## Try it

Your last release. Answer three questions in writing.

1. **Who signed the release gate, and what was in front of them?** If the answer is "the team agreed",
   there was no gate.
2. **Which open decisions were treated as hard that should have been soft?** Count the days the build
   waited.
3. **Did the cycle report reach the sponsor with both numbers on it?** If not, write the second number
   now, before somebody asks for it.

Then two more, which are harder and worth more.

4. **Score the six controls by running their tests, not by remembering.** Grep the prompts for a cap.
   Grep the tool signatures for the same cap. If the first finds it and the second does not, you have
   found a day-82 incident with the date not yet filled in.
5. **Diff your RACI against CODEOWNERS.** Every disagreement is an accountability the tooling does not
   support, and the tooling wins every time.

<details>
<summary>The pattern behind all three</summary>

Gates fail in one of two directions and teams are usually consistent about which. Either everything is
a gate, and the build queues behind decisions that could have run behind a stub, or nothing is, and
the first time anyone decides is in the postmortem. The four classification questions fix the first.
Naming one accountable person per artefact fixes the second.
</details>

<details>
<summary>What questions 4 and 5 usually turn up</summary>

Control 4 is the one that is most often marked present and is most often absent, because deciding a
cap feels like implementing one. The grep takes thirty seconds and settles it.

The RACI diff almost always drifts in the same direction: accountability that belongs to QA — the bar
file, the golden set — is owned in CODEOWNERS by whoever owns the directory it happens to sit in. The
fix is one line in CODEOWNERS and a convention that a bar change is its own commit, reviewed by
somebody who did not write the code it would let through. See [Journey: QA lead](Journey-QA-Lead).
</details>

---

**Next:** [The Evidence Pack](The-Evidence-Pack) · [How to Review by Risk Band](How-to-Review-by-Risk-Band)
· [Role: Sponsor](Role-Sponsor) · [Anti-Patterns](Anti-Patterns) ·
[Journey: Engineering lead](Journey-Engineering-Lead) · [Journey: DevOps](Journey-DevOps)
