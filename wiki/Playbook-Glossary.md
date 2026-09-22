# Playbook glossary

Terms as this playbook uses them, with a confidence mark on each:
**documented** (from a vendor's published documentation, dated) ·
**established** (a named, published practice) ·
**working method** (this playbook's construction — a default to tune).

Where the industry definition is contested, the contested part is said out loud.

The curriculum's wider glossary is
[docs/concepts/glossary.md](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/concepts/glossary.md);
this page is the playbook's own vocabulary.

---

## A–C

**Acceptance bar** · *working method* — The numeric success rate a best-guess step must meet to be
worth running unaided. Derived: `damage ÷ (damage + saving)`. Set **per slice**, never per feature.

**ADR (architecture decision record)** · *established* — One decision with its context, its
consequences and what it rejected, numbered and versioned next to the code, so settled questions stay
settled. Written **only at a trade-off point**. Nygard, 2011.

**Agentic** · *established* — Software that makes decisions and takes actions rather than following
fixed steps. The word that separates a rule-based system from one with a model in the loop.

**AI-DLC** · *established* — AI-Driven Development Life Cycle (AWS). Adaptive: run only the lifecycle
stages a given change actually needs. Here, the architect's judgement of **depth per change**.

**AiDD** · *established* — AI-driven development: the day-to-day craft of building with coding agents.
Context files, story files, editor agents, review by risk, cost habits.

**Authority budget** · *working method* — What the agent may change, touch or commit, decided
**before** what it may spend. A cheap task with too much authority is more dangerous than an expensive
one with none.

**Batch pricing** · *documented* — Work that can wait, such as re-scoring the golden set overnight,
runs at about half the on-demand price.

**Best-guess (probabilistic)** · *established* — Work a model does that is right a share of the time,
never every time. Proven by **measuring the share** on real cases, not by a yes/no test.

**BMAD** · *established* — Breakthrough Method for Agile AI-Driven Development. A pipeline of AI
personas — analyst, PM, architect, dev, QA — each handing a versioned artefact to the next. For
complex, multi-team, audited work.

**Bolt** · *working method* — A thin, shippable slice reviewed and integrated the same day. The unit
that replaces the sprint story when building is fast. The term comes from AWS's AI-DLC; **one risk per
bolt** is this playbook's rule.

**Cache (prompt cache)** · *documented* — Reusing the processed prefix of a prompt instead of
re-paying for it. Matches an **exact prefix** in the order tools → system → messages, up to a marked
block. Model-scoped. Break-even at the second use.

**Checker (inspector)** · *established* — An independent model, or the same model in a fresh context
with an adversarial brief, placed after a generating step. **Never the drafter grading itself.**

**Circuit breaker** · *established* — A maximum number of agent reasoning loops, then a hard stop and
a hand-off to a person. Five is a common working value.

**Compounding (pⁿ)** · *established* — Chained steps multiply. Four steps at 90% is **66%**. Length is
the enemy.

**Consequential step** · *working method* — A step that changes something real. Built as a tool **plus
a gate**; proven by a required confirmation.

**Context file** · *documented* — The markdown a coding tool reads at session start: `CLAUDE.md`
(Claude Code), `.github/copilot-instructions.md` (Copilot), `AGENTS.md` (Codex CLI),
`.cursor/rules/*.mdc` (Cursor). Copilot's steers suggestions; Claude Code's drives autonomous actions.

**Context layers (onion)** · *working method* — Shared → domain → product → task, each versioned. A
new product writes only its own layers and inherits the rest. Built on DRY and layered architecture,
not a named standard.

**Cost per case** · *working method* — The running cost of one handled case. Ratified as an NFR and
monitored like latency. The number most often ratified and then never measured.

---

## D–G

**Deterministic (exact)** · *established* — Work that must be right every single time. Done by code,
proven by a unit test. The model hands it numbers and reads the result.

**Door (one-way / two-way)** · *established* — A decision is a two-way door if it can be reversed
cheaply and a one-way door if it cannot. Bezos, 2015 letter to shareholders.

**Drift** · *established* — A probabilistic system changing behaviour when the world shifts under it,
**with no deploy and no error**. Watched as an output-mix KPI; a drift alert re-opens the release gate.

**EARS** · *established* — Easy Approach to Requirements Syntax. `WHEN` a condition `THE SYSTEM SHALL`
a behaviour, plus a boundary and a number. Mavin and colleagues, Rolls-Royce, 2009. The format
spec-driven tooling reads.

**Eight-field spec** · *working method* — Title, value, acceptance, the model's role, autonomy, the
bar, the fallback, the records. The smallest spec a coding agent can build from. **The five agentic
fields are the decisions nobody had made.**

**Enforced control** · *working method* — A limit written into the tool's own signature — a cap, a
confirmation token — which holds whatever the model is convinced of. Contrast with *a request*.

**Exact / best-guess map** · *working method* — Every step of a feature tagged exact, best-guess or
consequential, with the proof each kind owes. Drawn before any framework is chosen.

**Gate** · *established* — A decision with evidence in front of a named person and their name on it.
Five here: intent, plan, behaviour, release, expansion.

**Golden set** · *established* — Real historical cases with the expected outcome, one per line, run on
every change. **The acceptance bar made executable.** A slice below its bar rejects the change.

---

## H–P

**Hard gate / soft gate** · *working method* — A hard gate halts the phase until it is signed. A soft
gate lets the phase close behind a placeholder, with a named owner and a date. Four questions classify
any decision; one "no" makes it hard.

**Injection (prompt injection)** · *established* — Text that arrives as data and is read by the model
as an instruction. **The one genuinely new threat.** Every ingested text is untrusted, including
partner API responses.

**Judge (LLM-as-a-judge)** · *established* — An independent model scoring a best-guess output against
a rubric for tone, policy and false claims — **after** the exact checks have run.

**Layered defences** · *established* — Several imperfect layers in a row; harm gets through only if
every layer fails at once. Reason, 1990. The discipline is classifying each layer honestly as
enforced, a request, or absent.

**Least authority (least privilege)** · *established* — The narrowest permissions that still let the
agent work; read separated from write. Saltzer and Schroeder, 1975.

**Little's law** · *established* — Time in a queue equals work waiting divided by the rate served.
Little, 1961. Capacity is fixed by people; **slots needed is a policy variable**.

**Lower bound** · *established* — The lowest value a true score could plausibly have given the sample
size. **The bar is proven only when the lower bound clears it.** Wilson, 1927.

**MCP (Model Context Protocol)** · *documented* — One plug so any compliant AI client can use your
tools and data, turning M apps × N systems into M + N. A server exposes **tools** (actions),
**resources** (read-only data) and **prompts** (templates). Split reads from writes; require
confirmation on writes.

**Model gateway** · *documented* — One layer every model call passes through, giving routing, budgets,
fallbacks and a per-call log in one place. LiteLLM is the named example.

**P0 · P1 · P2 · P3** · *established* — Frame, Design & Spec, Build & Prove, Run & Learn. The spine.

**Paired indicators** · *established* — Every measure reported beside the one that shows its side
effect, so neither can be pushed alone. Grove, 1983; Goodhart's law, 1975.

---

## R–Z

**Request (a rule in a prompt)** · *working method* — A model can be talked past anything in its
prompt, so a prompt rule **lowers a probability and never removes a path**. The counterpart of an
enforced control.

**Risk ladder (R1–R5)** · *working method* — Reversible draft → reversible change → hard to reverse →
money, identity or policy → irreversible. The check grows with the band. **A change inherits the band
of whatever it touches.**

**Rule sheet** · *established* — Business rules extracted from legacy code into condition, action,
source line and confidence, so the agent reads rules instead of thousands of lines. Everything below
0.9 confidence gets a human check.

**SDD (spec-driven development)** · *established* — The spec, not the code, is what you maintain; code
is generated from it and regenerated on change. **The backbone. Use it always.**

**Sensitivity point** · *established* — An NFR rated high for both importance and difficulty, where
one design decision changes the outcome. ATAM. **Sensitivity points, and only they, earn an ADR.**

**Shadow deployment** · *established* — Run the agent beside the live process, deciding but never
acting, for a fixed window; compare; then cut over a slice on evidence. Also called dark launching.

**Slice** · *working method* — One kind of case with its own difficulty — same-day lookups, codeshare
tickets, refunds. **Bars, scores and gates are all per slice.**

**Story file (agent-ready)** · *working method* — One self-contained file the agent builds from:
context by reference, spec in EARS, tools, tests, done-when, cost. BMAD's shard and SDD's unit at
once. Reviewable as a diff.

**Strangler Fig** · *established* — Wrap the legacy system, route a slice to the new one, grow the new,
retire the old. Fowler, 2004.

**Trace** · *established* — One row per consequential action: input (redacted), tools called, the
decision, model version, approver, cost. Replayable, auditable, **and not a breach target**.

**Two numbers** · *working method* — Time saved **and** money spent, reported together, always. A first
cycle can save time and cost more. The programme is cancelled on the number you hid.

**Unknown-days** · *working method* — The sum, over every day, of the unknowns still open. The measure
that explains why the walking skeleton goes first.

**Walking skeleton** · *established* — A thin end-to-end slice that works, proving the pieces connect
before you add more. Cockburn, Crystal Clear, 2004. Day one of a bolt plan.

---

## The concept map

The playbook teaches **55 concepts**, grouped by the loop they belong to. Browse them with their
worked example and the episode each first appears in:
[the concept map](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/concepts).

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

**Next:** [Formulas and Calculators](Formulas-and-Calculators) · [Decision Trees](Decision-Trees) ·
[Sources and Confidence](Sources-and-Confidence) · [The Agentic PDLC](The-Agentic-PDLC)
