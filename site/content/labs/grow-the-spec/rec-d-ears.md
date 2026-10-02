## Acceptance criteria in EARS

**Offering alternatives**

**AC-1.** WHEN a passenger asks to change a flight AND at least one alternative flight is available THE SYSTEM SHALL show the alternative flights to the passenger WITHIN 30 seconds of the request.

**Rebooking**

**AC-2.** WHEN the passenger accepts an offered alternative AND the alternative departs on the same calendar day as the original flight AND neither flight is a partner flight THE SYSTEM SHALL rebook the passenger and show a confirmation WITHIN <MEASURE MISSING: M1>.

- BOUNDARY: THE SYSTEM SHALL NOT rebook a passenger who has not explicitly accepted the alternative.
- BOUNDARY: THE SYSTEM SHALL NOT rebook a change that is not same-day.

**Partner flights**

**AC-3.** WHEN the passenger accepts an offered alternative AND the original or the new flight is a partner flight THE SYSTEM SHALL send the proposed change to the contact centre and hold it uncommitted WITHIN <MEASURE MISSING: M2>.

**AC-4.** WHEN the hold window of <MEASURE MISSING: M3> has ended AND the contact centre has not stopped the change THE SYSTEM SHALL complete the rebooking and show a confirmation WITHIN <MEASURE MISSING: M4>.

**AC-5.** WHEN the contact centre stops a held change AND the hold window has not ended THE SYSTEM SHALL cancel the change, keep the original booking and tell the passenger WITHIN <MEASURE MISSING: M5>.

**AC-6.** WHEN the proposed change cannot be delivered to the contact centre AND the change involves a partner flight THE SYSTEM SHALL keep the original booking and hand the conversation to a human agent WITHIN <MEASURE MISSING: M6>.

- BOUNDARY: THE SYSTEM SHALL NOT commit a partner-flight change before the hold window has ended.
- BOUNDARY: THE SYSTEM SHALL NOT commit a partner-flight change that the contact centre has stopped.

**Refunds**

**AC-7.** WHEN the passenger has no acceptable alternative (none found, or all declined) AND the refund amount is $400.00 or less THE SYSTEM SHALL offer the refund to the passenger WITHIN <MEASURE MISSING: M7>.

**AC-8.** WHEN the passenger has no acceptable alternative AND the refund amount is more than $400.00 THE SYSTEM SHALL send the refund for sign-off and tell the passenger it is pending WITHIN <MEASURE MISSING: M8>.

**AC-9.** WHEN sign-off is recorded AND the refund amount is more than $400.00 THE SYSTEM SHALL offer the refund to the passenger WITHIN <MEASURE MISSING: M9>.

- BOUNDARY: THE SYSTEM SHALL NOT offer a refund while an offered alternative has not been declined.
- BOUNDARY: THE SYSTEM SHALL NOT offer or pay a refund of more than $400.00 without recorded sign-off.

**Handover**

**AC-10.** WHEN the assistant's confidence in its next action is below <MEASURE MISSING: M10> AND the conversation is still open THE SYSTEM SHALL hand the conversation, with its full history, to a human agent WITHIN <MEASURE MISSING: M11>.

- BOUNDARY: THE SYSTEM SHALL NOT rebook, refund or commit any change while its confidence is below the threshold.

## Vague terms removed and what replaced them

| # | Removed | Where | Replaced by |
|---|---|---|---|
| 1 | should | offer alternatives | SHALL in AC-1 |
| 2 | quickly | offer alternatives | 30 seconds in AC-1 |
| 3 | ideally | 30 seconds | hard limit of 30 seconds in AC-1 |
| 4 | about | 30 seconds | exactly 30 seconds in AC-1 |
| 5 | should | rebook | SHALL in AC-2 |
| 6 | should | partner flights | SHALL in AC-3 |
| 7 | where possible | partner flights | AC-3 always holds the change; AC-6 covers the case where the contact centre cannot be reached |
| 8 | may | refunds | SHALL in AC-7, split at $400.00 into AC-7, AC-8 and AC-9 |
| 9 | should | hand over | SHALL in AC-10 |
| 10 | as appropriate | hand over | hard condition in AC-10: always hand over below the threshold |
| 11 | unsure | hand over | a confidence threshold in AC-10 (value missing, M10) |

Terms 2, 4 and 11 were not on your list, but they are just as vague, so I removed them too.

## Choices I made that you should confirm

The original left these open, and each one changes behaviour:

1. **30 seconds is now a hard limit.** The original said "ideally within about". If 30 seconds was a target and the real limit is higher, change AC-1.
2. **"Where possible" now fails closed.** In AC-6, if the contact centre cannot be reached, the change does not go through. The other reading is that the change proceeds unreviewed. That is your call, not mine.
3. **"May" is now "always".** AC-7 offers the refund every time no flight works. If refunds are meant to be optional, I need the rule that decides.
4. **The trigger in AC-1 is assumed.** The original never says what starts the offer. I used "passenger asks to change a flight". A cancelled or delayed flight may be a second trigger.
5. **"Same-day" means the same calendar day at the departure airport.** The original does not say what happens to changes that are not same-day; I only wrote the prohibition.
6. **"Over $400" means more than $400.00.** A refund of exactly $400.00 needs no sign-off.
7. **Still unanswered:** who gives sign-off, what happens when sign-off is refused or never arrives, and what counts as a partner flight.

## Summary

**(a) Vague terms removed: 11.** Eight are from your list (should ×4, ideally, where possible, may, as appropriate). Three are extra (quickly, about, unsure).

**(b) Missing measures: 11.**

- M1 (AC-2): time from acceptance to confirmed rebooking
- M2 (AC-3): time to send the proposed change to the contact centre
- M3 (AC-4): length of the hold window the contact centre gets to stop a change
- M4 (AC-4): time to complete the rebooking after the hold window ends
- M5 (AC-5): time to cancel a stopped change and tell the passenger
- M6 (AC-6): time to hand over when the contact centre cannot be reached
- M7 (AC-7): time to offer a refund of $400.00 or less
- M8 (AC-8): time to send a refund over $400.00 for sign-off
- M9 (AC-9): time to offer the refund after sign-off
- M10 (AC-10): confidence threshold that defines "unsure"
- M11 (AC-10): time to complete the handover to a human agent
