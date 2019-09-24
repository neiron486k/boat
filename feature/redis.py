from flask_redis import FlaskRedis

redis_client = FlaskRedis()


def redis_feature(app):
    redis_client.init_app(app)
