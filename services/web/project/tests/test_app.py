import pytest
from project import app, db
from project.models import User, Tweet, Like
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/twitter_clone')
    
    with app.test_client() as client:
        with app.app_context():
            # Create tables
            db.create_all()
            
            # Load test data using generate_data.sql
            with open('services/postgres/generate_data.sql', 'r') as f:
                sql_commands = f.read()
                db.session.execute(sql_commands)
                db.session.commit()
            
            yield client
            
            # Clean up
            db.session.remove()
            db.drop_all()

def test_home_page(client):
    """Test that the home page loads and shows tweets"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tweets' in response.data

def test_search_functionality(client):
    """Test that search works and returns relevant results"""
    # First, create a test tweet with specific content
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        tweet = Tweet(content='This is a test tweet with specific words', user_id=user.id)
        db.session.add(tweet)
        db.session.commit()
    
    # Test search
    response = client.get('/search?q=test+tweet')
    assert response.status_code == 200
    assert b'This is a test tweet' in response.data

def test_like_functionality(client):
    """Test that liking tweets works"""
    # First, create a test user and tweet
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        tweet = Tweet(content='Test tweet', user_id=user.id)
        db.session.add(tweet)
        db.session.commit()
        
        # Login as the user
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)
        
        # Like the tweet
        response = client.post(f'/like/{tweet.id}', follow_redirects=True)
        assert response.status_code == 200
        
        # Verify the like was created
        like = Like.query.filter_by(user_id=user.id, tweet_id=tweet.id).first()
        assert like is not None

def test_pagination(client):
    """Test that pagination works on the home page"""
    response = client.get('/?page=2')
    assert response.status_code == 200
    assert b'Next' in response.data
    assert b'Previous' in response.data 