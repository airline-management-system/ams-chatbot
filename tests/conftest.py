import pytest

from application import create_app
from application.config import Config

class TestConfig(Config):
    TESTING = True

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client() 