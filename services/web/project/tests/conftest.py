import pytest
import os
from project import app, db

@pytest.fixture(scope='session')
def app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/twitter_clone')
    return app

@pytest.fixture(scope='session')
def _db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all() 