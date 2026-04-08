from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


=======
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

>>>>>>> 65ec06f446bc79dc95fc6151c6636ae6e5bb4d4d
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")

<<<<<<< HEAD

=======
>>>>>>> 65ec06f446bc79dc95fc6151c6636ae6e5bb4d4d
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

<<<<<<< HEAD

=======
>>>>>>> 65ec06f446bc79dc95fc6151c6636ae6e5bb4d4d
class TicketForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=5)])
    category = StringField("Category")
<<<<<<< HEAD
    priority = SelectField(
        "Priority",
        choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High"), ("Urgent", "Urgent")],
    )
    submit = SubmitField("Submit Ticket")


=======
    priority = SelectField("Priority", choices=[("Low","Low"),("Medium","Medium"),("High","High"),("Urgent","Urgent")])
    submit = SubmitField("Submit Ticket")

>>>>>>> 65ec06f446bc79dc95fc6151c6636ae6e5bb4d4d
class CommentForm(FlaskForm):
    body = TextAreaField("Comment", validators=[DataRequired(), Length(min=1)])
    submit = SubmitField("Add Comment")

<<<<<<< HEAD

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
=======
class StatusForm(FlaskForm):
    status = SelectField("Status", choices=[
        ("New","New"),
        ("Open","Open"),
        ("In Progress","In Progress"),
        ("Waiting on User","Waiting on User"),
        ("Resolved","Resolved"),
        ("Closed","Closed"),
    ])
    submit = SubmitField("Update Status")
>>>>>>> 65ec06f446bc79dc95fc6151c6636ae6e5bb4d4d
