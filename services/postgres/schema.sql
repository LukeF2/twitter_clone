-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(128) NOT NULL UNIQUE,
    active BOOLEAN NOT NULL
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Tweets table
CREATE TABLE IF NOT EXISTS tweets (
    id SERIAL PRIMARY KEY,
    content VARCHAR(280) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on user_id for faster lookups of user's tweets
CREATE INDEX IF NOT EXISTS idx_tweets_user_id ON tweets(user_id);
-- Create index on created_at for faster chronological queries
CREATE INDEX IF NOT EXISTS idx_tweets_created_at ON tweets(created_at);

-- Likes table
CREATE TABLE IF NOT EXISTS likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tweet_id INTEGER NOT NULL REFERENCES tweets(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Ensure a user can only like a tweet once
    UNIQUE(user_id, tweet_id)
);

-- Create index on tweet_id for faster lookups of tweet's likes
CREATE INDEX IF NOT EXISTS idx_likes_tweet_id ON likes(tweet_id);
-- Create index on user_id for faster lookups of user's likes
CREATE INDEX IF NOT EXISTS idx_likes_user_id ON likes(user_id); 