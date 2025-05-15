-- Generate 100 test users
INSERT INTO users (username, email)
SELECT 
    'user_' || generate_series,
    'user_' || generate_series || '@example.com'
FROM generate_series(1, 100);

-- Generate 100 test tweets
INSERT INTO tweets (content, user_id, created_at)
SELECT 
    'Test tweet ' || generate_series,
    (generate_series % 100) + 1,  -- Distribute tweets among users
    NOW() - (generate_series || ' minutes')::interval
FROM generate_series(1, 100);

-- Generate 100 test likes
INSERT INTO likes (user_id, tweet_id)
SELECT 
    (generate_series % 100) + 1,  -- Distribute likes among users
    (generate_series % 100) + 1   -- Distribute likes among tweets

-- Generate test data with 100 rows for each table
-- Users
INSERT INTO users (username, email, password_hash, bio, created_at)
SELECT 
    'user_' || generate_series,
    'user_' || generate_series || '@example.com',
    'pbkdf2:sha256:600000$test_hash$test_salt',  -- Test password hash
    'Test bio for user ' || generate_series,
    NOW() - (random() * interval '30 days')
FROM generate_series(1, 100);

-- Tweets
INSERT INTO tweets (content, user_id, created_at)
SELECT 
    'Test tweet ' || generate_series,
    (random() * 100 + 1)::integer,  -- Random user_id between 1 and 100
    NOW() - (random() * interval '30 days')
FROM generate_series(1, 100);

-- Likes
INSERT INTO likes (user_id, tweet_id, created_at)
SELECT 
    (random() * 100 + 1)::integer,  -- Random user_id between 1 and 100
    (random() * 100 + 1)::integer,  -- Random tweet_id between 1 and 100
    NOW() - (random() * interval '30 days')
FROM generate_series(1, 100); 