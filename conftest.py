from app import create_app
import pytest

@pytest.fixture
def app():
    application = create_app()
    yield application #chiede uno stato...

@pytest.fixture
def client (app):#client che ci serve per
    return app.test_client()
