from .models import Article
from feature.redis import redis_client
from flask import json
from feature.orm import db


class ArticleService(object):
    @staticmethod
    def get_articles() -> dict:
        q = Article.query

        if redis_client.exists(Article.RESULT_ID):
            data = json.loads(redis_client.get(Article.RESULT_ID))
        else:
            data = [article.to_dict() for article in q.all()]
            redis_client.set(Article.RESULT_ID, json.dumps(data))

        return data

    @staticmethod
    def create_article(article: Article) -> Article:
        db.session.add(article)
        db.session.commit()
        redis_client.delete(Article.RESULT_ID)
        return article
