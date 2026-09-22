"""Solution architect · steps 7-8."""

STEPS_C = [
{
 "n": 7, "id": "detail", "phase": "Detail",
 "title": "Layer the context, wrap the system, place the checker",
 "when": "P1 into P2, as the design becomes something an engineer can build",
 "purpose": (
   "Three details decide whether the design works, and none of them is visible in a diagram. "
   "**Context** is the largest single driver of both quality and cost, and it wants to be layered "
   "and inherited rather than pasted. A legacy system wants **one well-defined door** instead of a "
   "custom wire per product, which is what turns M applications times N systems into M + N. And a "
   "chain of best-guess steps **multiplies** rather than averages: four steps at 90% each is 66%, "
   "and it fails fluently, so nobody notices until a passenger does."),
 "activities": [
   {"do": "Draw the four context layers, each inherited by the one below",
    "detail": "Shared for org-wide standards, security and tone; domain for the business model; "
              "product for this application; task for this feature. A new product writes only the "
              "last two and onboards in a day instead of a week."},
   {"do": "Name what is genuinely domain-level",
    "detail": "This is the layer teams forget and it holds most of the real reuse — the booking "
              "model, the fare rules, the things every product in the area needs and each one "
              "currently re-invents in its own prompt."},
   {"do": "Make every override declare its reason and its scope",
    "detail": "A silent override is drift with a good explanation attached. Declared, it is a "
              "decision somebody can review; undeclared, it is the stale copy nobody can find."},
   {"do": "Send the slice a task needs, never the whole stack",
    "detail": "Forty thousand tokens of standards in every call is both the bill and the quality "
              "problem: a bigger context makes answers worse, not better, and it is the habit that "
              "hides behind *for context*."},
   {"do": "Wrap each system as one server with three primitives",
    "detail": "Tools are actions the model may invoke, resources are read-only data the application "
              "supplies, prompts are templates a person picks. Split reads from writes and require a "
              "confirmation on every write in the contract, not in the description."},
   {"do": "Multiply the chain, do not average it",
    "detail": "Four steps at 90% is 66%, end to end wrong one time in three. Length is the enemy, so "
              "the first defence is removing a step — every step you remove multiplies back."},
   {"do": "Place an independent checker after each costly, easy-to-miss generating step",
    "detail": "Independent means a different model, or the same model in a fresh context with an "
              "adversarial brief. A model reading its own output shares its own blind spots, which "
              "is exactly why *review your answer* does not work."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Paste a product's prompt dump and ask it to sort every line into shared, domain, product "
           "or task, with one line of reasoning each. It is fast and it makes the duplication "
           "obvious.",
    "caution": "It puts almost everything in shared, because shared is where general-sounding "
               "sentences go. The domain layer is the one it will not find for you."},
   {"tool": "Claude Code",
    "use": "Have it generate the server schema from an existing API surface: resources for read-only "
           "data, tools split into open reads and gated writes, prompts for the templates a person "
           "picks.",
    "caution": "It offers one broad manage_thing(action) tool because that is tidy. Any path through "
               "such a tool carries the authority of the worst action it can reach — reject it and "
               "make it enumerate."},
   {"tool": "Chat LLM",
    "use": "Write the checker's brief. It is an adversarial instruction — find what is wrong, list "
           "the violations, do not rewrite — and it is a different artefact from the brief that "
           "generated the answer.",
    "caution": "Never run the checker in the context that produced the output, and prefer a "
               "different model. Self-review returns a confident yes and no finding."},
   {"tool": "Do not delegate",
    "use": "Deciding where the checkers go. Each one costs a call, and putting them everywhere is "
           "the same error as putting them nowhere; the judgement is which wrong answers are both "
           "expensive and easy to miss.",
    "caution": None},
 ],
 "artifact": {
   "name": "Layered context spec + server schema + checker placement",
   "good": "One place to edit each rule, one server per system with reads open and writes gated in "
           "the contract, and a checker after each generating step whose errors are expensive and "
           "invisible.",
   "owner": "Solution architect"},
 "template": {
   "title": "Context layers, server schema and checker placement", "lang": "markdown",
   "body": """# Detail design · <feature>
_Owner: <name> · <date> · Read by: engineering and QA_

## 1 · Context layers, inherited downward
| Layer | Holds | Example files | Who edits |
|-------|-------|---------------|-----------|
| shared | org-wide standards, security, tone, glossary | <standards.md · security.md · tone.md> | <platform> |
| domain | the business model for this area | <booking-model.md · fare-rules.md> | <you> |
| product | this application's architecture and APIs | <architecture.md · apis.md> | <the product team> |
| task | this feature's spec, bar and file list | <spec.md · bar.md · files.md> | <the bolt's owner> |

**Rules**
- A new product writes ONLY product and task. It inherits the rest.
- A shared change is one commit, and every product picks it up.
- An override declares its reason and its scope. A silent override is a drift.
- Send the slice a task needs, never the whole stack: <40k> tokens becomes <2k>.
- The domain layer is the one teams forget, and it holds most of the reuse.

## 2 · The server for <system>
| Primitive | Controlled by | Entries |
|-----------|---------------|---------|
| resources — read-only data | the application | <booking_record · passenger_history · fare_rules> |
| tools — open reads | the model | <search_flights · check_availability> |
| tools — gated writes | the model, within the contract | <rebook (CONFIRM)> · <issue_refund (CONFIRM, amount at or below the cap)> |
| prompts — templates | the person | <draft_disruption_reply> |

- Transport: <Streamable HTTP in production, stdio for local development>
- Auth: <as the specification's authorization framework requires>
- Trace: every tool call logged — input, decision, output, model version
- **Rejected:** <one broad manage_booking(action) tool — any path through it could cancel>

M applications times N systems becomes M + N. Build the server once and any compliant
client plugs into it.

## 3 · The chain, and where the checkers go
> <0.9> x <0.9> x <0.9> x <0.9> = **<0.66>** — multiply, never average

| # | Step | Kind | Checker? | Why |
|---|------|------|----------|-----|
| <1> | <read the booking> | best-guess | no | <low stakes, caught downstream> |
| <2> | <choose the flights> | best-guess | **yes** | <costly to get wrong, easy to miss> |
| <3> | <compute the fare> | exact | no | <a unit test, not a checker> |
| <4> | <draft the message> | best-guess | **yes** | <false claims and tone, invisible to the drafter> |
| <5> | <rebook> | consequential | no | <a confirmation, not a checker> |

**Independence** — each checker runs on <a different model> OR <the same model in a
fresh context with an adversarial brief>. Never a self-review, and never inside the
context that produced the output.

**Checker brief, step <n>:** <Find what is wrong with this. Do these options satisfy
every stated constraint? List the violations. Do not rewrite.>

**Re-draft cap:** <2> rounds, then escalate to a person.
"""},
 "prompts": [
   {"title": "Sort a prompt dump into context layers",
    "when": "Every product pastes the same forty pages and one copy has gone stale",
    "body": """Below is everything currently pasted into the prompts of <product>.

Sort every line into exactly one of four layers and say why.

  SHARED   org-wide standards, security, tone of voice, glossary
  DOMAIN   the business model for this area: entities, rules that hold across products
  PRODUCT  this application's architecture, APIs and conventions
  TASK     this feature's spec, its bar and its file list

OUTPUT SHAPE:
1. A table: | Line (truncated) | Layer | Why | Duplicated in how many products? |
2. A DOMAIN section listed separately and in full. This is the layer teams forget and
   I want to read it on its own.
3. A list of lines that contradict each other, with both versions and the products they
   came from. These are the stale copies.
4. For each layer, the token count, so I can see what a task actually needs to be sent.

RULES:
- Resist putting things in SHARED. A line belongs in shared only if a product in a
  DIFFERENT business area would also need it. Apply that test explicitly per line.
- A line that names this feature is TASK, however general it sounds.
- Do not rewrite any line. Sorting is the job.

PROMPT DUMP:
<paste>"""},
   {"title": "Draft the server schema, reads open and writes gated",
    "when": "Before anyone writes a third custom integration to the same system",
    "body": """Design a single server exposing <system> to any compliant AI client.

Expose exactly three kinds of thing:
  RESOURCES  read-only data the application supplies
  TOOLS      actions the model may invoke
  PROMPTS    templates a person picks

OUTPUT SHAPE:
1. resources: name, what it returns, who controls it.
2. tools, in TWO separate lists: OPEN READS and GATED WRITES. Every gated write carries
   a required confirmation parameter in its signature and its risk band.
3. prompts: name and when a person would pick it.
4. A REJECTED section: designs you considered and discarded, with the reason.
5. The trace row each tool call writes.

RULES:
- Never propose one broad tool with an action parameter. Any path through such a tool
  carries the authority of the most dangerous action it can reach. Enumerate instead.
- A read tool must have no side effects, and you must say how that is enforced rather
  than asserted.
- Every write tool's confirmation is a typed parameter, not an instruction in the
  description. A description is a request.
- Where the underlying system exposes something that should not be reachable at all,
  say so and leave it out. Not every capability becomes a tool.

SYSTEM: <the API surface, or a link to it>"""},
   {"title": "Compute the chain and place the checkers",
    "when": "Engineering says ninety percent is solid",
    "body": """Here are the steps of <feature>, with each best-guess step's measured or estimated
accuracy: <paste>.

1. Compute the end-to-end success rate by MULTIPLYING the best-guess steps. Show the
   multiplication. Do not average anything.
2. Tell me what that rate means in plain words: wrong roughly one time in how many.
3. Option one, SHORTEN: which steps could be removed or merged, and what the rate
   becomes. Look especially for exact work that has crept into a prompt, and for two
   calls doing what one could do.
4. Option two, CHECK: which steps get an independent checker. Place them only where a
   wrong answer is COSTLY and EASY TO MISS. Give the rate after checkers, and state
   the assumption you used about what a checker recovers.
5. For each checker: the model or context that makes it independent, and its brief,
   written as an adversarial instruction.
6. The re-draft cap, and what happens when it is hit.

RULES:
- Exact steps do not get a checker. They get a unit test. Say so rather than skipping
  them silently.
- Consequential steps do not get a checker. They get a required confirmation.
- Do not propose raising the model tier on every step. That is the expensive answer to
  a structural problem, and say so if someone has suggested it."""},
 ],
 "example": {
   "title": "SkyWays · 66%, and the layer nobody had written",
   "body": "Two findings came out of the same afternoon. The chain had three best-guess steps in it, "
           "and multiplied rather than averaged it came out well below what the bar sheet implied — "
           "failing fluently, which is why nobody had noticed. Two checkers went in, after choosing "
           "the flights and after drafting the message, each on a different model with an adversarial "
           "brief and a re-draft cap of two rounds. The second finding was quieter. Every product was "
           "pasting forty pages of standards into every call; a security rule had changed the month "
           "before and two products still carried the old one with nobody able to say which. Four "
           "layers fixed it, and the layer that was missing entirely was **domain** — the booking "
           "model and the fare rules that every product in the area needed and each had re-invented. "
           "The same afternoon put the fifteen-year-old reservation system behind one server: "
           "resources for the read-only data, search open, rebook and refund gated in the contract, "
           "and a single broad manage_booking tool rejected because any path through it could cancel "
           "a booking."},
 "pitfalls": [
   "Everything in the shared layer. It is where general-sounding sentences go, and the result is a "
   "shared file every product has to read around and a domain layer that never gets written at all.",
   "One broad tool with an action parameter. It looks tidy in the schema, and it means every path "
   "through it carries the authority of the most dangerous action it can reach.",
   "A checker reading its own output in its own context. It shares the blind spots that produced the "
   "error, so it returns a confident yes and the chain keeps its 66%.",
 ],
 "done_when": "Every rule has exactly one place it can be edited, every write tool requires a "
              "confirmation the model cannot mint, and the chain accuracy is a multiplication with a "
              "checker after each step whose errors are expensive and invisible.",
},
{
 "n": 8, "id": "evolve", "phase": "Evolve",
 "title": "Make the running system cheap, auditable and able to redesign itself",
 "when": "P2 into P3, and then for as long as the system runs",
 "purpose": (
   "Three things decide whether an architecture survives contact with production. The **bill**, "
   "which is a design question and not a finance one: caching pays only if the layout lets it hit, "
   "and routing pays only if a breaker stops the runaway. The **trace**, which has to be replayable "
   "by audit without becoming a breach target, which means redact rather than omit. And the "
   "**incident**, which is where your next design decision comes from — a postmortem that produces "
   "a name has not finished; one that produces an enforced control has."),
 "activities": [
   {"do": "Lay the prompt out for the cache, with the marker on the last stable block",
    "detail": "The cache matches an exact prefix in the order tools, system, messages. Put the "
              "passenger's request first *for emphasis* and no two calls share a prefix, so caching "
              "is switched on and never hits."},
   {"do": "Count the reuse before turning caching on",
    "detail": "cost with cache = ( w + 0.1 × (N − 1) ) × T × p against N × T × p without. The "
              "documented multipliers, read September 2026: a five-minute write is 1.25× input, a "
              "one-hour write 2×, a read 0.1×, and Fable and Mythos 5.1 read at 0.025×. Break-even "
              "is the **second** use; at one use it costs more."},
   {"do": "Choose the window from the traffic pattern, not from the cheaper write",
    "detail": "Five minutes everywhere is the trap. On traffic arriving every twelve minutes the "
              "five-minute cache has always expired, so every call pays a write — and the cheaper "
              "write paid on every call costs more than the dearer write paid once."},
   {"do": "Route by complexity and put a breaker on every loop",
    "detail": "A delay lookup should not cost what a multi-leg international rebooking costs. "
              "MAX_LOOPS = 5, then a hard stop and a hand-off, because no legitimate case needs "
              "fifty and a runaway burns until somebody notices."},
   {"do": "Redact the trace, and mark the cache hits in it",
    "detail": "Masking keeps the decision replayable and the identifier out of the store; omitting "
              "the field breaks the audit. Then exclude cache hits from the latency alert, or a fast "
              "response gets reported as a suspected failure."},
   {"do": "Rewrite every incident as the missing-control question",
    "detail": "Which control, if present, would have made this impossible? Reconstruct the state "
              "from that question rather than from the timeline, and the answer is an ADR and a tool "
              "signature rather than a ticket and a name."},
   {"do": "Migrate legacy piece by piece, with a rule sheet where the docs are missing",
    "detail": "Score each module on risk, documentation, coupling, reversibility and how much it "
              "teaches; wrap it behind a clean interface, route a slice, grow the new, retire the "
              "old. Payments last, and never the whole codebase in one context."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Reorder one live prompt for the cache and add the assertion that proves it — cache tokens "
           "read above zero on the second call. Then have it pull the four ratios from the per-call "
           "log: tokens per call, tier mix, cache hit ratio, retries per conversation.",
    "caution": "Make it check for anything volatile inside the cached block. One timestamp or request "
               "id misses the prefix on every call, and the config file will still say caching is on."},
   {"tool": "Chat LLM",
    "use": "Compute the break-even and the saving for your reuse count and window, and tell you which "
           "window the traffic pattern actually argues for.",
    "caution": "Paste the vendor's current pricing page into the prompt rather than trusting its "
               "memory of the multipliers. A stale multiplier turns the arithmetic into a decision "
               "you cannot defend in front of finance."},
   {"tool": "Claude Code",
    "use": "Extract a rule sheet from a legacy module — rule id, condition, action, source line, "
           "confidence — so the agent reads a few hundred tokens of intent instead of four thousand "
           "lines that bury it.",
    "caution": "Everything below 0.9 confidence goes to a person first. Those rows are where the code "
               "is doing something the comments deny, which is the part worth reading yourself."},
   {"tool": "Do not delegate",
    "use": "The missing-control finding. Naming the control that would have made an incident "
           "impossible is the one judgement in the postmortem, and a model will happily propose a "
           "better prompt, which is a request rather than a control.",
    "caution": None},
 ],
 "artifact": {
   "name": "Caching and routing config · redacted trace spec · the incident ADR",
   "good": "One configuration file for caching and routing, reviewed like code; a trace row that is "
           "replayable and holds no raw identifier; and an incident record whose finding is an "
           "enforced control rather than a person.",
   "owner": "Solution architect"},
 "template": {
   "title": "Run-time architecture and the incident record", "lang": "markdown",
   "body": """# Run-time architecture · <feature>
_Owner: <name> · <date> · Config reviewed like code: <path>_

## Caching layout
[tools] [system] [shared context] [domain context <- cache marker] [task] [the request]
  stable ---------------------------------------------------------> | volatile

- The cache matches an EXACT prefix, in the order tools -> system -> messages, up to
  the marked block. The changing request goes last, always.
- Documented multipliers, read September 2026: five-minute write 1.25x input ·
  one-hour write 2x · read 0.1x · <Fable and Mythos 5.1 read at 0.025x>
- cost with cache = ( w + 0.1 x (N - 1) ) x T x p, against N x T x p without.
  **Break-even is the second use.** At N = 1 it costs more than not caching.
- Window: <five minutes> because <calls arrive seconds apart and each hit refreshes it
  free>. Choose one hour when <a call every twelve minutes means the short cache has
  always expired and every call pays a write>.
- Minimum cacheable block: <about 1,024 tokens, model dependent>

| What breaks the cache | Present here? |
|-----------------------|---------------|
| The request placed first, for emphasis | <no> |
| A timestamp, request id or session id inside the cached block | <no> |
| A model switch mid-task — the cache is model-scoped | <forbidden in the team rules> |
| Fewer than the minimum cacheable tokens | <no> |

## Routing and the breaker
| Complexity score | Tier | Example |
|------------------|------|---------|
| below <0.3> | <cheap> | <is my flight delayed?> |
| <0.3> to <0.7> | <mid> | <am I owed a hotel under the regulation?> |
| above <0.7> | <frontier> | <missed connection, lost bag, wedding tomorrow> |

- MAX_LOOPS = <5> on every loop, then a hard stop and a hand-off to a person.
- A per-transaction token cap, next to the breaker.
- Alert on cost per case at **3x** the ratified figure, from the daily per-call log.

## The trace row
ts · input (passport ****1234, card ****9902) · tools called · decision ·
model version · approver · cost · cache tokens read

- **Redact, do not omit.** Masking keeps the decision replayable and the identifier out
  of the store. Omitting the field breaks the audit instead.
- Retention: <90 days hot, then aggregate>. Traces are production data; guard them like
  production.
- Mark cache hits and EXCLUDE them from the latency alert, or a fast response is
  reported as a suspected failure and someone proposes switching the cache off.
- Test: <a passport number never reaches a row>.

## Incident to design change · <date>
**Reconstruct** <with the cap enforced: impossible. With the approver enforced:
impossible. Therefore both were absent — that is the state the system was in.>
**Finding** the enforced control that was missing: <name it>
**Not the finding** <the input, the person who typed it, or any control that would only
have detected it afterwards>
**Change** <the typed parameter, the gate or the permission — and the file it lives in>
**Record** <ADR-<n>> · autonomy on <action> drops one level, raised again only on evidence
**Verify** <QA re-runs the attack; it must now be stopped twice over>
"""},
 "prompts": [
   {"title": "Diagnose a bill that left its estimate",
    "when": "The invoice has moved and traffic has not",
    "body": """My token bill is <n>x its estimate and traffic is flat. Diagnose it from the
per-call log at <path>, not from the price list — the prices did not change.

Compute four ratios, the baseline period against now:
- tokens per call
- share of calls on the frontier tier
- cache hit ratio
- retries per conversation

OUTPUT SHAPE:
1. A table: | Signature | Baseline | Now | Factor |
2. The PRODUCT of the four factors, with the arithmetic shown. If the product is close
   to the ratio between the two invoices, say so and stop looking.
3. If the product is well below the invoice ratio, name what structural change is not
   explained by habit: traffic, a new feature, or a price change I should go and check.
4. A fix order, computed as priority = (factor - 1) / days to fix. Show the arithmetic.

RULES:
- Do NOT rank by the largest change in a ratio. Retries often rise the most in relative
  terms and contribute the smallest factor on the bill.
- For each fix, name where the control lives afterwards: a config file reviewed like
  code, a breaker constant, a rule about prompt ordering.
- Each of these was a sensible decision made by a careful person. "Remind the team to
  be careful with tokens" is not a fix; say what makes the habit visible on the day."""},
   {"title": "Turn the incident into an enforced control",
    "when": "After any incident, while the room is still discussing the input",
    "body": """Turn this incident into a design change. Use EXACTLY this structure.

**Timeline** — what happened, minute by minute, from the input to the consequence
**Reconstruct** — for each control that was supposed to exist, state whether the
  incident is POSSIBLE or IMPOSSIBLE with it enforced. The combination that is possible
  is the state the system was actually in.
**Finding** — the ENFORCED control that, if present, would have made this IMPOSSIBLE
**Not the finding** — the input, the person, and any control that would only have
  DETECTED it
**Change** — the typed parameter, the confirmation token or the permission, and the
  file it will live in
**Record** — the record number, and the autonomy level that drops as a result
**Verify** — the test QA re-runs, and what "stopped twice over" means here

RULES:
- Do not name a person. Do not name the input that triggered it.
- "A better prompt" is NOT a control. A prompt is a request a model can be talked past.
  If your finding is a prompt change, you have not found the control yet.
- Classify every layer that was supposed to help as ENFORCED, A REQUEST, or ABSENT, and
  be honest about the ones that were written down only in the prompt.
- Separate detection from prevention and say which yours is. An alert tells you
  afterwards; a cap makes it impossible.

INCIDENT:
<paste the trace and the postmortem notes>"""},
   {"title": "Extract a rule sheet from a legacy module",
    "when": "A team lead wants to feed the whole codebase to the agent",
    "body": """Extract a rule sheet from this legacy module, so an agent can read the intent
instead of the code.

OUTPUT SHAPE, one table:
| rule_id | Condition | Action | Source (file:line) | Confidence 0-1 |

RULES:
- One row per business rule. A rule is a condition and an action, not a code path.
- Every row cites a file and a line. A rule with no source cannot be verified and must
  not be written down.
- Confidence is your honest reading of whether the code does what the row claims.
  Anything below 0.9 goes to a person before it goes anywhere near the agent; mark
  those rows clearly.
- Where a comment and the code disagree, follow the CODE and say so in the row. Low
  confidence usually means the code does something the comments deny.
- Do not modify any code and do not propose a refactor.

Then, separately:
- A migration score for this module out of 25: risk, documentation, coupling,
  reversibility, and how much it teaches. Say where it falls in the order, and confirm
  that anything touching payments is last.
- The clean interface this module should sit behind before the agent touches it.

MODULE: <path>"""},
 ],
 "example": {
   "title": "SkyWays · day 75 and day 82",
   "body": "Two numbers from the same fortnight, and two different kinds of design change. On **day "
           "75 the bill was 4.4 times its estimate** with traffic flat, which meant behaviour had "
           "changed and behaviour is only visible per call. The four ratios explained it exactly: "
           "tokens per call 1.6, frontier share 1.5, cache hit ratio 1.3, retries 1.41, and 1.6 × "
           "1.5 × 1.3 × 1.41 = 4.40. Four habits, each a sensible decision made by a careful person. "
           "It had started with an engineer reordering a prompt for clarity and moving the "
           "passenger's request to the front, which changed the prefix on every call and left "
           "caching switched on and never hitting. The fix order came from (factor − 1) ÷ days, "
           "which put the context trim first and the retry breaker last — the breaker being the "
           "right fix in the wrong position. Then **day 82** and the $2,000 refund, which produced "
           "the other kind of change: not a ticket and not a name, but an ADR, a typed parameter and "
           "an autonomy level dropped by one. The cost-per-case NFR had been ratified on day nine at "
           "$0.60 and then never measured, which is how four weeks passed before anybody looked. The "
           "record was amended to make it a monitored number with a named owner and an alert at "
           "three times."},
 "pitfalls": [
   "Turning caching on without counting the reuse. Below two uses of the same prefix it costs more "
   "than it saves, and the configuration file will still report that caching is enabled.",
   "A latency alert that flags cache hits as suspected failures. It reports hundreds of them, "
   "somebody proposes switching the cache off, and the bill rises by about a third within a day "
   "because the anomaly was the cache working.",
   "A postmortem that ends in a name, or in a better prompt. Neither is a control, and the next "
   "incident of the same class is already scheduled.",
 ],
 "done_when": "The second call on a live prompt reports cache tokens read, a runaway loop stops at "
              "five, a passport number never reaches a trace row, and your last incident produced a "
              "typed parameter rather than a name.",
},
]
