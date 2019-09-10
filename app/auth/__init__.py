from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import logout_user, login_required, login_user
from feature.users import login_manager
from app.user.models import User
from .forms import LoginForm
from flask import request
import bcrypt
from feature.orm import db

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.data.get('email')).first()
        login_user(user)
        return redirect(request.args.get('next') or "/")

        if next:
            return redirect(next)

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password').encode('utf-8')
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
    user = User(email=email, password=password_hash)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('auth.login'))


@login_manager.request_loader
def request_loader(request):
    pass


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)
