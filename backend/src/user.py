from flask import Blueprint, jsonify, request
from flask_login import login_user, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user ,JWTManager
from .models import UserDetails, UserPreferences
from . import db

user = Blueprint('user', __name__)

@user.route('/user-preference', methods=['GET','POST'])
@jwt_required()
def user_prefence():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        try:
            preferences_model = UserPreferences(**data,user_id=current_user.id)
            db.session.add(preferences_model)
            db.session.commit()
            # gym_list = []
            # for gym in gyms:
            #     gym_model = UserDetails(gym=gym, user_id=current_user.id)
            #     gym_list.append(gym_model)

            # db.session.bulk_save_objects(gym_list)
            # db.session.commit()
            return jsonify({"msg":"Successfully updated match preferences"}), 200
        except:
            return jsonify({"msg":"Error updating preferences"})

@user.route('/user-details', methods=['GET','POST'])
@jwt_required()
def user_details():
    if request.method == 'POST':
        data = request.get_json()
        try:
            gym_model = UserDetails(**data,user_id=current_user.id)
            db.session.add(gym_model)
            db.session.commit()
            # gym_list = []
            # for gym in gyms:
            #     gym_model = UserDetails(gym=gym, user_id=current_user.id)
            #     gym_list.append(gym_model)

            # db.session.bulk_save_objects(gym_list)
            # db.session.commit()
            return jsonify({"msg":"Successfully updated user details"}), 200
        except:
            return jsonify({"msg":"Error updating details"})    