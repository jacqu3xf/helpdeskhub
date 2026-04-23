HelpDeskHub (Flask + Bootstrap Ticketing System)

HelpDeskHub is a basic ticketing/helpdesk web app scaffold built with Flask, Bootstrap, SQLAlchemy (SQLite), Flask-Login, and Flask-WTF.


It supports:
 - User registration + login + logout
 - Roles (user / rep / admin)
 - Users can create tickets, view their own tickets, and comment
 - Reps/Admins can view the queue, claim tickets, update status (with basic transition rules), and comment
 - Simple Bootstrap UI

Tech Stack:
 - Python + Flask
 - Flask-SQLAlchemy (SQLite for local dev)
 - Flask-Login (sessions)
 - Flask-WTF (forms + CSRF protection)
 - Bootstrap 5 (CDN)

Folder Structure:
helpdeskhub/
 - app.py
 - models.py
 - forms.py
 - requirements.txt
 - templates/
 - static/

-----------------------
Setup
1) Create and activate a virtual environment and install dependencies:**

**Windows (CMD) - run terminal in root folder**
 - python -m venv .venv
 - .venv\\Scripts\\activate
 - pip install -r requirements.txt

**UNIX - terminal in folder**
 - python3 -m venv .venv
 - source .venv/bin/activate
 - pip install -r requirements.txt

**2) Run the app - from terminal**
 - python app.py

*Note: The app runs at: http://127.0.0.1:5000*

**3) Initialize the database (one-time per machine)**
Open:
 - http://127.0.0.1:5000/init-db

*Note: This creates the database tables and seeds a default admin account:*

**Default Admin:**
- Email: admin@admin.com
- Password: admin123


Merged repository notes:
- Added a dedicated /admin/login route and separate admin portal UI.
- Added admin dashboard, admin user management, and admin ticket review pages.
- Added ticket search/filter for end users and a card-style queue for reps/admins.
- Added TRACKING COMMENT markers in Python code where repo merge changes were introduced.

David's Test Changes:
