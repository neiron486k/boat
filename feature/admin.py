from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from flask import url_for, request, redirect
from flask_admin.contrib.sqla import ModelView
from .orm import db
from app.user.models import User, Role
from app.article.models import Article

admin = Admin()


class AdminMixin:
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('admin'):
            return True

        return False

    def inaccessible_callback(self, name, **kwargs):
        print(1)
        return redirect(url_for('auth.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


def admin_feature(app):
    admin.init_app(app, index_view=HomeAdminView(endpoint=''))
    admin.url = '/'
    admin.name = 'Boat'
    admin.add_views(AdminView(User, db.session))
    admin.add_views(AdminView(Role, db.session))
    admin.add_views(AdminView(Article, db.session, endpoint='articles'))
