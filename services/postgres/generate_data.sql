-- Generate 1,000,000 likes
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
FROM generate_series(1, 2000000)  -- Generate more than needed to account for duplicates
ON CONFLICT (user_id, tweet_id) DO NOTHING; 