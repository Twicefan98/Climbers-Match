from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()
DB_NAME = "climbersmatch"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdfdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:root@localhost:3306/{DB_NAME}'
    app.config["JWT_SECRET_KEY"] = "dfsdfsdofigdfogj9r4rer0jrtburt09jr"
    jwt.init_app(app)
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .match import match
    from .user import user

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(match, url_prefix="/match")
    app.register_blueprint(user, url_prefix="/user")

    from .models import User, MatchRequest
    with app.app_context():
        # db.drop_all()
        db.create_all()
    
    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

    return app

