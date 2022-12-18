from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user ,JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from . import jwt

auth = Blueprint('auth', __name__)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@auth.route('/test', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(
        email=current_user.email,
        first_name=current_user.first_name
    )

@auth.route('/sign-in', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).one_or_none()
        if user and check_password_hash(user.password, password):
            # login_user(user, remember=True)
            access_token = create_access_token(identity=user)
            return jsonify({"token":access_token}), 200
        else:
            return "Incorrect username/password"

@auth.route('/sign-out')
# @login_required
def sign_out():
    # logout_user()
    return "Successfully logged out"

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('firstName')
        # gender = request.form.get('gender')

        user = User.query.filter_by(email=email).first()
        if user:
            return "User already exists"
        
        try:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return "Successful sign up"
        except:
            return "Error: Failed to sign up"

@auth.route('/get-users')
@jwt_required()
def get_users():
    user_list = []
    users = User.query.all()
    for user in users:
        user_list.append(user._getdict())
    
    return jsonify(user_list)