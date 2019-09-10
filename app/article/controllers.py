from flask.views import MethodView
from flask import jsonify, request
from feature.orm import db
from .models import Article
from .forms import ArticleForm
from app.user.permission import admin_permission


class ArticleAPI(MethodView):
    # decorators = [admin_permission.require()]

    def get(self):
        data = [article.to_dict() for article in Article.query.all()]
        print('111')
        return jsonify(data)

    @admin_permission.require()
    def post(self):
        data = request.get_json(force=True)
        form = ArticleForm(item=data)

        if not form.validate():
            return jsonify(form.errors), 400

        a = Article(**data)
        db.session.add(a)
        db.session.commit()
        return jsonify(a.to_dict())


article_view = ArticleAPI.as_view('article_api')
