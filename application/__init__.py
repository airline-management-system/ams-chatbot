from flask import Flask
from flask_cors import CORS
from application.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    # Register blueprints
    from application.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app 