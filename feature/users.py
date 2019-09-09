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

    @login_manager.request_loader
    def request_loader(request):
        pass

    @login_manager.user_loader
    def load_user(user_id: int):
        return User.query.get(user_id)

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

    # @app.errorhandler(PermissionDenied)
    # def special_exception_handler(error):
    #     return 'Permission denied', 403
