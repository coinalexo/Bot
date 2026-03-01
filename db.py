import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            sol REAL DEFAULT 0,
            wallet_pub TEXT,
            wallet_secret TEXT
        )
    """)

    con.commit()
    con.close()

def get_user(user_id: str):
    con = get_conn()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user = cur.fetchone()
    con.close()
    return user

def create_user(user_id: str, pub: str, secret: str):
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (user_id, wallet_pub, wallet_secret) VALUES (%s,%s,%s)",
        (user_id, pub, secret),
    )
    con.commit()
    con.close()

def update_balance(user_id: str, sol: float):
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "UPDATE users SET sol=%s WHERE user_id=%s",
        (sol, user_id),
    )
    con.commit()
    con.close()

