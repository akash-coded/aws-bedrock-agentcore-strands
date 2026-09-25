# Role: product manager

<!-- tutorial:lesson -->*The short version is the lesson **[For product managers](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/agentic-pdlc-for-product-managers/)**, the whole role in one sitting. This page goes deeper.*<!-- /tutorial:lesson -->

You are on the hook for **what gets built, why, and how much the machine may do without asking.**
Nothing about that is new. What is new is that the thing you write is read by a machine that cannot
ask you what you meant, and that a feature can now be right *a share of the time* rather than always.

> **Looking for what to do on Monday?** That is the
> [journey](Journey-Product-Manager) — eight steps in order, each with the artefact it produces, a
> template to write it and prompts to draft it faster, and
> [interactive on the site](https://akash-coded.github.io/aws-bedrock-agentcore-strands/product-manager/).
>
> This page is the standing definition of the job: what you own, what you may settle alone, what
> crosses your desk, how the role fails, and how anyone can tell from outside whether it is being
> done.

---

## What stays the same, and what changes

| You have always done this | What a model in the middle adds |
| --- | --- |
| Discovery, stakeholder interviews, the numbers behind the ask | The pain is written as a **measurement**, and an AI-fit verdict is added. Most of a backlog is deterministic and earns no agentic ceremony |
| Prioritisation, the business case, RICE or a weighted score | The value line carries a **running cost**: tokens per case, the judge, the retries. At scale, value per case can turn negative |
| The PRD: problem, users, scope, success metrics | It becomes **eight fields** a coding agent can read, acceptance in EARS, a bar per slice. Five of the eight are decisions nobody had made |
| Roadmap, sprints, milestones, dependencies | Sprints become **bolts**. The shadow run is a milestone, and cut-over starts at five percent |
| Steering committees, status reports, trade-off calls | Autonomy is a product decision with a **door** on it. You own three gates. The committee gets **two numbers** |
| Adoption, usage, satisfaction | **Drift** joins the KPI list. An incident becomes the next P0 brief |

---

---

## What you own, what you shape, and what you must not touch

The commonest argument on an agentic programme is not about the work, it is about who settles a
question. Three columns end most of them.

| | |
| --- | --- |
| **You own** | The pain register · the AI-fit decision record · the value line · the autonomy decision · the eight-field spec · the acceptance bar sheet · the bolt plan · the gate decisions that are yours · the cut-over · the two-number report |
| **You shape** | The agent map, which is the architect's · the contents of the golden set, which are QA's · the order of work inside a bolt, which is engineering's · the alarm thresholds, which are the platform's. You are consulted on all four and you settle none of them |
| **You must not touch** | The verdict on a slice — *proven*, *failed* and *unproven* are QA's three words · where the checkers go · what a cap is set to in code · declaring an incident over |

The third column is the one worth reading twice. A product manager who overturns a QA verdict has not
sped anything up; they have removed the only independent reading the programme had.

---

## The eight decisions only you can make

One per step, and each is the same kind of thing: a fact about your business, your regulator or your
ledger that no amount of context makes knowable from outside. A model can draft everything around
them.

| Step | The decision | Why it cannot be delegated | Where it lands |
| --- | --- | --- | --- |
| [Discover](Journey-Product-Manager) | Which pain is worth solving | A model ranks by how vividly a pain was described, which tracks who spoke last, not what it costs | Pain register |
| [Qualify](Journey-Product-Manager) | Whether a wrong action can be undone | Recoverability is a fact about your ledger and your regulator, not a property of the text | AI-fit decision record |
| [Frame](Journey-Product-Manager) | The autonomy level itself | This is the decision money and regulators hang off, and it carries your name | Autonomy decision record |
| [Specify](Journey-Product-Manager) | The bar, and the autonomy fields | Both are business risk decisions with a formula behind them, not preferences | Eight-field spec · bar sheet |
| [Plan](Journey-Product-Manager) | Which slice ships first | A call about where the value and the risk are, made under a deadline you own | Bolt plan |
| [Gate](Journey-Product-Manager) | The gate decision itself | A gate is defined by a name on it, and a model cannot hold accountability | Gate decision record |
| [Launch](Journey-Product-Manager) | The cut-over, and any decision to exclude a slice from gating | Excluding a slice changes what the gate means, silently | Cut-over decision |
| [Learn](Journey-Product-Manager) | What the sponsor sees | Everything else in the step can be drafted; choosing what is reported is the job | Two-number report |

If you are ever unsure whether a call is yours, ask what a model would have to know about your
organisation to make it, and whether that knowledge exists anywhere it could read. If the answer is
no, it is yours.

---

## What crosses your desk

Hand-offs are where agentic programmes actually fail, and the P1 → P2 crossing is the one nothing
downstream survives without. See [the hand-off table](The-Agentic-PDLC) for the full set.

<!-- picture:wikimap:role-product-manager -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-product-manager.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-product-manager.dark.webp"><img alt="What arrives on the product manager's desk, from whom, and what leaves it, to whom" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-product-manager.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-product-manager.light.webp">Open the picture full size</a></sub>
<!-- /picture -->

| Phase | You receive | You hand over | To |
| --- | --- | --- | --- |
| **P0 · Frame** | The request, in whatever form it arrived | Pain register · AI-fit record · autonomy ceiling | Solution architect |
| **P1 · Design & Spec** | Constraint register · ratified NFRs · the exact / best-guess / consequential map | The eight-field spec · a bar per slice · the bolt plan | Engineering lead · QA lead |
| **P2 · Build & Prove** | Golden-set readout *with its lower bound* · the shadow comparison | The gate decision — or a waiver naming its blast radius and its closure date | Engineering lead |
| **P3 · Run & Learn** | Trace · drift readout · the bill decomposed into its four factors | Two-number report · the brief the next P0 starts from | Sponsor |

Note what you receive in P2: a **lower bound**, not a score. If what arrives is a single percentage,
the hand-off is incomplete and the gate cannot be held on it.

---

## The gates you own

| Gate | Yours? | What you need in front of you |
| --- | --- | --- |
| Intent | **Yours** | Pain register, AI-fit verdict, value line |
| Plan | **Shared** with the architect | Bolt cut, authority budget, gate map |
| Behaviour | QA's | — |
| Release | **Yours** | Shadow comparison, rollback rehearsed |
| Expansion | QA's | — |

List the approvals you gave last month and strike the ones you could not evaluate. Ask to be removed
from behaviour and expansion sign-offs. They are QA's, and your name on them helps nobody.

---

---

## How this role fails

Five modes, each with its tell. A tell is something an outsider can observe, not a feeling you have
about the team.

**Ambition laundering.** The AI-fit check returns four rules and one genuinely agentic request, and
the four get built as agents anyway because the verdict was read as a lack of ambition.
*The tell:* an AI-fit record with no rejected alternative written in it.

**One bar for the product.** A single accuracy target applied across every slice, which is always
too strict for the cheap ones and too loose for the expensive one.
*The tell:* the bar sheet has one row.

**The gate you cannot evaluate.** Your name on the behaviour and expansion gates, which are QA's.
*The tell:* look at last month's approvals and strike the ones you could not have argued with. If
anything is struck, ask to be removed from that gate.

**The baseline taken afterwards.** The two-number report with nothing to compare against, because
nobody measured the before.
*The tell:* the first number is a percentage and there is no dated figure behind it. This is an
afternoon's work before the pilot and impossible after it.

**The spec that is still a PRD.** Eight fields where the three classical ones fill themselves in and
the five agentic ones are blank or aspirational.
*The tell:* the acceptance field contains the words *accurate* or *helpful* and no number.

---

## How you are measured

Two numbers, reported together, every time:

| | What it is | Why both |
| --- | --- | --- |
| **Person-days per unit of work** | The change against a dated baseline | Alone, it invites the reply *"at what cost?"* |
| **Cost per unit of work** | Tokens, judge calls and retries, per story or per case | Alone, it looks like a bill with no benefit attached |

Carry the two honest rows underneath them — **review hours added** and **re-runs per unit** — because
those are what someone sceptical will find, and finding them yourself is the difference between a
report and a defence.

**If you do not offer these, you will be measured on something worse.** The vacuum is filled by tool
adoption — seats bought, teams onboarded — which measures purchasing and not delivery, and which
cannot fall when the work gets worse.

---

## Your first thirty days in the role

Ordered so that the things which become impossible later happen first.

1. **Take the baseline this week.** Person-days per story and cost per story, dated, before anything
   ships. Nothing on this list is more time-critical; it is an afternoon now and unavailable later.
2. **Run the three AI-fit questions over the top five requests.** Expect four rules and one agentic.
   Write down what was rejected and why — that record is what lets you say no with evidence.
3. **Find the one feature that is already live** and write its bar sheet retrospectively, per slice.
   You will usually discover there was never a bar, only a hope.
4. **Read last month's approvals** and strike the ones you could not have evaluated. Hand those gates
   back.
5. **Write the two authority lists** — allowed alone, needs a person — for one feature, before anyone
   sizes a token budget. Authority first, tokens second; doing it the other way round is how a cap
   ends up set to whatever was affordable.
6. **Ask who closes the cost loop and the incident loop.** Not which team — which person. If you
   cannot get a name, that loop is absent, and absent is the honest word.

---

## Your Monday list

Five things, in order, that move a team furthest for the least effort:

1. Take one live request phrased as a vibe and rewrite it as **who · volume · cost · evidence**.
2. Run the three AI-fit questions on your top five requests.
3. Fill the acceptance bar sheet for one feature's slices. Find the slice with the highest bar; that
   is where the human hold goes.
4. Write the two authority lists — allowed alone, needs a person — **before** anyone sizes tokens.
5. Take the baseline for the two-number report **before** the pilot. It is an afternoon's work and it
   is worthless afterwards.

---

---

## Try it

**Exercise 1.** Your PRD is thirty pages. Write the eight fields for one feature in it. Title, value,
acceptance, the model's role, autonomy, the bar, the fallback, the records.

<details>
<summary>What you should notice</summary>

The three classical fields fill themselves in from the PRD. The five agentic ones will not, because
nobody decided them. That is the finding, not a failure of the exercise: **the five agentic fields are
the decisions your team has been leaving to whoever writes the code.** Settle each with its owner —
autonomy with you, the bar with QA, the fallback with the architect.
</details>

**Exercise 2.** An executive asks you to raise the assistant's autonomy on refunds because "it has been
right every time for two months". What do you need before you say yes?

<details>
<summary>A defensible answer</summary>

Three things. **The number of refund cases in those two months** — "right every time" over eleven cases
proves nothing, and the lower bound of the score is what matters, not the score. **The damage per wrong
case**, which sets the bar; refunds are real money and hard to reverse, so the bar is high. And **what
the door is** — is raising the level reversible if it goes wrong, and how fast?

If the evidence supports it, the level moves one step, not to the top, and it stays gated above the
cap. Levels rise on evidence, one step at a time. See
[How to Prove the Bar](How-to-Prove-the-Bar).
</details>

**Exercise 3.** Three months after launch the assistant starts offering credits instead of refunds. No
code changed. What is the artefact that should have caught it, and who owns it?

<details>
<summary>Answer</summary>

A **drift readout** — the output mix charted weekly with an alert threshold, 5% week over week as a
starting default. It is a **product** KPI, not an engineering log, and it sits on your dashboard next
to conversion, because the question it answers is "is it still doing what we launched?"

The rule that turns it into a control: **a drift alert re-opens the release gate automatically.**
</details>

---

**Next:** [Role: Solution architect](Role-Solution-Architect) · [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts)
· [Gates and Governance](Gates-and-Governance) · [Decision Trees](Decision-Trees)

---

## Where the detail lives

| You want | Go to |
| --- | --- |
| The day-to-day walk, with templates and prompts | [Journey · Product Manager](Journey-Product-Manager) |
| Whether this is AI at all | [Decision Trees](Decision-Trees) |
| Deriving a bar, and proving it | [How to Prove the Bar](How-to-Prove-the-Bar) |
| Every formula on this page, with its derivation | [Formulas and Calculators](Formulas-and-Calculators) |
| What a gate is, and who holds it | [Gates and Governance](Gates-and-Governance) |
| Practising the judgement calls | [Exercises](Exercises-and-Answers) · [Scenario Library](Scenario-Library) |
| The whole method in one picture | [The agentic PDLC](The-Agentic-PDLC) |

**Next:** [Journey · Product Manager](Journey-Product-Manager) ·
[Role: Solution Architect](Role-Solution-Architect) · [Role: Sponsor](Role-Sponsor)
