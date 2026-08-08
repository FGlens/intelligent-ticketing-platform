from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Create database object
db = SQLAlchemy()

# Create login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'   # Redirect to login page if not logged in
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints (routes)
    from app.routes.auth import auth_bp
    from app.routes.events import events_bp
    from app.routes.bookings import bookings_bp
    from app.routes.recommendations import recommendations_bp
    from app.routes.organizer import organizer_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(organizer_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
