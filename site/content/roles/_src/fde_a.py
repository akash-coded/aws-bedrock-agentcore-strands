"""Forward-deployed engineer · the HEAD, and Frame: steps 1 to 4. Imported by build_content.py.

A staged role. HEAD["stages"] names the three stages, and each step carries what a staged role needs
beyond the five roles' format: "stage", "level", "hats", "internal", "say", "question" and
"artifact.short". In prose, {{S7-scope}} puts a dated quotation from fde_sources.py on the page and
[[S26]] cites a source without quoting it; nobody's words are typed here in quotation marks.

The case: you are the FDE, from a vendor or from SkyWays' own central AI team. Frame is the three weeks
before the project's day 1, so its numbers are illustrative and agree with the canon: one week's 234 a
day becomes the project's 240, 22 codeshare cases in 200 is its 11%, and every lower bound uses the
site's rule (normal approximation; Wilson under 100 cases).
"""

HEAD = {
    "id": "forward-deployed-engineer",
    "name": "Forward-deployed engineer",
    "short": "FDE",
    "accent": "#1E7FA8",          # --dg-sky, the colour of the FDE row on the home page since council 3
    "tagline": "From a customer's pain to a system they run after you leave",
    "arc": ["Qualify", "Scope", "Prove", "Decide",
            "Mobilise", "Sign", "Build", "Hand over",
            "Reframe", "Codify", "Reuse", "Review"],
    # The three stages spell the role. Each runs the manual's four phases on its own object, and ends
    # in a signature that opens the next. "people" is what the customer's own staff do in that stage;
    # "brief" is the stage page's five-row table (how long, the client's people, you think at, it ends
    # with, what goes wrong here).
    "stages": [
        {"id": "frame", "name": "Frame", "object": "the engagement",
         "question": "Should we do this, and what exactly will we prove?",
         "span": "Days", "people": "The client's people watch.",
         "signed": "the go decision", "signer": "the client's sponsor",
         "brief": {
             "long": "Days to three weeks, before a contract or a charter",
             "people": "Watch, answer, and label a sample. Their sponsor decides",
             "think": "One question. The proof is a POC: throwaway code, real cases",
             "ends": "The go decision, signed by the client's sponsor",
             "wrong": "The demo becomes the success criterion. Nobody owns the risk. Nobody will run it "
                      "after you"}},
        {"id": "deliver", "name": "Deliver", "object": "the system",
         "question": "Does it work in their world, and can they run it without you?",
         "span": "Weeks", "people": "The client's people build with you.",
         "signed": "the handover", "signer": "the person who will run it",
         "brief": {
             "long": "Weeks. At SkyWays, days 1 to 97",
             "people": "Build with you. Their engineers pair, their experts label, their risk owner signs",
             "think": "One slice (MVP), then every slice (build), then the organisation (deploy)",
             "ends": "The handover, signed by the person who will run it",
             "wrong": "A limit that lives only in a prompt. A harness that comments instead of blocking. "
                      "Leaving with nobody owning it"}},
        {"id": "evolve", "name": "Evolve", "object": "the relationship",
         "question": "What did it teach them and us, and what comes next?",
         "span": "Months", "people": "The client's people run it.",
         "signed": "the next frame, or a clean close", "signer": "the client's sponsor",
         "brief": {
             "long": "Months, for as long as the system runs",
             "people": "Run it. You meet their sponsor each quarter",
             "think": "The portfolio: their next frame and your product's next pattern",
             "ends": "The next frame, or a clean close, signed by the client's sponsor",
             "wrong": "The fourth bespoke copy. The review nobody holds. The champion who left"}},
    ],
    "intro": [
        "You are an engineer who works inside someone else's organisation and owns the outcome there. "
        "That runs from the first question, through a system in production, to what the next customer "
        "inherits from this one. Some weeks you are the whole team. Every week, the decisions that carry their "
        "risk stay theirs.",
        "The guide runs in three stages that spell the role: **Frame**, **Deliver** and **Evolve**. Each asks the manual's "
        "four questions, P0 to P3, about a different thing: the engagement, the system, the relationship. "
        "Each ends in a signature, and the signature opens the next stage.",
        "Twelve steps. Each ends in an artefact somebody signs or inherits, with the template to write "
        "it, the prompts to draft it, and the words to say when the conversation gets hard.",
    ],
    "owns": [
        "The **engagement's spec**: the statement of work, its first slice and its success criteria",
        "Every **lead-time item**, filed on day one and chased by name",
        "The **build** in their stack, and the harness that proves it in their pipeline",
        "The **handover**: runbooks, timed switches, and the person on their side who will run it, accepting in writing",
        "The **pattern log**, and the write-up that takes each repeat home",
        "The **quarterly value review**, the saving beside the spend",
    ],
    "not_yours": [
        "**Their limits**: the refund cap, the autonomy of each action, who approves above a cap",
        "**Their pass mark**: what counts as a right answer is their experts' call",
        "**Go-live and every widening**: you bring the evidence, they decide",
        "**Whether your pattern becomes product**: the product owner or the FDPM decides",
    ],
    "ai_stance": (
        "Use a model to go faster through the work that is yours, and never through a decision that is "
        "theirs. At a customer the tools work differently: you are in their repository, under their "
        "policy, often on their cloud account. One context file in their repository, read by both Claude "
        "Code and Codex, keeps the rules in one place. Their documents are untrusted input to your agent, "
        "and their data goes only into the tools their policy approves. Where a step below says *do not "
        "delegate*, the model has no standing to decide, and neither, often, do you."
    ),
    "reads": [
        ["The lesson: what is an FDE?", "../learn/what-is-a-forward-deployed-engineer/"],
        ["The Deliver stage in depth, with AI-DLC and AIDD", "../learn/ai-dlc-for-forward-deployed-engineers/"],
        ["Ten FDE interview questions, by stage", "../learn/forward-deployed-engineer-interview-questions/"],
    ],
}

STEPS_A = [
{
 "n": 1, "id": "qualify", "phase": "Qualify", "stage": "frame", "level": None,
 "hats": ["consultant", "product"],
 "question": "Is this engagement worth taking?",
 "title": "Find the pain, the owner and a reason to say no",
 "when": "The first week of a lead, before anyone promises a proof",
 "purpose": (
   "Three things sink an engagement before it starts: no pain anyone can measure, nobody who can "
   "accept the risk, and nobody to run the system after you leave. Each can be found in days, from "
   "their data and their people, before a proof makes the work feel agreed. The brief this step "
   "writes is allowed to say no, and it is worth most on the day it does."),
 "activities": [
   {"do": "Get the ask in their words, then the last time it hurt",
    "detail": "The ask is usually a solution: *an AI assistant*. Ask who was waiting, and for how long, "
              "the last time it went badly; then what has been tried before, and what another team is "
              "trying now. Write the answers down in their words. Scale says its best forward-deployed "
              "product managers {{S19-difference}}."},
   {"do": "Measure it from one export",
    "detail": "A week of tickets gives the volume, the hard cases' share and the wait. That is enough to "
              "qualify and not enough to size, so the brief says which, and no number from it goes "
              "into a contract."},
   {"do": "Ask the three AI-fit questions",
    "detail": "A genuine judgement call, the volume to carry evaluation, and, action by action, whether a "
              "wrong answer can be undone: [the product manager's step 2](../../product-manager/#qualify). "
              "A rule in disguise is a cheaper engagement, or none."},
   {"do": "Map five people, by name",
    "detail": "The sponsor who pays, the risk owner who signs the risk, the person who will run it after "
              "you, the expert whose staff label the cases, and the sceptic who can stop it. Ask the "
              "experts what changes by shift or by kind of case: the rules nobody wrote down live there. "
              "Meet the sceptic early: their objection is your best success criterion."},
   {"do": "Check the three disqualifiers",
    "detail": "No path for their data to a model inside their policy and region. No one who can sign the "
              "risk. No one to run it after you. One left open is a no, or a not yet with the condition "
              "that clears it."},
   {"do": "Write the verdict, and what would change it",
    "detail": "Go to scoping, not yet, or no, in one sentence with its evidence. Stopping at discovery "
              "is not a failure when the evidence says stop [[S26b]], and a written no keeps the door "
              "open for a later yes."},
 ],
 "internal": (
   "Inside your company the sponsor is often your manager's peer. The disqualifiers are the same, and "
   "saying no is harder, so write them down before the meeting. Send them to your own manager first, "
   "so the no belongs to the team and not to you alone."),
 "say": [
   {"to": "When the first meeting opens on the solution",
    "words": "We will get to the assistant. First, walk me through the last disruption that went badly: "
             "who was waiting, and for how long?"},
   {"to": "When three of the five people have no name",
    "words": "We can start when three people are named: who signs the risk, who runs it after we "
             "leave, and whose experts label the cases."},
   {"to": "When the answer is no, or not yet",
    "words": "I would not build this yet. Here is what would change my mind, and who can make it "
             "happen."},
 ],
 "ai": [
   {"tool": "Chat model",
    "use": "Give it the request and the account team's notes, and ask for the first meeting's "
           "questions, ordered by which answer could end the engagement.",
    "caution": "Strike every question that assumes the assistant exists. It asks about the solution, "
               "because the request was about the solution."},
   {"tool": "Claude Code or Codex",
    "use": "Have it count the export: cases a day, the hard cases' share, the wait, with the script "
           "shown before the numbers.",
    "caution": "Only on an export their policy lets you take out. Read the date column and the filter: "
               "a count over the wrong column is confidently wrong."},
   {"tool": "Chat model, against you",
    "use": "Ask for the strongest case against taking the engagement, from your own notes. It is the "
           "cheapest review the verdict will get.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The names, and the verdict. Whether a person can accept the risk, or will run the system, "
           "you learn by asking them; a model reading an org chart guesses.",
    "caution": None},
 ],
 "artifact": {
   "name": "Discovery brief",
   "short": "Discovery brief",
   "good": "Two pages at most: the ask in their words, the pain with its source, three AI-fit answers, "
           "five people each named or marked unknown with who was asked, the three disqualifiers, and "
           "a verdict with what would change it.",
   "owner": "Forward-deployed engineer, with the account or engagement lead"},
 "template": {
   "title": "Discovery brief", "lang": "markdown",
   "body": """# Discovery brief · <customer> · <the ask, in five words>
_<date> · Drafted by <FDE> · For <engagement lead> · Verdict: go to scoping / not yet / no_

## 1. The ask, in their words
> "<the request, verbatim>" (<who said it>, <date>)

The last time it hurt: <the incident, dated, told by someone who was there>

## 2. The pain, measured
| Who has it | How often | Cost today | Evidence | Window |
|------------|-----------|------------|----------|--------|
| <role> | <n a day> | <minutes, or $ per case> | <export, system, owner> | <dates> |

Enough to qualify, not to size. No number here goes into a contract.

## 3. Is it AI at all?
| Question | Answer | Why |
|----------|--------|-----|
| A genuine judgement call? | yes / no | <two competent people could differ about ...> |
| Volume to carry evaluation and gates? | yes / no | <n a day> |
| Can a wrong answer be undone? | yes / no / partly | <the actions that cannot> |

## 4. Five people
| Part | Name, role | Wants | Fears | Can stop it? |
|------|------------|-------|-------|--------------|
| Sponsor: pays, decides go | | | | |
| Risk owner: signs the risk | | | | |
| The person who will run it | | | | |
| Expert: their staff label the cases | | | | |
| Sceptic: can stop it | | | | |

A blank is a finding. Write down who you asked.

## 5. The three disqualifiers
| Disqualifier | Open or cleared | Evidence | What clears it |
|--------------|-----------------|----------|----------------|
| No path for their data to a model, inside their policy and region | | | |
| No one who can sign the risk | | | |
| No one to run it after you | | | |

## 6. Verdict
**Go to scoping / not yet / no**, because <one sentence>.
Conditions: <condition> · <owner> · <date>
What would change the answer: <the evidence, and who holds it>
"""},
 "prompts": [
   {"title": "Turn the request into the first meeting's questions",
    "when": "Before the first meeting, with whatever the account team sent you",
    "body": """A customer has asked for: "<the request, verbatim>".
What we know so far: <paste the account team's notes>

Write the questions for a first 45-minute meeting with <who will be there>.

RULES:
- No question may assume the solution. Ask about the work and the pain, never the assistant.
- Ask for the last time it went badly: who was waiting, for how long, what it cost.
- Find five people: who pays, who signs the risk, who will run it after us, whose experts
  can label cases, who could stop it. Ask for names; a title is not an answer.
- Ask what data exists, who owns it, and where it is allowed to go.
- Order the questions by which answer could end the engagement. Those come first.

OUTPUT: the questions in order, each with one line on why it is there."""},
   {"title": "Draw the stakeholder map from your notes, and mark what you do not know",
    "when": "After the first two meetings",
    "body": """Below are my notes from <n> meetings at <customer>.

Fill in this map:
| Part | Name and role | Wants | Fears | Can stop it? | Where in my notes |

The five parts: sponsor (pays, decides go) · risk owner (signs the risk) · the person who
will run it after us · expert (whose staff label the cases) · sceptic (can stop it).

RULES:
- Never infer a name from a title. If my notes name nobody, write UNKNOWN.
- Wants and fears only from what was said or done, with the line it came from.
- If one person holds two parts, say so: that is a risk, not a saving.
- After the table, list every UNKNOWN with the question that fills it and who to ask.

NOTES:
<paste>"""},
   {"title": "Make the case against taking this engagement",
    "when": "Before you write the verdict",
    "body": """Here is my draft discovery brief: <paste>.

Make the strongest case that we should say no, or not yet. Use only the brief's own
evidence, and test it against three disqualifiers:
1. no path for their data to a model, inside their policy and region;
2. no one who can sign the risk of the actions the system would take;
3. no one to run it after we leave.

Then the AI-fit questions: is it a genuine judgement call, is the volume enough to carry
evaluation and gates, can a wrong answer be undone?

End with the one piece of evidence that would settle go or no, and who holds it.
Do not soften the case to be polite."""},
 ],
 "example": {
   "title": "SkyWays · three weeks before day 1",
   "body": "The ask was *make rebooking smarter*. One week's export held 1,640 disruption tickets: about "
           "234 a day, roughly one in ten codeshare, an average wait near 40 minutes. Enough to qualify, "
           "not to size: the project's own measurement in its first days made it 240 a day, 11% and 38 "
           "minutes. AI fit: yes, yes and partly, because a proposed rebooking can be withdrawn and a "
           "cash refund cannot. Three of the five were named that week: Ines as sponsor, the contact-centre "
           "head over the experts, Lena as the person who would run it. The risk owner was not, so the "
           "verdict read *go to scoping, once compliance names a person for refunds*. One gap went "
           "unseen. Every expert in the brief worked the day shift, and the evening shift's rule about "
           "one partner after 18:00 stayed in six people's heads until the shadow run found it "
           "([step 7](../deliver/#build))."},
 "pitfalls": [
   "Qualifying on the sponsor's enthusiasm. A sponsor who wants it and a risk owner nobody has met is "
   "how a proof ends as a demo and a contract ends in week six.",
   "Putting the qualifying number in the contract. One week's export says yes to scoping; quoted as "
   "the business case, it becomes a promise the real measurement breaks.",
   "Saying yes to protect the relationship. A no with its reason, and the condition that would change "
   "it, keeps the relationship; a proof that was never going to pass ends it.",
 ],
 "done_when": "A colleague who was not in the meetings can read the brief and say whether to take the "
              "work, and what would change the answer.",
},
{
 "n": 2, "id": "scope", "phase": "Scope", "stage": "frame", "level": None,
 "hats": ["consultant", "product"],
 "question": "What will we prove, and who signs?",
 "title": "Write the statement of work a sceptic would sign",
 "when": "Frame, after the discovery brief and before the proof starts",
 "purpose": (
   "A statement of work is the engagement's spec. It says what you will prove and deliver, by when, "
   "what the customer must supply, and which decisions stay theirs. Write it so that a sceptic in "
   "their procurement team and another in your own could each sign it without asking what a line "
   "means. Every vague line becomes an argument in week six, and every dependency you leave out "
   "becomes your delay. Anthropic's Technical Deployment Leads structure one with {{S7-scope}}; the "
   "template below adds the decisions that stay theirs, and change control."),
 "activities": [
   {"do": "Name the first slice, and say why it comes first",
    "detail": "One kind of case, chosen for proof: high volume, low damage per mistake, and an existing "
              "process to compare against. Write the reason beside it, so the slice is not argued again "
              "in every meeting."},
   {"do": "Write success as numbers, each with an owner on their side",
    "detail": "A measure, the cases it is measured on, the threshold, the person who measures it and the "
              "date. *Faster rebooking* is not a criterion. *The desk agrees with the first option on 80% "
              "of standard cases, as a lower bound on 500 of their past cases* is."},
   {"do": "List what is out, and what is not yet",
    "detail": "Out stays out. Not yet has the condition that brings it in, such as a limit compliance has "
              "not signed. Both lists stop the same request arriving every week."},
   {"do": "Write their dependencies with names and dates",
    "detail": "Data access, model access in the region their data must stay in, the security review, the "
              "hours their experts will spend labelling, the person who signs risk. Their delays are your "
              "delays, so the statement says what happens to the plan when one slips."},
   {"do": "Write down which decisions stay theirs",
    "detail": "The autonomy of each action, every limit and who approves above it, the pass mark for each "
              "kind of case, go-live, and who runs it afterwards. You draft them; they sign them. Writing "
              "it now makes it normal later."},
   {"do": "Put the proof in, with its own way to fail",
    "detail": "Its one question, its days, and its endings: go, go with conditions, change course, or "
              "stop. A proof that cannot end in stop is a demo, and their sceptic will know it."},
   {"do": "Agree how a new ask gets in",
    "detail": "Change control in one paragraph: who may ask, who sizes it in days, who signs. Without it, "
              "every yes you give in a corridor is a promise the plan cannot keep."},
 ],
 "internal": (
   "Inside your own company the statement of work is a charter, and it is no softer. The business "
   "unit's head signs it, and the hours their experts give are written down as a commitment. The "
   "person who will run the system after you is named before you start. With no invoice to enforce "
   "it, the charter is the only thing that makes their side's work real."),
 "say": [
   {"to": "A feature that does not fit the first slice",
    "words": "That is a good second slice. It goes on the not-yet list with the condition that brings it "
             "in, so it is not lost and it does not slow the first."},
   {"to": "A date the scope cannot meet",
    "words": "We can meet that date with the first slice, or this scope by the end of the month. Which "
             "matters more to you?"},
   {"to": "A decision that is theirs",
    "words": "I will draft the refund limit with the numbers beside it. Your compliance officer signs it, "
             "because it is your risk."},
 ],
 "ai": [
   {"tool": "Chat model, as their procurement",
    "use": "Paste the redacted draft and have it read the statement twice, as their head of procurement "
           "and as their security lead, listing every line each would refuse to sign and the wording each "
           "would accept.",
    "caution": "Paste only what their contract and your policy allow. A customer's confidential terms do "
               "not go into a tool nobody approved."},
   {"tool": "Chat model, as your delivery lead",
    "use": "Give it the phases and the work in each, and ask for every dependency on the customer the "
           "plan assumes and does not name, longest lead time first.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The numbers in the success criteria, and the list of decisions that stay theirs. A model writes "
           "criteria that sound measurable and are not, and it cannot know which risks this customer "
           "may hand to you.",
    "caution": None},
 ],
 "artifact": {
   "name": "Statement of work (inside your own company, an engagement charter)",
   "short": "Statement of work",
   "good": "Two pages. A first slice with its reason, success criteria a stranger could measure, their "
           "dependencies with names and dates, the decisions that stay theirs, the proof with its way to "
           "fail, and one paragraph of change control. Signed by their sponsor and by yours.",
   "owner": "Forward-deployed engineer, with the engagement lead where there is one"},
 "template": {
   "title": "Statement of work", "lang": "markdown",
   "body": """# Statement of work · <customer> · <engagement>
_Version <n> · <date> · Drafted by <FDE> · For signature by <their sponsor> and <your lead>_

## 1. The problem, measured
<who has the pain> · <how often> · <what it costs today> · <the evidence, with its source>

## 2. The first slice
**In:** <one kind of case>
**Why first:** <n> a day · <what one mistake costs> · compared against <their current process>

## 3. Value hypothesis
| Measure | Today | Target | Measured by | Baseline from |
|---------|-------|--------|-------------|---------------|
| <handling time per case> | <n min> | <n min> | <their ops lead> | <export, date> |

## 4. Success criteria
| # | Criterion | Cases it is measured on | Who measures | By |
|---|-----------|-------------------------|--------------|----|
| 1 | <lower bound of agreement with their desk, per slice, at or above the pass mark> | <n of their past cases, labelled by their experts> | <name> | <date> |

## 5. Phases
| Phase | The one question | Ends with | Date |
|-------|------------------|-----------|------|
| Proof, <n> days | <can it ...?> | go · go with conditions · change course · stop | <date> |
| First slice, in shadow | <does it agree with their staff?> | shadow report | <date> |
| Cut-over and handover | <does it run without us?> | handover signed by the person who will run it | <date> |

## 6. What we need from you
| Dependency | Owner on your side | Needed by | How we know it works | If it is late |
|------------|--------------------|-----------|----------------------|---------------|
| Read access to <system> | <name> | <date> | <one record read, logged> | the plan moves by the same days |
| Model access in <the region your data must stay in> | <name> | <date> | <one call from that region, logged> | |
| Security review | <name> | <date> | <the signed review> | |
| <n> hours of expert labelling | <name> | <date> | <the first 50 cases labelled> | |
| A named owner for each consequential action | <name> | <date> | <a signature in section 7> | nothing is built past it |

A dependency is met when its test passes, not when someone says it is done.

## 7. Decisions that stay yours
| Decision | We draft it | You sign it | Signed by |
|----------|-------------|-------------|-----------|
| Autonomy of each action | yes | yes | <name> |
| Every limit, and who approves above it | yes | yes | <name> |
| The pass mark for each kind of case | yes | yes | <name> |
| Go-live, and each widening | no | yes | <name> |
| Who runs it after handover | no | yes | <name> |

Every limit you sign is enforced in the tool that acts, with a test, never only in the
instructions the model reads.

## 8. Out, and not yet
- **Out:** <...>
- **Not yet:** <...>, which comes in when <condition>

## 9. Change control
A new request is written down, sized in days by <FDE>, and signed by <their sponsor> before
work starts. A request that changes a decision in section 7 goes back to whoever signed it.

## 10. Signatures
| For <customer> | For <us> |
|----------------|----------|
| <name, role, date> | <name, role, date> |
"""},
 "prompts": [
   {"title": "Red-team the statement as their procurement and their security lead",
    "when": "Before the draft leaves your hands",
    "body": """Below is a draft statement of work for an AI deployment at <customer>.

Read it twice: first as their head of procurement, then as their chief information
security officer.

For each reading, give a table:
| Section | The line | Why you would refuse to sign it | The wording you would accept |

Then list, separately:
- every success criterion a stranger could not measure from the text alone;
- every dependency on the customer the plan assumes and does not name;
- every decision the vendor appears to make that the customer should sign.

Do not rewrite the statement. Do not soften a finding to be polite.

DRAFT (names, prices and confidential terms removed):
<paste>"""},
   {"title": "Turn the outcomes they described into criteria someone can measure",
    "when": "You have adjectives and need numbers",
    "body": """The customer described what success looks like, in their words:
<paste their words>

For each outcome, write a success criterion with five parts:
1. the measure: a count, a rate or a time;
2. the cases it is measured on: which, how many, labelled by whom;
3. the threshold, and whether it applies to the score or to its lower bound;
4. the person on the customer's side who measures it;
5. the date.

If an outcome cannot be measured inside this engagement, say so, and propose the nearest
measure that can. Mark every number you had to assume as ASSUMED. Never invent a baseline."""},
   {"title": "Find the dependencies the plan hides",
    "when": "Before the dependency table is final",
    "body": """Here is our delivery plan for <customer>: <paste the phases and the work in each>.

List everything this plan needs from the customer that it does not name: access, data,
people's time, approvals, environments and decisions. For each, give:
| What we need | Who on their side usually owns it | The latest week we can have it without moving the plan | What we do if it is late |

Order the list by how long each usually takes to obtain, longest first. Data access, model
access in the region their data must stay in, and the security review usually lead."""},
 ],
 "example": {
   "title": "SkyWays · two weeks before day 1",
   "body": "The sponsor, Ines, asked the vendor to *make rebooking smarter*. The statement she signed, "
           "before the proof began, was two pages. The first slice was rebooking options for the 89% of "
           "disruption cases that are not codeshare. A wrong option there costs a passenger a worse "
           "flight, not money, and the desk's own choices give a baseline. Codeshare became its own "
           "slice with its own pass mark. Refunds went on the not-yet list, drafted for a person to "
           "approve until compliance signed a limit; on day 6 it signed the first decision in section 7, "
           "a named approver for every refund over $400. The line that mattered most was in section 6: "
           "model access in the region the passengers' data must stay in, by day 5. It was met on paper. "
           "Access came in week one in the wrong region, nobody made one call to check it until day 13, "
           "and six days went ([step 5](../deliver/#mobilise))."},
 "pitfalls": [
   "A success criterion with an adjective in it. *Accurate* and *fast* are signed happily in week one "
   "and argued about in week six.",
   "Leaving the customer's dependencies out to keep the statement short. The plan then rests on things "
   "nobody promised, and the delay lands on you.",
   "Taking a decision that is theirs because it unblocks you today. A limit you chose becomes your risk "
   "on the day it is wrong.",
   "A proof that can only end in go. If it cannot fail, it is a demo, and their sceptic will say so.",
 ],
 "done_when": "Their procurement lead and your delivery lead can each read it cold and name the first "
              "slice, the go date, what they supply by when, and which decisions are theirs.",
},
{
 "n": 3, "id": "prove", "phase": "Prove", "stage": "frame", "level": "POC",
 "hats": ["engineer", "qa"],
 "question": "Does it work on their data?",
 "title": "Prove it on their cases in days, and write what it does not prove",
 "when": "Frame, in the days after the statement is signed, and never for weeks",
 "purpose": (
   "A proof answers one question on their data. It is not a small product, and its code is not the "
   "first commit of one. Measure on their real cases with the sample size beside every number, and "
   "write down what it does not prove: that list is what their sceptic reads, and it is what stops a "
   "good score being taken for a decision to build."),
 "activities": [
   {"do": "Write the question in one sentence",
    "detail": "*Can it rank the desk's own choice first, on their past cases?* One question a number can "
              "answer, and beside it, before a case is scored, the result that would mean stop. A "
              "question with *and* in it is two proofs, and in days you finish neither."},
   {"do": "Take a real sample, with the hard slice in it",
    "detail": "A couple of hundred recent cases from their export, redacted under their policy, the hard "
              "slice at its real share or more. Never invented cases: nobody invents the mess they have "
              "not read."},
   {"do": "Have two of their experts label it, blind",
    "detail": "Each alone, with no answer from the system on screen, because an expert who can see an "
              "answer agrees with it. Where the two agree is the ceiling: no score above it means "
              "anything."},
   {"do": "Build the thinnest thing, in a sandbox",
    "detail": "In GOV.UK's words for a prototype, {{S26-complex}}. A coding agent writes most of it; log "
              "the tokens and seconds of every case, because the readout's cost line comes from them. "
              "Read the scorer line by line: one that counts an abstention as right is how a proof lies."},
   {"do": "Put their people at the keyboard",
    "detail": "Palantir's bootcamp is the public model: {{S14-five-days}}. An afternoon of their staff "
              "working their own cases tells you more about adoption than the score does."},
   {"do": "Measure by slice, with the lower bound",
    "detail": "Score, cases and lower bound on one row per slice, Wilson under a hundred cases, as "
              "[the QA lead measures](../../qa/#measure). A slice of twenty cases proves nothing, and "
              "the sheet says so."},
   {"do": "Read twenty failures, then write what it does not prove",
    "detail": "Group the failures by cause: missing data, a rule nobody wrote down, a call the experts "
              "split on. Then the list: volume, latency, cost, their live systems, any action, the "
              "slices it never saw."},
 ],
 "internal": (
   "Inside your company the proof is skipped because people trust each other. Run it anyway: it is "
   "the only evidence the business unit's head will have before they commit their experts' hours."),
 "say": [
   {"to": "When the proof is agreed",
    "words": "This proof answers one question: can it rank the desk's own choice first, on your past "
             "cases. It does not tell you whether it is safe to let it act."},
   {"to": "When they ask for one more thing in the proof",
    "words": "That belongs in the build. If I add it here, the proof stops answering anything in days."},
   {"to": "When a slice is too small to read",
    "words": "Twenty-two cases cannot tell us whether codeshare works. They tell us it needs its own "
             "cases before anyone judges it."},
 ],
 "ai": [
   {"tool": "Claude Code or Codex",
    "use": "Let it write the loader, the redaction and the scoring by slice from your one-sentence "
           "question. Throwaway code against a fixed question is what these tools do best.",
    "caution": "Read the scorer line by line. It counts a partial match or an abstention as right unless "
               "told not to, and that one line is the whole proof."},
   {"tool": "Chat model",
    "use": "Give it the twenty failures with the experts' labels, and ask for groups by cause, each with "
           "its cases' ids.",
    "caution": "It groups by wording. Re-read each group asking what would fix it: two different fixes "
               "means two groups."},
   {"tool": "Chat model, as their sceptic",
    "use": "Paste the finished sheet and ask what a sceptic would conclude that the proof does not "
           "support. Each answer goes into section 5.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The labels. A model that labels its own test cases measures its agreement with itself, and "
           "the number looks exactly like a proof.",
    "caution": None},
 ],
 "artifact": {
   "name": "Proof-of-concept sheet",
   "short": "Proof-of-concept sheet",
   "good": "One page their sceptic can check: the question, the sample and who labelled it, the experts' "
           "ceiling, results by slice with lower bounds, twenty failures by cause, what it does not "
           "prove, and the date the code is deleted.",
   "owner": "Forward-deployed engineer, with their experts' lead"},
 "template": {
   "title": "Proof-of-concept sheet", "lang": "markdown",
   "body": """# Proof-of-concept sheet · <customer> · <the question, in five words>
_<dates> · Built by <FDE> · Sent to <their sceptic> before the readout_

## 1. The question
Can <the system> <do what> on <their cases>, as well as <their staff>?
One question. A question with "and" in it is two proofs.

## 2. The sample
| Source | Window | Cases | Redacted by | Labelled by | Blind? |
|--------|--------|-------|-------------|-------------|--------|
| <export> | <dates> | <n> | <who> | <two experts, by role> | yes |

The mix: <slice> <n> (<share>) · <slice> <n> (<share>)
The ceiling: the experts agreed on <n> of <n> (<%>). No score above it means anything.

## 3. Results, by slice
| Slice | Right | Of | Score | Lower bound |
|-------|-------|----|-------|-------------|
| All | | | | |
| <standard> | | | | |
| <the hard slice> | | | | <low> to <high>, Wilson |

Lower bound = p − 1.96 × √(p(1 − p) ÷ n). Under 100 cases, Wilson.

## 4. Twenty failures, read by hand
| Group | Cases | One example | Cause | Fixable in the build? |
|-------|-------|-------------|-------|-----------------------|
| | | | | |

## 5. What this does not prove
- Latency and cost at <n> cases a day, in the peak hour
- Their live systems: it read an export, not <system>
- Model access in <the region their data must stay in>: the sandbox ran in <where>
- Security, and their data policy beyond the sandbox
- Any action: it proposed, it never <acted>
- Slices not in the sample: <list>

## 6. What happens to it
Code: deleted from <sandbox> on <date>.
Labelled cases: handed to <their QA lead> on <date>, under <their policy>.
"""},
 "prompts": [
   {"title": "Check my sample against their real mix",
    "when": "Before anyone labels a case",
    "body": """Here is a sample drawn for a proof of concept, and the export it came from.
SAMPLE: <counts by slice, weekday, hour and type>
EXPORT: <the same counts for the whole export>

Report:
| Dimension | Export share | Sample share | Gap | Does it matter? |

Then list:
- every slice under 30 cases, with the width of its 95% interval at a likely score
  and how many cases it would need to be judged at all;
- anything the export holds that the sample lacks entirely (a type, an hour, a season);
- whether the window is recent enough to reflect how the work is done today.

Do not redraw the sample. Tell me what is wrong with it."""},
   {"title": "List what this proof does not prove",
    "when": "Before the sheet goes to their sceptic",
    "body": """This proof answered one question: <the question>.
Setup: <the sample, the sandbox, what the system could see and do, what it never did>.
Results: <the table, by slice>.

List every conclusion a reader might draw that this proof does NOT support. Cover at
least: volume and peak latency, cost at their volume, their live systems, security and
data handling, any action the system would take, slices not in the sample, and whether
the experts' own agreement caps the score.

| The tempting conclusion | Why the proof cannot support it | What would, and when |

Write it for a sceptic: plain words, no reassurance."""},
   {"title": "Group twenty failures by cause",
    "when": "After scoring, before the readout",
    "body": """Below are 20 cases the system got wrong, each with the case, the experts' label,
the system's answer and its reasoning.
<paste>

Group them by CAUSE, not by symptom: missing data, a rule nobody wrote down, a call the
experts themselves split on, retrieval that found the wrong record, an instruction the
system ignored.

| Cause | Cases (ids) | One example, in a line | Fixable in the build, or inherent? |

RULES: a case goes in one group only. If a group would need two different fixes, it is
two groups. Finish with the cause you would fix first, and why."""},
 ],
 "example": {
   "title": "SkyWays · twelve to eight days before day 1",
   "body": "200 past cases from the Q2 export, redacted, 22 of them codeshare. Two frontline agents "
           "labelled them. The first fifty were labelled with the assistant's answer on screen, so they "
           "were set aside and fifty fresh cases drawn: an expert who has seen an answer remembers it. "
           "Blind, the two agreed on 184 (92%), the ceiling, and the contact-centre head settled the "
           "other 16. The assistant's first option matched the label on "
           "151 (75.5%, lower bound 69.5%); on standard cases, 142 of 178 (79.8%, lower bound 73.9%); "
           "on codeshare, 9 of 22, somewhere between 23% and 61%. The most useful number was the "
           "widest: twenty-two cases could say only that codeshare needed many more of its own before "
           "anyone judged it."},
 "pitfalls": [
   "A proof built like a product, or kept like one. Hardening eats the days the question had, and "
   "later someone copies its logic into the build because it worked: a path nobody designed is in "
   "production.",
   "Invented cases. Nobody invents the mess they have not read, so the hard slice is missing and the "
   "score is high for the wrong reason.",
   "One number for the whole sample. The easy cases carry the average, and the slice that holds the "
   "risk stays invisible until it is live.",
 ],
 "done_when": "Their sceptic can read the sheet cold and agree with its one number, its ceiling and its "
              "list of what it does not prove.",
},
{
 "n": 4, "id": "decide", "phase": "Decide", "stage": "frame", "level": None,
 "hats": ["consultant"],
 "question": "Go, at what cost, on what conditions?",
 "title": "Read the proof out with the failures first, and let them decide",
 "when": "The end of Frame, within a week of the proof",
 "purpose": (
   "A proof is worth what it changes. The readout turns it into a decision the client makes, on "
   "evidence, with the bad news first and the cost beside the saving. Lead with what failed and you "
   "keep the right to recommend; bury it and their sceptic finds it after the signature. The meeting "
   "ends in go, go with conditions, change course or stop, signed and dated, and never in *keep "
   "going*."),
 "activities": [
   {"do": "Send the sheet to their sceptic before the meeting",
    "detail": "Two days before, and walk their sponsor through the failures one to one. Bad news told "
              "early costs nothing; told first in the room, it costs the trust the decision needs."},
   {"do": "Open with what failed, by slice",
    "detail": "Score, cases and lower bound, the worst slice first. A room that hears the overall number "
              "first anchors on it, and reads the failing slice as a footnote."},
   {"do": "Cost it at their volume, review load included",
    "detail": "Tokens per case, the share a person checks and the minutes each check takes, at their "
              "cases a day, as [the product manager's value line](../../product-manager/#frame) does. "
              "The review load is the term most readouts leave out."},
   {"do": "Name the lead-time items, with dates",
    "detail": "Data access, model access in the region their data must stay in, the security review, "
              "the experts' hours. They set the build's calendar, so their owners hear them now."},
   {"do": "Recommend one of four, in one sentence",
    "detail": "Go, go with conditions, change course, or stop. Each condition gets an owner, a date and "
              "what happens if it is missed, or it is a hope written down."},
   {"do": "Get it signed, and hand it on",
    "detail": "The signed record is Deliver's first page: first slice, pass mark, milestones. At a larger "
              "vendor it passes between two people: Anthropic's pre-sales lead works beside "
              "{{S8-counterpart}}."},
   {"do": "Delete the code, and keep the cases",
    "detail": "The proof's code goes, as GOV.UK expects of a prototype [[S26]]. Its labelled cases go "
              "first, under their policy, to whoever will own the golden set, who confirms receipt "
              "before the sandbox is wiped: nobody labels the same cases twice."},
 ],
 "internal": (
   "Inside your company the readout is where a project quietly becomes permanent. Ask for a decision "
   "with a date, never for *keep going*. A business unit that says go is also giving its experts' "
   "hours, so write them into the decision."),
 "say": [
   {"to": "Opening the readout",
    "words": "Here is what did not work, first. Then what it costs at your volume, then what I "
             "recommend."},
   {"to": "The recommendation",
    "words": "My recommendation is go, with two conditions. Each has an owner and a date, and if one is "
             "missed, the decision comes back to this room."},
   {"to": "When the room wants to keep going without deciding",
    "words": "I can hold the team for this until Friday. By then I need go, go with conditions, change "
             "course or stop, so that we can both plan."},
 ],
 "ai": [
   {"tool": "Chat model",
    "use": "Draft the readout from the proof sheet in the fixed order, failures first, so the first "
           "draft already says the hard thing first.",
    "caution": "It softens. Delete every *promising* and *encouraging*, and put the number back where "
               "the adjective was."},
   {"tool": "Claude Code or Codex",
    "use": "Build the cost line as a small sheet, every assumption in a named cell, so their finance "
           "lead can change one and watch the net move.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The recommendation, and the sentence that says what would make it stop. A model recommends "
           "go, because everything in front of it is about going.",
    "caution": None},
 ],
 "artifact": {
   "name": "Readout and decision record",
   "short": "Readout and decision",
   "good": "One page read aloud and one page signed: the failures by slice, the cost at their volume, "
           "the lead-time items, one recommendation, each condition with an owner and a date, and the "
           "decision, dated. Deliver's plan starts from it.",
   "owner": "Forward-deployed engineer; the decision is the client's sponsor's"},
 "template": {
   "title": "Readout and decision", "lang": "markdown",
   "body": """# Readout and decision · <customer> · <the proof's question>
_<date> · Presented by <FDE> · Decided by <their sponsor> · Sheet sent to <their sceptic> on <date>_

## 1. What failed, first
| Slice | Score | Of | Lower bound | Pass mark | Why it failed |
|-------|-------|----|-------------|-----------|---------------|
| | | | | | |

## 2. What worked
| Slice | Score | Of | Lower bound | Pass mark |
|-------|-------|----|-------------|-----------|
| | | | | |

## 3. What it does not prove
<copied from the proof sheet, word for word>

## 4. What it costs at your volume
| Term | Per case | Per day at <n> cases | Assumption, and its source |
|------|----------|----------------------|----------------------------|
| Saving | | | <minutes saved × cost per minute> |
| Tokens | | | <from the proof's own runs> |
| Review load | | | <share checked × minutes per check> |
| **Net** | | | |

## 5. What takes longest to get
| Item | Owner on your side | Needed by | If it is late |
|------|--------------------|-----------|---------------|
| | | | |

## 6. Four options
| Option | What it means here | The evidence for it |
|--------|--------------------|---------------------|
| Go | | |
| Go with conditions | | |
| Change course | | |
| Stop | | |

**Recommendation:** <option>, because <one sentence>.

## 7. Conditions
| # | Condition | Owner | By | If it is not met |
|---|-----------|-------|----|------------------|
| 1 | | | | |

## 8. Decision
<go / go with conditions / change course / stop> · <name, role> · <date>

## 9. What the build starts with
First slice: <...> · Pass mark: <lower bound at or above <n>% on <n> cases> · First milestone: <...>
The proof's code: deleted on <date> · Its labelled cases: with <name> since <date>
"""},
 "prompts": [
   {"title": "Draft the readout, failures first",
    "when": "The day the proof sheet is final",
    "body": """Draft the readout of a proof of concept for <customer>'s sponsor.
The proof sheet: <paste>

ORDER, and do not change it:
1. What failed, by slice, each with its score, its n and its lower bound.
2. What worked, the same way.
3. What the proof does not prove, copied from the sheet.
4. What it costs at their volume, every assumption named.
5. The items with the longest lead time, each with an owner and a date.
6. Four options (go, go with conditions, change course, stop), each with its evidence.
7. One recommendation, and its conditions, each with an owner and a date.

RULES:
- Never open with the overall score.
- No adjective without a number, and no number without its n.
- Mark every figure you assumed rather than read as ASSUMED.
- One page. If it runs over, cut adjectives, never failures."""},
   {"title": "Cost it at their volume, with every assumption named",
    "when": "Before the readout, with the proof's own numbers",
    "body": """Work out what this system is worth at <customer>'s volume.

Inputs, each with its source:
- cases a day: <n> (<source>)
- minutes saved per case: <n> (<source>)
- loaded cost per minute: $<n> (<source>)
- token cost per case: $<n> (from the proof's own runs)
- share of cases a person checks: <n>% · minutes per check: <n>

Show the gross saving, the token cost, the review load and the net, each per day and per
year, with the arithmetic. Then name the ONE input that, moved by a plausible amount,
turns the net negative, and by how much it would have to move.

Mark any input I did not give you as ASSUMED. Never invent a baseline."""},
 ],
 "example": {
   "title": "SkyWays · three days before day 1",
   "body": "The readout opened on what failed: codeshare, 9 of 22 and somewhere between 23% and 61%, "
           "and standard cases whose lower bound, 73.9%, sat under the statement's 80%. Then the cost at "
           "their volume and the lead-time items, model access in the passengers' region first. The "
           "recommendation was go with two conditions: no launch on a score, so if the lower bound on "
           "500 of their cases fell short the shadow would run first; and the experts' hours to label "
           "those 500, committed by the contact-centre head. Ines signed both. On day 45 the first "
           "held: 82.4%, lower bound 79.1%, and the shadow started instead of the launch. One thing was "
           "lost. The proof's 200 labelled cases went with its sandbox, so the project's first "
           "evaluation was seeded with twelve cases written by hand on a Friday, none of them "
           "codeshare, and its 94% was believed for a fortnight."},
 "pitfalls": [
   "Opening on the overall score. The room anchors on it, and the slice that fails becomes a footnote "
   "it reads after saying yes.",
   "Accepting *keep going*. Nobody said yes, so nobody can say stop, and the proof becomes the product "
   "by default.",
   "Conditions without owners. A condition nobody owns is met by luck, and the first person to notice "
   "it was missed is in production.",
   "Deleting the cases with the code. The code should go; the labelled cases are the golden set's "
   "first rows, and nobody will label them twice.",
 ],
 "done_when": "The decision is signed and dated, every condition has an owner and a date, and the "
              "build's first plan can be written from the record without asking what anything meant.",
},
]
