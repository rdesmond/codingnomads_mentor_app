import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# from .config import ProductionConfig, DevelopmentConfig

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=False)

login = LoginManager(app)
login.login_view = 'auth.login'


def create_app():
    """Construct the core application."""
    app_settings = os.environ.get('APP_SETTINGS')
    app.config.from_object(app_settings)
    db.init_app(app)
    
    with app.app_context():

        # Imports
        from . import routes
        from . import models
        from . import admin
        from . import errors

        # Create tables for our models
        db.create_all()

        @app.shell_context_processor
        def ctx():
            return {'app': app, 'db':db}


        # User Loader
        @login.user_loader
        def load_user(user_id):
            return db.user.get(id = user_id)

        return app