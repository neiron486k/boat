from flask import Blueprint
from .controllers import article_view
from .models import *

article_bp = Blueprint('article', __name__)
article_bp.add_url_rule('/articles', view_func=article_view, methods=['GET', 'POST'])
