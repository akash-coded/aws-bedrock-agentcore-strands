**1. Tools I will build**

- `find_alternatives(booking)`: searches same-day seats on SkyWays and partner flights and returns them ranked.
- `record_acceptance(booking, option)`: stores the passenger's explicit yes to one specific option. Every booking change checks for it first.
- `rebook_skyways(booking, option)`: moves the booking to an accepted same-day SkyWays flight and sends the confirmation.
- `hold_partner_change(booking, option)`: puts a partner-flight change on hold, commits it when the veto window ends with no veto, and cancels it if vetoed.
- `handoff_to_agent(case, transcript, reason)`: passes the case to the contact centre with the full transcript.
- `issue_refund(amount, approver)`: only if refunds are in scope at all (see list 3). It refuses any amount above $400 without a named approver.
- `log_action(...)`: an empty interface only. I will not decide what it stores, because R-1 is open.

**2. Limits I will enforce in code**

- Alternatives are returned within 30 seconds. Source, AC-1: "THE SYSTEM SHALL present ranked alternatives WITHIN 30 seconds at P95." In code this is a hard timeout on the search plus a latency metric, since P95 can only be checked by measuring, not per request.
- Only same-day SkyWays flights are rebooked directly. Source, AC-2: "WHEN the passenger accepts a same-day SkyWays flight THE SYSTEM SHALL rebook and confirm to the passenger."
- A partner-flight change never commits immediately. Source, AC-3: "THE SYSTEM SHALL hold the change for a veto window before it commits."
- No refund above $400 without an approver's name on the request. Source, B-1: "The system shall NEVER issue a refund above $400 without a named approver."
- No booking change without a recorded acceptance, including partner holds. Source, B-2: "The system shall NEVER change a booking without the passenger's acceptance."
- Any tool error or undecided case goes to a human with the transcript, with no silent retry loop. Source, F-1: "WHEN the model cannot decide OR a tool fails THE SYSTEM SHALL hand the case to a contact-centre agent with the transcript."

**3. What I would have to guess**

- **Veto window:** how long it is, who can veto (passenger, operations, the partner), how they are told, and what happens to the passenger after a veto.
- **Refunds:** whether this assistant issues refunds at all, since no acceptance criterion asks for one. Also the currency, whether $400 is per refund or per booking in total, and who counts as a "named approver" and how that is verified.
- **Acceptance:** what counts as acceptance (a button, a typed "yes"), how long it stays valid, and whether a price or seat change after the offer needs a new one.
- **No seat at all:** what to do when there is no same-day seat on SkyWays or a partner. The spec only covers the cases where a seat exists.
- **Partner options:** whether partner flights are shown when a SkyWays seat also exists, and whether partner flights must also be same-day.
- **Definitions:** what makes a passenger "disrupted", and which time zone "same-day" uses.
- **Ranking:** the criteria for ordering alternatives.
- **The 30 seconds:** where the clock starts and stops, and what to do when a request runs past it (I would assume F-1 handoff).
- **Fallback details:** what "cannot decide" means in practice, whether a failed tool gets one retry, what the transcript contains, and what the passenger is told during handoff.
- **Confirmation:** the channel (email, SMS, app) and its content.
- **Records:** what is logged and for how long. R-1 says this is not decided and belongs to compliance, so I would ask rather than guess.
- **Not mentioned at all:** fare differences, cabin class, group bookings, connections, bags, and the booking and partner systems I would call.

Before I write code I would want answers on three of these: the veto window, whether refunds are in scope, and R-1. The rest I can build with a stated default and flag it.
