from .models import Article
from flask import request, json
from app.main.services import DefaultService
from feature.orm import db
from feature.redis import redis_client
import functools


class MyCache(object):
    def __init__(self, key=None):
        self.key = key

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            stored_data = redis_client.get(self.key)

            if stored_data is None:
                data = fn(*args, **kwargs)
                redis_client.set(self.key, json.dumps(data))
            else:
                data = json.loads(stored_data)

            return data

        return decorated


class ArticleService(DefaultService):
    @MyCache(key='articles')
    def get_articles(self) -> dict:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        data = self.paginate(Article.query, page=page, limit=limit)
        data['data'] = [article.to_dict() for article in data['data']]
        return data

    @staticmethod
    def create_article(article: Article) -> Article:
        db.session.add(article)
        db.session.commit()
        return article
