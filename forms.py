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

    category = SelectField('Failure Category')
    printerbrand = SelectField('Printer Brand')
    printer = SelectField('Printer')
    filamentbrand = SelectField('Filament Brand')
    filament = SelectField('Filament')
    failure = StringField('Failure Description', validators=[DataRequired()])
    solution = StringField('Solution Description', validators=[DataRequired()])
