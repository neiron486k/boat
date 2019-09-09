from flask import Flask
from .feature import orm, users, admin


def create_app(config=None):
    """
    Create app
    """
    from config import DefaultConfig

    if config is None:
        config = DefaultConfig

    app = Flask(__name__)
    app.config.from_object(config)
    orm.init_app(app)
    users.init_app(app)
    admin.init_app(app)

    # Blueprints #
    from app.article import article_bp
    app.register_blueprint(article_bp)

    # from app.user import user_bp
    # app.register_blueprint(user_bp, url_prefix='/user')

    return app
