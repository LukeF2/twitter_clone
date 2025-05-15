-- Generate 1,000,000 likes
WITH user_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY random()) as rn
    FROM users
),
tweet_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY random()) as rn
    FROM tweets
),
random_pairs AS (
    SELECT 
        u.id as user_id,
        t.id as tweet_id,
        NOW() - (random() * interval '365 days') as created_at
    FROM generate_series(1, 2000000) g
    JOIN user_ids u ON u.rn = (g % (SELECT COUNT(*) FROM users)) + 1
    JOIN tweet_ids t ON t.rn = (g % (SELECT COUNT(*) FROM tweets)) + 1
)
INSERT INTO likes (user_id, tweet_id, created_at)
SELECT DISTINCT user_id, tweet_id, created_at
FROM random_pairs
ON CONFLICT (user_id, tweet_id) DO NOTHING; 