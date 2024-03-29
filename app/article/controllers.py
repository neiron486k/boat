from flask.views import MethodView
from flask import jsonify, request
from .models import Article
from .forms import ArticleForm
from .services import ArticleService
from app.user.permission import admin_permission


class ArticleAPI(MethodView):
    # decorators = [admin_permission.require()]

    def get(self):
        return jsonify(ArticleService().get_articles())

    @admin_permission.require()
    def post(self):
        data = request.get_json(force=True)
        form = ArticleForm(item=data)

        if not form.validate():
            return jsonify(form.errors), 400

        a = Article(**data)
        ArticleService().create_article(a)
        return jsonify(a.to_dict())


article_view = ArticleAPI.as_view('article_api')
