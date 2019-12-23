from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import ProductionConfig, DevelopmentConfig

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=False)

login = LoginManager(app)
login.login_view = 'auth.login'

# @login.user_loader
# def load_user(user_id):
#     #return User.get(user_id)
#     return None  # TODO: change this for proper auth handling

def create_app():
    """Construct the core application."""
    app.config.from_object(DevelopmentConfig)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    
    with app.app_context():

        # Imports
        from . import routes
        from . import models
        from . import admin

        # Create tables for our models
        db.create_all()


        # User Loader
        @login.user_loader
        def load_user(user_id):
            return db.user.get(id = user_id)

        return app