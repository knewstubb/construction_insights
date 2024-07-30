from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize SQLAlchemy
db = SQLAlchemy()
# Initialize Flask-Migrate
migrate = Migrate()

def create_app(config_class=Config):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Migrate with the app and db
    migrate.init_app(app, db)

    # Import models
    from app import models

    # Import and register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

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