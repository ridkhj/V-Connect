from flask import Flask
from app.routes.upload_routes import upload_bp
from app.config import DevConfig, Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(upload_bp)

    return app
