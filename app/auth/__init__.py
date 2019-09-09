from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, login_required
from feature.users import login_manager
from app.user.models import User
from .forms import LoginForm

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.validate())
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@login_manager.request_loader
def request_loader(request):
    pass


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)
