from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Ticket, Comment
from forms import RegisterForm, LoginForm, TicketForm, CommentForm, StatusForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdeskhub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

ALLOWED_TRANSITIONS = {
    "New": {"Open", "In Progress"},
    "Open": {"In Progress", "Waiting on User", "Resolved"},
    "In Progress": {"Waiting on User", "Resolved"},
    "Waiting on User": {"Open", "In Progress"},
    "Resolved": {"Closed", "Open"},  # allow reopen for reps/admin
    "Closed": set(),
}

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def rep_required():
    if not current_user.is_authenticated or not current_user.is_rep_or_admin():
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/init-db")
def init_db():
    db.create_all()
    admin = User.query.filter_by(email="admin@example.com").first()
    if not admin:
        admin = User(name="Admin", email="admin@example.com", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
    flash("DB initialized. Default admin: admin@example.com / admin123", "success")
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower()).first()
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
        return redirect(url_for("tickets_list"))

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("index"))

@app.route("/tickets")
@login_required
def tickets_list():
    if current_user.role in ["rep", "admin"]:
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        tickets = Ticket.query.filter_by(created_by=current_user.id).order_by(Ticket.created_at.desc()).all()
    return render_template("tickets_list.html", tickets=tickets)

@app.route("/tickets/new", methods=["GET", "POST"])
@login_required
def ticket_new():
    form = TicketForm()
    if form.validate_on_submit():
        t = Ticket(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            category=(form.category.data.strip() if form.category.data else "General"),
            priority=form.priority.data,
            status="New",
            created_by=current_user.id,
            assigned_to=None,
        )
        db.session.add(t)
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
        tickets = Ticket.query.filter_by(assigned_to=current_user.id).order_by(Ticket.created_at.desc()).all()
    elif view == "all":
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        tickets = Ticket.query.filter(Ticket.assigned_to.is_(None)).order_by(Ticket.created_at.desc()).all()

    return render_template("tickets_queue.html", tickets=tickets, view=view)

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
                c = Comment(ticket_id=ticket.id, user_id=current_user.id, body=comment_form.body.data.strip())
                db.session.add(c)
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

@app.errorhandler(403)
def forbidden(e):
    return render_template("index.html", error="403 Forbidden: You don’t have access to that."), 403

# Dashbaord added
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role in ["rep", "admin"]:
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(created_by=current_user.id).all()

    status_counts = {}
    priority_counts = {}
    for t in tickets:
        status_counts[t.status] = status_counts.get(t.status, 0) + 1
        priority_counts[t.priority] = priority_counts.get(t.priority, 0) + 1

    return render_template(
        "dashboard.html",
        tickets=tickets,
        status_counts=status_counts,
        priority_counts=priority_counts,
    )
#end of dahsboard

if __name__ == "__main__":
    app.run(debug=True)
