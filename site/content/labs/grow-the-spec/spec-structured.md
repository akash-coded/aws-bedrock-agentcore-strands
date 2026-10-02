# Spec · Rebooking assistant

## 3 Acceptance criteria
AC-1  WHEN a disrupted passenger requests rebooking AND a same-day seat exists
      THE SYSTEM SHALL present ranked alternatives WITHIN 30 seconds at P95.
AC-2  WHEN the passenger accepts a same-day SkyWays flight
      THE SYSTEM SHALL rebook and confirm to the passenger.
AC-3  WHEN the only available seat is on a partner flight
      THE SYSTEM SHALL hold the change for a veto window before it commits.
B-1   BOUNDARY  The system shall NEVER issue a refund above $400 without a named approver.
B-2   BOUNDARY  The system shall NEVER change a booking without the passenger's acceptance.

## 7 Fallback
F-1   WHEN the model cannot decide OR a tool fails
      THE SYSTEM SHALL hand the case to a contact-centre agent with the transcript.

## 8 Records
R-1   NOT DECIDED: what is logged for each action and for how long. Owner: compliance.
