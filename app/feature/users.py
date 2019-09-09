from flask import session
from flask_login import current_user, LoginManager, login_user
from flask_principal import Identity, identity_loaded, RoleNeed, UserNeed, AnonymousIdentity, Principal, \
    identity_changed
from app.user.models import User

login_manager = LoginManager()
principal = Principal()


def init_app(app):
    """
    Add users feature
    :param app:
    :return:
    """

    # init login manager
    login_manager.init_app(app)

    @login_manager.request_loader
    def request_loader(request):
        pass

    @login_manager.user_loader
    def load_user(user_id: int):
        return User.query.get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        user = User.query.get(1)
        login_user(user)
        identity_changed.send(app, identity=Identity(user.id))
        return str(user.id)

    def logout():
        session.pop('identity.name', None)
        session.pop('identity.auth_type', None)

    # init principal
    principal.init_app(app)

    @principal.identity_loader
    def load_identity():
        if current_user.is_authenticated:
            return Identity(current_user.id)
        session.pop('identity.name', None)
        session.pop('identity.auth_type', None)
        return AnonymousIdentity()

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

        return identity
