from .config import Config
from flask import Flask
from .build import db, migrate, login_manager, csrf, jwt

from .routes.main import main
from .routes.requests import requests
from .routes.auth import auth
from .routes.dashboard import dashboard
from .routes.admin import api


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.json.ensure_ascii = False

    app.register_blueprint(main)
    app.register_blueprint(requests)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(api)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.init_app(app)

    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app
