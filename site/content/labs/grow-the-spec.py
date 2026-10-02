"""Lab 1 · Grow the spec: from a one-page PRD-lite to a spec a coding agent can build from.

The words and the beats are here. The documents the lab works on, the prompts the player assembles and the
recorded replies are files in ``grow-the-spec/``, so that each can be read, diffed and re-run on its own.
A recording is the reply a model gave to the exact prompt the lab shows; the build checks that the parts
the player assembles join into that prompt, byte for byte.
"""
from pathlib import Path

_D = Path(__file__).resolve().parent / "grow-the-spec"
_MODEL, _DATE = "Claude", "2 October 2026"


def _f(name: str) -> str:
    return (_D / name).read_text(encoding="utf-8").rstrip("\n")


def _rec(name: str, prompt: str, **more) -> dict:
    return dict(model=_MODEL, date=_DATE, text=_f(f"rec-{name}.md"), prompt=_f(f"prompt-{prompt}.txt"), **more)


# ---------------------------------------------------------------------------------------------- the prompts
A_ASK = ("Below is a one-page PRD-lite for a rebooking assistant at an airline. Do not write the PRD yet. List the "
         "questions this page does not answer and a build could not start without. Most blocking first, eight at most, "
         "one line each. After each question, name the role that usually owns the answer.")
A_DRAFT = "Below is a one-page PRD-lite for a rebooking assistant at an airline. Write the full PRD from it. Keep it to one page."
B_HEAD = """Below is a PRD. Turn it into a one-screen spec with exactly these eight fields:
1 Title
2 Value
3 Acceptance criteria
4 The model's role (which steps a model decides, which are exact code)
5 Autonomy (for each action: may it act alone, or who approves)
6 The bar (how often it must be right, for each kind of case)
7 Fallback (what happens when it cannot decide or a tool fails)
8 Records (what is written down for each action)"""
B_DEFAULTS = "Where the PRD is silent, use a sensible default so that the spec is complete."
B_FLAG = ("For fields 4 to 8, where the PRD does not say, write NOT DECIDED: followed by the question that must be answered "
          "and who should answer it. Do not infer and do not fill in a sensible default. Those gaps are what I am looking for.")
D_HEAD = """Rewrite these acceptance criteria in EARS.

Format: WHEN <trigger> AND <condition> THE SYSTEM SHALL <observable behaviour> WITHIN <measure>.

Rules:
- Every SHALL ends in a measure: a time, a count or a threshold. If the original has no number, write WITHIN <MEASURE MISSING> and list it at the end.
- Turn every "should", "may", "where possible", "as appropriate" and "ideally" into a hard condition or a separate criterion. List each one you removed and what replaced it.
- Add a BOUNDARY line for every implied prohibition.

Finish with: (a) the count of vague terms removed, (b) the list of missing measures."""
E_HEAD = """You are a coding agent about to implement the feature described below. Before you write any code, answer in three short lists:
1. The tools or functions you will build.
2. Every limit you will enforce in code, each with the exact line of the document it comes from.
3. Everything you would have to guess, because the document does not say."""

# ---------------------------------------------------------------------------------------------- the spec, as it grows
# The eight fields. "draft" is what the PRD gives; "guessed" is a model's text standing in for a decision;
# "open" is NOT DECIDED with an owner; "decided" is a person's answer.
FROM_PRD = [
    {"id": "t", "body": "Rebooking assistant. Owner: Priya (product). From PRD v1.", "state": "decided"},
    {"id": "v", "body": ("Disrupted passengers wait 38 minutes on average for a rebooking decision: 240 cases a day, 11% "
                         "codeshare, $9.40 a case. A decision in minutes, and most cases needing no agent."), "state": "decided"},
    {"id": "ac", "body": ("1 Ranked alternative flights within 30 seconds.\n2 A same-day SkyWays rebooking when the passenger accepts.\n"
                          "3 A partner flight when no SkyWays seat exists.\n4 A refund when no acceptable flight exists; above $400 a named "
                          "person approves.\n5 Hand to an agent when it cannot finish.\nOut of scope: compensation claims, group bookings.\n"
                          "Not testable yet: \"minutes\" and \"most cases\" have no number."), "state": "draft"},
]
GUESSED_NONE = [
    {"id": "role", "state": "guessed", "body": ("Model decides (proposed): the ranking, what the passenger's reply means, whether any flight "
                                                "is acceptable, when to hand over. Exact code (proposed): eligibility, seat and fare lookup, "
                                                "the same-day rule, SkyWays first, the $400 cap, the transactions, logging.")},
    {"id": "auto", "state": "guessed", "body": ("Offer ranked flights: alone. Same-day SkyWays: alone after acceptance. Partner flight: "
                                                "proposed, an agent approves at launch. Refund up to $400: proposed, alone after acceptance. "
                                                "Above $400: a named person; the name is missing. Hand to an agent: alone.")},
    {"id": "bar", "state": "guessed", "body": ("Open (Priya, with Maya). Proposed: 100% for the rules in code; one number each for SkyWays "
                                               "rebooking, partner rebooking, refunds and hand-overs, from a test set of past cases.")},
    {"id": "fb", "state": "guessed", "body": ("Cannot finish: hand to an agent with everything gathered. Fare engine down: proposed, retry "
                                              "once, then hand over. Approval never arrives: not stated.")},
    {"id": "rec", "state": "guessed", "body": ("Open (compliance). Proposed minimum: case ID, booking reference, time, action, options shown, "
                                               "the choice, who decided, refund amount, outcome, hand-over reason. Retention: for compliance.")},
]
GUESSED_DEFAULTS = [
    {"id": "role", "state": "guessed", "body": ("Model decides: the ranking, the wording, what the reply means, when it cannot finish. Exact "
                                                "code: eligibility, lookups, the same-day rule, the no-SkyWays-seat check, the $400 cap, "
                                                "scope checks, the transactions. Written as fact; the PRD says nothing about it.")},
    {"id": "auto", "state": "guessed", "body": ("Offer: alone. Same-day SkyWays: alone after acceptance. Partner: alone when the partner "
                                                "confirms at no extra fare (default). Refund up to $400: alone (default). Above $400: a named "
                                                "Finance approver. A later day: an agent (default). Hand off: alone.")},
    {"id": "bar", "state": "guessed", "body": ("(default) Options valid 99%; SkyWays rebooking 99%; partner rebooking 99%; the refund rules "
                                               "100%; \"no acceptable flight\" 98%; hand-over 95%.")},
    {"id": "fb", "state": "guessed", "body": ("Cannot decide or out of scope: an agent, with a summary. Fare engine down (default): retry "
                                              "once, book nothing, queue the case flagged. A booking fails: retry once, then hand over. "
                                              "Nothing in 30 seconds: hand over.")},
    {"id": "rec", "state": "guessed", "body": ("(default) Case ID, booking reference, time, action, options and their order, the choice, "
                                               "model version, tool calls, approver, refund amount, hand-off reason. Bookings and refunds "
                                               "kept 7 years; conversation text 12 months.")},
]
OPEN = [
    {"id": "role", "state": "open", "body": "NOT DECIDED: which of the five steps a model decides and which are exact code. Who: Arjun (architecture), with Priya."},
    {"id": "auto", "state": "open", "body": "NOT DECIDED, for each action: may the assistant act alone, or who approves. Who: Priya; Finance names the refund approver."},
    {"id": "bar", "state": "open", "body": "NOT DECIDED: one number, or one for each kind of case, and which kinds. Who: Priya, with Maya (QA)."},
    {"id": "fb", "state": "open", "body": ("Cannot finish: a contact-centre agent (PRD). NOT DECIDED: what \"cannot finish\" means; the fare "
                                           "engine down; any other tool failing. Who: Priya; Arjun.")},
    {"id": "rec", "state": "open", "body": "NOT DECIDED: what is logged for each action, and for how long. Who: compliance."},
]
DECIDED = [
    {"id": "role", "state": "decided", "body": ("Model decides: the ranking of options, what the passenger's reply means, and when to hand "
                                                "over. Exact code: eligibility, seat and fare lookup, the same-day rule, SkyWays before partner, "
                                                "the $400 cap, the booking and refund transactions, logging. (Arjun)")},
    {"id": "auto", "state": "decided", "body": ("Offer ranked flights: alone. Rebook same-day SkyWays: alone, after the passenger accepts. "
                                                "Rebook a partner flight: held for a veto window before it commits. Refund up to $400: alone, "
                                                "after the passenger accepts. Refund above $400: a named approver in Finance. Hand to an "
                                                "agent: alone. (Priya; Finance)")},
    {"id": "bar", "state": "decided", "body": ("One number per kind of case, from the cost of a wrong answer against the saving of a right "
                                               "one, measured on 500 past cases with codeshare as its own group: rules in code 100%; same-day "
                                               "rebooking 95%; partner rebooking 95%; refund decisions 98%; hand-over when it should 90%. "
                                               "(Priya, with Maya)")},
    {"id": "fb", "state": "decided", "body": ("Cannot decide, or any tool fails: hand the case to a contact-centre agent with the transcript. "
                                              "Fare engine down: book nothing on a stale fare; the case queues for an agent, flagged. No "
                                              "silent retry. (Arjun)")},
    {"id": "rec", "state": "open", "body": ("NOT DECIDED: what is logged for each action, and for how long. Who: compliance. Chased twice, no "
                                            "reply. The gate holds until it is in.")},
]
DECIDED_LATE = DECIDED[:-1] + [
    {"id": "rec", "state": "guessed", "body": ("Filled in by the engineers the day the logging was built: case ID, booking reference, time, "
                                               "action, options, choice, approver, refund amount, hand-off reason. Compliance has not seen "
                                               "it. Owner: nobody yet.")},
]
AC_EARS = [{"id": "ac", "state": "decided", "body": (
    "AC-1  WHEN a disrupted passenger requests rebooking AND a same-day seat exists\n"
    "      THE SYSTEM SHALL present ranked alternatives WITHIN 30 seconds at P95.\n"
    "AC-2  WHEN the passenger accepts a same-day SkyWays flight\n"
    "      THE SYSTEM SHALL rebook and confirm to the passenger.\n"
    "AC-3  WHEN the only available seat is on a partner flight\n"
    "      THE SYSTEM SHALL hold the change for a veto window before it commits.\n"
    "B-1   BOUNDARY  The system shall NEVER issue a refund above $400 without a named approver.\n"
    "B-2   BOUNDARY  The system shall NEVER change a booking without the passenger's acceptance.\n"
    "Measures still missing, with their owners: the veto window (operations), the time from acceptance to a confirmed "
    "rebooking (Arjun), the refund path's wait (Finance). Each holds the gate, not the design.")}]

# ---------------------------------------------------------------------------------------------- the lab
LAB = {
    "n": 1, "phase": 1, "minutes": 12,
    "title": "Grow the spec",
    "does": "Turn a product manager's one page into a spec a coding agent can build from, without letting a model make the five decisions nobody has made.",
    "who": "The product manager, with the architect and QA",
    "makes": "a one-screen spec with the undecided fields named and owned",
    "tool": {"name": "a chat window and the clipboard"},
    "lesson": ("p1-design-and-spec", "The lesson"),
    "artefact": {
        "name": "spec-rebooking-assistant.md",
        "versions": ["PRD-lite", "PRD v1", "Spec, gaps named", "Spec v1"],
        "sections": [
            {"id": "t", "head": "1 Title"}, {"id": "v", "head": "2 Value"}, {"id": "ac", "head": "3 Acceptance criteria"},
            {"id": "role", "head": "4 The model's role"}, {"id": "auto", "head": "5 Autonomy"}, {"id": "bar", "head": "6 The bar"},
            {"id": "fb", "head": "7 Fallback"}, {"id": "rec", "head": "8 Records"},
        ],
    },
    "files": [
        {"id": "prdlite", "name": "PRD-lite · Rebooking assistant", "note": "Priya's page, draft 2", "body": _f("prd-lite.md")},
        {"id": "criteria", "name": "The criteria, as the sponsor's slide has them", "note": "one paragraph", "body": _f("criteria-prose.txt")},
    ],
    "replies": {
        "a-ask": _rec("a-ask", "a-ask", after=(
            "Six of the eight were not on the page at all. The two that were (the refund cap, the logging) are the two Priya "
            "already knew about. The model's list is not the answer; it is the list of people to go and ask, by name.")),
        "a-draft": _rec("a-draft", "a-draft",
                        flags=[("| R1 |", "Sixty seconds, three options and the ranking rule are the model's. The page said \"quickly\" and \"the best ones\"."),
                               ("| R4 |", "Twenty-four hours is the model's test for \"no sensible flight\". Nobody at the airline has said so."),
                               ("| Time to a rebooking decision |", "\"Under 5 minutes\" is a target the sponsor has not set. It will be quoted back as a promise."),
                               ("| Cases finished with no agent |", "60% is a guess at \"most\". The contact centre's staffing will be planned on it."),
                               ("| Wrong rebookings or refunds |", "\"Under 1%\" is the bar, and the bar is the one number that has to come from money, per kind of case."),
                               ("Compensation claims. Group bookings. Rebooking", "A new exclusion, inferred from \"same-day\". It may be right; it is not Priya's.")],
                        sound=[("| R2 |", "This is the page's own rule: the change happens only after the passenger accepts."),
                               ("| What is the refund cap? |", "An open question, kept open, with its owner. This is what the whole table should look like."),
                               ("Three things to settle first", "The model names the three decisions that change the design. Good advice, at the bottom of a page that already decided them.")],
                        read=("Every guess is marked **[proposed]**, which is more honest than most drafts. It still does not help: the next reader "
                              "sees a complete PRD with numbers in it, and a number on a page outlives the bracket beside it. The build will "
                              "be planned on sixty seconds and sixty percent.")),
        "b-none": _rec("b-none", "b-none",
                       flags=[("- Model decides (Proposed)", "Which steps a model decides is the architect's call, and it changes what gets tested. The PRD says nothing about it."),
                              ("- Exact code (Proposed)", "The limits that live in code, decided by the model. These are the lines the coding agent will build from."),
                              ("| Rebook partner flight |", "Whether an agent approves a partner rebooking is a policy, and the partner contract has a say."),
                              ("| Refund up to $400 |", "\"Acts alone\" for a refund is money moving with nobody watching. The PRD only said the refund is offered."),
                              ("Open (Priya, with Maya). Proposed", "The bar is open, and then proposed anyway. One sentence undoes the other."),
                              ("- Rules in code (cap", "100% is right for a rule in code, and it is still the model's number until Maya says so."),
                              ("- SkyWays rebooking, partner rebooking", "The kinds of case are the model's grouping; the bar sheet starts from the kinds, so this decides the test set."),
                              ("- Fare engine down: open (Arjun). Proposed", "Open, then proposed. Retry once on a fare engine is a design decision with a stale-fare risk inside it."),
                              ("Open (compliance, no reply yet). Proposed", "A record list that compliance has not seen. It will be built, and then rebuilt.")],
                       sound=[("| Refund above $400 |", "Straight from the PRD, and it says what is missing: the name."),
                              ("- A refund is offered only when no acceptable flight exists", "From the PRD, with the cap. A criterion a tester can check."),
                              ("- Not testable yet", "The model flagged the two soft words in the PRD. Keep this line.")],
                       read=("Told nothing, the model did the sensible thing and marked each guess **Proposed**. Nine of them. The spec is now "
                             "complete, and that is the problem: whoever reads it next reads a decided document, and the word \"proposed\" "
                             "is the first thing a skim drops.")),
        "b-defaults": _rec("b-defaults", "b-defaults",
                           flags=[("Cuts the wait for a rebooking decision from 38 minutes to under 5", "Under five minutes and 70% are the sponsor's numbers to set. They are now in the value line, where the sponsor will read them as agreed."),
                                  ("- Every handoff carries the full case", "A criterion the PRD never had, written in the voice of the others."),
                                  ("- Model decides: how to rank", "Field 4 is written as fact, with no (default) on it. The PRD says nothing about which steps a model decides."),
                                  ("- Exact code: eligibility check", "Also written as fact. These are the limits the coding agent will put in signatures, chosen by a model."),
                                  ("| Partner rebooking |", "A partner rebooking \"alone\" is a policy the partner contract has a say in."),
                                  ("| Refund up to $400 |", "Money moving with nobody watching, by default."),
                                  ("| Rebooking on a later day |", "An action the PRD never mentioned, with an approver chosen for it."),
                                  ("- Options offered are valid", "99% is a bar. Bars come from money, per kind of case, and Maya has not seen this."),
                                  ("- Same-day SkyWays rebooking is correct", "99% again. A wrong rebooking and a weak ranking do not cost the same."),
                                  ("- Partner rebooking is correct", "The same number for a partner change that the contract may price differently."),
                                  ("- Refund within the cap", "98% for \"no acceptable flight\" decides how many refunds go out wrongly. Finance has not seen it."),
                                  ("- Cases that should go to an agent", "95% of hand-overs: the rest are passengers stuck with a bot. Whose number?"),
                                  ("- Fare engine down **(default", "Retry once, then queue. Arjun's open question, answered by a model."),
                                  ("For each action: case ID", "Seven years and twelve months are retention periods. Compliance has not replied, and this will be built.")],
                           sound=[("| Refund above $400 |", "From the PRD. The model even says the name is missing."),
                                  ("- A refund is offered only when", "From the PRD, with the cap."),
                                  ("- Cannot decide, unclear reply, or out of scope", "The PRD's own fallback: hand to an agent."),
                                  ("**6. The bar** **(default; open with Priya and Maya)**", "A heading that says default is doing its job. The lines under it are the guesses.")],
                           read=("You asked for defaults and the model gave good ones, labelled. Count the lines you marked: those are decisions, "
                                 "each with an owner at the airline, now written in the owner's absence. Field 4 has no label at all. A "
                                 "complete spec with fourteen defaults in it is not a spec; it is a list of people who were not asked.")),
        "b-flag": _rec("b-flag", "b-flag",
                       flags=[("NOT DECIDED: For each of the five steps", "Field 4, the model's role, is not on the PRD's list of open questions. Nobody had noticed it was undecided."),
                              ("| Show ranked options |", "Not on the list. Whether staff see the options first is a policy the contact centre will have a view on."),
                              ("| Rebook on SkyWays, same day |", "Not on the list. \"The passenger accepts\" is in the PRD; whether that is enough is not."),
                              ("| Rebook on a partner flight |", "Not on the list, and the partner contract has a say."),
                              ("| Refund |", "Half on the list: the PRD knows the cap. It does not say whether the assistant pays the refund or only offers it."),
                              ("| Hand to an agent |", "Not on the list. Whether a hand-off needs accepting decides what a stuck passenger experiences."),
                              ("- Cannot decide: NOT DECIDED", "Not on the list. \"Cannot finish\" and \"cannot decide\" are different cases, and the PRD names one."),
                              ("- Any other tool fails: NOT DECIDED", "Not on the list. The PRD mentions one tool; the assistant will call five.")],
                       sound=[("NOT DECIDED: How right must it be", "On the PRD's list, with its owners. The model kept it open and kept the names."),
                              ("NOT DECIDED: What must be logged", "On the PRD's list. Still open, still compliance's."),
                              ("- Fare engine down: NOT DECIDED", "On the PRD's list, with Arjun's name.")],
                       read=("The PRD listed three open questions. Told where to stop, the model found eight more, and named a suggested "
                             "owner for each. Nothing in this spec is a guess. It is also the only version of the three that a reviewer "
                             "cannot mistake for finished, because the gaps are in capitals.")),
        "d-ears": _rec("d-ears", "d-ears",
                       flags=[("**AC-1.**", "\"A passenger asks to change a flight\" is the trigger the model chose. The paragraph never says what starts the offer; a cancellation is the likelier trigger."),
                              ("**AC-4.**", "Silence means go: if the contact centre does not answer, the change commits. The paragraph said \"a chance to stop\", not \"a deadline to stop\"."),
                              ("**AC-6.**", "\"Where possible\" became fail closed: no contact centre, no change. The other reading is just as faithful. This is the operations lead's call."),
                              ("**AC-7.**", "\"May be offered\" became \"shall offer\", every time. The paragraph left the refund optional on purpose, or by accident; either way it was Finance's."),
                              ("**AC-10.**", "\"Unsure\" became a confidence threshold, a number that will be tuned by whoever writes the prompt. That is a design decision, not a criterion.")],
                       sound=[("**AC-2.**", "Same-day, on acceptance, with a confirmation: all in the paragraph. The missing measure is honestly missing."),
                              ("**AC-3.**", "\"Hold it uncommitted\" is what \"a chance to stop the change before it goes through\" means. Faithful."),
                              ("- BOUNDARY: THE SYSTEM SHALL NOT offer or pay a refund of more than $400.00", "The paragraph's one hard limit, now a boundary line. This is what the format is for.")],
                       read=("The model did the honest thing with the numbers: eleven measures missing, listed. It did the quiet thing with the words: "
                             "every \"should\" and \"may\" had to become a rule, so it chose one, and then listed its choices at the bottom. A format "
                             "that forbids vagueness forces a decision at each vague word, and the model makes it unless the owner is in the room.")),
        "e-prose": _rec("e-prose", "e-prose"),
        "e-struct": _rec("e-struct", "e-struct"),
    },
    "beats": [
        {"id": "start", "kind": "note", "move": "Priya's page",
         "say": ("Priya, the product manager, has written one page for an assistant that rebooks stranded passengers. It is on the desk. "
                 "It is clear, it is short, and a build could not start from it: nothing in it says what the assistant may do alone, how right "
                 "it must be, or what happens when it cannot decide.\n\nThis lab turns the page into a spec. Every prompt you assemble is "
                 "run for real and the reply is a recording. Your job is to notice where a model, left to itself, makes a decision that "
                 "belongs to a person."),
         "button": "Open the page"},
        {"id": "ask", "kind": "compose", "move": "Ask for the next document", "title": "Prompt A",
         "say": "Everyone agrees the page is not enough. The choice is what you ask a model to do about it.",
         "parts": [{"id": "what", "label": "What do you ask for?",
                    "options": [{"id": "draft", "label": "Write the full PRD from it", "text": A_DRAFT},
                                {"id": "ask", "label": "List the questions it does not answer", "text": A_ASK, "book": True}]},
                   {"file": "prdlite"}]},
        {"id": "ask-draft", "kind": "mark", "of": "ask", "doc": "a-draft", "when": {"ask.what": "draft"},
         "ask": "Mark every line where the model put a number or a rule that Priya's page does not contain."},
        {"id": "ask-ask", "kind": "run", "of": "ask", "reply": {"what=ask": "a-ask", "*": "a-ask"}, "when": {"ask.what": "ask"}},
        {"id": "prd", "kind": "note", "move": "Priya answers",
         "say": ("The eight questions go to their owners by name. A week later PRD v1 is on the desk: five answered, three still open, "
                 "each open one with an owner. That is the document the spec is made from, and its first three fields are already in it."),
         "gives": [{"id": "prd", "name": "PRD · Rebooking assistant, v1", "note": "Priya, after the owners replied", "body": _f("prd.md")}],
         "patch": [{"version": 1}] + FROM_PRD},
        {"id": "gaps", "kind": "compose", "move": "From the PRD to the eight fields", "title": "Prompt B",
         "say": ("The spec has eight fields on one screen. The PRD fills the first three. The other five are the decisions nobody has made "
                 "yet, and the one sentence you add to this prompt decides what the model does when it reaches each of them."),
         "parts": [{"text": B_HEAD},
                   {"id": "gaps", "label": "Where the PRD is silent",
                    "options": [{"id": "none", "label": "Say nothing", "text": ""},
                                {"id": "defaults", "label": "Fill in a sensible default", "text": B_DEFAULTS},
                                {"id": "flag", "label": "Write NOT DECIDED and who decides", "text": B_FLAG, "book": True}]},
                   {"file": "prd", "lead": "PRD:\n"}]},
        {"id": "gaps-none", "kind": "mark", "of": "gaps", "doc": "b-none", "when": {"gaps.gaps": "none"},
         "ask": "Mark every line where the model decided something that is a person's to decide."},
        {"id": "gaps-defaults", "kind": "mark", "of": "gaps", "doc": "b-defaults", "when": {"gaps.gaps": "defaults"},
         "ask": "Mark every line where the model decided something that is a person's to decide."},
        {"id": "gaps-flag", "kind": "mark", "of": "gaps", "doc": "b-flag", "when": {"gaps.gaps": "flag"},
         "ask": "The PRD listed three open questions. Mark each NOT DECIDED that was not on the PRD's list."},
        {"id": "call", "kind": "choose", "move": "What goes in the spec",
         "ask": "Fields 4 to 8 are on the screen. What goes in the spec that leaves this desk?",
         "options": [
             {"id": "owners", "label": "NOT DECIDED, the question and the owner's name, in each of the five, and each question to its owner today", "right": True,
              "detail": "The spec is incomplete and says so, and five people have one question each.",
              "after": ("The spec now has five holes in capitals, each with a name beside it. That is the right shape: a reviewer cannot "
                        "mistake it for finished, the gate cannot pass it, and each owner has one question to answer rather than a "
                        "document to read."),
              "patch": [{"version": 2}] + OPEN},
             {"id": "keep", "label": "What the model wrote, as it stands, sent round for review",
              "detail": "The reviewers will see what is proposed and what is open.",
              "after": ("A reviewer reads what is on the page. A proposed value reads as a value, and a NOT DECIDED that nobody is chasing "
                        "stays in capitals until the gate finds it. In the game this is the thirty pages the engineers never read. The book "
                        "keeps the capitals and sends five questions today, each to a name.")},
             {"id": "self", "label": "Your own answers, decided now, so the build starts Monday",
              "detail": "You are the product manager; deciding is the job.",
              "after": ("Three of the five are not yours. The bar needs Maya's test set, the fallback needs Arjun, the records need "
                        "compliance. A product manager who fills them in alone has made the same move as the model, with a better title. "
                        "The book writes NOT DECIDED and the owner's name, and sends five questions today.")}]},
        {"id": "answers", "kind": "note", "move": "The owners answer", "when": {"call": "owners"},
         "say": ("Over the week the answers come back. Arjun names the steps that are code and the steps the model decides. Priya sets "
                 "autonomy per action, and Finance names the approver. Priya and Maya derive the bar per kind of case from what a wrong "
                 "answer costs, on 500 past cases. Arjun answers the fare engine. Compliance still has not replied, so field 8 stays "
                 "open, and the gate holds until it is in."),
         "patch": DECIDED},
        {"id": "answers-keep", "kind": "note", "move": "The owners answer, late", "when": {"call": "keep"},
         "say": ("The spec went round as it stood, and two reviewers signed it without asking a question. Arjun caught field 4 at the "
                 "architecture review a week later and wrote it himself. Priya and Maya reset the bar when the test set came in. Finance's "
                 "approver is still unnamed, because nobody asked. Fields 4 to 7 are decided now, a week late. The engineers filled field 8 "
                 "in themselves the day the logging was built, and compliance has not seen it."),
         "patch": [{"version": 2}] + DECIDED_LATE},
        {"id": "answers-self", "kind": "note", "move": "The owners answer, after the fact", "when": {"call": "self"},
         "say": ("The build started Monday on your answers. Arjun rewrote field 4 at the architecture review, because two of your \"exact "
                 "code\" steps need a model. Maya's test set moved your refund bar. Compliance has still not replied, and field 8 is now "
                 "yours, not theirs: whatever is logged, you decided it."),
         "patch": [{"version": 2}] + DECIDED_LATE},
        {"id": "ears", "kind": "compose", "move": "Criteria a tester can run", "title": "Prompt D",
         "say": ("Field 3 came from the PRD as five bullets, which is rarer than it sounds. What most teams have is a paragraph: the "
                 "one on the sponsor's slide, which the contact-centre lead quoted in the meeting. It is on the desk. Run the EARS "
                 "rewrite on it and watch what a strict format does to soft words."),
         "parts": [{"text": D_HEAD}, {"file": "criteria", "lead": "CRITERIA:\n"}], "button": "Run this prompt"},
        {"id": "ears-mark", "kind": "mark", "of": "ears", "doc": "d-ears",
         "ask": "The paragraph never said these. Mark each criterion whose behaviour the paragraph does not contain."},
        {"id": "measures", "kind": "choose",
         "ask": "Eleven measures are missing. What happens to them?",
         "options": [
             {"id": "owners", "label": "Three go to their owners now; the rest stay as MEASURE MISSING and hold the gate", "right": True,
              "detail": "The veto window, the time to a confirmed rebooking, and the refund path move money or a seat.",
              "after": ("Three measures decide whether money or a seat moves without a person seeing it, and those three have owners "
                        "who can answer this week. The other eight are real, and they block the launch, not the design. Field 3 is now "
                        "five lines a tester can run, with the missing numbers named rather than guessed."),
              "patch": [{"version": 3}] + AC_EARS},
             {"id": "fill", "label": "Fill them with sensible values, so every SHALL has a number",
              "detail": "The format asked for a measure on every line.",
              "after": ("Eleven numbers nobody set, in the one field a tester reads literally. The veto window you pick decides how long a "
                        "partner change hangs; the threshold you pick for \"unsure\" decides which passengers reach a person. The book sends "
                        "the three that move money or a seat to their owners and leaves the rest as MEASURE MISSING.")},
             {"id": "drop", "label": "Drop the WITHIN clauses; the PRD never had them",
              "detail": "Keep the SHALL lines, lose the measures.",
              "after": ("Without a measure a SHALL is a wish, and a tester cannot fail it. The whole point of the rewrite was to find the "
                        "numbers nobody had set; dropping them hides the finding. The book keeps every MEASURE MISSING and gives three "
                        "of them owners today.")}]},
        {"id": "hand", "kind": "compare", "move": "Hand it to the builder",
         "say": ("Prompt E is the same for both: a coding agent, asked before any code what it will build, what it will enforce, and "
                 "what it would have to guess. One column hands it the paragraph; the other hands it the spec's fields 3, 7 and 8."),
         "ask": "Which document do you hand to the coding agent?",
         "cols": [{"id": "prose", "label": "The paragraph", "body": E_HEAD + "\n\nDOCUMENT:\n" + _f("spec-prose.md"), "reply": "e-prose",
                   "pick": "Hand over the paragraph",
                   "after": ("Read the agent's second list. \"Ideally within about 30 seconds\" became a target it would log and not enforce: "
                             "nobody decided that. \"We will need a record\" became a rule that an action which cannot be recorded does not "
                             "run: nobody decided that either. Every limit it found came out of a sentence with \"should\" in it, and its "
                             "third list runs to nineteen guesses. The book hands over the spec.")},
                  {"id": "struct", "label": "The spec, fields 3, 7 and 8", "body": E_HEAD + "\n\nDOCUMENT:\n" + _f("spec-structured.md"),
                   "reply": "e-struct", "pick": "Hand over the spec", "right": True,
                   "after": ("Every limit in this reply quotes a line. The agent left the logging function empty because R-1 says the records "
                             "are not decided, and it named the veto window, the refund scope and the records as the three things it will not "
                             "guess. Its guesses are fewer and sharper, and each one is a question the spec can now go back and answer.")}]},
        {"id": "file", "kind": "file", "move": "File the spec",
         "say": "The spec is one screen: three fields from the PRD, four decided by their owners this week, and one still open with a name on it."},
    ],
    "debrief": {
        "title": "A default that ships is a decision nobody made",
        "trap": ("The three prompts that went wrong all did the same thing: they let the model keep going when it reached a decision "
                 "nobody had made. The full PRD had six numbers in it Priya never gave. The spec with defaults had a field 4 written as "
                 "fact. The EARS rewrite turned \"where possible\" into a rule that fails closed. Each time the reply was fluent and "
                 "complete, and that is the trap: a complete document reads as a decided one, and nobody skims for the word \"proposed\"."),
        "habit": ("Ask for the gaps before the draft. When the draft comes, tell the model where to stop: where the document does not say, "
                  "write NOT DECIDED and who decides. Keep those words in the spec until the owner replaces them, and let them hold the "
                  "gate. Hand the builder the structured document, and ask it to quote a line for every limit it will enforce."),
        "tool": {"title": "Doing this with your own model",
                 "body": ("Every prompt in this lab copies. Paste it into any model with the document under it and compare the reply with "
                          "the recording. The numbers it invents will differ; the places it invents them will not.")},
        "links": [("Spec-driven development, the method this borrows from", "../../learn/what-is-spec-driven-development/")],
    },
}
