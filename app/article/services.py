from .models import Article
from feature.redis import redis_client
from flask import json, request
from feature.orm import db
from hashlib import md5


class ArticleService:
    def get_articles(self) -> list:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        cache_id = Article.RESULT_ID
        key = 'page=' + str(page) + 'limit=' + str(limit)
        hashed_key = md5(key.encode('utf-8')).hexdigest()

        if redis_client.exists(cache_id):
            data = json.loads(redis_client.get(cache_id))

            if data.get(hashed_key) is None:
                data[hashed_key] = self.paginate(Article.query, page=page, limit=limit)
                redis_client.set(cache_id, json.dumps(data))
        else:
            d = self.paginate(Article.query, page=page, limit=limit)
            data = dict()
            data[hashed_key] = d
            redis_client.set(cache_id, json.dumps(data))

        return data.get(hashed_key)

    @staticmethod
    def create_article(article: Article) -> Article:
        db.session.add(article)
        db.session.commit()
        redis_client.delete(Article.RESULT_ID)
        return article

    @staticmethod
    def paginate(query, page: int = 1, limit: int = 10):
        paginated_data = query.paginate(per_page=limit, page=page)
        data = [article.to_dict() for article in paginated_data.items]
        meta = dict(
            total=paginated_data.total,
            page=paginated_data.page,
            pages=paginated_data.pages
        )
        return dict(data=data, meta=meta)
