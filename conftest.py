from app import create_app
import pytest


@pytest.fixture
def app():
    application = create_app()
    yield application


@pytest.fixture
def client(app):
    return app.test_client()