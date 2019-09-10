from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, PasswordField
from wtforms.validators import DataRequired, EqualTo
from app.user.models import User
import bcrypt


class FormMixin:
    email = StringField('email', validators=[DataRequired()])


class LoginForm(FormMixin, FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if not user:
            raise ValidationError("User not found")

        # check password
        if not bcrypt.checkpw(self.password.data.encode('utf-8'), user.password.encode('utf-8')):
            raise ValidationError("Incorrect password")


class SignupForm(FormMixin, FlaskForm):
    password = PasswordField('password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat password')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError("Exists email")
