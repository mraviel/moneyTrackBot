from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
# from passlib.hash import pbkdf2_sha256
from flask_login import login_user
import models as M
from Constants import Admin_Username, Admin_Password


def invalid_credentials(form, field):
    """ Username and password checker """

    username_entered = form.username.data
    password_entered = field.data

    admin_user = M.AdminUser(username=username_entered, password=password_entered)

    if username_entered == Admin_Username and password_entered == Admin_Password:
        login_user(admin_user)
    else:
        raise ValidationError("username or password not correct")


class LoginForm(FlaskForm):
    """ Login form """

    username = StringField('username_label',
                           validators=[InputRequired(message="Username reuired")])

    password = StringField('password_label',
                           validators=[InputRequired(message="Password required"), invalid_credentials])

    submit_button = SubmitField('Login')
