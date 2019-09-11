from flask.views import MethodView
from flask import jsonify, request
from feature.orm import db
from .models import Article
from .forms import ArticleForm
from flask_login import login_required
from flask_principal import Permission, RoleNeed

admin_permission = Permission(RoleNeed('admin'))


class ArticleAPI(MethodView):
    # decorators = [admin_permission.require()]

    def get(self):
        data = [article.to_dict() for article in Article.query.all()]
        return jsonify(data)

    @admin_permission.require()
    # @login_required
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
