# Testing Guide

## 1. Install dependencies
```bash
pip install -r requirements.txt
```

## 2. Start the app
```bash
python app.py
```

## 3. Initialize the database
Open this in the browser:

```text
http://127.0.0.1:5000/init-db
```

This creates the SQLite tables and seeds the default admin accounts.

## 4. Default admin login
```text
Email: admin@admin.com
Password: admin123
```

Legacy backup admin:

```text
Email: admin@example.com
Password: admin123
```

## 5. Manual test checklist
- Register a normal user.
- Log in as the normal user.
- Create a ticket with title, description, category, and priority.
- Confirm the ticket appears under Tickets.
- Log out.
- Log in as admin.
- Go to Users and create/promote a rep user.
- Log in as the rep.
- Go to Queue.
- Claim the new ticket.
- Confirm the ticket status changes from `New` to `Open`.
- Open the ticket detail page.
- Change status from `Open` to `In Progress`.
- Confirm the status-history section shows both changes.
- Log in as admin and confirm the dashboard/tickets/users pages still load.

## 6. Optional smoke test
A smoke-test script is included as `smoke_test.py`.

Run:

```bash
python smoke_test.py
```

Expected result:

```text
ALL TESTS PASSED
```
