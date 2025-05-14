from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(160))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tweets = db.relationship('Tweet', backref='author', lazy=True)

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def root():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Get tweets with user info, ordered by creation time
    tweets = db.session.query(Tweet, User)\
        .join(User)\
        .order_by(Tweet.created_at.desc())\
        .offset((page - 1) * per_page)\
        .limit(per_page)\
        .all()
    
    # Get total count for pagination
    total_tweets = Tweet.query.count()
    total_pages = (total_tweets + per_page - 1) // per_page
    
    return render_template('root.html', 
                         tweets=tweets,
                         current_page=page,
                         total_pages=total_pages)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return 'logout_page'

if __name__ == '__main__':
    app.run(port=1147)