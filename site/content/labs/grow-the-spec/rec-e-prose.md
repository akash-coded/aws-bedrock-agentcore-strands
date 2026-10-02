Here is where I stand before writing any code. The document is a single paragraph, so "line" below means the sentence I am quoting.

## 1. Tools or functions I will build

- `search_alternatives(booking)` - find alternative flights for the passenger.
- `rebook_same_day(booking, flight, acceptance)` - make the change, only once the passenger has accepted.
- `hold_partner_change(booking, flight)` - for partner flights, tell the contact centre and give them a chance to stop the change before it is committed.
- `offer_refund(booking, amount)` - offer a refund when no flight works.
- `request_refund_signoff(booking, amount)` - send refunds over $400 for approval and wait for the answer.
- `handoff_to_agent(booking, reason)` - pass the case to a human agent.
- `record_action(event)` - write a record of every step the assistant takes. Called by all of the above.

## 2. Limits I will enforce in code

| Limit | Source in the document |
|---|---|
| No rebooking without the passenger's acceptance | "should rebook same-day changes when the passenger accepts" |
| Only same-day changes are rebooked automatically | "should rebook same-day changes when the passenger accepts" |
| Partner flight changes pass through a contact-centre stop step before they are committed | "For partner flights it should, where possible, give the contact centre a chance to stop the change before it goes through." |
| A refund can only be offered after the flight search has come back with nothing that works | "Refunds may be offered if no flight works" |
| A refund over $400 is blocked until sign-off is recorded | "though anything over $400 needs sign-off" |
| Every action writes a record, and an action that cannot be recorded does not run | "we will need a record of what it did" |

Two things in the document look like limits but are not hard enough to enforce as written:

- **The 30 seconds.** "ideally within about 30 seconds" is a target. I would measure and log it, not fail the request on it.
- **The handover.** "If it is unsure it should hand over to an agent as appropriate" gives no test for "unsure", so there is nothing concrete to code against yet.

## 3. What I would have to guess

**Timing**
- Is 30 seconds a hard timeout or a goal? Measured from what moment? What should happen when it is missed?

**Rebooking**
- What "same-day" means: same calendar day as the original departure, or as the request? In which time zone?
- What happens to changes that are not same-day: refuse, hand over, or offer but not book?
- What counts as acceptance, and whether it needs to be stored as proof.
- How many alternatives to offer, how to rank them, and who pays any fare difference or change fee.
- What makes a flight "work": cabin, connection time, arrival window, same airports?

**Partner flights**
- How a partner flight is identified (operating carrier, marketing carrier, codeshare).
- How the contact centre is told, how long they get, and whether silence means "go ahead" or "stop".
- What "where possible" means, and whether the change proceeds or is blocked when the check is not possible.

**Refunds**
- Whether "no flight works" means none was found, or the passenger turned them all down.
- "May be offered": is the refund always offered in that case, or is it someone's call?
- Whether $400 is per passenger, per ticket or per booking, and in which currency. I would treat exactly $400 as not needing sign-off, since the text says "over".
- Who signs off, through what system, how long it can take, and what the passenger is told while waiting.
- How the refund amount is worked out, and whether the assistant issues it or only offers it.

**Handover**
- What "unsure" means in practice: a confidence score, a failed lookup, a passenger request, repeated misunderstanding?
- What "as appropriate" means: which queue, and what context goes with the handover.

**Record**
- Which fields, where it is stored, how long it is kept, who can read it, and how personal data is handled.

**Everything around it**
- Which booking, payment and contact-centre systems I am calling, and how the passenger's identity is checked.
- What to do when a step fails halfway, for example the seat is gone between the offer and the rebook.

The guesses I would least want to make on my own are the partner-flight stop window, the refund sign-off path, and the definition of "same-day", because each one decides whether money or a seat moves without a human seeing it. I would ask for those three before starting.
