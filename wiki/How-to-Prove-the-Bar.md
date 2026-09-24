# How to prove the bar

<!-- tutorial:lesson -->*New to this? Start with the lesson **[Prove the agent meets its bar](How-to-Prove-an-AI-Agent-Meets-Its-Bar)** — the idea step by step, with a worked problem. This page is the reference.*<!-- /tutorial:lesson -->

A score is not proof. This page is the ladder from "the model seems good" to "we have earned wider
use", and every rung has a number on it.

This closes the [trust loop](The-Eight-Loops#trust). The QA lead owns it.

**Run it interactively:**
[the acceptance-bar calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/bar)
· **[the deadline simulation](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/simulations/deadline)**

### At a glance

| | |
| --- | --- |
| **Reach for it when** | A score is being offered as proof. |
| **Owner** | QA lead |
| **Phase** | P1 → P2 |
| **Closes** | [Trust](The-Eight-Loops#trust) — P2 → P3 |
| **Moves** | 7 |
| **You leave with** | A bar per slice with its derivation, a golden set tagged by slice, a lower bound rather than a score, and a shadow comparison |

---

## The ladder

<!-- picture:wikimap:prove-bar -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-prove-bar.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-prove-bar.dark.webp"><img alt="Seven moves for proving the bar, with the lower-bound test as a gate before the shadow run" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-prove-bar.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-prove-bar.light.webp">Open the picture full size</a></sub>
<!-- /picture -->

| # | Move | Produces | Done when |
| --- | --- | --- | --- |
| 1 | [Set the bar, per slice](#1--set-the-bar-per-slice) | Bar sheet | Every slice has a bar, and each one names the two money figures it came from |
| 2 | [Build the golden set](#2--build-the-golden-set) | Golden-set manifest | Every case is real, tagged by slice, with an expected outcome a person wrote |
| 3 | [Score in the right order](#3--score-in-the-right-order) | Judge rubric and calibration record | Exact checks run first, and the judge agrees with human labels on a held-back sample |
| 4 | [Report the lower bound](#4--report-the-lower-bound) | Evidence readout | What gets reported is an interval, with the sample size beside it |
| 5 | [The shadow run](#5--the-shadow-run) | Shadow-run comparison | Agreement is reported per slice, with nothing left out for low volume |
| 6 | [Cut over at five percent](#6--cut-over-at-five-percent) | Cut-over decision | The days of evidence are arithmetic, and the rollback has been rehearsed |
| 7 | [Widen on live evidence](#7--widen-on-live-evidence) | Widening schedule | Each widening names the evidence that earned it, never the date |

| # | Move | Produces | Done when |
| --- | --- | --- | --- |
| 1 | [Set the bar, per slice](#1--set-the-bar-per-slice) | Bar sheet, one row per slice | Every bar is derived from a damage and a saving, not chosen |
| 2 | [Build the golden set](#2--build-the-golden-set) | Tagged cases with expected outcomes | Every case carries a slice tag and a real historical outcome |
| 3 | [Score in the right order](#3--score-in-the-right-order) | Per-slice scores, cheap checks first | The judge only ever sees output that passed schema and maths |
| 4 | [Report the lower bound](#4--report-the-lower-bound) | Evidence readout, per slice | Nobody in the room has seen a bare point estimate |
| 5 | [The shadow run](#5--the-shadow-run) | Agreement per slice over a fixed window | "Shadow never writes" is a test that fails the build |
| 6 | [Cut over at five percent](#6--cut-over-at-five-percent) | A live slice and a rehearsed rollback | Somebody has watched the rollback thrown, on a date |
| 7 | [Widen on live evidence](#7--widen-on-live-evidence) | Widening schedule, conditions not dates | Every widening step names the evidence that unlocks it |

Skipping a rung is always possible and always shows up later, usually at rung 7 with real passengers.

---

## 1 · Set the bar, per slice

**Before a single case is collected. A bar chosen after the score is known is not a bar.**

> **N = damage ÷ saving**, and **bar = N ÷ (N + 1)**

One wrong case undoes the saving from N right ones, so the assistant breaks even at N right for every
wrong.

| Slice | Saving | Damage | N | Bar |
| --- | --- | --- | --- | --- |
| Same-day lookup | $4 | $4 | 1 | **50%** |
| Codeshare rebook | $9 | $36 | 4 | **80%** |
| Refund, no hold | $12 | $600 | 50 | **98%** |
| Refund, with a human hold | $12 | $30 | 2.5 | **71%** |

The last two rows are the lever. **A hold lowers the damage, so it lowers the bar.** Ship at 71% with
a person confirming the charge, rather than waiting for a 98% you will never reach.

Read the formula the other way and it is a design instrument rather than a test threshold. You
cannot move the damage of a wrong refund by asking the model to try harder; you move it by putting
a person between the decision and the money, and the arithmetic hands back twenty-seven points of
bar.

### What you actually do

1. **Get the saving from the process owner, in money per case.** Not "it saves time" — minutes times
   a loaded rate, from the person whose budget carries it. A saving nobody will sign is a saving that
   evaporates at the first steering meeting.
2. **Get the damage from the person who cleans it up.** Ask for the last real instance and what it
   cost end to end: the refund, the call, the goodwill voucher, the compliance write-up. The number
   is almost always larger than engineering guesses and smaller than compliance fears.
3. **Compute, do not choose.** `N = damage ÷ saving`, then `bar = N ÷ (N + 1)`. A bar that arrives by
   judgement gets re-argued every release; a bar that arrives by division gets argued once, about its
   inputs, which is the productive argument.
4. **Sanity-check any bar above 95%.** It is telling you the damage is fifty times the saving, which
   usually means the action should not be autonomous at all. Take that finding to the authority
   budget rather than to the eval harness.
5. **Ask what would halve the damage, for each high bar.** A hold, a cap, a reversal window, a second
   pair of eyes on anything over a threshold. Re-derive the bar with the mitigation in place and put
   both rows on the sheet, so the trade is visible.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Turn an incident write-up into a damage figure with its components itemised — refund, handling time, escalation, compliance. It finds the costs you forgot; you supply the rates |
| **Chat LLM, adversarially** | "For each of these slices, what mitigation would most reduce the damage, and what would the bar become?" It reliably surfaces the hold-lowers-the-bar move on slices where you had not thought to look |
| **Claude Code** | Keep the sheet as a small data file and generate the bar column from damage and saving, so a bar can never be edited without editing its inputs |
| **Do not delegate** | The damage figure itself. It is a claim about your business that somebody has to defend in front of a sponsor, and a plausible number is exactly the failure this move exists to prevent |

### The artefact

<details><summary><b>Template · Bar sheet</b></summary>

```markdown
# Acceptance bars · <product> · v<n> · <date>
Owner: <name, QA lead>   Ratified with: <NFR register version>
Rule: bar = N / (N + 1), where N = damage / saving. Bars are DERIVED, never chosen.

## Bars in force
| Slice | Volume/day | Saving per right case | Damage per wrong case | N | Bar | Mitigation assumed |
|-------|-----------|----------------------|----------------------|---|-----|--------------------|
| <same-day lookup> | <n> | $<n> | $<n> | <n> | <n>% | none |
| <codeshare rebook> | <n> | $<n> | $<n> | <n> | <n>% | none |
| <refund> | <n> | $<n> | $<n> | <n> | <n>% | **human hold on the charge** |

## Where each number came from
| Number | Value | Source (person + document) | Date | Confidence |
|--------|-------|---------------------------|------|------------|
| <saving, same-day> | $<n> | <name>, <time study / ledger> | | high / medium / low |
| <damage, refund> | $<n> | <name>, <incident <id>> | | |

## The mitigation trade, stated
| Slice | Bar without mitigation | Bar with it | What the mitigation costs | Decision |
|-------|-----------------------|-------------|---------------------------|----------|
| <refund> | <n>% | <n>% | <n> s of desk time per case | <ship gated / wait> |

## Bars we refuse to set, and amendments
| Action | Why there is no bar | Where it went instead |
|--------|--------------------|-----------------------|
| <identity change> | Damage is unbounded; no N exists | Authority budget — not delegated (R5) |

| Amended | Slice | From | To | Why | Approved by |
|---------|-------|------|----|-----|-------------|
```
</details>

<details><summary><b>Prompt · Derive bars from damage and saving</b></summary>

```text
Here are the slices of an agent's work, with a saving per correct case and a damage per
incorrect case.

TABLE ONE:
| Slice | Saving | Damage | N = damage/saving | bar = N/(N+1), percentage to 1 dp |

TABLE TWO:
| Slice | Cheapest mitigation that lowers DAMAGE | New damage | New bar | Points recovered |

Rules:
- Show N and the bar to one decimal place before rounding. Do NOT round a bar down:
  98.04% rounds to 98%, never to 95%.
- If a damage figure is missing, write DAMAGE MISSING and say who in an airline
  operations team would hold it. Do not estimate it.
- Flag every bar at or above 95% and say in one sentence what that implies about whether
  the action should be autonomous at all.
- In table two the mitigation must reduce the DAMAGE of a wrong case, not the probability
  of one. A better prompt is not a mitigation; a hold, a cap, a reversal window or a
  second approver is. State what each costs, in seconds of human time or in delay.

SLICES:
<paste>
```
</details>

**Done when** — every bar on the sheet is the output of a division whose two inputs are sourced,
dated and owned by a named person.

---

## 2 · Build the golden set

**As soon as the bars exist, and from history rather than imagination.**

Real historical cases with the expected outcome, one per line, **tagged by slice**.

```jsonl
{"id":"c-0412","slice":"codeshare","input":{"pnr":"QX7T2A","disruption":"cancelled"},"expect":{"action":"propose","partner":"allowed"}}
{"id":"c-0414","slice":"refund","input":{"pnr":"RT1K8D","fare":"non-refundable"},"expect":{"action":"escalate","reason":"no_entitlement"}}
```

**Fifty cases to start, five hundred to trust.** And **oversample the rare hard slice deliberately** —
a stratified sample beats a large random one that happens to contain nine codeshare cases.

The reason stratification matters is arithmetic, not taste. Cases needed to prove a bar depends on
the gap between the score and the bar, and it is computed **per slice**. A thousand cases distributed
by natural traffic gives SkyWays roughly six hundred same-day lookups it did not need and forty
codeshare cases, which proves nothing about the slice that carries the risk. Sample for the slice
that is hard to prove, not for the slice that is easy to collect.

### What you actually do

1. **Pull from history, one slice at a time.** Sample within a slice, not across the corpus.
   Sampling across the corpus reproduces your traffic mix, and your traffic mix is exactly what makes
   the dangerous slice too small to prove.
2. **Write the expectation as a decision, not as a sentence.** `{"action":"escalate","reason":"no_entitlement"}`
   can be checked by a machine. "Should hand it to a human politely" cannot, and it will be graded
   inconsistently forever.
3. **Have the desk agree the expected outcome, and record who agreed.** Where two experienced agents
   disagree about the right answer, that case is not ground truth — it is a policy gap, and it goes
   to a separate list that is more valuable than the case was.
4. **Tag beyond the slice.** Fare class, partner carrier, disruption cause, time of day. The tags cost
   nothing at capture time and they are what lets you answer "which cases does it fail" instead of
   "how often does it fail".
5. **Freeze a version, hash it, and seal twenty percent of it unseen.** A set that changes between
   runs makes every comparison meaningless, and a holdout never used for iteration is the only
   defence against a set that has been tuned against until it says yes.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Build the extractor from the ticket system to the JSONL, with the slice tag derived from fields rather than from prose. It is a data job, done once, and it is how you get five hundred cases instead of fifty |
| **Chat LLM** | Propose the tag vocabulary from thirty sample cases — the dimensions you would not have thought of, like partner carrier or fare family. Then you pick from its list |
| **Do not delegate** | Writing the expected outcomes. A model that invents ground truth produces a set that measures agreement with the model, which is a number that will pass every bar and mean nothing |

### The artefact

<details><summary><b>Template · Golden-set manifest</b></summary>

```markdown
# Golden set · <product> · v<n> · frozen <date>
Hash: <sha256 of the jsonl>   Owner: <name>   Cases: <n>

## Composition, against the bar sheet
| Slice | Cases in set | Share of set | Share of live traffic | Bar | Cases needed to prove | Enough? |
|-------|-------------|--------------|----------------------|-----|----------------------|---------|
| <same-day> | <n> | <n>% | <n>% | <n>% | <n> | yes |
| <codeshare> | <n> | <n>% | <n>% | <n>% | <n> | **no — <n> short** |
| <refund> | <n> | <n>% | <n>% | <n>% | <n> | |

Deliberately oversampled: <slices>. Reason: <these are the slices that are hard to prove,
not the slices that are common>.

## Provenance
| Source | Cases | Date range | Who confirmed the expected outcome |
|--------|-------|-----------|-----------------------------------|
| <resolved tickets> | <n> | <from> to <to> | <name, role> |
| <escalation log> | <n> | | |
## Cases where the desk disagreed with itself
| Case id | Agent A said | Agent B said | Status |
|---------|-------------|--------------|--------|
| <id> | | | **Policy gap — <owner>, due <date>. Removed from the set.** |

## Held back, unseen
<n> cases (<n>%), sealed <date>, opened only for <the pre-release run>.
Opened on: <never / date, by name>
```
</details>

<details><summary><b>Prompt · Stratify the set against the bars</b></summary>

```text
I have a golden set and a bar sheet. Tell me whether the set can prove the bars.

| Slice | Cases held | Observed score | Bar | Cases needed | Shortfall |

Use: cases needed = 1.96^2 * p * (1-p) / (p - bar)^2, where p is the observed score.

Rules:
- If the score is BELOW the bar, do not compute cases needed. Write "cannot be proven at
  this score" — more cases will not fix it.
- If the score is within 2 points of the bar, say how steeply the requirement grows,
  because (p - bar) is squared in the denominator.
- Show the arithmetic for one slice so I can check it by hand.

Then a sampling plan: additional cases per slice, and which slices need NO more cases
even though they are the biggest part of live traffic.

BARS AND CURRENT SET:
<paste>
```
</details>

**Done when** — every case carries a slice tag and an expected outcome a person confirmed, the set is
hashed and frozen, and the composition table shows which slices are still short.

---

## 3 · Score in the right order

**Every run, and the order is the whole point.**

Exact checks first, because they are cheap and definitive. The judge second, on what survives.

| Order | Check | Catches |
| --- | --- | --- |
| 1 | Schema | Malformed output |
| 2 | Exact: fare math, eligibility, no waived tax | The money bugs |
| 3 | Independent judge against a rubric | Tone, policy, false claims |
| 4 | Score against the bar, **per slice** | Regressions the average hides |

Running the judge first spends money grading outputs the schema check would have rejected for free.

There is a second reason for the order, and it matters more than the money. A judge asked to grade a
response that contains an arithmetic error will often grade it well, because the response reads
correctly and the judge is a language model. Deterministic checks are not merely cheaper than the
judge; on everything they can see, they are **better** than the judge. Reserve the judge for what
only a reader can assess, and it becomes reliable because you have narrowed its job.

> **A judge that shares the generator's model shares its blind spots.** Use a different model, or at
> minimum a different prompt lineage, and calibrate it against a hundred human-graded cases before
> you let it gate anything.

### What you actually do

1. **Fail fast and record where it failed.** A case that dies at schema is not a case that dies at
   policy, and a run that reports one failure count has thrown away the diagnosis.
2. **Write the exact checks as assertions on fields, not on prose.** `refund_amount == fare − tax`
   is a check. "The refund should be right" is a hope wearing a check's clothing.
3. **Give the judge a rubric with levels, not a score out of ten.** Three or four named levels with
   a worked example of each. Ask for the level and the evidence quote; discard any grade with no
   quote.
4. **Calibrate the judge before you trust it.** A hundred cases graded by a person, then by the
   judge. Report the agreement, and report it per slice — judges are usually fine on the easy slice
   and poor on the one you care about.
5. **Score per slice and never publish the average as the headline.** SkyWays saw an overall score
   rise from 79% to 84% while codeshare fell from 81% to 77% against a bar of 80. The headline
   improved because the easy high-volume slice improved.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Write the harness: schema, then assertions, then judge, short-circuiting at each stage, with per-slice output. It is a day's work and it runs for the life of the product |
| **Chat LLM** | Draft the judge rubric with levels and worked examples from your policy document, then check its examples against the policy yourself |
| **Do not delegate** | The calibration verdict. Deciding that a judge is trustworthy enough to gate a release is a QA judgement with your name on it, and the judge cannot make it about itself |

### The artefact

<details><summary><b>Template · Judge rubric and calibration record</b></summary>

```markdown
# Judge rubric · <slice> · v<n>
Judge model: <model>   Generator model: <model>   (these MUST differ)
Calibrated <date> against <n> human-graded cases by <name>.

## Levels
| Level | Name | Definition | Worked example |
|-------|------|-----------|----------------|
| 3 | Correct and complete | <all entitled options offered, policy stated, no claim unsupported> | <paste a real one> |
| 2 | Correct but thin | <right decision, missing an option the passenger was entitled to> | |
| 1 | Wrong but safe | <declines or escalates when it should have acted> | |
| 0 | Wrong and unsafe | <acts without entitlement, invents a rule, or misstates money> | |

Passing level: <2 or better>. Anything at 0 is an incident, not a score.
Every grade must carry the level, a VERBATIM quote justifying it, and the policy line
applied. No quote, no grade — discard the row.

## Calibration
| | Human said | Judge said | Agreement |
|---|-----------|-----------|-----------|
| Overall | <n> cases | | <n>% |
| <per slice, one row each> | <n> | | <n>% |

**Disagreements, all of them**
| Case | Human | Judge | Who was right | Rubric change made |
|------|-------|-------|---------------|--------------------|

Verdict: <the judge may / may not gate a release on this slice>.
Signed: <name>, <date>. Re-calibrate: <date, or on any rubric or model change>.
```
</details>

**Done when** — the judge only ever sees output that has already passed schema and the money checks,
and every grade it returns carries a quote.

---

## 4 · Report the lower bound

**The moment anybody asks "did it pass". This is the rung most teams skip.**

> **lower bound = p − z × √( p × (1 − p) ÷ n )**
>
> **cases needed = z² × p × (1 − p) ÷ (p − bar)²**

| Score | Cases | 95% lower bound | Bar | Proven? |
| --- | --- | --- | --- | --- |
| 82% | 40 | 70.1% | 80% | No |
| 82% | 150 | 75.9% | 80% | No |
| 82% | 500 | 78.6% | 80% | No |
| 86% | 500 | 83.0% | 80% | **Yes** |

Two things to take from that table. **82% never proves an 80% bar**, at any sample size you will
realistically collect — the estimate is simply too close to the bar. And the cases-needed formula has
`(p − bar)²` in the denominator, so the cost of proving grows *quadratically* as your score
approaches the bar.

Under about a hundred cases, use the **Wilson** bound; the normal approximation misbehaves at small n
and near 0 or 1.

**SkyWays, day 45.** Codeshare scores **82.4% on 500 cases** against the 80% bar. The lower bound is
**79.1%**, which is below the bar, so the slice is not proven. Cases needed at that score is
**968** — the team is **468 cases short**, and at 5% of 240 cases a day it would take **81 days** to
collect them live. That is the real conversation: not "did we pass", but "eighty-one days, or raise
the score, or lower the damage with a hold".

| The three answers to an unproven slice | What it costs | When it is right |
| --- | --- | --- |
| Collect the cases owed | Time, measured in days of evidence | The score is comfortably above the bar and n is simply small |
| Raise the score | Engineering, unbounded | There is a known, nameable defect class in the failures |
| Lower the damage, re-derive the bar | A human in the loop, per case | The gap is small and the mitigation is cheap — usually the fastest of the three |

The fourth answer, rounding the lower bound up in the slide, is the one that reaches production.

Tool: [Golden-set confidence calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/confidence)

### What you actually do

1. **Put the lower bound in the column where the score used to be.** Not beside it, not in a
   footnote. Whatever occupies the position people read becomes the number they act on.
2. **Report n on every row, always.** A percentage without its denominator is not a measurement, and
   a 40-case slice reading 82% looks identical to a 500-case slice reading 82% until you print n.
3. **Switch to Wilson under about a hundred cases.** The normal approximation gives bounds that are
   too narrow at small n and can run below zero or above one near the extremes, which is how a tiny
   slice gets declared proven.
4. **Say "unproven", never "failed", when the score is above the bar and the bound is not.** They are
   different findings with different remedies, and collapsing them wastes a sprint.
5. **Quote cases owed as a number of days, not a number of cases.** `days = cases needed ÷ (share ×
   cases per day)` is the sentence a sponsor can act on; "468 more cases" is not.
6. **Flag any slice that got worse, even if it still passes.** A pass that fell four points is a
   trend, and trends are cheaper to fix than incidents.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Emit the readout from the harness output automatically, with lower bound, n, bar and verdict as columns that cannot be omitted because they are generated |
| **Chat LLM** | Paste a vendor's or a team's results and ask for the same table with lower bounds added. It will reliably reveal that half the slices are unproven rather than passing |
| **Chat LLM** | Turn "468 cases short" into the three options with their costs, so the readout arrives as a decision rather than as a complaint |
| **Do not delegate** | The pass verdict. It is a gate, a gate is a name, and the model cannot hold accountability for a slice going live |

### The artefact

<details><summary><b>Template · Evidence readout</b></summary>

```markdown
# Evidence readout · <feature> · run <id> · <date>
Golden set v<n>, hash <short>. Bars from bar sheet v<n>.

## The table
| Slice | n | Score | 95% lower bound | Method | Bar | Verdict | Cases owed | Days at <n>% |
|-------|---|-------|-----------------|--------|-----|---------|-----------|--------------|
| <same-day> | <n> | <n>% | <n>% | normal | <n>% | PASS | — | — |
| <codeshare> | 500 | 82.4% | 79.1% | normal | 80% | **UNPROVEN** | 468 | 81 |
| <refund> | <n> | <n>% | <n>% | Wilson (n < 100) | <n>% | | | |

PASS means the LOWER BOUND is at or above the bar. Nothing else means pass.
UNPROVEN is not FAIL: the score is above the bar and the sample is too small to show it.

Overall score: <n>% — recorded here and reported nowhere else. It averages slices with
different bars and different stakes.

## For every unproven slice, the three options
| Slice | Collect the cases | Raise the score | Lower the damage |
|-------|------------------|-----------------|------------------|
| <codeshare> | <n> days at <n>% of traffic | <the named defect class, if there is one> | <mitigation> -> bar becomes <n>%, verdict becomes <n> |

## Slices that got worse since run <id>
| Slice | Was | Now | Still passing? | Owner |
|-------|-----|-----|----------------|-------|

## Recommendation, one line
<ship <slices>; hold <slices>; the reason is <one clause>>
```
</details>

<details><summary><b>Prompt · Per-slice lower-bound readout</b></summary>

```text
Convert these evaluation results into an evidence readout.

ONE table:
| Slice | n | Score | 95% lower bound | Method | Bar | PASS / FAIL / UNPROVEN | Cases owed |

Rules:
- lower bound = p - 1.96 * sqrt(p*(1-p)/n). Compute it even if I gave you only the score
  and n. If n < 100 use the WILSON score interval instead and put "Wilson" in Method.
- PASS only if the LOWER BOUND is at or above the bar.
- If the score is at or above the bar but the lower bound is not, mark UNPROVEN, not FAIL,
  and compute cases owed = 1.96^2 * p * (1-p) / (p - bar)^2, minus the n I already have.
- If the SCORE is below the bar, write "more cases will not help" in Cases owed.
- Never report an overall figure as the headline. Label any you include
  "recorded, not the verdict".

Then, for each UNPROVEN slice, three options with their cost: collect the cases (as DAYS,
using days = cases owed / (traffic share x cases per day)), raise the score, or lower the
damage and re-derive the bar as N/(N+1).

Finish with one line: ship, or do not ship, and the single reason.

BARS: <paste>
RESULTS: <paste>
TRAFFIC: <cases per day, and the share this slice would run at>
```
</details>

**Done when** — nobody in the room has seen a bare point estimate, and every unproven slice carries a
number of days rather than a shrug.

---

## 5 · The shadow run

**After the golden set clears, before any real passenger is affected.**

The agent runs beside the live desk, **deciding and logged, never acting**. Compare decision by
decision, nightly, for a window fixed in advance.

| Parameter | Working default | Yours to tune |
| --- | --- | --- |
| Agreement threshold | 95% | Yes |
| Window | 14 days | Yes |
| Money actions | Excluded from automatic agreement; always gated | **No** |

Make **"shadow never writes"** a test, not an intention. And compare **per slice** — overall
agreement of 96% can hide 64% on refunds.

If it does not match, you learned for free. That is the point of the rung.

The golden set and the shadow run test different things. The golden set proves the agent is right
about cases **you curated**; the shadow run proves it agrees with the live desk on **today's
traffic**, including the storm day and the fare class that only appears in August. Only one of the
two uses cases you did not choose.

> **Half the disagreements will be the desk being wrong.** That is not a reason to discount them —
> it is the most valuable output of the whole rung, because it is a policy finding you could not have
> got any other way.

### What you actually do

1. **Fix the window before a launch date exists.** Fourteen days written down in week two survives
   pressure; fourteen days proposed in week nine gets negotiated to three.
2. **Assert the no-write property in code.** A test that fails the build if the shadow path can reach
   a write. An intention is not a control, and the shadow path will be edited by somebody who does
   not know why it exists.
3. **Read every disagreement yourself in week one.** Personally, all of them. After that, cluster.
   The clusters are only useful once you know what the edges look like.
4. **Rank disagreements by cost, not by count.** Forty tone differences matter less than one wrongly
   refused refund, and a frequency-ranked list will bury it.
5. **Keep money actions out of the agreement statistic entirely.** Not weighted down — out. They stay
   gated regardless of what the shadow shows, so including them tells you nothing and invites the
   argument that a high number should unlock them.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Build the nightly comparison job: agreement per slice, the disagreement list ranked by estimated cost, and the assertion that fails if a write occurs. Insist on per-slice from the first night, because retrofitting slices means re-running the window |
| **Chat LLM** | Cluster a week of disagreements into at most six named themes, and say for each whether the agent or the desk was more often right. Forty disagreements usually collapse into four causes |
| **Chat LLM** | For the top theme, ask whether the fix belongs in the spec, the prompt, the tools or the bar. It is right often enough to save you the first hour of the argument |
| **Do not delegate** | Deciding that the desk was wrong. That reclassifies a disagreement as a policy finding and it changes what the agent is allowed to do, which is a decision with a name on it |

### The artefact

<details><summary><b>Template · Shadow-run comparison</b></summary>

```markdown
# Shadow run · <feature> · day <n> of <n>
Window: <start> to <end>, fixed on <date> BEFORE any launch date existed.
No-write assertion: <test name> — last failed: <never / date>.

## Agreement, per slice, tonight and last night
| Slice | Decisions | Agreed | Agreement | Last night | Threshold | Met? |
|-------|-----------|--------|-----------|------------|-----------|------|
| <same-day> | <n> | <n> | <n>% | <n>% | 95% | |
| <codeshare> | <n> | <n> | <n>% | <n>% | 95% | |
| <refund> | <n> | <n> | <n>% | <n>% | **n/a — gated regardless** | — |

Overall: <n>%. Recorded only — a 96% overall has been observed sitting on top of 64% on
refunds.

## Disagreements, ranked by cost of being wrong
| # | Case | Agent said | Desk said | Who was right | Est. cost of the difference | Theme |
|---|------|-----------|-----------|---------------|---------------------------|-------|
| 1 | <id> | | | agent / desk / unclear | $<n> | |

## Themes this week
| Theme | Count | Agent right | Desk right | Fix belongs in | Owner |
|-------|-------|------------|-----------|----------------|-------|
| <partner eligibility read too narrowly> | <n> | <n> | <n> | <tools / spec / prompt / bar> | |

## Policy findings — cases where the DESK was wrong
| Case | What the desk did | What policy says | Raised with | Date |
|------|------------------|------------------|-------------|------|

## Conditions still open before cut-over
| Condition | Status |
|-----------|--------|
| <n> consecutive days at or above threshold on <slice> | <n> of <n> |
| Every week-one disagreement read by <name> | |
| Rollback rehearsed | <date / not yet> |
```
</details>

<details><summary><b>Prompt · Specify the nightly comparison job</b></summary>

```text
Write the specification for a nightly job that compares an agent's shadow decisions
against the live human desk.

It must output, PER SLICE and never only in aggregate:
- decisions compared, agreed, agreement percentage, and last night's figure beside it
- a disagreement list ranked by ESTIMATED COST of the difference, not by frequency:
  case id, input summary, agent decision, desk decision, estimated cost
- a flag on any slice whose agreement fell against the previous night

Hard constraints:
- Money actions are reported separately and never counted toward the agreement statistic.
- The shadow path must not write. Include an assertion that FAILS THE JOB if a write is
  detected, and say what it asserts against.
- The comparison key is the decision, not the wording. Define agreement per slice.
- Output one markdown file for people and one CSV for the record.

Then list the three ways this job could silently produce a wrong agreement number, and
the check that catches each.

Our slices: <list>. Where decisions are logged: <system>. Cases per day: <n>.
```
</details>

**Done when** — "shadow never writes" is an assertion that can fail the build, and agreement is
reported per slice with money actions outside the statistic.

---

## 6 · Cut over at five percent

**The first real passengers. Everything before this was rehearsal.**

> **days of evidence = cases needed ÷ (traffic share × cases per day)**

At 240 cases a day and 5% of traffic you see 12 cases a day, so 500 cases takes **42 days**. A small
share is the safe place to start and a slow place to learn — which is exactly why a cut-over
*widens* rather than sitting at five percent forever.

Cutting over at fifty percent means half your passengers meet the first-day failure.

Rehearse the rollback **before** the cut-over, not during it. With a flag-driven shadow path, the
rollback is the flag.

Tool: [Cut-over evidence calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/cutover)

### What you actually do

1. **Rehearse the rollback with a person watching, and time it.** Write the number of minutes on the
   decision. A rollback nobody has thrown is a rollback of unknown duration, which is the same as not
   having one.
2. **Name who may throw it without asking.** At least two people, on the desk, not in engineering.
   The cost of an unnecessary rollback is an hour; the cost of waiting for approval is the incident.
3. **Pick the five percent deliberately, not randomly.** Exclude nothing that would make the sample
   unrepresentative, but do exclude the slices that are still gated — mixing them in makes the live
   numbers uninterpretable.
4. **Watch the same per-slice readout you built at rung 4.** The live numbers must arrive in the same
   shape as the golden-set numbers, or nobody will compare them and the comparison is the point.
5. **Set the stop condition before day one.** One graded-zero case, or any money action taken without
   a gate, stops the cut-over. Written down in advance, it costs nothing to honour.
6. **Tell the desk what to do with a bad answer.** A feedback path that takes ten seconds produces
   evidence; a path that takes an email produces silence and a rumour.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Wire the flag so the shadow path and the live path are the same code with one switch, and the rollback is a config change rather than a deploy |
| **Chat LLM** | Write the pre-mortem: "it is two weeks after cut-over and this went badly — list the ten causes in order of likelihood". Cheap, and it usually names the stop condition you had not written |
| **Do not delegate** | The cut-over decision. It is the release gate, it has one name on it, and it is the moment the programme stops being an experiment |

### The artefact

<details><summary><b>Template · Cut-over decision</b></summary>

```markdown
# Cut-over decision · <feature> · <date>
Decided by: <name>  (one name)   Shadow window: <start> to <end>, <n> days

## Evidence in front of me
| What | Value | Link |
|------|-------|------|
| Golden-set lower bound, per slice, vs bar | <table ref> | |
| Shadow agreement, per slice, over the full window | <table ref> | |
| Consecutive days at or above threshold | <n> | |
| No-write assertion, last failure | <never / date> | |
| Rollback rehearsed on | <date>, by <name>, took <n> minutes | |

## What goes live, and what does not
| Slice | Share on day one | Gated? | Why |
|-------|-----------------|--------|-----|
| <same-day> | 5% | no | <lower bound <n>% vs bar <n>%> |
| <codeshare> | 0% | — | **<unproven: lower bound <n>% vs bar 80%>** |
| <refund> | 5% | **yes, named approver on the charge** | <bar is 71% only because of the hold> |

Cases seen per day at this share: <n>.  days = cases needed / (share x cases per day).

## Rollback
Mechanism: <the flag, and where it lives>. Rehearsed <date>, time to revert <n> minutes,
watched by <name>. May be thrown without asking by <two names, on the desk>.
In-flight cases when it is thrown: <describe>.

## Stop conditions, agreed in advance
| Condition | Action |
|-----------|--------|
| Any case graded 0 | Stop, review same day |
| Any money action without its gate | Stop, incident, postmortem |
| Live lower bound on <slice> falls below its bar | Stop that slice, keep the others |

## Decision
<cut over to 5% on <date> | extend the shadow by <n> days | do not proceed, because ...>
```
</details>

**Done when** — somebody has watched the rollback thrown, the time it took is written on the
decision, and two named people on the desk may throw it without asking.

---

## 7 · Widen on live evidence

**From week two onward, forever. This is the rung with no end.**

A cut-over that never widens is a pilot with a longer name. Widening is earned by evidence, and the
schedule is written as **conditions, not dates**.

Worked for SkyWays codeshare at 82.4%, needing 968 cases against the 80% bar:

| Share | Cases per day | Days to 968 cases, rounded up |
| --- | --- | --- |
| 5% | 12 | **81** |
| 25% | 60 | **17** |
| 100% | 240 | **5** |

Which shows the bind plainly: the safe share is the slow one. The answer is not to start at
twenty-five percent. It is to widen the moment the *lower bound at the current share* clears the bar,
which happens long before you have collected every case the formula asks for at that share — because
the formula assumes you are stuck at the score you have, and a slice that improves proves itself
faster.

> **Widen one dimension at a time.** Share, or slices, or autonomy — never two in the same week. When
> something moves after a double change, you have learned nothing about which change moved it.

### What you actually do

1. **Write the schedule as conditions.** "Widen to 25% when the live lower bound on same-day holds at
   or above its bar for seven consecutive days" survives a slipped date; "widen to 25% on the 14th"
   does not survive a bad week.
2. **Flag any step that would take more than thirty days at its share.** That step needs a bigger
   starting share, a different mitigation, or a different approach — and you need to know it now
   rather than in week five.
3. **Keep the gated actions gated through every widening.** Share widens; authority does not. Moving
   both together is how a refund gets taken at scale by a system nobody re-approved.
4. **Re-run the sealed holdout before each widening.** Twenty percent of the golden set, never used
   for iteration, is the only evidence that you have improved the agent rather than the set.
5. **Watch one output mix weekly, and wire its drift alert to re-open the release gate.** Choose the
   mix that would embarrass you if it moved. That one line of policy turns a chart nobody opens
   into a control.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Compute the widening arithmetic: cases needed per slice, then days at 5%, 25% and 100%, and flag every step over thirty days |
| **Claude Code** | Generate the weekly live readout in the same shape as the golden-set readout, so the two are directly comparable without anybody re-typing a table |
| **Do not delegate** | The expansion gate. Wider use is the decision that puts more real passengers behind the agent, and a model cannot be accountable for that |

### The artefact

<details><summary><b>Template · Widening schedule</b></summary>

```markdown
# Widening schedule · <feature> · v<n> · <date>
Rule: conditions, never dates. One dimension at a time. Authority never widens with share.

## Steps
| Step | Slice | Share | Cases needed | Days at this share | Widen WHEN | Owner |
|------|-------|-------|-------------|--------------------|-----------|-------|
| 1 | <same-day> | 5% -> 25% | <n> | <n> | <live lower bound >= bar for 7 consecutive days AND zero graded-0 cases> | |
| 2 | <same-day> | 25% -> 100% | <n> | <n> | <as above, plus drift inside threshold for 14 days> | |
| 3 | <codeshare> | 0% -> 5% | 968 | 81 | <golden-set lower bound reaches 80% on the sealed holdout> | |
| 4 | <refund> | 5% -> 25% | <n> | <n> | <as step 1 — and the approver gate STAYS> | |

**Steps flagged as too slow (> 30 days at their share): <list>.** For each, the
alternative: <bigger share / a mitigation that lowers the bar / not this quarter>.

## What does not widen
| Action | Band | Stays gated because |
|--------|------|--------------------|
| <issue_refund above $400> | R4 | <named approver is a constraint, not a target> |
| <identity change> | R5 | <not delegated at all> |

## Narrowing conditions — the same list, read backwards
| Condition | Action | Who may act without asking |
|-----------|--------|---------------------------|
| <live lower bound below bar on any slice> | Narrow that slice to 0% | <names> |
| <drift above threshold on the watched mix> | Re-open the release gate, automatically | — |

## Drift watch
| Output mix | Baseline | This week | Change | Alert at | Wired to the gate? |
|-----------|----------|-----------|--------|----------|--------------------|
| <% refund vs credit> | <n>% | <n>% | <n>pp | 5pp w/w | yes |

## Sealed holdout
Opened before step <n> on <date>. Holdout <n>% vs <n>% on the worked set. A gap here
means we improved the set, not the agent.
```
</details>

<details><summary><b>Prompt · Widening arithmetic and the too-slow flag</b></summary>

```text
Compute a widening schedule from these slices, scores, bars and traffic.

For each slice and each of the shares 5%, 25% and 100%, give me:
| Slice | Score | Bar | Cases needed | Cases/day at this share | Days of live evidence |

Use:
  cases needed = 1.96^2 * p * (1-p) / (p - bar)^2
  days = cases needed / (share x cases per day)

Rules:
- Show the arithmetic for one row in full so I can check it by hand.
- If the score is below the bar, write "cannot be proven at this score" and produce no
  day counts for it.
- FLAG every step over 30 days at its share, and propose exactly one of: a larger
  starting share, a mitigation that lowers the damage and therefore the bar, or an
  explicit "not this quarter".

Then write the schedule as CONDITIONS, never dates: "widen <slice> from <a>% to <b>% when
the live lower bound holds at or above <bar> for <n> consecutive days and <condition>".

Finally, list anything that must NOT widen with the share, one clause each.

SLICES, SCORES, BARS: <paste>
CASES PER DAY: <n>
```
</details>

**Done when** — every widening step names the evidence that unlocks it, no step is a date, and the
steps that would take more than a month are flagged in writing.

---

## Under a deadline

The sponsor wants six weeks and the full plan needs ten. The instinct is to drop the gates and the
golden set as overhead. That build does go faster, and it reaches production with no bar, no cap and
no evidence — and the incident arrives inside the six weeks rather than after them.

**Bend scope, never the hard gates.**

| What bends | What does not |
| --- | --- |
| Number of slices shipped | The bar, the cap, the shadow run |
| Shadow window: 7 days instead of 14, on the simple slice only | Money actions staying gated |
| Soft gates → placeholder, named owner, date | The three hard gates |

Pick the slice a deadline rewards: **the one that can be proven quickly.** Same-day lookups are 60% of
the volume and already score 97%; seven days at 144 cases a day is about 1,000 decisions, which bounds
a 97% slice tightly. Codeshare sits at 76% against a bar of 80, and no deadline moves that number.

Then tell the sponsor it as a **trade, not a delay**: "60% of the load in six weeks, proven, with
codeshare next on the plan." Same facts, and the sponsor keeps listening.

---

## Common mistakes

| Mistake | What it costs | Instead |
| --- | --- | --- |
| A bar chosen rather than derived | It is re-argued every release, and it drifts down to meet the score | `bar = N/(N+1)` from a sourced damage and saving, published before scoring |
| Reporting the point estimate | 82% on 40 cases reads exactly like 82% on 500 | The lower bound in the column where the score used to be, with n beside it |
| "Failed" when it means "unproven" | A sprint of engineering on a slice that only needed cases | Three named options: collect, raise, or lower the damage |
| One overall accuracy number | Codeshare falls from 81% to 77% while the headline rises from 79% to 84% | Per slice, against its own bar, always |
| The judge run first | Money spent grading output the schema check rejects for free | Schema, then exact checks, then the judge on what survives |
| Skipping the shadow run because the golden set passed | You have proven the agent on cases you chose | The shadow tests today's traffic, including the storm day nobody curated |
| Cutting over at fifty percent | Half your passengers meet the first-day failure | Five percent, then widen on evidence |
| A widening schedule made of dates | The first bad week turns the plan into a negotiation | Conditions: a bound, a number of consecutive days, an incident count |
| Widening share and authority together | A money action goes to scale without anybody re-approving it | One dimension at a time; authority never widens with share |

---

## Try it

**Exercise 1.** A slice scores 88% on 120 cases against an 85% bar. Proven?

<details>
<summary>Answer</summary>

Margin = 1.96 × √(0.88 × 0.12 ÷ 120) ≈ 1.96 × 0.0297 ≈ **5.8 points**. Lower bound ≈ **82.2%**, which
is below the 85% bar. **Not proven.**

Cases needed = 1.96² × 0.88 × 0.12 ÷ (0.03)² ≈ **451**. You are 331 cases short, and the reason it is
so many is that 88% sits only three points above the bar.

The useful conversation is not "pass or fail" but "331 cases owed, or raise the score, or lower the
damage with a hold".
</details>

**Exercise 2.** The team wants to skip the shadow run because the golden set already clears every bar.
What do you say?

<details>
<summary>Answer</summary>

The golden set proves the agent is right about **cases you already curated**. The shadow run proves
something different: that it agrees with the **live desk on today's traffic**, including the cases
nobody thought to curate — the storm day, the partner outage, the fare class that only appears in
August.

They test different things, and only one of them uses cases you did not choose.

If the deadline is genuinely hard, shorten the window rather than deleting it: seven days on the
simplest slice, with every disagreement read by a person. Three days as a formality is worse than
nothing, because it does not include a weekend or a disruption day, and it buys false confidence.
</details>

**Exercise 3.** A refund slice has a saving of $12 and a damage of $600, and the team's best score
after two sprints is 94%. What do you do?

<details>
<summary>Answer</summary>

N = 600 ÷ 12 = 50, so the bar is 50 ÷ 51 = **98%**. At 94% you are below the bar, and no number of
additional cases will change that — more evidence makes a wrong answer more certain, not more
acceptable.

So do not go to the harness. Go to the design. Put a human hold on the charge and the damage of a
wrong case falls to the handling cost, say $30. Then N = 30 ÷ 12 = 2.5 and the bar becomes 2.5 ÷ 3.5
= **71%**. At 94% the slice now clears comfortably, and it ships this quarter with a person
confirming the money.

The instinct is to treat 98% as an engineering target. It is a statement about damage, and damage is
a design variable.
</details>

---

**Next:** [Role: QA lead](Role-QA-Lead) · [How to Run a Missing-Control Postmortem](How-to-Run-a-Missing-Control-Postmortem)
· [How to Review by Risk Band](How-to-Review-by-Risk-Band) · [Gates and Governance](Gates-and-Governance)
· [Formulas and Calculators](Formulas-and-Calculators) · [The Eight Loops](The-Eight-Loops)
