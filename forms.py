from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, TextAreaField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from models import User, Group, Bill


class RegistrationForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired(), Length(min=5)])
    verified_password = PasswordField("Repeat password", [
        EqualTo('password', "The password must match.")])
    submit = SubmitField('Register')

    def check_email(self, email):
        user = User.query.filter_by(
            email=email.data).first()
        if user:
            raise ValidationError(
                'This email is used!!! Choose another.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email', [DataRequired()])
    password = PasswordField(
        'Password', [Length(min=5), DataRequired()])
    submit = SubmitField('Login')


class AddBillForma(FlaskForm):
    amount = IntegerField('Amount', [DataRequired()])
    description = StringField('Description', [DataRequired()])
    submit = SubmitField('Add')


class AddGroupForma(FlaskForm):
    group_id = StringField('Group ID', [DataRequired()])
    submit = SubmitField('Add')
