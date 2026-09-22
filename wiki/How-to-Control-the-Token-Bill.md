# How to control the token bill

The bill is 4.4 times the estimate, traffic is flat, and finance wants an answer by Friday.

Traffic is flat, so **behaviour** changed — and behaviour is only visible per call. This page is how
you find which behaviour, in what order to fix it, and how to stop it recurring.

This closes the [cost loop](The-Eight-Loops#cost), which closes into **P1**. A bill blowout is a
design question, not a finance one.

---

## Look in the per-call log, not the price list

The prices did not change. An hour spent checking them leaves you with an invoice showing one number
and nothing beneath it.

Four ratios are worth reading, and together they explain almost every blowout:

| Signature | Baseline | Now | Factor |
| --- | --- | --- | --- |
| Tokens per call | 2,100 | 3,360 | **1.6** |
| Frontier tier share | 50% | 100% | **1.5** |
| Cache hit ratio | 71% | 9% | **1.3** |
| Retries per conversation | 1.2 | 1.7 | **1.41** |

> **They multiply.** 1.6 × 1.5 × 1.3 × 1.41 = **4.40**

Four separate habits, each a sensible decision made by a careful person, and the product of them is
the invoice.

The trap is to chase the biggest *ratio* change. Retries rose by more than five times in relative
terms and contribute the **smallest** factor. The largest change in a ratio is not the largest factor
on the bill.

---

## Fix in the order that removes the most multiplier per day

> **priority = (factor − 1) ÷ days to fix**

| Fix | Factor | Days | Priority | Order |
| --- | --- | --- | --- | --- |
| Trim the context: send the slice, not the document | 1.6 | 0.5 | **1.2** | 1st |
| Restore routing by complexity | 1.5 | 0.5 | **1.0** | 2nd |
| Pin the model within a session | 1.3 | 1 | **0.3** | 3rd |
| Add the retry breaker | 1.41 | 2 | **0.2** | 4th |

The breaker is the right fix in the wrong position. Start with it and two days pass with the bill
still at 4.4, having removed the least multiplier available.

---

## The four habits, and what each one actually is

| Habit | What happens | The fix |
| --- | --- | --- |
| **Model switched mid-task** | The cache is model-scoped, so it is discarded and the full prefix is re-read | One model per task, written into the team's rules |
| **Whole document or codebase pasted** | 40k tokens per call, and *worse* answers | Send the slice. For legacy code, send a rule sheet |
| **Biggest model for everything** | Up to 160× on simple lookups | Route by complexity |
| **No circuit breaker** | A loop burns until somebody notices | `MAX_LOOPS = 5` |
| **Vague asks** | Wrong output, re-run | A sharper spec; track the re-run column |

---

## Caching that actually pays

The cache matches an **exact prefix**, in the order **tools → system → messages**, up to the block you
mark.

```
┌─ tools ─────────────────┐
│ ─ system ───────────────│  stable
│ ─ shared context ───────│  stable
│ ─ domain context ───────│  stable  ⟵ cache marker here
└─ the passenger request ─┘  volatile
```

Documented multipliers, read September 2026:

| | Relative to the input price |
| --- | --- |
| Five-minute cache **write** | 1.25× |
| One-hour cache **write** | 2× |
| Cache **read** | 0.1× — *Fable and Mythos 5.1 read at 0.025×* |

> **cost with cache = ( w + 0.1 × (N − 1) ) × T × p**, against **N × T × p** without.
> Break-even is the **second** use.

Used once, caching costs more. Used a hundred times it saves roughly 89%.

### Which window

| Traffic pattern | Window | Why |
| --- | --- | --- |
| Daytime chat, calls seconds apart | **Five minutes** | Refreshes free on each hit; the cheaper write |
| Overnight, one call every twelve minutes | **One hour** | The five-minute cache has always expired, so every call pays a 1.25× write. One 2× write beats twelve of them |

"Five minutes everywhere, it is the cheaper write" is the trap. **The cheaper write paid on every call
is more expensive than the dearer write paid once.**

### What breaks a cache

- Passenger details placed first "so the model sees the person first" — no two calls share a prefix
- A timestamp, request id or session id inside the cached block
- A model switch mid-task
- Fewer than about 1,024 cacheable tokens, which is below the minimum

Tool: [Cache break-even calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/cache)

---

## Batch what nobody is waiting for

Batch processing trades latency for price — documented at about **half** the on-demand rate, with
results returned within a day.

| Workload | Batch it? |
| --- | --- |
| Nightly re-scoring of the 500-case golden set | **Yes.** Nobody is waiting |
| Live passenger chat | **No.** A passenger who waits hours has already phoned the desk |

"Batch both to save the most" is the wrong answer to the right question.

---

## The dashboard trap

Cache hits return fast. A latency dashboard that flags very fast responses as suspected failures will
report hundreds of them, and somebody will propose switching the cache off — which raises the bill by
about a third within a day, because the anomaly *was the cache working*.

> **Mark cache hits in the trace, and exclude them from the alert.**

The response metadata already reports how many tokens were read from cache. Put
`cache_read_input_tokens` in the trace row and the false alarm disappears.

This is worth stating plainly because it is the observability trap that gets a working solution
switched off: **a cache hit counted as a wrong answer.**

---

## Guards, so it does not recur

It took four weeks for anybody to notice the bill had left its estimate.

| Guard | Setting |
| --- | --- |
| Alert on cost per case | **3× the estimate** — turns a monthly surprise into a daily signal |
| Loop cap | `MAX_LOOPS = 5` — makes a runaway impossible, however it is triggered |
| Per-transaction token cap | Next to the breaker |
| Cache hit ratio | A monitored number with a threshold |
| The caching and routing config | **One file, reviewed like code** |

"A reminder to the team to be careful with tokens" does nothing. Each of the four habits was a
sensible decision made by a careful person; being careful was never what went wrong.

The Day 75 bill began with an engineer reordering a prompt for clarity. A reviewed configuration file
and a watched ratio are what make that visible on the day rather than on the invoice.

---

## Close the loop in P1

The cost loop does **not** close in finance. It closes in a decision record.

The cost-per-case NFR of $0.60 was ratified on Day 9 and then never measured — which is how four
habits went unwatched for four weeks. The fix:

```
ADR-001 (amended) · cost per case
  Added:  cost per case is a MONITORED number.
  Owner:  the solution architect.
  Alert:  3× the ratified $0.60, on the daily per-call log.
```

Without that amendment the design stays silent about cost per case, and the next feature inherits the
same silence.

---

## Try it

**Exercise.** Pull your own four ratios for last month against the month before: tokens per call, tier
mix, cache hit ratio, retries per conversation.

<details>
<summary>How to read them</summary>

Multiply the four factors. If the product is close to the ratio between the two invoices, you have
explained the bill and you can stop looking.

If the product is well below the invoice ratio, something structural changed that is not a habit —
usually traffic, a new feature, or a price change you should now go and check.

And if you cannot compute the four ratios at all, that is the finding: **the per-call log is the
artefact you are missing**, and it is the one thing that turns a bill into a diagnosis. A model
gateway gives you routing, budgets, fallbacks and that log in one place.
</details>

---

**Next:** [Role: Solution architect](Role-Solution-Architect) · [Role: Engineering lead](Role-Engineering-Lead)
· [Formulas and Calculators](Formulas-and-Calculators) · [Anti-Patterns](Anti-Patterns)
