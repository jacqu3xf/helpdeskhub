# 🎫 HelpDeskHub

**HelpDeskHub** is a lightweight Flask + Bootstrap ticketing system designed for a small IT/helpdesk environment. It gives end users a clean place to submit support requests while reps and admins can manage ticket queues, ownership, status changes, comments, and resolution history.

---

## 🚀 Project Overview

HelpDeskHub keeps support work centralized instead of letting requests get lost in email, chat, or hallway conversations. The system supports three main roles:

| Role | Purpose |
|---|---|
| **User** | Submit tickets, view their own tickets, and add comments. |
| **Rep** | View the support queue, claim tickets, update statuses, and respond to users. |
| **Admin** | Access the admin portal, manage users, review all tickets, and oversee the system. |

---

## ✨ Current Features

- User registration, login, and logout
- Role-based access for **User**, **Rep**, and **Admin**
- Dedicated admin login and admin portal
- Admin dashboard with system-level visibility
- Admin user-management page with account creation and role updates
- End-user ticket creation with title, description, category, and priority
- User-facing **My Tickets** page
- Rep/admin ticket queue with claim functionality
- Ticket comments for communication and updates
- Ticket status history/audit trail
- Controlled ticket status transitions
- Search and filtering for tickets
- Bootstrap-based responsive interface
- Visual badges for priority, category, and status

---

## 🎨 Ticket Status Colors

| Status | Badge Color |
|---|---|
| **New** | Red |
| **Open** | Orange |
| **In Progress** | Blue |
| **Waiting on User** | Green |
| **Resolved** | Purple |
| **Closed** | Black |

---

## 🔁 Ticket Workflow

The ticket workflow is flexible enough for testing but still has obvious restrictions so tickets do not jump around randomly.

Typical flow:

```text
New → Open → In Progress → Waiting on User → Resolved → Closed
```

Supported workflow behavior:

- New tickets start as **New**.
- Reps/admins can claim a ticket, which moves it to **Open**.
- Reps/admins can move work through **In Progress**, **Waiting on User**, **Resolved**, and **Closed**.
- Tickets waiting on the user can still be resolved or closed by a rep/admin.
- Status changes are written into ticket history for tracking.

---

## 🧰 Tech Stack

| Layer | Tool |
|---|---|
| Backend | Python + Flask |
| Database | SQLite with Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Forms | Flask-WTF |
| Frontend | Bootstrap 5 + custom CSS |
| Testing | Flask test client smoke test |

---

## 📁 Project Structure

```text
helpdeskhub/
├── app.py                         # Main Flask routes, app config, workflow logic
├── models.py                      # SQLAlchemy database models
├── forms.py                       # Flask-WTF form definitions
├── requirements.txt               # Python dependencies
├── smoke_test.py                  # Automated functionality check
├── TESTING_GUIDE.md               # Manual testing checklist
├── MERGE_NOTES.md                 # Notes from branch consolidation
├── CHANGE_NOTES_STATUS_BADGES.md  # Notes for latest status/category badge update
├── static/
│   └── styles.css                 # Custom UI styling and badge colors
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── ticket_new.html
    ├── ticket_detail.html
    ├── tickets_list.html
    ├── tickets_queue.html
    ├── admin_login.html
    ├── admin_dashboard.html
    ├── admin_users.html
    └── admin_tickets.html
```

---

## ⚙️ Setup Instructions

### 1. Create and activate a virtual environment

**Windows CMD or PowerShell:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the database

Start the app first:

```bash
python app.py
```

Then open this route in your browser:

```text
http://127.0.0.1:5000/init-db
```

This creates the SQLite database tables and seeds the default admin account.

---

## 🔐 Default Admin Login

```text
Admin URL: http://127.0.0.1:5000/admin/login
Email: admin@admin.com
Password: admin123
```

---

## ▶️ Running the App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## ✅ Running the Smoke Test

```bash
python smoke_test.py
```

Expected result:

```text
ALL TESTS PASSED
```

The smoke test performs a quick automated check of the main app flow. It uses a temporary in-memory test database, so it does **not** modify your real local database file.

---

## 🧪 What the Smoke Test Checks

The smoke test verifies that the most important pieces of the app still work after code changes:

- Public pages load correctly
- Default admin seeding works
- Test user and test rep accounts can be created
- User login works
- User can create a ticket
- New ticket starts with **New** status
- Rep login works
- Rep can access the queue
- Rep can claim a ticket
- Claiming a ticket changes status from **New** to **Open**
- Ticket history records the claim/status change
- Rep can move ticket to **In Progress**
- Rep can move ticket to **Waiting on User**
- Rep can move ticket from **Waiting on User** to **Resolved**
- Rep can move ticket from **Resolved** to **Closed**
- Admin login works
- Admin dashboard, users, tickets, and dashboard pages load
- Admin can create a new rep user

This does not replace full manual testing, but it gives a fast confidence check before committing or presenting the project.

---

## 📝 Latest Merge Notes

This model combines the extracted branch work into one definitive testing version.

Major updates included:

- Consolidated backend, database, admin, and UI changes
- Cleaned duplicate or conflicting route logic
- Removed unresolved merge conflict markers
- Added safe database initialization behavior
- Added dedicated admin portal flow
- Added admin user creation
- Added ticket history tracking
- Added status transition restrictions
- Added status and category badge styling
- Added smoke testing for core functionality

## 📌 Project Status

Current state: **Testing-ready**
