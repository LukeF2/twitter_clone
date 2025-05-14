import os
import sys
import psycopg2
from faker import Faker
from datetime import datetime, timedelta
import random

def load_test_data(num_rows, is_test=False):
    # Connect to the database using Unix socket
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'hello_flask_dev'),
        user=os.getenv('POSTGRES_USER', 'hello_flask'),
        password=os.getenv('POSTGRES_PASSWORD', 'hello_flask'),
        host='/var/run/postgresql'  # Use Unix socket instead of TCP/IP
    )
    cur = conn.cursor()
    
    fake = Faker()
    
    # Generate users
    print(f"Generating {num_rows} users...")
    for i in range(num_rows):
        email = fake.email()
        
        cur.execute(
            "INSERT INTO users (email, active) VALUES (%s, %s)",
            (email, True)
        )
        if not is_test and i % 10000 == 0:
            print(f"Generated {i} users...")
            conn.commit()
    
    conn.commit()
    print("Users generated successfully")
    
    # Generate tweets (10x more than users)
    print(f"Generating {num_rows * 10} tweets...")
    for i in range(num_rows * 10):
        user_id = random.randint(1, num_rows)
        content = fake.text(max_nb_chars=280)
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
        
        cur.execute(
            "INSERT INTO tweets (user_id, content, created_at) VALUES (%s, %s, %s)",
            (user_id, content, created_at)
        )
        if not is_test and i % 100000 == 0:
            print(f"Generated {i} tweets...")
            conn.commit()
    
    conn.commit()
    print("Tweets generated successfully")
    
    # Generate likes (5x more than users)
    print(f"Generating {num_rows * 5} likes...")
    likes_generated = 0
    max_attempts = num_rows * 20  # Allow more attempts to ensure we get enough unique likes
    attempts = 0
    
    while likes_generated < num_rows * 5 and attempts < max_attempts:
        user_id = random.randint(1, num_rows)
        tweet_id = random.randint(1, num_rows * 10)
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
        
        try:
            cur.execute(
                "INSERT INTO likes (user_id, tweet_id, created_at) VALUES (%s, %s, %s)",
                (user_id, tweet_id, created_at)
            )
            likes_generated += 1
            if not is_test and likes_generated % 100000 == 0:
                print(f"Generated {likes_generated} likes...")
                conn.commit()
        except psycopg2.IntegrityError:
            # Skip if this user already liked this tweet
            conn.rollback()
        
        attempts += 1
    
    conn.commit()
    print(f"Likes generated successfully (generated {likes_generated} likes after {attempts} attempts)")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Check if we're running in test mode (GitHub Actions)
    is_test = os.getenv('GITHUB_ACTIONS') == 'true'
    
    # Use small numbers for testing, large numbers for production
    if is_test:
        num_rows = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    else:
        num_rows = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
    
    load_test_data(num_rows, is_test) 