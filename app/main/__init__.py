from flask import Blueprint, render_template, json
from werkzeug.exceptions import HTTPException

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
def home():
    return render_template('home.html')


@main.errorhandler(HTTPException)
def error_handler(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
