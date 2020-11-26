import os


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///travelly.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # using Gmail passwords in apps
    # https://support.google.com/accounts/answer/185833?hl=en
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
