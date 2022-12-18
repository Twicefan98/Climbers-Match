from flask import Blueprint
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/')
# @login_required
def home():
    return "<h1>Test Home Page</h1>"