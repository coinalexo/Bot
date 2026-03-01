import sqlite3
import json
import os

DB_NAME = "/data/bot.db"

def init_db():
    con = sqlite3.connect(DB_NAME)
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
    con.close()

def get_user(user_id):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("SELECT sol, tokens, wallet_pub, wallet_secret FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()

    if not row:
        con.close()
        return None

    sol, tokens_json, pub, secret = row
    tokens = json.loads(tokens_json)

    con.close()
    return {"sol": sol, "tokens": tokens, "pub": pub, "secret": secret}

def create_user(user_id, pub, secret):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO users (user_id, wallet_pub, wallet_secret) VALUES (?, ?, ?)",
        (user_id, pub, secret)
    )
    con.commit()
    con.close()

def update_balance(user_id, sol=None, tokens=None):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    if sol is not None:
        cur.execute("UPDATE users SET sol=? WHERE user_id=?", (sol, user_id))

    if tokens is not None:
        cur.execute("UPDATE users SET tokens=? WHERE user_id=?", (json.dumps(tokens), user_id))

    con.commit()
    con.close()

