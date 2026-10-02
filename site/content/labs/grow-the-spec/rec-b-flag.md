# Spec: Rebooking assistant

**1 Title**
Rebooking assistant. Owner: Priya (product). Version 1.

**2 Value**
Passengers whose flight is cancelled, or delayed past a connection, wait 38 minutes on average for a rebooking decision. There are 240 cases a day, 11% of them codeshare, at a measured cost of $9.40 a case (Q2 ticket export). The assistant should give a decision in minutes and leave most cases needing no agent.

**3 Acceptance criteria**
- A passenger sees ranked alternative flights within 30 seconds.
- When the passenger accepts, a same-day change on a SkyWays flight is rebooked.
- When no SkyWays seat exists, the passenger is rebooked onto a partner (codeshare) flight.
- When no acceptable flight exists, a refund is offered. A refund does not exceed $400 unless a named person approves more.
- When the assistant cannot finish, the case goes to a contact-centre agent.
- Compensation claims and group bookings are not handled.
- Not testable yet: "a decision in minutes" and "most cases need no agent" have no number in the PRD.

**4 The model's role**
NOT DECIDED: For each of the five steps (rank the options, rebook on SkyWays, rebook on a partner, offer a refund and check the $400 cap, hand to an agent), which does a model decide and which is exact code? Who: Arjun (architecture) with Priya. The PRD names no owner for this.

**5 Autonomy**

| Action | What the PRD says | Gap |
|---|---|---|
| Show ranked options | The assistant offers them | NOT DECIDED: May it show options with no check by staff? Who: Priya |
| Rebook on SkyWays, same day | The passenger must accept | NOT DECIDED: Is the passenger's acceptance enough, or must staff also approve? Who: Priya |
| Rebook on a partner flight | Done when no SkyWays seat exists | NOT DECIDED: Must the passenger accept, and must an agent or the partner approve first? Who: Priya |
| Refund | Capped at $400 unless a named person approves more | NOT DECIDED: Who is the named person? May the assistant issue a refund up to $400 alone, or only offer it? Who: Finance |
| Hand to an agent | The assistant does this when it cannot finish | NOT DECIDED: Does anyone need to accept the hand-off? Who: Priya, with the contact-centre lead |

The PRD names no owner for any of these.

**6 The bar**
NOT DECIDED: How right must it be before launch: one number, or one for each kind of case? If one for each kind, what are the kinds? Who: Priya, with Maya (QA). This is an open question in the PRD.

**7 Fallback**
- Cannot finish: the case goes to a contact-centre agent (PRD).
- Cannot decide: NOT DECIDED: What counts as "cannot finish", and does a case the assistant cannot decide go the same way? Who: Priya.
- Fare engine down: NOT DECIDED: What happens to a case when the fare engine is down? Who: Arjun (architecture). This is an open question in the PRD.
- Any other tool fails: NOT DECIDED: What happens to the case? Who: Arjun. The PRD does not mention any tool other than the fare engine.

**8 Records**
NOT DECIDED: What must be logged for each action, and for how long? Who: compliance. This is an open question in the PRD, with no reply yet.

---

**Summary of gaps.** Fields 4, 6 and 8 are fully undecided. Fields 5 and 7 are partly decided. The PRD's three open questions cover fields 6, 8 and one line of 7. The gaps the PRD does not list at all are the model's role (field 4), most of autonomy (field 5), and failure of any tool other than the fare engine. Where the PRD names no owner, the name I gave is a suggestion for you to confirm.
