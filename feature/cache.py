from flask_caching import Cache

cache = Cache()


def cache_feature(app):
    cache.init_app(app)
