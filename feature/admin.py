from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from flask import url_for, request, redirect
from flask_admin.contrib.sqla import ModelView
from .orm import db
from app.user.models import User

admin = Admin()


class AdminMixin:
    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role('admin'):
            return True

        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


def admin_feature(app):
    admin.init_app(app, index_view=HomeAdminView(name='Home'), url='/')
    admin.add_views(AdminView(User, db.session))
