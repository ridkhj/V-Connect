from flask import Flask
from flask_mail import Mail
from app.routes.generate_pdf import generate_pdf_bp
from app.routes.upload_file import upload_file_bp
from app.routes.send_email import send_email_bp
from app.config import DevConfig, Config
from dotenv import load_dotenv
import os

load_dotenv()

mail = Mail()

def create_app():
    app = Flask(__name__)
   
    app.config.from_object(DevConfig)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.config.update(
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_PORT=int(os.getenv('MAIL_PORT')),
        MAIL_USE_TLS=bool(os.getenv('MAIL_USE_TLS')),
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
    )
   
    mail.init_app(app)

    app.register_blueprint(upload_file_bp)
    app.register_blueprint(generate_pdf_bp)
    app.register_blueprint(send_email_bp)
        
    return app
