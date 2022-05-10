from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class PostForm(FlaskForm):

    printer_modified = SelectField('printer state')
    printer = StringField('brand and printer model')
    filament = StringField('brand and filament type')
    failure = TextAreaField('describe the failure', validators=[DataRequired()])
    solution = TextAreaField('describe the solution', validators=[DataRequired()])

printer_mod_choices = [(1, "Stock"),(2, "Modified")]

class CommentForm(FlaskForm):

    comment = TextAreaField('add a comment', validators=[DataRequired()])
