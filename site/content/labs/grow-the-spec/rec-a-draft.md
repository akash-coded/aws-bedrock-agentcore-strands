Here is the full PRD, kept to one page. The PRD-lite leaves several things without a number ("quickly", "reasonable limit", "most", "rare"), so I filled those with suggested values and marked each one **[proposed]**. None of those come from your data, so please confirm or replace them.

---

# PRD · Rebooking assistant

Owner: Priya (product) · Draft 3 · Status: for review

## 1. Problem

Disrupted passengers wait 38 minutes on average for a rebooking decision. There are 240 cases a day, 11% of them codeshare (about 26 a day). Each case costs $9.40 (Q2 ticket export), which is about $2,256 a day.

## 2. Goal

Offer a stranded passenger a new flight and make the change when they accept, so that agents handle only the hard cases.

## 3. Users

- **Passengers** whose flight is cancelled, or delayed past a connection.
- **Contact-centre agents**, who take over when the assistant cannot finish.

## 4. Requirements

| # | The assistant must | Done when |
|---|---|---|
| R1 | Find alternative flights and offer the best ones | Up to 3 options shown within 60 seconds **[proposed]**, ranked by earliest arrival, then fewest stops **[proposed]** |
| R2 | Rebook same-day changes on our own flights | The change is made only after the passenger accepts, and a confirmation is sent |
| R3 | Handle codeshare flights where possible | Partner flights are rebooked where the partner allows it; all others go to an agent |
| R4 | Offer a refund when no sensible flight exists | Offered when no option arrives within 24 hours of the original arrival **[proposed]**, up to the Finance cap; above the cap goes to an agent |
| R5 | Hand over to an agent when unsure | The agent receives the itinerary, the options offered and the reason for handover, and does not need to ask the passenger again |
| R6 | Keep a record | Every offer, acceptance, change, refund and handover is logged; fields to be set by Compliance |

## 5. Success measures

| Measure | Today | Target |
|---|---|---|
| Time to a rebooking decision | 38 min | Under 5 min **[proposed]** |
| Cases finished with no agent | Not measured | 60% **[proposed]** |
| Wrong rebookings or refunds | Not measured | Under 1% of cases **[proposed]** |
| Cost per case | $9.40 | Set after the targets above are agreed |

## 6. Out of scope

Compensation claims. Group bookings. Rebooking onto a later day on our own flights goes to an agent (implied by "same-day"; please confirm).

## 7. Open questions

| Question | Owner | Blocks |
|---|---|---|
| What is the refund cap? | Finance | R4 |
| What must be logged, and for how long? | Compliance | R6 and launch |
| Which partners allow automated rebooking? | Not assigned | R3 |
| What exactly counts as "unsure"? | Priya | R5 |
| Which channel does the passenger use (app, web chat, SMS)? | Priya | R1, R2 |

## 8. Risks

- **A wrong rebooking leaves a passenger worse off.** Nothing changes without the passenger's acceptance, and any failed step goes to an agent.
- **Refunds without a cap.** R4 does not ship until Finance replies.
- **Logging gaps found after launch.** R6 does not ship until Compliance replies.

---

Three things to settle first, because they change the design and not only the numbers: the refund cap, the logging rules, and a precise rule for when the assistant hands over. The last two questions in section 7 (handover rule and channel) are ones I added; the PRD-lite does not mention them, but the build cannot start without them.
