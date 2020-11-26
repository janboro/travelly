from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from travelly.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# we set the login_view in order to redirect the user to login
# when he wants to access a page when he's not logged in
login_manager.login_view = "users.login"
# setting the message class to 'info' for styling
# (default message: 'Please log in to access this page.')
login_manager.login_message_category = "info"

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # blueprins here
    from travelly.main.routes import main
    from travelly.users.routes import users
    from travelly.locations.routes import locations
    from travelly.plan.routes import plan
    from travelly.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(locations)
    app.register_blueprint(plan)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    return app
