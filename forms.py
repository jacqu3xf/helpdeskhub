from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class TicketForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=5)])
    category = StringField("Category")
    priority = SelectField(
        "Priority",
        choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High"), ("Urgent", "Urgent")],
    )
    submit = SubmitField("Submit Ticket")


class CommentForm(FlaskForm):
    body = TextAreaField("Comment", validators=[DataRequired(), Length(min=1)])
    submit = SubmitField("Add Comment")


class StatusForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[
            ("New", "New"),
            ("Open", "Open"),
            ("In Progress", "In Progress"),
            ("Waiting on User", "Waiting on User"),
            ("Resolved", "Resolved"),
            ("Closed", "Closed"),
        ],
    )
    submit = SubmitField("Update Status")


# TRACKING COMMENT: added for the separated admin console so role management stays in Flask-WTF/Bootstrap.
class UserRoleForm(FlaskForm):
    user_id = HiddenField("User ID", validators=[DataRequired()])
    role = SelectField(
        "Role",
        choices=[("user", "user"), ("rep", "rep"), ("admin", "admin")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Save Role")

class AdminCreateUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    role = SelectField(
        "Role",
        choices=[("user", "User"), ("rep", "Rep"), ("admin", "Admin")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create User")