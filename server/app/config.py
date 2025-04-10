import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'assets')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevConfig(Config):
    DEBUG = True
