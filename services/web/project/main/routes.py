from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from project import db
from project.main import bp
from project.models import User, Tweet, Like

@bp.route('/')
@bp.route('/index')
def index():
    # Get the most recent tweets
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).limit(20).all()
    return render_template('index.html', title='Home', tweets=tweets)

@bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tweets = Tweet.query.filter_by(user_id=user.id).order_by(Tweet.created_at.desc()).all()
    return render_template('user.html', user=user, tweets=tweets)

@bp.route('/tweet', methods=['GET', 'POST'])
@login_required
def tweet():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            tweet = Tweet(content=content, user_id=current_user.id)
            db.session.add(tweet)
            db.session.commit()
            flash('Your tweet has been posted!')
            return redirect(url_for('main.index'))
    return render_template('tweet.html', title='New Tweet')

@bp.route('/like/<int:tweet_id>', methods=['POST'])
@login_required
def like(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)
    like = Like.query.filter_by(user_id=current_user.id, tweet_id=tweet_id).first()
    
    if like:
        db.session.delete(like)
        db.session.commit()
        flash('You unliked this tweet')
    else:
        like = Like(user_id=current_user.id, tweet_id=tweet_id)
        db.session.add(like)
        db.session.commit()
        flash('You liked this tweet')
    
    return redirect(request.referrer or url_for('main.index')) 