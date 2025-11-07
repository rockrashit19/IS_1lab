from flask import Flask
from .config import Config
from .database import db
from .auth import auth_bp
from .routes import api_bp
from flask_jwt_extended import JWTManager

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
