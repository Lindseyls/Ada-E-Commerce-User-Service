from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .models.user import User
from .routes.user_routes import bp as users_bp 

import os

def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users_bp)

    @app.get('/')
    def index():
        return {
        "status": "ok"
        }

    return app