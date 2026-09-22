# Decision trees

Eleven decisions this playbook makes the same way every time, each drawn as a tree. Print the ones you
use; they are meant to be settled in minutes, not debated in meetings.

---

## 1 · Is this AI at all?

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

---

## 2 · What kind of step is this?

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

---

## 3 · How much autonomy?

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

---

## 4 · Hard gate or soft gate?

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

---

## 5 · How many agents?

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

---

## 6 · Where does this rule live?

```mermaid
flowchart TD
  A["A rule"] --> Q1{"If the model were talked<br/>past it, would it cost money,<br/>expose data or be irreversible?"}
  Q1 -->|yes| T["<b>The tool signature.</b><br/>Typed, bounded, raises.<br/>Keep the sentence in the prompt as policy."]
  Q1 -->|no| P["<b>The prompt.</b><br/>It is policy, and policy is fine there."]
```

> A prompt is a **request**. A tool contract is a **boundary**.

---

## 7 · Which review band?

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

---

## 8 · Does caching pay here?

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

---

## 9 · Which model tier?

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

---

## 10 · How deep a process for this change?

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

---

## 11 · Ship it, or not?

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

---

## Try it

Take the decision your team argued about most recently. Find it on this page.

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
</details>

---

**Next:** [Formulas and Calculators](Formulas-and-Calculators) · [The Agentic PDLC](The-Agentic-PDLC)
· [Exercises and Answers](Exercises-and-Answers) · [Anti-Patterns](Anti-Patterns)
