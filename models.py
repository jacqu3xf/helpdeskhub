from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

ROLES = ["user", "rep", "admin"]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="user", nullable=False)

    def set_password(self, plain_text_password: str):
        self.password_hash = generate_password_hash(plain_text_password)

    def check_password(self, plain_text_password: str) -> bool:
        return check_password_hash(self.password_hash, plain_text_password)

    def is_rep_or_admin(self) -> bool:
        return self.role in ["rep", "admin"]

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(80), default="General")
    priority = db.Column(db.String(20), default="Medium")  # Low/Medium/High/Urgent
    status = db.Column(db.String(30), default="New")       # New/Open/In Progress/Waiting on User/Resolved/Closed

    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    creator = db.relationship("User", foreign_keys=[created_by], backref="created_tickets")
    assignee = db.relationship("User", foreign_keys=[assigned_to], backref="assigned_tickets")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    ticket = db.relationship("Ticket", backref="comments")
    user = db.relationship("User")

# Added New Class to Keep Track of Ticket History
class TicketHistory(db.Model):
    id = db.Column(db.Ineger, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"), nullable=False)
    user_id = db.Column(db.Ineger, db.ForgeignKey("user.id"), nullable=False)

    action = db.Column(db.String(255), nullable=False)
    old_value = db.Column(db.string(255), nullable=False)
    new_value = db.Column(db.string(255), nullable=False)

    # createing a digtial timestamp of the ticket time
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    ticket = db.relationship("Ticket", backref="history_entries")
    user = db.relationship("User", backref="history_entries")