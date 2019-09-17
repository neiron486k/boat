from flask import session
from flask_login import current_user, LoginManager
from flask_principal import Identity, identity_loaded, RoleNeed, UserNeed, AnonymousIdentity, Principal
from app.user.models import User

login_manager = LoginManager()
principal = Principal()


def users_feature(app):
    """
    Add users feature
    :param app:
    :return:
    """

    # init login manager
    login_manager.init_app(app)

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
