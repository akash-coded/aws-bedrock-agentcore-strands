# Formulas and calculators

Every number in the playbook, with the formula behind it and a worked example. Seventeen of these have
a live calculator: [the toolkit](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/aifit).

**Confidence marks** appear against each one:
**documented** (from a vendor's published documentation, dated) ·
**established** (a named, published practice) ·
**working method** (this playbook's own construction — a default to tune, not a standard).

---

## Value and worth

### The value line · *working method*

> **net = cases × minutes × rate − cases × run cost − cases × share reviewed × review minutes × rate**

Value is arithmetic, not adjectives. The two terms people omit are the last two: what it costs to
**run** (tokens) and what it costs to **check** (review).

*Worked:* 240 cases/day × 8 minutes × $0.75/min = $1,440 saved. Less run cost 240 × $0.60 = $144.
Less review 240 × 30% × 3 min × $0.75 = $162. **Net $1,134/day.**

The review term is high in cycle one and falls as the artefacts sharpen. Leaving it out is what makes
cycle two look like a regression.

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/value)

### The acceptance bar · *working method*

> **N = damage ÷ saving** , **bar = N ÷ (N + 1)**

One wrong case undoes the saving from N right ones.

| Slice | Saving | Damage | N | Bar |
| --- | --- | --- | --- | --- |
| Same-day lookup | $4 | $4 | 1 | 50% |
| Codeshare rebook | $9 | $36 | 4 | 80% |
| Refund, no hold | $12 | $600 | 50 | 98% |
| Refund **with a hold** | $12 | $30 | 2.5 | **71%** |

**A human hold lowers the damage, so it lowers the bar.** That is the lever that lets a best-guess
feature ship safely.

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/bar)

---

## Requirements and decisions

### Utility-tree priority · *established* (ATAM)

> **priority = value × (4 − complexity)** , each scored 1–3

Two stakeholders whose priority for the same NFR differs by **5 or more** have a conflict, and every
conflict is a decision-record trigger.

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/utree)

### Weighted decision matrix · *established* (Pugh, 1981)

> **score = Σ weight × rating**

Plus two numbers no vendor page carries: the **three-year cost with the people counted**, and the
**door** (one-way or two-way).

**The flip test:** how far must one weight move before the winner changes? A decision that flips on
one point is a decision to describe as close, in the record.

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/bvb)

### Hand-off count · *established*

> **hand-offs = n(n − 1) ÷ 2** for n agents

Five agents have **ten** possible hand-offs, each one a place to get coordination wrong. This is the
arithmetic behind "start single, escalate on a named limit".

---

## Reliability

### Chained probability · *established*

> **end-to-end = p ⁿ**

| Steps at 90% | End to end |
| --- | --- |
| 2 | 81% |
| 4 | **66%** |
| 6 | 53% |

**Length is the enemy.** Multiply, never average. Four steps at 90% is wrong one time in three, and
it fails fluently.

### The lower bound of a score · *established* (Wilson, 1927)

> **lower bound = p − z × √( p × (1 − p) ÷ n )**

The bar is proven only when the **lower bound** clears it, not the point estimate.

| Score | n | 95% lower bound |
| --- | --- | --- |
| 82% | 40 | 70.1% |
| 82% | 500 | 78.6% |
| 86% | 500 | 83.0% |

Under about 100 cases, use the Wilson interval; the normal approximation misbehaves at small n.

### Cases needed to prove a bar · *established*

> **n = z² × p × (1 − p) ÷ (p − bar)²**

*Worked:* to prove 88% against an 85% bar: 1.96² × 0.88 × 0.12 ÷ 0.03² ≈ **451 cases**.

The `(p − bar)²` denominator is the thing to internalise: **the closer your score sits to the bar, the
quadratically more cases it takes to prove.**

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/confidence)

### Days of live evidence · *working method*

> **days = cases needed ÷ ( traffic share × cases per day )**

*Worked:* 500 cases ÷ (5% × 240/day) = 500 ÷ 12 = **42 days**.

A small traffic share is the safe place to start and a slow place to learn. That is why a cut-over
widens.

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/cutover)

---

## Delivery

### Queue time · *established* (Little, 1961)

> **queue time = review slots needed ÷ review slots available per day**

*Worked:* 9 changes × 2 reviewers = 18 slots ÷ 4.5 per day = **4.0 days**.
Routed by band (2 changes × 2, 3 × 1, 4 × 0) = 7 slots ÷ 4.5 = **1.6 days**.

Capacity is fixed by people. **Slots needed is a policy variable.**

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/queue)

### Exposure in unknown-days · *working method*

> **exposure = Σ, over every day, of the unknowns still open**

The measure that explains why the walking skeleton goes first: it retires the largest unknown — "do
these pieces connect" — on day one, for half a day's work.

---

## Cost

### Cache break-even · *documented*

> **cost with cache = ( w + 0.1 × (N − 1) ) × T × p** , against **N × T × p** without

where **w** is the write multiplier and **N** the number of uses.

| | Relative to the input price |
| --- | --- |
| Five-minute write | **1.25×** |
| One-hour write | **2×** |
| Read | **0.1×** — *Fable and Mythos 5.1 read at 0.025×* |

Minimum about 1,024 cacheable tokens. The five-minute cache refreshes free on each hit; the cache is
model-scoped.

**Break-even is the second use.** Used once it costs more; used a hundred times it saves ~89%.

*Multipliers as documented by Anthropic and Amazon Bedrock, read September 2026.*

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/cache)

### The four bill factors · *working method*

> **context factor** = tokens per call now ÷ baseline
> **tier factor** = blended price now ÷ baseline, where blended = frontier share × price ratio + (1 − frontier share)
> **cache factor** = (1 − 0.9 × hit ratio now) ÷ (1 − 0.9 × hit ratio baseline)
> **retry factor** = retries now ÷ baseline
>
> **They multiply.**

*Worked:* 1.6 × 1.5 × 1.3 × 1.41 = **4.40** — which is the whole of a bill 4.4× its estimate.

### Fix order · *working method*

> **priority = (factor − 1) ÷ days to fix**

| Fix | Factor | Days | Priority |
| --- | --- | --- | --- |
| Trim the context | 1.6 | 0.5 | **1.2** |
| Restore routing | 1.5 | 0.5 | **1.0** |
| Pin the model per session | 1.3 | 1 | 0.3 |
| Retry breaker | 1.41 | 2 | 0.2 |

The largest *change in a ratio* is not the largest *factor on the bill*, and neither is the same as
the best *first fix*.

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/leaks)

---

## Governance

### The two-number report · *working method*

> **fewer person-days = (baseline − now) ÷ baseline**
> **net = person-days saved, reported beside tokens spent and review hours added**

Two rows keep it honest: **review hours added** (high in cycle one) and **re-runs** (the leak signal).

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/report)

### Maturity level · *working method*

> **level = the number of the six controls in place; the next step is the first one missing**

Context file · spec with a bar and an owner · harness gating the merge per slice · caps in tool
signatures · a redacting trace · production evidence by segment with drift watched.

[Calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/maturity)

---

## Quick reference card

| Question | Formula |
| --- | --- |
| Is it worth it? | net = cases × min × rate − run − review |
| How right must it be? | bar = N ÷ (N + 1), N = damage ÷ saving |
| Which NFR first? | priority = value × (4 − complexity) |
| How many agents? | hand-offs = n(n−1)/2 — so: one |
| Will the chain hold? | pⁿ |
| Have we proven it? | lower bound = p − z√(p(1−p)/n) |
| How many more cases? | n = z²p(1−p) ÷ (p − bar)² |
| How long at 5%? | days = cases ÷ (share × cases/day) |
| How long is the queue? | slots needed ÷ slots per day |
| Does caching pay? | break-even at the 2nd use |
| Why is the bill high? | context × tier × cache × retry |
| What do I fix first? | (factor − 1) ÷ days |

---

**Next:** [Decision Trees](Decision-Trees) · [Exercises and Answers](Exercises-and-Answers) ·
[Playbook Glossary](Playbook-Glossary) · [Sources and Confidence](Sources-and-Confidence)
