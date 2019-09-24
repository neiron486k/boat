from flask_redis import FlaskRedis
import fakeredis

redis_client = FlaskRedis()


def redis_feature(app):
    if app.testing:
        redis_client.from_custom_provider(fakeredis)

    redis_client.init_app(app)
