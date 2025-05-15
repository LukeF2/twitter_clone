from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import text
import os

app = Flask(__name__)
# Use environment variables for database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://hello_flask:hello_flask@localhost:5432/hello_flask_dev')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # Required for flash messages
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
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
    content_tsv = db.Column(db.Text)  # For full-text search

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    if not query:
        return render_template('search.html', tweets=[], query='', current_page=1, total_pages=0)
    
    # Create the search query using RUM index
    search_query = text("""
        SELECT t.id as tweet_id, t.content, t.created_at as tweet_created_at,
               u.id as user_id, u.username, u.email,
               ts_rank_cd(t.content_tsv, to_tsquery('english', :query)) as rank,
               ts_headline('english', t.content, to_tsquery('english', :query), 
                          'StartSel=<mark>,StopSel=</mark>,MaxFragments=1,MaxWords=50') as highlighted_content
        FROM tweets t
        JOIN users u ON t.user_id = u.id
        WHERE t.content_tsv @@ to_tsquery('english', :query)
        ORDER BY rank DESC
        LIMIT :limit OFFSET :offset
    """)
    
    # Convert search terms to tsquery format
    tsquery = ' & '.join(query.split())
    
    # Execute the search query
    results = db.session.execute(
        search_query,
        {'query': tsquery, 'limit': per_page, 'offset': (page - 1) * per_page}
    ).fetchall()
    
    # Get total count for pagination
    count_query = text("""
        SELECT COUNT(*)
        FROM tweets
        WHERE content_tsv @@ to_tsquery('english', :query)
    """)
    total_results = db.session.execute(count_query, {'query': tsquery}).scalar()
    total_pages = (total_results + per_page - 1) // per_page
    
    return render_template('search.html',
                         tweets=results,
                         query=query,
                         current_page=page,
                         total_pages=total_pages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('root'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('root'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('create_account.html')
            
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('create_account.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('create_account.html')
            
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('create_account.html')

@app.route('/create_message', methods=['GET', 'POST'])
@login_required
def create_message():
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content:
            flash('Message cannot be empty', 'error')
            return render_template('create_message.html')
            
        tweet = Tweet(
            content=content,
            user_id=current_user.id
        )
        
        db.session.add(tweet)
        db.session.commit()
        
        flash('Message posted successfully!', 'success')
        return redirect(url_for('root'))
        
    return render_template('create_message.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1147)