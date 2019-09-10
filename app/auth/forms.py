from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash
from app.user.models import User
import bcrypt


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if not user:
            raise ValidationError("User not found")

        # check password
        if not bcrypt.checkpw(self.password.data.encode('utf-8'), user.password.encode('utf-8')):
            raise ValidationError("Incorrect password")
