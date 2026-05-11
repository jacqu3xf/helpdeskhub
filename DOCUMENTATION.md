# HelpDeskHub Detailed Documentation Guide

## 1. Project Overview

**HelpDeskHub** is a lightweight helpdesk and ticketing web application built with Flask, Bootstrap, SQLAlchemy, Flask-Login, and Flask-WTF. The purpose of the application is to centralize support requests so users can submit issues, IT representatives can manage and resolve those issues, and administrators can oversee the system from a dedicated admin portal.

The project is designed as a class/capstone-level software system. It focuses on practical helpdesk functionality instead of over-engineered enterprise features. The application supports user registration, secure login, role-based access, ticket creation, ticket queues, ticket claiming, ticket comments, controlled status transitions, status history tracking, admin user management, admin ticket review, dashboard metrics, and visual status/category/priority badges.

The final merged model combines the working backend, database/status-history updates, admin functionality, UI improvements, and README/testing updates into one testable version.

---

## 2. Core Purpose

The main problem HelpDeskHub solves is the lack of centralized visibility for support requests. Without a ticketing system, issues can get lost in emails, direct messages, verbal conversations, or scattered spreadsheets. HelpDeskHub gives each support issue a single place to live, a visible status, ownership through assignment, and a comment/status history that can be reviewed later.

The application is intended for three major groups:

1. **End Users**
   - Submit support tickets.
   - View their own tickets.
   - Add comments to their tickets.
   - Track ticket status.

2. **IT Representatives / Reps**
   - View support queues.
   - Claim unassigned tickets.
   - Update ticket status.
   - Add comments.
   - Review all tickets when needed.

3. **Administrators**
   - Access a dedicated admin dashboard.
   - Manage users and roles.
   - Create new user, rep, or admin accounts.
   - Review all tickets.
   - View dashboard metrics.
   - Manage tickets with rep-level capabilities.

---

## 3. Current Feature Set

### Authentication and Roles

HelpDeskHub includes role-based authentication through Flask-Login. Users authenticate with an email and password. Passwords are not stored in plain text; they are stored as password hashes using Werkzeug's password hashing functions.

Supported roles are:

| Role | Purpose |
|---|---|
| `user` | Standard end user who submits and tracks their own tickets. |
| `rep` | IT representative who can view queues, claim tickets, comment, and update statuses. |
| `admin` | Administrator with full visibility, user management, and admin dashboard access. |

### Ticket Creation

Logged-in users can create tickets using the `/tickets/new` route. A ticket includes:

- Title
- Description
- Category
- Priority
- Status
- Creator
- Assignee
- Created timestamp
- Updated timestamp

New tickets are created with:

```text
status = New
assigned_to = None
```

This means the ticket starts as unassigned and ready for a rep/admin to claim.

### Ticket Queue

Reps and admins can view the queue at `/queue`. The queue has three main views:

| Queue View | Meaning |
|---|---|
| `unassigned` | Tickets that do not have an assigned rep/admin. |
| `mine` | Tickets assigned to the current logged-in rep/admin. |
| `all` | All tickets in the system. |

The queue helps simulate a real IT helpdesk workflow where new issues first sit unassigned, then get claimed by available support staff.

### Ticket Claiming

A rep/admin can claim an unassigned ticket. When a ticket is claimed:

- `assigned_to` is set to the current rep/admin user's ID.
- If the ticket status is `New`, the status automatically changes to `Open`.
- A status history record is created showing the transition from `New` to `Open`.

This creates a clear audit trail showing when the ticket was picked up.

### Ticket Comments

Users, reps, and admins can comment on tickets they are allowed to access. Comments are stored separately from tickets and are linked by `ticket_id` and `user_id`.

Comments are useful for:

- Asking follow-up questions.
- Providing updates.
- Recording troubleshooting steps.
- Documenting resolution details.

### Ticket Status History

Ticket status changes are recorded in the `TicketHistory` table. Each history record stores:

- Ticket ID
- User ID
- Action type
- Old status
- New status
- Optional note
- Timestamp

This allows the system to show not just the current ticket state, but how it got there.

### Admin Portal

The admin portal is intentionally separated from the regular user experience. Admins can log in through `/admin/login`, and successful admin login redirects to `/admin`.

Admin features include:

- Dashboard summary metrics.
- User list.
- Staff user count.
- Ticket overview.
- Recent tickets.
- User role updates.
- New user creation.
- Ticket filtering by status and priority.

---

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language. |
| Flask | Web framework used for routes, requests, templates, and app structure. |
| Flask-SQLAlchemy | Database ORM used to define and interact with models. |
| SQLite | Local development database. |
| Flask-Login | Handles user sessions and login protection. |
| Flask-WTF | Handles secure forms and validation. |
| WTForms | Defines form fields and validation rules. |
| Bootstrap 5 | Frontend layout and responsive styling. |
| Custom CSS | Application-specific styling, badges, dashboard cards, and UI polish. |
| Werkzeug Security | Password hashing and password verification. |

---

## 5. Folder and File Structure

The current project structure is intentionally simple:

```text
helpdeskhub/
├── app.py
├── models.py
├── forms.py
├── requirements.txt
├── README.md
├── Guide.md
├── MERGE_NOTES.md
├── TESTING_GUIDE.md
├── CHANGE_NOTES_STATUS_BADGES.md
├── DETAILED_DOCUMENTATION.md
├── smoke_test.py
├── static/
│   └── styles.css
└── templates/
    ├── admin_dashboard.html
    ├── admin_login.html
    ├── admin_tickets.html
    ├── admin_users.html
    ├── base.html
    ├── dashboard.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── ticket_detail.html
    ├── ticket_new.html
    ├── tickets_list.html
    └── tickets_queue.html
```

### `app.py`

This is the main Flask application file. It handles:

- Flask app configuration.
- Database initialization.
- Login manager setup.
- Route definitions.
- Role checks.
- Ticket access rules.
- Ticket status transitions.
- Admin dashboard logic.
- Ticket creation.
- Ticket claiming.
- Ticket commenting.
- Ticket status updates.
- User management.
- Error handling.

Most of the application behavior is controlled here.

### `models.py`

This file defines the database models:

- `User`
- `Ticket`
- `Comment`
- `TicketHistory`

It also defines shared constants:

```python
ROLES = ["user", "rep", "admin"]
STATUSES = ["New", "Open", "In Progress", "Waiting on User", "Resolved", "Closed"]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]
```

### `forms.py`

This file defines Flask-WTF forms:

- `RegisterForm`
- `LoginForm`
- `TicketForm`
- `CommentForm`
- `StatusForm`
- `UserRoleForm`
- `AdminCreateUserForm`

Forms validate required fields, email format, password length, role values, and ticket content.

### `static/styles.css`

This file controls custom styling. It includes:

- Layout styling.
- Dashboard card styling.
- Button styling.
- Ticket cards.
- Priority badge colors.
- Category badge colors.
- Status badge colors.
- White status badge font overrides.
- Admin portal styling.

### `templates/`

This folder stores all HTML templates. Templates use Jinja2 syntax and Bootstrap classes.

### `smoke_test.py`

This script performs an automated health check of the application. It uses an in-memory SQLite database so the test does not modify the real local database.

---

## 6. Database Schema

### User Table

The `User` model represents anyone who can log into the application.

| Field | Type | Purpose |
|---|---|---|
| `id` | Integer primary key | Unique user ID. SQLite auto-increments this ID. |
| `name` | String | User display name. |
| `email` | String, unique | Login email. Must be unique. |
| `password_hash` | String | Hashed password. |
| `role` | String | User role: `user`, `rep`, or `admin`. |

Important methods:

| Method | Purpose |
|---|---|
| `set_password()` | Hashes and stores a password. |
| `check_password()` | Verifies login password against stored hash. |
| `is_rep_or_admin()` | Checks whether a user has support staff access. |

### Ticket Table

The `Ticket` model stores support requests.

| Field | Type | Purpose |
|---|---|---|
| `id` | Integer primary key | Unique ticket ID. SQLite auto-increments this ID. |
| `title` | String | Short summary of the issue. |
| `description` | Text | Full issue description. |
| `category` | String | Ticket category, such as Network, Hardware, Email, etc. |
| `priority` | String | Low, Medium, High, or Urgent. |
| `status` | String | Current ticket status. |
| `created_by` | Foreign key to User | User who created the ticket. |
| `assigned_to` | Foreign key to User | Rep/admin assigned to the ticket. Can be empty. |
| `created_at` | DateTime | When the ticket was created. |
| `updated_at` | DateTime | When the ticket was last updated. |

Relationships:

| Relationship | Purpose |
|---|---|
| `creator` | Links ticket to the user who created it. |
| `assignee` | Links ticket to the rep/admin assigned to it. |

### Comment Table

The `Comment` model stores comments on tickets.

| Field | Type | Purpose |
|---|---|---|
| `id` | Integer primary key | Unique comment ID. |
| `ticket_id` | Foreign key to Ticket | Ticket the comment belongs to. |
| `user_id` | Foreign key to User | User who wrote the comment. |
| `body` | Text | Comment content. |
| `created_at` | DateTime | When the comment was created. |

### TicketHistory Table

The `TicketHistory` model stores status-change audit history.

| Field | Type | Purpose |
|---|---|---|
| `id` | Integer primary key | Unique history record ID. |
| `ticket_id` | Foreign key to Ticket | Ticket that changed. |
| `user_id` | Foreign key to User | User who made the change. |
| `action` | String | Currently defaults to `status_change`. |
| `old_status` | String | Previous ticket status. |
| `new_status` | String | New ticket status. |
| `note` | Text | Optional note about the change. |
| `created_at` | DateTime | When the status change occurred. |

---

## 7. Status Workflow

The ticket workflow is designed to be flexible but controlled. Reps/admins should be able to handle realistic support situations, but the system should still prevent random jumps that do not make sense.

Current statuses:

| Status | Meaning |
|---|---|
| `New` | Ticket was created and has not yet been actively worked. |
| `Open` | Ticket has been acknowledged or claimed. |
| `In Progress` | Work is actively being performed. |
| `Waiting on User` | Support is waiting for a response, confirmation, or action from the user. |
| `Resolved` | The issue is considered fixed, but may not be formally closed yet. |
| `Closed` | Ticket is complete and closed out. |

### Allowed Status Transitions

Current transition rules are defined in `app.py` as `ALLOWED_TRANSITIONS`.

| Current Status | Allowed Next Statuses |
|---|---|
| `New` | `Open`, `In Progress` |
| `Open` | `In Progress`, `Waiting on User`, `Resolved`, `Closed` |
| `In Progress` | `Open`, `Waiting on User`, `Resolved`, `Closed` |
| `Waiting on User` | `Open`, `In Progress`, `Resolved`, `Closed` |
| `Resolved` | `Open`, `In Progress`, `Closed` |
| `Closed` | `Open` |

### Why These Rules Matter

These rules allow normal helpdesk behavior while still keeping the process understandable:

- A ticket can move from `New` to `Open` once it has been acknowledged.
- A ticket can move from `Open` to `In Progress` once active work starts.
- A ticket can move to `Waiting on User` when the support team needs the requester to respond.
- A ticket can move from `Waiting on User` directly to `Resolved` or `Closed` when enough information is provided or the issue is no longer active.
- A `Resolved` ticket can be reopened if needed.
- A `Closed` ticket can be reopened to `Open` if the issue comes back.

---

## 8. Badge Styling and Visual Status Design

The UI uses visual badges to make tickets easier to scan.

### Status Badge Colors

All status badges use white font for readability.

| Status | Color Meaning |
|---|---|
| `New` | Red |
| `Open` | Orange |
| `In Progress` | Blue |
| `Waiting on User` | Green |
| `Resolved` | Purple |
| `Closed` | Black with white font |

### Category Badge Logic

The app maps category text into visual category badge classes. This lets the system handle categories even if the user types slight variations.

Examples:

| Input Category Text | Badge Category |
|---|---|
| `Network`, `WiFi`, `Internet` | Network |
| `Hardware`, `Device`, `Laptop`, `Computer` | Hardware |
| `Software`, `Application`, `App` | Software |
| `Email`, `Outlook`, `Mail` | Email |
| `Account`, `Login`, `Password`, `Access` | Access |
| `Printer`, `Scanner`, `Print`, `Scan` | Printer |
| `Security`, `MFA`, `Phishing` | Security |
| Anything else | General |

This logic is handled by the `category_badge_class()` function in `app.py`.

---

## 9. Route Documentation

### Public Routes

| Route | Methods | Purpose |
|---|---|---|
| `/` | GET | Landing page. |
| `/register` | GET, POST | User registration. |
| `/login` | GET, POST | Standard login for users, reps, and admins. |
| `/admin/login` | GET, POST | Dedicated admin login page. |
| `/logout` | GET | Logs out current user. |
| `/init-db` | GET | Initializes database tables and seeds default admin accounts. |

### Ticket Routes

| Route | Methods | Access | Purpose |
|---|---|---|---|
| `/tickets` | GET | Logged-in users | Shows ticket list. Users see their own tickets; reps/admins see all tickets. |
| `/tickets/new` | GET, POST | Logged-in users | Creates a new ticket. |
| `/tickets/<ticket_id>` | GET, POST | Ticket owner, rep, admin | Shows ticket detail, comments, status form, and history. |
| `/tickets/<ticket_id>/claim` | POST | Rep/admin | Claims an unassigned ticket. |
| `/queue` | GET | Rep/admin | Shows queue views for support staff. |

### Dashboard Routes

| Route | Methods | Access | Purpose |
|---|---|---|---|
| `/dashboard` | GET | Logged-in users | Shows dashboard metrics. Users see their own tickets; reps/admins see all tickets. |
| `/admin` | GET | Admin only | Admin dashboard. |
| `/admin/users` | GET, POST | Admin only | Manage roles and create users. |
| `/admin/tickets` | GET | Admin only | Admin ticket review and filtering. |

---

## 10. Role-Based Access Rules

### Standard Users

A standard user can:

- Register.
- Log in.
- Create tickets.
- View their own tickets.
- Comment on their own tickets.
- View their dashboard.

A standard user cannot:

- View other users' tickets.
- Access the rep queue.
- Claim tickets.
- Update ticket statuses.
- Access admin pages.
- Create users.
- Change roles.

### Reps

A rep can:

- Log in.
- Access the queue.
- View all tickets.
- Claim unassigned tickets.
- Update ticket status.
- Comment on tickets.
- View dashboard metrics.

A rep cannot:

- Access admin-only pages.
- Create users through the admin portal.
- Change user roles.

### Admins

An admin can:

- Log in through regular login or admin login.
- Access the admin dashboard.
- View all tickets.
- Claim and update tickets.
- Comment on tickets.
- Create users.
- Change user roles.
- View admin ticket filters.

An admin is prevented from accidentally removing their own admin access through the user role form.

---

## 11. Database Initialization

The `/init-db` route performs two major actions:

1. Runs `db.create_all()` to create database tables if they do not already exist.
2. Runs `seed_admin_users()` to seed default admin accounts.

Default admin credentials:

```text
Email: admin@admin.com
Password: admin123
```

A legacy admin account may also be seeded for compatibility:

```text
Email: admin@example.com
Password: admin123
```

### Important Note About Re-Running `/init-db`

The seeding logic has been patched to safely handle repeated `/init-db` runs. Earlier versions could fail with this error:

```text
IntegrityError: UNIQUE constraint failed: user.email
```

The current version checks for existing admin accounts first and uses rollback handling if a duplicate insert is attempted.

---

## 12. Local Setup Guide

### Step 1: Open Terminal

Use a normal terminal. Administrator mode is not required for normal setup.

On Windows, use Command Prompt or PowerShell.

### Step 2: Move Into the Project Folder

Example:

```bash
cd %USERPROFILE%\Downloads\helpdeskhub
```

PowerShell alternative:

```powershell
cd $env:USERPROFILE\Downloads\helpdeskhub
```

### Step 3: Create a Virtual Environment

Windows Command Prompt:

```bash
python -m venv .venv
.venv\Scripts\activate
```

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, use Command Prompt instead or temporarily adjust PowerShell execution policy for the current process.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Smoke Test

```bash
python smoke_test.py
```

Expected result:

```text
ALL TESTS PASSED
```

### Step 6: Run the App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

### Step 7: Initialize the Database

Open this once in the browser:

```text
http://127.0.0.1:5000/init-db
```

Then log in with:

```text
admin@admin.com
admin123
```

---

## 13. Smoke Test Explanation

The smoke test is a quick automated check that verifies the most important parts of the app still work after changes.

The test file is:

```text
smoke_test.py
```

It uses this database setting:

```python
os.environ["HELPDESKHUB_DATABASE_URI"] = "sqlite:///:memory:"
```

That means it creates a temporary database in memory. It does not modify the real local SQLite database file.

### What the Smoke Test Checks

The smoke test verifies:

1. The app starts in testing mode.
2. Database tables can be created.
3. Default admin users can be seeded.
4. Test user and test rep accounts can be created.
5. Public pages load correctly.
6. A regular user can log in.
7. A user can create a ticket.
8. A new ticket starts with `New` status.
9. A rep can log in.
10. A rep can access the queue.
11. A rep can claim a ticket.
12. Claiming a `New` ticket changes it to `Open`.
13. Ticket history records the claim/status change.
14. A rep can update status to `In Progress`.
15. A rep can update status to `Waiting on User`.
16. A rep can update from `Waiting on User` to `Resolved`.
17. A rep can update from `Resolved` to `Closed`.
18. Ticket history count increases correctly.
19. Admin login works.
20. Admin dashboard pages load.
21. Admin can create a new rep user.

### What the Smoke Test Does Not Check

The smoke test is useful, but it is not a full test suite. It does not fully check:

- Every visual design element.
- Browser rendering details.
- CSS caching behavior.
- Every possible invalid form submission.
- Every possible permission edge case.
- Production deployment.
- Multi-user concurrency.

For this project, the smoke test is still valuable because it catches major breakages quickly.

---

## 14. Manual Testing Checklist

After running `python app.py`, manually test the following.

### Public Pages

- Open `/`.
- Open `/login`.
- Open `/register`.
- Open `/admin/login`.

Expected result: all pages load without errors.

### User Flow

1. Register a new user.
2. Log in as that user.
3. Create a new ticket.
4. Confirm the ticket appears under `/tickets`.
5. Open the ticket detail page.
6. Add a comment.
7. Confirm the comment appears.

### Rep Flow

1. Log in as a rep account.
2. Open `/queue`.
3. Confirm unassigned tickets appear.
4. Claim a ticket.
5. Confirm the assignee is updated.
6. Confirm status changes from `New` to `Open`.
7. Update status to `In Progress`.
8. Update status to `Waiting on User`.
9. Update status to `Resolved`.
10. Update status to `Closed`.
11. Confirm history appears on the ticket detail page.

### Admin Flow

1. Log in at `/admin/login`.
2. Confirm redirect to `/admin`.
3. Open `/admin/users`.
4. Create a new rep user.
5. Change a user's role.
6. Confirm admin cannot remove their own admin role.
7. Open `/admin/tickets`.
8. Filter by status.
9. Filter by priority.

### UI Validation

Confirm the status badges use these colors and white font:

- New: red
- Open: orange
- In Progress: blue
- Waiting on User: green
- Resolved: purple
- Closed: black

If badge colors do not update, hard refresh the browser:

```text
Ctrl + F5
```

---

## 15. Troubleshooting Guide

### Issue: `IntegrityError: UNIQUE constraint failed: user.email`

Cause: The app attempted to seed an admin account that already existed.

Current status: This has been patched. The seed function now checks existing admin users and safely handles duplicates.

If the local database is already in a bad state, stop the app and delete:

```text
instance/helpdeskhub.db
```

Then rerun:

```text
http://127.0.0.1:5000/init-db
```

### Issue: Badge Text Still Is Not White

Cause: Browser cached the old CSS.

Fix:

```text
Ctrl + F5
```

Also confirm that `templates/base.html` is loading the updated CSS file and `static/styles.css` contains the status badge white font override.

### Issue: App Does Not Start Because Flask Is Missing

Cause: Dependencies are not installed in the active Python environment.

Fix:

```bash
pip install -r requirements.txt
```

### Issue: `python` Command Not Found

Cause: Python may not be installed or added to PATH.

Fix:

Use:

```bash
py app.py
```

or reinstall Python and check the option to add Python to PATH.

### Issue: PowerShell Blocks `.venv` Activation

Cause: PowerShell execution policy blocks script activation.

Quick workaround: use Command Prompt instead.

Alternative PowerShell command:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### Issue: GitHub Rejects Push to `main`

Cause: Protected branch rule prevents direct pushes.

Fix: Push to a feature branch and open a pull request.

```bash
git checkout -b documentation-update
git push origin documentation-update
```

Then open a PR from `documentation-update` into `main`.

---

## 16. Git Workflow for Future Changes

Because `main` is protected, future work should follow this workflow.

### Step 1: Update Local Main

```bash
git checkout main
git pull origin main
```

### Step 2: Create a New Branch

```bash
git checkout -b documentation-update
```

Use a clear branch name depending on the work:

```text
documentation-update
status-workflow-fix
admin-dashboard-polish
sla-tracking-feature
```

### Step 3: Make Changes

Edit files locally.

### Step 4: Review Changed Files

```bash
git status
```

### Step 5: Stage Changes

```bash
git add .
```

### Step 6: Commit Changes

```bash
git commit -m "Add detailed HelpDeskHub documentation"
```

### Step 7: Push Branch

```bash
git push origin documentation-update
```

### Step 8: Open Pull Request

On GitHub:

```text
base: main
compare: documentation-update
```

### Step 9: Merge Pull Request

If branch protection requires approval, another teammate must approve unless rules are temporarily adjusted.

For simple documentation commits, `Squash and merge` is usually the cleanest option.

---

## 17. Recommended Pull Request Description for This Documentation

When committing this documentation later, use a pull request title like:

```text
Add detailed HelpDeskHub project documentation
```

Suggested PR description:

```text
This pull request adds a detailed documentation guide for the final HelpDeskHub model.

Included documentation:
- Project overview and purpose
- Technology stack
- File and folder structure
- Database schema
- Role-based access rules
- Ticket workflow and status transitions
- Admin portal behavior
- Badge/category styling explanation
- Route documentation
- Local setup instructions
- Smoke test explanation
- Manual testing checklist
- Troubleshooting guide
- Git workflow for protected main branch
```

Suggested commit message:

```bash
git commit -m "Add detailed HelpDeskHub documentation guide"
```

---

## 18. Current Known Limitations

The current version is strong for a class/capstone MVP, but it is not a production enterprise helpdesk system yet.

Current limitations include:

- No email notifications.
- No file attachments.
- No password reset flow.
- No SLA timer engine yet.
- No due dates.
- No ticket escalation rules.
- No advanced search filters.
- No pagination for large ticket/user lists.
- No API endpoints.
- No deployment configuration for production hosting.
- Secret key is still a development placeholder.
- SQLite is fine for local/class use, but not ideal for production multi-user deployment.

---

## 19. Recommended Future Enhancements

### SLA Tracking

Future SLA work should use ticket status history instead of only the current ticket status. This is important because SLA time may depend on when a ticket entered or left certain statuses.

Example future SLA ideas:

- Track time from `New` to `Open`.
- Track time from `Open` to `Resolved`.
- Pause SLA while `Waiting on User`.
- Show SLA warning badges.
- Add due-by timestamps.
- Add dashboard metrics for overdue tickets.

### Attachments

Allow users to upload screenshots, logs, or documents when creating or commenting on tickets.

### Notifications

Send email notifications when:

- A ticket is created.
- A ticket is assigned.
- A ticket status changes.
- A comment is added.
- A ticket is resolved or closed.

### Better Admin Controls

Future admin features could include:

- Disable user accounts.
- Reset user passwords.
- Assign tickets manually.
- Change ticket priority.
- Change ticket category.
- Export tickets to CSV.

### Improved Reporting

Add dashboard charts for:

- Tickets by status.
- Tickets by priority.
- Tickets by category.
- Average time to resolution.
- Tickets resolved this week.
- Open tickets by assignee.

---

## 20. Presentation Summary

For a presentation, HelpDeskHub can be summarized like this:

HelpDeskHub is a Flask and Bootstrap-based ticketing system that gives end users a simple way to submit support requests while giving IT reps and admins a structured workflow for tracking, assigning, updating, and resolving tickets. The system includes role-based access, admin controls, ticket comments, controlled status transitions, status history, dashboard metrics, and visual badges for readability. The final version combines the project branches into one stable model and includes a smoke test to quickly verify that the major workflows still function correctly.

---

## 21. Key Talking Points for Demo

Use these during a live demo:

1. Show the landing page and explain the purpose of the app.
2. Log in as a standard user.
3. Create a ticket.
4. Show that the user can only see their own tickets.
5. Log in as a rep.
6. Open the queue and claim the ticket.
7. Show automatic `New` to `Open` transition.
8. Update the ticket through the workflow.
9. Show status history on the ticket detail page.
10. Log in as admin.
11. Show the admin dashboard.
12. Show user management.
13. Create a rep account.
14. Show ticket filtering in admin ticket review.
15. Mention the smoke test and how it validates the main workflows.

---

## 22. Final Notes

This documentation should be committed with the final project because it explains not only how to run the application, but also why the application is structured the way it is. It gives future contributors enough context to understand the codebase, test it, troubleshoot it, and continue building features such as SLA tracking, attachments, notifications, and reporting.
