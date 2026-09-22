# Sources and confidence

Every claim in this playbook carries one of three marks. The point of the marks is to let you argue
with the right things: a documented price is checkable, a working method is a default to tune, and
confusing the two wastes everybody's time.

| Mark | Means | How to treat it |
| --- | --- | --- |
| **documented** | From a vendor's published documentation, read on a date | Check it. Prices and limits change |
| **established** | A named, published practice with an author and a year | Standard. Read the source if you want depth |
| **working method** | This playbook's own construction | A **default to tune on your own traffic**, not a standard |

> The documented figures were checked in **September 2026** and will change. The working-method
> thresholds are starting points, not findings.

---

## Documented

| Claim | Source |
| --- | --- |
| Cache write 1.25× input for five minutes, 2× for one hour; read 0.1× (Fable and Mythos 5.1 at 0.025×); ~1,024-token minimum; model-scoped; five-minute cache refreshes free on hit | Anthropic and Amazon Bedrock prompt-caching documentation, read September 2026 |
| Batch processing at about half the on-demand rate, results within a day | Anthropic and Amazon Bedrock batch documentation |
| MCP: a server exposes tools, resources and prompts; stdio locally, Streamable HTTP in production; consequential calls designed for human review | Model Context Protocol specification |
| Context files: `CLAUDE.md`, `.github/copilot-instructions.md` (plus scoped `*.instructions.md`), `AGENTS.md`, `.cursor/rules/*.mdc`. Copilot's steers suggestions; Claude Code's drives autonomous actions | Anthropic, GitHub, OpenAI and Cursor documentation |
| A model gateway giving routing, budgets, fallbacks and a per-call log | LiteLLM, as the named example |

---

## Established

| Practice | Source |
| --- | --- |
| Utility trees, sensitivity points, trade-off points | ATAM — Kazman, Klein and Clements, SEI, 2000 |
| Six-part quality attribute scenarios | Bass, Clements and Kazman |
| EARS acceptance syntax | Mavin, Wilkinson, Harwood and Novak, Rolls-Royce, 2009 |
| Architecture decision records | Nygard, 2011; MADR |
| Walking skeleton | Cockburn, *Crystal Clear*, 2004 |
| Risk-first ordering | Boehm, 1988 |
| One-way and two-way doors | Bezos, 2015 letter to shareholders |
| Least privilege | Saltzer and Schroeder, 1975 |
| Layered defences | Reason, 1990; *BMJ*, 2000 |
| Blameless postmortems | Beyer and colleagues, *Site Reliability Engineering*, 2016 |
| Strangler Fig | Fowler, 2004 |
| Little's law | Little, 1961 |
| Confidence bounds for a proportion | Wilson, 1927 |
| Stratified sampling | Neyman, 1934 |
| Concept selection by weighted matrix | Pugh, 1981 |
| Total cost of ownership | Gartner, 1987 |
| Stage-gate systems | Cooper, 1990 |
| Paired indicators | Grove, 1983 |
| Goodhart's law | 1975 |
| Conway's law | Conway, 1968 |
| Shadow deployment, canary release, LLM-as-a-judge | General practice |
| The **bolt** as a work cycle of hours or days | AWS AI-Driven Development Lifecycle (AI-DLC) |

---

## Industry measurements quoted

Treat these as dated observations about a fast-moving field, not as constants.

| Figure | Source |
| --- | --- |
| 90% of developers use AI at work | DORA 2025, ~5,000 respondents |
| 80% report a productivity gain | DORA 2025 |
| 30% place little or no trust in AI-generated code | DORA 2025 |
| 16% of organisations deploy on demand; most deploy less than monthly | DORA 2025 |
| 42% of committed code is AI-assisted, by developers' own estimate | Sonar 2025 survey |
| Median time a pull request sits in review rose sharply in 2026 | Faros AI, 22,000 developers, 2026 |
| 31% more pull requests merging with no review at all | Faros AI, 2026 |
| 98% more pull requests merged per developer, while org-level delivery stayed flat | Faros AI, 2025, 10,000 developers |
| 66% more epics completed per developer once organisations adapted | Faros AI Engineering Report, 2026 |
| Multi-agent delegation paid off on routine work, not on the hardest problems | Anthropic, on its own multi-agent research system |

The two Faros lines that matter most are the last two taken together: **more changes are produced;
the same number of people read them.** That is the argument for
[review by risk band](How-to-Review-by-Risk-Band), stated in data.

---

## Working methods · this playbook's own constructions

These have no external source. They are offered as defaults because they have worked, and they are
the parts you should expect to change as you tune them.

- The **P0–P3 phase names** and the eight-loop ring
- The **hard and soft gate split**, and the four classification questions
- The **minimum artefact set** at each hand-off
- The **eight-field spec** and its reading test
- The **acceptance bar** formula, and the hold as a documented lever
- The **exact / best-guess / consequential** map and its proof column
- The **R1–R5 risk ladder** and routing review by band
- **One unknown per bolt**, and exposure measured in unknown-days
- The **four bill signatures** and the `(factor − 1) ÷ days` fix order
- The **two-number report** and its net line
- The **maturity ladder** of six controls
- Every numeric default: 5% drift alert, 95% shadow agreement over 14 days, 5% first cut-over,
  `MAX_LOOPS = 5`, 3× cost alert, 0.9 rule-extraction confidence

**Tune them on your own traffic.** A default that you have measured and changed is better than a
default you inherited, and this list exists so you know which numbers are yours to change.

---

## Corrections

Prices drift, documentation moves, and measurements are superseded. If a figure here is wrong or
out of date, that is worth reporting and it will be fixed with credit:

- [Open a discussion](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101)
- [Report a problem](https://github.com/akash-coded/aws-bedrock-agentcore-strands/issues/new/choose)

A source and a date beat an opinion.

---

**Next:** [Playbook Glossary](Playbook-Glossary) · [Formulas and Calculators](Formulas-and-Calculators)
· [The Agentic PDLC](The-Agentic-PDLC) · [Contributing to this Wiki](Contributing-to-this-Wiki)
