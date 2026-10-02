Here is the one-screen spec. The PRD leaves three of the eight fields undecided (6, 7 and 8) and is silent on parts of 4 and 5, so where I filled a gap I marked it **Proposed**. Everything else comes straight from the PRD.

## Spec: Rebooking assistant (from PRD v1, owner Priya)

**1. Title**
Rebooking assistant for passengers whose flight is cancelled or delayed past a connection.

**2. Value**
Cuts the wait for a rebooking decision from an average of 38 minutes to a few minutes. Covers 240 cases a day (11% codeshare, about 26) that cost $9.40 each today, about $2,256 a day. Most cases should close without an agent.

**3. Acceptance criteria**
- The passenger sees ranked alternative flights within 30 seconds.
- A same-day change to a SkyWays flight is booked once the passenger accepts.
- A partner flight is booked only when no SkyWays seat exists.
- A refund is offered only when no acceptable flight exists, and never above $400 without a named approver.
- A case the assistant cannot finish reaches a contact-centre agent.
- Compensation claims and group bookings are not handled.
- Not testable yet: "minutes" and "most cases" need numbers.

**4. The model's role**
- Model decides (Proposed): the ranking of options, what the passenger's reply means, whether any flight is acceptable, and when to give up and hand over.
- Exact code (Proposed): eligibility and scope checks, seat and fare lookup, the same-day rule, the "SkyWays first, partner second" rule, the $400 cap, the booking and refund transactions, and logging.

**5. Autonomy**

| Action | Who decides |
|---|---|
| Offer ranked flights | Acts alone |
| Rebook same-day SkyWays flight | Acts alone, after the passenger accepts |
| Rebook partner flight | Not stated. Proposed: agent approves at launch |
| Refund up to $400 | Acts alone, after the passenger accepts (Proposed; the PRD only says "offers") |
| Refund above $400 | A named person approves. The name is missing |
| Hand to an agent | Acts alone |

**6. The bar**
Open (Priya, with Maya). Proposed: one bar for each kind of case, because a wrong refund costs more than a weak ranking.
- Rules in code (cap, scope, no booking without acceptance): 100%.
- SkyWays rebooking, partner rebooking, refund decisions, hand-over decisions: one number each, set by Priya and Maya from a test set of past cases.

**7. Fallback**
- Cannot decide or cannot finish: hand the case to an agent with everything gathered so far.
- Fare engine down: open (Arjun). Proposed: retry once, then hand to an agent. Never book on a stale fare.
- Approval does not arrive: not stated.

**8. Records**
Open (compliance, no reply yet). Proposed minimum for each action: case ID, booking reference, time, action taken, options shown, the passenger's choice, who decided (model, code or named approver), refund amount, outcome, and the reason for any hand-over. Retention period: for compliance to set.

## Four answers needed before this can be built
1. The numbers for field 6.
2. The fare-engine fallback for field 7.
3. The logging rules and retention for field 8.
4. Who approves refunds above $400, and whether partner rebooking needs approval.

If you tell me which of the proposed items you accept, I can tighten this into a final version.
