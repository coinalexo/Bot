import os
import json
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            sol REAL DEFAULT 0,
            tokens TEXT DEFAULT '{}',
            wallet_pub TEXT,
            wallet_secret TEXT
        )
    """)

    con.commit()
    cur.close()
    con.close()

def get_user(user_id):
    con = get_conn()
    cur = con.cursor()

    cur.execute(
        "SELECT sol, tokens, wallet_pub, wallet_secret FROM users WHERE user_id=%s",
        (user_id,)
    )
    row = cur.fetchone()
    cur.close()
    con.close()

    if not row:
        return None

    sol, tokens_json, pub, secret = row
    return {"sol": sol, "tokens": json.loads(tokens_json), "pub": pub, "secret": secret}

def create_user(user_id, pub, secret):
    con = get_conn()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO users (user_id, wallet_pub, wallet_secret) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
        (user_id, pub, secret)
    )

    con.commit()
    cur.close()
    con.close()

def update_balance(user_id, sol=None, tokens=None):
    con = get_conn()
    cur = con.cursor()

    if sol is not None:
        cur.execute("UPDATE users SET sol=%s WHERE user_id=%s", (sol, user_id))

    if tokens is not None:
        cur.execute("UPDATE users SET tokens=%s WHERE user_id=%s", (json.dumps(tokens), user_id))

    con.commit()
    cur.close()
    con.close()
