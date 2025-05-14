import os
import sys
import psycopg2
from faker import Faker
from datetime import datetime, timedelta
import random

def load_test_data(num_rows):
    # Connect to the database
    conn = psycopg2.connect(
        dbname="hello_flask_dev",
        user="hello_flask",
        password="hello_flask",
        host="localhost"
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
    
    conn.commit()
    print("Tweets generated successfully")
    
    # Generate likes (5x more than tweets)
    print(f"Generating {num_rows * 50} likes...")
    for i in range(num_rows * 50):
        user_id = random.randint(1, num_rows)
        tweet_id = random.randint(1, num_rows * 10)
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
        
        try:
            cur.execute(
                "INSERT INTO likes (user_id, tweet_id, created_at) VALUES (%s, %s, %s)",
                (user_id, tweet_id, created_at)
            )
        except psycopg2.IntegrityError:
            # Skip if this user already liked this tweet
            conn.rollback()
            continue
    
    conn.commit()
    print("Likes generated successfully")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Default to 100 rows for testing, but can be overridden
    num_rows = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    load_test_data(num_rows) 