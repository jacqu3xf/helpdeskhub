# HelpDeskHub Definitive Testing Model - Merge Notes

## Purpose
This version consolidates the uploaded branch ZIPs into one clean Flask/Bootstrap model for testing before anything is committed to `main`.

## Branch inputs reviewed
- `helpdeskhub-main.zip`
- `helpdeskhub-replace-main-working.zip`
- `helpdeskhub-Backend-Database.zip`
- `helpdeskhub-backend-batabase-update.zip`
- `helpdeskhub-backend-batabase-update (1).zip`
- `helpdeskhub-Iris-s-Branch-admin-functionality.zip`
- `helpdeskhub-Iris-s-Branch-admin-functionality (1).zip`
- `helpdeskhub-merged-ui-admin-update.zip`

## Main merge decisions
- Used the working backend structure as the stability base.
- Preserved the improved Bootstrap UI/admin dashboard styling from the UI/admin branch.
- Removed unresolved Git conflict markers from the UI/admin branch.
- Removed the bundled `.venv` from the final project package.
- Consolidated duplicate route definitions into one clean `app.py`.
- Standardized admin login and normal login behavior.
- Added admin dashboard as the default landing page for admin users.
- Kept default admin credentials aligned with the README: `admin@admin.com` / `admin123`.
- Preserved a legacy admin seed account: `admin@example.com` / `admin123`.

## Functional fixes included
- Fixed broken `admin_portal` redirect references by routing admin users to `admin_dashboard`.
- Fixed broken status-history code that referenced undefined variables/classes.
- Added a clean `TicketHistory` model with `old_status`, `new_status`, `action`, `note`, `created_at`, and user/ticket relationships.
- Status updates now save into the ticket history table.
- Ticket claiming now opens a `New` ticket and logs that status change.
- Added `updated_at` to tickets for cleaner tracking.
- Added admin-side user creation directly inside `/admin/users`.
- Preserved role management for user/rep/admin.
- Preserved ticket filters by status and priority.
- Preserved user-side ticket search and status filtering.

## Tested flows
The included smoke test validates:
- Public pages load.
- Normal user login redirects to tickets.
- Normal user can create a ticket.
- Rep login redirects to queue.
- Rep can claim a ticket.
- Claiming a ticket changes status from `New` to `Open` and records history.
- Rep can update ticket status to `In Progress` and records history.
- Admin login redirects to admin dashboard.
- Admin dashboard, users page, tickets page, and dashboard page load.
- Admin can create a new rep user.

## Known notes before committing
- This is a consolidated testing model, not yet pushed to GitHub.
- The app uses SQLite and `db.create_all()` through `/init-db`; there are no formal database migrations yet.
- `SECRET_KEY` is still a development placeholder and should be replaced before any production-style deployment.
- CSRF is enabled for normal Flask-WTF forms; the smoke test disables CSRF only inside the test configuration.

## Patch: init-db duplicate admin fix
- Fixed `/init-db` crashing when it was run more than once against an existing database.
- `seed_admin_users()` now checks for existing admin emails without triggering premature autoflush.
- Existing seeded users are preserved and promoted back to admin if needed.
- Duplicate insert attempts are safely rolled back instead of breaking the app.
