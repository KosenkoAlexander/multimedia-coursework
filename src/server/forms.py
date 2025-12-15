from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional

class MainButtonsForm(FlaskForm):
    start = SubmitField('start')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])#, Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create account')

    def validate_username(self, username):
        pass #TODO

    def validate_email(self, email):
        pass #TODO


class ProfileUsernameForm(FlaskForm):
    username = StringField('New username', validators=[DataRequired()])
    submit_username = SubmitField('Change')

class ProfilePasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[DataRequired()])
    password2 = PasswordField('Repeat new password', validators=[DataRequired(), EqualTo('password')])
    submit_password = SubmitField('Change')

class BookForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
        
    authors = SelectMultipleField(
        'Authors',
        coerce=int,
        validators=[Optional()]
    )

    genres = SelectMultipleField(
        'Genres',
        coerce=int,
        validators=[Optional()]
    )

    shops = SelectMultipleField(
        'Shop',
        coerce=int,
        validators=[Optional()]
    )

    libraries = SelectMultipleField(
        'Library',
        coerce=int,
        validators=[Optional()]
    )

    submit = SubmitField('Save')