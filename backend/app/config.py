# import os
# from dotenv import load_dotenv
# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
#     SQLALCHEMY_DATABASE_URI = os.getenv("CENTRAL_DB_URI")  # central DB
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
#     SMTP_HOST = os.getenv("SMTP_HOST")
#     SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
#     SMTP_USER = os.getenv("SMTP_USER")
#     SMTP_PASS = os.getenv("SMTP_PASS")
#     APP_DOMAIN = os.getenv("APP_DOMAIN", "localhost")
#     APP_PORT = int(os.getenv("APP_PORT", 5000))




#     MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
#     MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.getenv("MAIL_USERNAME")
#     MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")




import os
from dotenv import load_dotenv

# Make sure .env loads before Config class
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("CENTRAL_DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Force JWT_SECRET_KEY to be consistent
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "evoltechs_secret_2025"

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    APP_DOMAIN = os.getenv("APP_DOMAIN", "localhost")
    APP_PORT = int(os.getenv("APP_PORT", 5000))

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
