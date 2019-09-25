from flask import Flask
from feature import orm, users, admin, logger, redis, toolbar, cache


def create_app(config=None):
    """
    Create app
    """
    from config import DefaultConfig

    if config is None:
        config = DefaultConfig

    app = Flask(__name__)
    app.config.from_object(config)
    cache.cache_feature(app)
    orm.orm_feature(app)
    users.users_feature(app)
    admin.admin_feature(app)
    logger.logging_feature(app)
    redis.redis_feature(app)
    toolbar.toolbar_feature(app)

    #: Blueprints
    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from app.main import main
    app.register_blueprint(main)

    from app.article import article_bp
    app.register_blueprint(article_bp, url_prefix="/api")

    return app
