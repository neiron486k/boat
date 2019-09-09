from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash
from app.user.models import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("User not found")

        # check password
        if not check_password_hash(user.password, self.password.data):
            raise ValidationError("Incorrect password")
