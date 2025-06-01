from flask import Flask
from flask_mail import Mail
from app.routes.upload_file import upload_file_bp
from app.routes.update_routes.get_updates import get_updates_bp
from app.routes.process_files import process_files_bp   
from app.routes.letter_routes.get_letters import get_letters_bp
from app.routes.letter_routes.get_letters_pdf import get_letters_pdf_bp
from app.routes.cdpr_routes.get_cdpr import get_cdpr_bp
from app.routes.update_routes.get_updates_pdf  import get_updates_pdf_bp
from app.routes.cdpr_routes.get_cdpr_pdf import get_cdpr_pdf_bp
from app.routes.get_files import get_files_bp
from app.config import DevConfig, Config
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
   
    app.config.from_object(DevConfig)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(upload_file_bp)
    app.register_blueprint(process_files_bp)

    app.register_blueprint(get_letters_bp)
    app.register_blueprint(get_letters_pdf_bp)

    app.register_blueprint(get_updates_bp)
    app.register_blueprint(get_updates_pdf_bp)
    
    app.register_blueprint(get_cdpr_bp)
    app.register_blueprint(get_cdpr_pdf_bp)

    app.register_blueprint(get_files_bp)

    return app
