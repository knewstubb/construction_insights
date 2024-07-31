from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, LoginManager
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize SQLAlchemy
db = SQLAlchemy()
# Initialize Flask-Migrate
migrate = Migrate()
# Initialize LoginManager
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Migrate with the app and db
    migrate.init_app(app, db)

    # Add this line after initializing the app
    login.init_app(app)

    # Import and register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Set up logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/construction_insights.log', 
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Construction Insights startup')

    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    return app

# Import models at the bottom to avoid circular imports
from app import models

@login.user_loader
def load_user(id):
    return models.User.query.get(int(id))

# Comments:
# 1. We import LoginManager from flask_login.
# 2. We initialize LoginManager and set the login view.
# 3. In create_app, we initialize LoginManager with the app.
# 4. We import and register a new auth blueprint.
# 5. We add a user_loader function to load users from the database.




