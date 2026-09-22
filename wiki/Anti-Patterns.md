# Anti-patterns

Sixteen ways this goes wrong, what each one costs, and the move that prevents it.

None of these are carelessness. Every one is a sensible decision made by a competent person, which is
why "be more careful" has never fixed any of them.

---

## In requirements

**Consolidating in the room.**
*Costs:* two stakeholders leave believing they were dropped, and the dropped voice returns in week
five as a constraint that reshapes three NFRs.
*Instead:* read back with credit, consolidate in the email.

**NFRs left as adjectives.**
*Costs:* the workshop argues about words for two hours and never reaches the conflicts, which were the
only reason six people were in a room.
*Instead:* six-part scenarios with a number, written **before** the room meets.

**Constraints gathered after ratification.**
*Costs:* the room ratifies a latency the legacy system cannot deliver, and the workshop runs twice.
*Instead:* constraints by type — technical, regulatory, commercial — first.

**A vote with dots on a wall.**
*Costs:* the loudest group wins. Cost per case gets two dots and comes back as a crisis on day 75.
*Instead:* utility trees, merged, scoring value and complexity separately.

---

## In design

**A record for every decision.**
*Costs:* forty records in a week, nobody reads the forty-first, and the three that mattered are buried
among them.
*Instead:* one record per **trade-off point**, and nowhere else.

**A swarm for work one tool can fan out.**
*Costs:* five agents have ten possible hand-offs, each one a coordination failure waiting to happen —
for work a single fan-out tool does with none.
*Instead:* start single. Escalate only on a **named limit**, written into the record.

**Fixing the model's knobs in a spec.**
*Costs:* the spec is wrong at the next framework release, because the knob was renamed or removed.
*Instead:* behaviour in the spec, the knob in engineering's configuration. **Specify behaviour, never
knobs.**

**Treating every decision as a hard gate.**
*Costs:* the build waits behind eleven open decisions.
*Instead:* the four classification questions. For SkyWays, three halt and eight run behind
placeholders.

---

## In building

**A cap that lives in a prompt.**
*Costs:* a $2,000 refund that was not owed. A prompt is a request, and a model can be talked past a
request.
*Instead:* a typed, bounded parameter that raises, plus a confirmation token the model cannot mint.
Keep the prompt sentence as **policy**, never as enforcement.

**The drafter grading itself.**
*Costs:* a review step that adds cost and catches nothing, because the model reviewing its own output
shares its own blind spots.
*Instead:* a different model, or a fresh context with an adversarial brief, given constraints and
output only.

**A plug scheduled after its consumer.**
*Costs:* a day lost mid-sprint when the rebook bolt cannot be built because its MCP server is
scheduled for Thursday.
*Instead:* dependency order. Walking skeleton first, exact code early, the plug before any gated write
that needs it.

**Reviewing by size of diff.**
*Costs:* four hundred lines of help text get two senior readers, and three lines in a refund cap get a
quick approval.
*Instead:* the band follows **what the change touches**, assigned by a path rule, never by the author.

---

## In proving

**Counting cache hits as wrong answers.**
*Costs:* a false quality alarm, a wasted week, and a serious proposal to switch off the thing that was
working. Switching it off raises the bill by about a third within a day.
*Instead:* record cache-read tokens in the trace and exclude hits from the latency alert.

**Reporting a score without its sample size.**
*Costs:* 82% on forty cases is presented as clearing an 80% bar. The lower bound is 70%.
*Instead:* the bar is proven when the **lower bound** clears it. Never quote a score without its n.

**Cutting over at fifty percent.**
*Costs:* half your customers meet the first-day failure.
*Instead:* five percent with the shadow result in hand, widen on evidence, and rehearse the rollback
first.

---

## In running

**Reporting one number.**
*Costs:* the steering committee learns the token bill from finance instead of from you, and stops
trusting the report.
*Instead:* two numbers, always together, with the review-hours and re-run rows that keep them honest.

**A postmortem that ends in a name.**
*Costs:* fifty-five minutes of one person's defence, and a refund tool that still accepts any amount.
*Instead:* "which enforced control would have made this impossible?" — and the hour produces a
control, a record and a brief.

**Counting AI tools as a maturity metric.**
*Costs:* it rewards the least mature behaviour available. Nine tools with no gates is level one.
*Instead:* six controls, each present or absent. The level is how many; the next step is the first
missing one.

---

## The two that cause the most damage

If you fix nothing else on this page:

> **1 · A rule that lives only in a prompt.**
> It reads exactly like a rule and nothing in code review flags it. Everyone believes the cap exists.
> Grep your prompts for `never`, `always`, `do not`, `ask before` and any currency symbol, and move
> every consequential one into a signature.

> **2 · A score without its sample size.**
> It is the most common way a team ships something that has not been proven, and it is invisible in
> every dashboard, because the dashboard shows the point estimate.

---

## Try it

Pick the three from this page you recognise in your own team. For each, write who would have to do
what, this week, to prevent it.

<details>
<summary>What to expect</summary>

Most of these are prevented by an artefact that takes an afternoon: the authority budget, the bar
sheet, the path rule, the drift chart. That is the genuinely good news about this list — the fixes are
small, and they are small because each one moves a decision from *the moment of pressure* to *a
document written calmly in advance*.

The ones that take longer are the cultural two: the postmortem question and the two-number report.
Both need a sponsor to ask for them consistently, and neither survives being introduced once.
</details>

---

**Next:** [Decision Trees](Decision-Trees) · [Scenario Library](Scenario-Library) ·
[Gates and Governance](Gates-and-Governance) · [Exercises and Answers](Exercises-and-Answers)
