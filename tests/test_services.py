import pytest
from app import create_app
from config import TestDefaultConfig
from app.article.models import Article
from feature.orm import db

app = create_app(TestDefaultConfig)


class MixinTestCase:
    @pytest.fixture
    def client(self):
        client = app.test_client()

        with app.app_context():
            article = Article(title='test title', content='test content')
            db.drop_all()
            db.create_all()
            db.session.add(article)
            db.session.commit()

        yield client


class TestArticle(MixinTestCase):
    def test_articles(self, client):
        rv = client.get('/articles')
        data = rv.get_json()
        assert 'test title' == data[0]['title']
        assert 'test content' == data[0]['content']
        assert isinstance(data[0]['title'], str)
        assert isinstance(data[0]['content'], str)
