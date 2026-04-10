HelpDeskHub is a basic Flask + Bootstrap ticketing system scaffold that supports user registration/login, ticket creation, ticket viewing, comments, and a rep/admin queue for managing tickets. It uses SQLite via Flask-SQLAlchemy for persistence and Flask-Login for session-based authentication. The UI is rendered with Jinja templates styled by Bootstrap CDN, with a simple top navigation that changes depending on whether a user is logged in and what role they have.



###### **Core behavior:**



* Users can register and log in. Passwords are stored as hashed values (Werkzeug) and verified at login. Session state is handled by Flask-Login (login\_required, current\_user).
* A one-time “/init-db” route creates the database tables and seeds a default admin account (admin@example.com
* &#x20;/ admin123) if one doesn’t exist.
* Tickets can be created by any authenticated user. Each ticket stores a title, description, category, priority, status, creator, optional assignee, and creation timestamp.

* **Ticket visibility is role-based:**

  * Standard users see only tickets they created.
  * Reps/Admins can view all tickets (and use the queue views).

* Ticket detail pages show the description, current status, assignment, and a comment thread.
* Users can comment on tickets they can access; reps/admins can comment on any ticket.

* **Reps/Admins have a “Queue” page with three filters:**

  * Unassigned tickets
  * Assigned-to-me tickets
  * All tickets

* Reps/Admins can “Claim” an unassigned ticket, which assigns it to themselves and moves status from New → Open automatically.
* Reps/Admins can update ticket status using a dropdown. The app enforces basic status transition rules using an ALLOWED\_TRANSITIONS map (prevents random jumps like New → Closed).



###### **File-by-file summary:**



* app.py: Main Flask app, route definitions, role/permission helpers, allowed status transitions, login/register flow, ticket creation, ticket detail actions (comment/claim/status), and the queue page.
* models.py: SQLAlchemy models for User, Ticket, Comment. Includes password hashing helpers on User and relationships for creator/assignee and comment threading.
* forms.py: Flask-WTF forms for register, login, ticket creation, ticket commenting, and status updates.
* templates/\*.html: Bootstrap-based UI pages (base layout + individual screens).
* static/styles.css: Placeholder stylesheet (currently minimal).



###### **Known limitations (by design):**



* No “edit ticket” or “delete ticket” support.
* No ability for admins to manage users/roles from the UI (roles are currently in the DB only).
* No assignment to a different rep (only claim-to-self).
* No status history/audit log (only the current status is stored).
* No attachments, tags, SLA/overdue logic, or notifications.
* The /init-db route is not locked down (fine for dev; should be removed/secured in production).

