from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    gyms = db.relationship('UserDetails', backref='user')
    preferences = db.relationship('UserPreferences', backref='user')
    def _getdict(self):
        return {
            "id": self.id,
            "email": self.email,
            # "password": self.password,
            "first_name": self.first_name,
        }
    # match_requests = db.relationship('MatchRequest')

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(150), nullable=False)
    boulder_world = db.Column(db.Boolean())
    boulder_plus = db.Column(db.Boolean())
    boulder_planet = db.Column(db.Boolean())
    boulder_movement = db.Column(db.Boolean())
    bff_climb = db.Column(db.Boolean())
    boruda = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    # user = db.relationship("User", back_populates='user')
    def _getdict(self):
        return {
            "gender": self.gender,
            "boulder_world": self.boulder_world,
            "boulder_plus": self.boulder_plus,
            "boulder_planet": self.boulder_planet,
            "boulder_movement": self.boulder_movement,
            "bff_climb": self.bff_climb,
            "boruda": self.boruda,
            "user_id": self.user_id
        }

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(150))
    boulder_world = db.Column(db.Boolean())
    boulder_plus = db.Column(db.Boolean())
    boulder_planet = db.Column(db.Boolean())
    boulder_movement = db.Column(db.Boolean())
    bff_climb = db.Column(db.Boolean())
    boruda = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    # user = db.relationship("User", back_populates='user')
    def _getdict(self):
        return {
            "gender": self.gender,
            "boulder_world": self.boulder_world,
            "boulder_plus": self.boulder_plus,
            "boulder_planet": self.boulder_planet,
            "boulder_movement": self.boulder_movement,
            "bff_climb": self.bff_climb,
            "boruda": self.boruda,
            "user_id": self.user_id
        }

class MatchRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    match_status = db.Column(db.String(150), nullable=False)
    from_user = db.relationship("User", foreign_keys=[from_user_id])
    to_user = db.relationship("User", foreign_keys=[to_user_id])

    def _getdict(self):
        return {
            "id": self.id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "match_status": self.match_status
        }