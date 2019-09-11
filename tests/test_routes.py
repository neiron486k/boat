import pytest
from app import create_app
from config import TestDefaultConfig
from app.article.models import Article
from app.user.services import UserService
from feature.orm import db
from app.user.models import Role
import json

app = create_app(TestDefaultConfig)


class MixinTestCase:
    client = app.test_client()

    @pytest.fixture
    def app_init(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            yield app

    @pytest.fixture
    def admin(self, app_init):
        with app_init.app_context():
            user = UserService().create(dict(
                email='admin@example.com',
                password='admin',
                confirm='admin'
            ))
            role = Role(
                name='admin'
            )
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            yield user

    @pytest.fixture
    def article(self, app_init):
        with app.app_context():
            a = Article(title='test title', content='test content')
            db.session.add(a)
            db.session.commit()
            yield a

    def login(self, username: str, password: str):
        self.client.post('/auth/login', data=dict(
            email=username,
            password=password
        ), follow_redirects=True)


class TestArticle(MixinTestCase):
    @pytest.mark.usefixtures('article')
    def test_articles(self):
        rv = self.client.get('/articles')
        data = rv.get_json()
        assert 'test title' == data[0]['title']
        assert 'test content' == data[0]['content']
        assert isinstance(data[0]['title'], str)
        assert isinstance(data[0]['content'], str)

    def test_create_article(self, app_init, admin):
        prepare_date = dict(
            title='first article',
            content='some content'
        )
        self.login('admin@example.com', 'admin')
        self.client.post('/articles', data=json.dumps(prepare_date), content_type='application/json')
        article = Article.query.filter_by(title=prepare_date['title']).first()
        assert prepare_date['title'] == article.title