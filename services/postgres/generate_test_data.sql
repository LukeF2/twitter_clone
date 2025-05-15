-- Generate 100 users
INSERT INTO users (username, email, password_hash)
SELECT 
    'user_' || generate_series,
    'user_' || generate_series || '@example.com',
    'pbkdf2:sha256:600000$' || md5('password' || generate_series::text)
FROM generate_series(1, 100);

-- Generate 100 tweets
INSERT INTO tweets (content, user_id, created_at)
SELECT 
    'Test tweet ' || generate_series,
    (generate_series % 100) + 1,  -- Distribute tweets among users
    NOW() - (random() * interval '365 days')
FROM generate_series(1, 100);

-- Generate 100 likes
WITH tweet_ids AS (
    SELECT id FROM tweets
),
user_ids AS (
    SELECT id FROM users
)
INSERT INTO likes (user_id, tweet_id, created_at)
SELECT DISTINCT
    (SELECT id FROM user_ids ORDER BY random() LIMIT 1),  -- Random existing user_id
    (SELECT id FROM tweet_ids ORDER BY random() LIMIT 1),  -- Random existing tweet_id
    NOW() - (random() * interval '365 days')  -- Random timestamp within last year
FROM generate_series(1, 200)  -- Generate more than needed to account for duplicates
ON CONFLICT (user_id, tweet_id) DO NOTHING; 