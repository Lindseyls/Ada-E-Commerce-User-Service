import os
import pytest
from app.db import db
from app import create_app
from dotenv import load_dotenv
from app.models.user import User
from flask.signals import request_finished

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }

    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_user(app):
    user = User(first_name="Ada", last_name="Lovelace", email="ada@example.com")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def three_users(app):
    users = [
        User(first_name="Ada", last_name="Lovelace", email="ada@example.com"),
        User(first_name="Grace", last_name="Hopper", email="grace@example.com"),
        User(first_name="Alan", last_name="Turing", email="alan@example.com"),
    ]
    db.session.add_all(users)
    db.session.commit()
    return users
