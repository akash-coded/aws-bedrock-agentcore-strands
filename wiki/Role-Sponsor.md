# Role: sponsor

You own the one loop no delivery role owns: **governance**, P0 all the way to P3. You are also the
person the programme is cancelled in front of, which makes you the only one whose incentives are
aligned with hearing bad news early.

This page is for sponsors, heads of product, delivery leads and anyone who signs the budget. It is
deliberately short. Your job is four questions, asked consistently.

---

## The four questions

Ask these every cycle, in this order, and most of the failure modes in this playbook cannot survive
in your programme.

### 1. "Which of these are rules?"

Ask it of the roadmap, not of one feature. Most of a backlog is deterministic and earns no agentic
ceremony. A team under an *agent-first* directive will build agents for things a `CASE` statement does
better, and will not tell you, because you asked for agents.

**What good looks like:** an [AI-fit verdict](Role-Product-Manager) on record for each item, with
two or three of the top five coming back as rules. That is the healthy answer.

### 2. "What may it do without a person, and who decided?"

Not *what can it do*. What is it **allowed** to do, per action, and where is that written.

**What good looks like:** an autonomy record per action with a reversibility column, and the caps
living in tool signatures rather than in prompt text. The difference is not pedantry — a prompt is a
request the model can be talked past; a signature is a boundary.

Ask one follow-up: **"show me the cap."** If someone opens a prompt file, you have found a gap.

### 3. "What are the two numbers?"

Never accept one.

```
                             baseline      now       change
person-days per story            8.0        4.6      −43%
token spend per story              –      $310
review hours added per story     1.2        2.0       +0.8
re-runs per story                  –        1.4
──────────────────────────────────────────────────────────
net              saved 3.4 person-days, spent $310 + 0.8 review hours
```

A first cycle can genuinely save time **and** cost more. That is normal and it is survivable — if it
arrives from the team rather than from finance. Cost turns positive from cycle two as the review load
falls.

**Three things to insist on:** the baseline is taken *before* the pilot; the review-hours row stays
visible; the re-run row stays visible because it is the leak signal.

> The programme is cancelled on the number that was hidden, never on the one that was shown.

### 4. "What level are we, and what is the next control?"

Not how many AI tools the teams have adopted. Tool count is the metric that rewards the least mature
behaviour available.

| # | Control | The test you can apply yourself |
| --- | --- | --- |
| 1 | A context file the agent reads | Ask to see it. Is it current? |
| 2 | Every item has a spec with a bar and an owner | Pick a story at random |
| 3 | The harness gates the merge, per slice | "What happens if one slice regresses?" |
| 4 | Caps live in tool signatures | "Show me the cap" |
| 5 | The trace redacts | "Is there a passport number in the log?" |
| 6 | Production evidence by segment, drift watched | "What re-opens the release gate?" |

A team with nine tools and none of these is at level one. A team with one tool and four of these is
further along, ships more safely, and costs less.

---

## The three reports you should receive

| Report | Cadence | From | If it is missing |
| --- | --- | --- | --- |
| **Two numbers** | Every cycle | PM, from the engineering ledger | You will hear the cost number from finance instead |
| **Drift readout** | Weekly | PM | Behaviour will change with no deploy and no alert |
| **Incident brief** | On each incident | PM and architect | Postmortems will end in a name rather than a control |

---

## What to do when the bill arrives

It will. A bill several times its estimate with flat traffic is a normal event in the first cycles,
and it is a **design** question, not a finance one. The cost loop closes into P1.

Four signatures explain almost every blowout. Ask which one it is:

| Signature in the per-call log | The habit behind it | The fix |
| --- | --- | --- |
| Tokens per call rose | Whole documents pasted instead of slices | Send the slice |
| Tier mix moved to frontier | No routing | Route by complexity |
| Cache hit ratio fell | Model switched mid-task, or something volatile inside the cached block | One model per task |
| Retries per conversation rose | Vague asks, or a model too weak for the slice | Sharper spec; right-size the tier |

The wrong response is a spending freeze, which stops the work and teaches nothing. The right response
is "which signature, and which decision record allowed it".

See [How to Control the Token Bill](How-to-Control-the-Token-Bill).

---

## What to do when the incident arrives

One question runs the whole room:

> **Which enforced control, if it had been present, would have made this impossible?**

Not who typed it. Not what the passenger sent. If the postmortem produces a name, it has not
finished; if it produces a control, a decision record and a lowered autonomy level, it has.

Expect the autonomy level to drop after an incident, and expect it to rise again only on evidence.
That is the system working, not a setback.

See [How to Run a Missing-Control Postmortem](How-to-Run-a-Missing-Control-Postmortem).

---

## What not to ask for

| Do not ask for | Because | Ask instead |
| --- | --- | --- |
| A single accuracy number | It hides the slice that carries the risk | "What is the score **per slice**, against its bar?" |
| A demo on day fourteen | It is the one day the team optimises for | "What shipped yesterday?" |
| AI tool adoption counts | It rewards the least mature behaviour | "What level are we, and what is the next control?" |
| A launch date before the shadow run | The date will win the argument against the evidence | "What is the shadow threshold, and when does the window close?" |
| Your sign-off on a pull request | You cannot evaluate it, and your name on it helps nobody | "Bring me intent and release" |

---

## Try it

**Exercise.** At your next steering meeting, ask only question three — "what are the two numbers?" —
and then say nothing for ten seconds.

<details>
<summary>What the answer tells you</summary>

**Both numbers, with a baseline taken before the pilot.** The team has an engineering ledger and a PM
who built the report from it. Ask question four next cycle.

**The saving only.** Nobody is tracking spend per story, which means the first person to compute it
will be finance, in a meeting you did not schedule. Ask for the token row by the next cycle; it is a
day's work to start.

**Both numbers, but the baseline was taken after the pilot.** An honest team with an unusable number.
The fix is cheap on the *next* feature: an afternoon of measurement before it starts.

**A percentage with no denominator.** "40% faster" on what, measured how, over how many stories. This
is the most common answer, and it is the one that collapses under the first serious question in a
board meeting.
</details>

---

**Next:** [Gates and Governance](Gates-and-Governance) · [The Eight Loops](The-Eight-Loops) ·
[Role: Product manager](Role-Product-Manager) · [Anti-Patterns](Anti-Patterns)
