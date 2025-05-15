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
FROM generate_series(1, 100); 