import pytest
from app import create_app, db


@pytest.fixture
def app():
    test_app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TMDB_API_KEY': 'test-key',
        'CACHE_TYPE': 'NullCache',
    })
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()
