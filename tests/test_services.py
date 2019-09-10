import pytest
from app import create_app
from config import TestDefaultConfig


@pytest.fixture
def client():
    app = create_app(TestDefaultConfig)
    client = app.test_client()
    yield client


def test_articles(client):
    rv = client.get('/articles')
    print(rv.get_json())
    pass
