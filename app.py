from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import or_

from models import db, User, Ticket, Comment
from forms import RegisterForm, LoginForm, TicketForm, CommentForm, StatusForm, UserRoleForm, AdminCreateUserForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdeskhub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# TRACKING COMMENT: status workflow kept from both repositories and preserved in one place.
ALLOWED_TRANSITIONS = {
    "New": {"Open", "In Progress"},
    "Open": {"In Progress", "Waiting on User", "Resolved"},
    "In Progress": {"Waiting on User", "Resolved"},
    "Waiting on User": {"Open", "In Progress"},
    "Resolved": {"Closed", "Open"},
    "Closed": set(),
}


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def rep_required():
    if not current_user.is_authenticated or not current_user.is_rep_or_admin():
        abort(403)


def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)


def can_view_ticket(ticket: Ticket) -> bool:
    if current_user.role in ["rep", "admin"]:
        return True
    return ticket.created_by == current_user.id


def can_comment_ticket(ticket: Ticket) -> bool:
    if current_user.role in ["rep", "admin"]:
        return True
    return ticket.created_by == current_user.id


def can_update_ticket(ticket: Ticket) -> bool:
    return current_user.role in ["rep", "admin"]


def get_dashboard_counts(tickets):
    status_counts = {}
    priority_counts = {}
    for ticket in tickets:
        status_counts[ticket.status] = status_counts.get(ticket.status, 0) + 1
        priority_counts[ticket.priority] = priority_counts.get(ticket.priority, 0) + 1
    return status_counts, priority_counts


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/init-db")
def init_db():
    db.create_all()

    # TRACKING COMMENT: repo README now documents admin@admin.com, so the seed user matches that contract.
    admin = User.query.filter_by(email="admin@admin.com").first()
    if not admin:
        admin = User(name="Primary Admin", email="admin@admin.com", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)

    # TRACKING COMMENT: keep backwards compatibility with earlier seeded admin account if it already existed.
    legacy_admin = User.query.filter_by(email="admin@example.com").first()
    if not legacy_admin:
        legacy_admin = User(name="Legacy Admin", email="admin@example.com", role="admin")
        legacy_admin.set_password("admin123")
        db.session.add(legacy_admin)

    db.session.commit()
    flash("Database initialized. Default admin: admin@admin.com / admin123", "success")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if existing:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            role="user",
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))

        login_user(user)
        flash("Logged in.", "success")

        # TRACKING COMMENT: admins get routed to a separate admin area instead of blending into the user UI.
        if user.role == "admin":
            return redirect(url_for("admin_portal"))
        elif user.role == "rep":
            return redirect(url_for("tickets_queue"))
        else:
            return redirect(url_for("tickets_list"))

    return render_template("login.html", form=form, title="User Login")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if not user or not user.check_password(form.password.data) or user.role != "admin":
            flash("Admin credentials were not accepted.", "danger")
            return redirect(url_for("admin_login"))

        login_user(user)
        flash("Admin login successful.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin_login.html", form=form, title="Admin Login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("index"))


@app.route("/tickets")
@login_required
def tickets_list():
    query = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "").strip()

    tickets_query = Ticket.query
    if current_user.role not in ["rep", "admin"]:
        tickets_query = tickets_query.filter_by(created_by=current_user.id)

    if query:
        tickets_query = tickets_query.filter(
            or_(
                Ticket.title.ilike(f"%{query}%"),
                Ticket.description.ilike(f"%{query}%"),
                Ticket.category.ilike(f"%{query}%"),
            )
        )

    if status_filter:
        tickets_query = tickets_query.filter_by(status=status_filter)

    tickets = tickets_query.order_by(Ticket.created_at.desc()).all()
    return render_template(
        "tickets_list.html",
        tickets=tickets,
        query=query,
        status_filter=status_filter,
        statuses=list(ALLOWED_TRANSITIONS.keys()),
    )


@app.route("/tickets/new", methods=["GET", "POST"])
@login_required
def ticket_new():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            category=(form.category.data.strip() if form.category.data else "General"),
            priority=form.priority.data,
            status="New",
            created_by=current_user.id,
            assigned_to=None,
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket created.", "success")
        return redirect(url_for("tickets_list"))

    return render_template("ticket_new.html", form=form)


@app.route("/queue")
@login_required
def tickets_queue():
    rep_required()

    view = request.args.get("view", "unassigned")
    if view == "mine":
        tickets = (
            Ticket.query.filter_by(assigned_to=current_user.id)
            .order_by(Ticket.created_at.desc())
            .all()
        )
    elif view == "all":
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        tickets = (
            Ticket.query.filter(Ticket.assigned_to.is_(None))
            .order_by(Ticket.created_at.desc())
            .all()
        )

    unassigned_count = Ticket.query.filter(Ticket.assigned_to.is_(None)).count()
    mine_count = Ticket.query.filter_by(assigned_to=current_user.id).count()
    closed_count = Ticket.query.filter_by(status="Closed").count()

    return render_template(
        "tickets_queue.html",
        tickets=tickets,
        view=view,
        unassigned_count=unassigned_count,
        mine_count=mine_count,
        closed_count=closed_count,
    )


@app.route("/tickets/<int:ticket_id>/claim", methods=["POST"])
@login_required
def claim_ticket(ticket_id):
    rep_required()
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.assigned_to is None:
        ticket.assigned_to = current_user.id
        if ticket.status == "New":
            ticket.status = "Open"
        db.session.commit()
        flash("Ticket claimed.", "success")
    else:
        flash("Ticket is already assigned.", "warning")

    return redirect(request.referrer or url_for("ticket_detail", ticket_id=ticket.id))


@app.route("/tickets/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not can_view_ticket(ticket):
        abort(403)

    comment_form = CommentForm()
    status_form = StatusForm()
    status_form.status.data = ticket.status

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "comment":
            if not can_comment_ticket(ticket):
                abort(403)
            if comment_form.validate_on_submit():
                comment = Comment(
                    ticket_id=ticket.id,
                    user_id=current_user.id,
                    body=comment_form.body.data.strip(),
                )
                db.session.add(comment)
                db.session.commit()
                flash("Comment added.", "success")
            return redirect(url_for("ticket_detail", ticket_id=ticket.id))

        if action == "claim":
            if not can_update_ticket(ticket):
                abort(403)
            if ticket.assigned_to is None:
                ticket.assigned_to = current_user.id
                if ticket.status == "New":
                    ticket.status = "Open"
                db.session.commit()
                flash("Ticket claimed.", "success")
            else:
                flash("Ticket already assigned.", "warning")
            return redirect(url_for("ticket_detail", ticket_id=ticket.id))

        if action == "status":
            if not can_update_ticket(ticket):
                abort(403)
            new_status = request.form.get("status")
            if new_status and new_status != ticket.status:
                allowed = ALLOWED_TRANSITIONS.get(ticket.status, set())
                if new_status not in allowed:
                    flash(f"Invalid transition: {ticket.status} → {new_status}", "danger")
                else:
                    # Log History - Updated
                    history_comment = Comment(
                        ticket_id=ticket.id,
                        user_id=current_user.id,
                        action="Status Changed",
                        old_value = ticket.status,
                        new_value = new_status
                    )
                    db.session.add(history_comment)
                    # Updates the ticket status
                    ticket.status = new_status
                    db.session.commit()
                    flash(f"Status updated to {new_status}.", "success")
            return redirect(url_for("ticket_detail", ticket_id=ticket.id))

        flash("Unknown action.", "warning")
        return redirect(url_for("ticket_detail", ticket_id=ticket.id))

    return render_template(
        "ticket_detail.html",
        ticket=ticket,
        comment_form=comment_form,
        status_form=status_form,
    )


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role in ["rep", "admin"]:
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        tickets = (
            Ticket.query.filter_by(created_by=current_user.id)
            .order_by(Ticket.created_at.desc())
            .all()
        )

    status_counts, priority_counts = get_dashboard_counts(tickets)
    return render_template(
        "dashboard.html",
        tickets=tickets,
        status_counts=status_counts,
        priority_counts=priority_counts,
    )


@app.route("/admin")
@login_required
def admin_portal():
    admin_required()
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    users = User.query.order_by(User.role.desc(), User.name.asc()).all()

    status_counts, priority_counts = get_dashboard_counts(tickets)
    stats = {
        "total_tickets": len(tickets),
        "open_tickets": sum(1 for t in tickets if t.status in ["New", "Open", "In Progress", "Waiting on User"]),
        "resolved_tickets": sum(1 for t in tickets if t.status in ["Resolved", "Closed"]),
        "total_users": len(users),
        "staff_users": sum(1 for u in users if u.role in ["rep", "admin"]),
        "unassigned_tickets": sum(1 for t in tickets if t.assigned_to is None),
    }
    return render_template(
        "admin_dashboard.html",
        tickets=tickets[:8],
        users=users[:8],
        status_counts=status_counts,
        priority_counts=priority_counts,
        stats=stats,
    )


@app.route("/admin/users", methods=["GET", "POST"])
@login_required
def admin_users():
    admin_required()
    users = User.query.order_by(User.role.desc(), User.name.asc()).all()
    role_form = UserRoleForm()

    if role_form.validate_on_submit():
        target = User.query.get_or_404(int(role_form.user_id.data))
        if target.id == current_user.id and role_form.role.data != "admin":
            flash("You cannot remove your own admin access.", "danger")
            return redirect(url_for("admin_users"))

        target.role = role_form.role.data
        db.session.commit()
        flash(f"Updated role for {target.name}.", "success")
        return redirect(url_for("admin_users"))

    return render_template("admin_users.html", users=users, role_form=role_form)


@app.route("/admin/tickets")
@login_required
def admin_tickets():
    admin_required()
    status_filter = request.args.get("status", "").strip()
    priority_filter = request.args.get("priority", "").strip()

    tickets_query = Ticket.query
    if status_filter:
        tickets_query = tickets_query.filter_by(status=status_filter)
    if priority_filter:
        tickets_query = tickets_query.filter_by(priority=priority_filter)

    tickets = tickets_query.order_by(Ticket.created_at.desc()).all()
    return render_template(
        "admin_tickets.html",
        tickets=tickets,
        status_filter=status_filter,
        priority_filter=priority_filter,
        statuses=list(ALLOWED_TRANSITIONS.keys()),
        priorities=["Low", "Medium", "High", "Urgent"],
    )


@app.route("/admin/create-user", methods=["GET", "POST"])
@login_required
def admin_create_user():
    admin_required()

    form = AdminCreateUserForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            role=form.role.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("User created successfully.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_users.html", form=form)


@app.errorhandler(403)
def forbidden(error):
    return (
        render_template("index.html", error="403 Forbidden: You do not have access to that page."),
        403,
    )


if __name__ == "__main__":
    app.run(debug=True)
