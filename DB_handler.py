import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

DB_KEY = os.getenv('DB_KEY')

def insert_comment(data):
    try:
        with psycopg2.connect(DB_KEY) as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO comments (username, fullname, comment) VALUES (%s, %s, %s)"
                cur.execute(sql, data) 
                conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

def insert_prompt(data):
    try:
        with psycopg2.connect(DB_KEY) as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO prompt (username, fullname, prompt_text) VALUES (%s, %s, %s)"
                cur.execute(sql, data) 
                conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

