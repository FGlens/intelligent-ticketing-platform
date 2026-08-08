import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret key for security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-change-this-in-production'

    # Using SQLite for now (easy, no installation needed)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ticketing.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder for event images (optional)
    UPLOAD_FOLDER = 'app/static/images/events'