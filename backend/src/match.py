from flask import Blueprint, jsonify, request
from flask_login import login_user, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user ,JWTManager
from .models import MatchRequest, User, UserDetails, UserPreferences
from . import db

match = Blueprint('match', __name__)

match_status = {"pending": 1, "confirmed": 2, "rejected": 0}

@match.route('/create-match', methods=['GET','POST'])
@jwt_required()
def create_match():
    if request.method == "POST":
        data = request.get_json()
        from_user_id = current_user.id
        to_user_id = data['to_user_id']
        update_status = data['update_status']

        existing_request = MatchRequest.query.filter_by(to_user_id=from_user_id,from_user_id=to_user_id).first()
        if existing_request:
            res = update_match_request(update_status,existing_request)
            return jsonify({"msg":res, "status":200})
        elif update_status != "rejected":
            match_request = MatchRequest(
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                match_status=match_status["pending"]
            )
            try:
                db.session.add(match_request)
                db.session.commit()
                return jsonify({"msg":"Successfully added match request", "status": 200}), 200
            except:
                return "Error in match request"

# CONTINUE ON FRIDAY
@match.route('/show-users', methods=['GET','POST'])
@jwt_required()
def show_users():
    # Filter by prefered gyms and gender
    user_preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
    preferences_dict = user_preferences._getdict()
    preferences_dict.pop("user_id")
    print(preferences_dict)
    results = UserDetails.query.filter_by(**preferences_dict).filter("user_id"!=current_user.id).all()
    print(results)
    result_list = []
    for result in results:
        print(result.user)
        user = result.user
        result_list.append(user._getdict())
    # results = User.query.join(User.gyms).filter(User.id!=current_user.id)
    # results = UserDetails.query.with_entities(UserDetails.user_id).distinct().filter(UserDetails.gym=="Boulder+", UserDetails.user_id!=current_user.id).first()
    # print(results)
    return jsonify(result_list),200
    # return jsonify(results.all()[0]._getdict())

@match.route("/get-all")
@jwt_required()
def get_all_user_request():
    match_list = []
    match_requests = MatchRequest.query.filter_by(from_user_id=current_user.id).all()
    for match in match_requests:
        match_list.append(match._getdict())

    return jsonify(match_list)

def update_match_request(update_status, match_request):
    match_request.match_status = match_status[update_status]
    db.session.commit()

    if update_status == "confirmed":
        return "Successful Match!"
    else:
        return "Failed to Match!"

    