Here is the one-screen spec. Anything marked **(default)** is my assumption where the PRD is silent, so the named owner should confirm it.

# Spec: Rebooking assistant (v1)

**1. Title**
Rebooking assistant for disrupted SkyWays passengers

**2. Value**
Cuts the wait for a rebooking decision from 38 minutes to under 5 **(default)** for 240 cases a day. Those cases cost $9.40 each today, about $2,256 a day. Target: at least 70% of cases finish with no agent **(default for "most")**.

**3. Acceptance criteria**
- A passenger whose flight is cancelled, or delayed past a connection, sees ranked alternatives within 30 seconds.
- A same-day SkyWays rebooking completes once the passenger accepts, and a confirmation is sent.
- A partner (codeshare) flight is offered only when no SkyWays seat exists.
- A refund is offered only when no acceptable flight exists, and never above $400 without a named approver.
- Compensation claims and group bookings are recognised and passed to an agent untouched.
- Every handoff carries the full case, so the passenger does not repeat anything **(default)**.

**4. The model's role**
- Model decides: how to rank the options for this passenger, how to word the offer, what the passenger's reply means, and when it cannot finish.
- Exact code: eligibility check, seat and fare lookups, the same-day rule, the "no SkyWays seat" check, the $400 cap, scope checks, and the booking and refund transactions themselves.

**5. Autonomy**

| Action | Who decides |
|---|---|
| Offer ranked options | Assistant alone |
| Same-day SkyWays rebooking | Assistant alone, after the passenger accepts |
| Partner rebooking | Assistant alone, after the passenger accepts and the partner confirms the seat at no extra fare; otherwise an agent approves **(default)** |
| Refund up to $400 | Assistant alone, after the passenger accepts **(default)** |
| Refund above $400 | Named Finance approver (name not in the PRD) |
| Rebooking on a later day | Agent approves **(default)** |
| Hand off to an agent | Assistant alone |

**6. The bar** **(default; open with Priya and Maya)**
One number for each kind of case, because a wrong refund costs more than a weak ranking.
- Options offered are valid and bookable: 99%
- Same-day SkyWays rebooking is correct (passenger, flight, date, cabin): 99%
- Partner rebooking is correct: 99%
- Refund within the cap and the rules: 100% (enforced by code); "no acceptable flight" judged correctly: 98%
- Cases that should go to an agent do go: 95%

Measured on past cases before launch, with codeshare cases tested as their own group.

**7. Fallback**
- Cannot decide, unclear reply, or out of scope: hand to an agent with a case summary and tell the passenger.
- Fare engine down **(default; open with Arjun)**: retry once, then book nothing on an unconfirmed fare. Queue the case for an agent, flagged "fare engine down".
- Booking or partner system fails: retry once, change nothing until the new seat is confirmed, then hand to an agent.
- No options within 30 seconds: tell the passenger and hand over.

**8. Records** **(default; compliance has not replied)**
For each action: case ID, booking reference, time, action taken, options shown and their order, the passenger's choice, model version, tool calls and results, approver (if any), refund amount, and handoff reason. Bookings and refunds kept 7 years; conversation text kept 12 months.

Three of these defaults stand in for the PRD's open questions (the bar, the records, and the fare engine outage), and the refund approver still needs a name. I would get those four confirmed before build starts.
