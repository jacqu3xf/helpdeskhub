# Status Transition and Badge Update Notes

## Workflow updates
- Admin and rep ticket status updates now show only the current status plus valid next statuses.
- `Waiting on User` can now move directly to:
  - `Open`
  - `In Progress`
  - `Resolved`
  - `Closed`
- `Open` and `In Progress` can also move to `Resolved` or `Closed` when appropriate.
- `Closed` tickets can be reopened to `Open`, but cannot jump to every other status.

## Visual updates
- Ticket status badges now use the requested color scheme:
  - New: red
  - Open: orange
  - In Progress: blue
  - Waiting on User: green
  - Resolved: purple
  - Closed: black with white font
- Category badges now have distinct colors similar to priority badges.
- Category badge coloring supports common categories/keywords including:
  - General
  - Hardware
  - Software
  - Network/Wi-Fi/Internet
  - Email/Outlook/Mail
  - Account/Login/Password/Access
  - Printer/Scanner
  - Security/MFA/Phishing

## Testing
- Smoke test was updated and passed.
- Added coverage for `Waiting on User -> Resolved` and `Resolved -> Closed`.
