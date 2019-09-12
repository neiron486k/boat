from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, login_required, login_user
from flask_principal import identity_changed, Identity, AnonymousIdentity
from feature.users import login_manager
from app.user.models import User
from .forms import LoginForm, SignupForm
from flask import request
from app.user.services import UserService
from .signals import signup as signup_signal

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.data.get('email')).first()
        login_user(user)

        # Tell Flask-Principal the identity changed
        identity_changed.send(auth, identity=Identity(user.id))

        return redirect(request.args.get('next') or url_for('main.home'))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(auth, dentity=AnonymousIdentity())

    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        data = form.data
        data.pop('confirm')
        new_user = UserService().create(User(**data))
        login_user(new_user)
        signup_signal.send(new_user)
        return redirect(url_for('main.home'))

    return render_template('signup.html', form=form)


@login_manager.request_loader
def request_loader(request):
    pass


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(user_id)
