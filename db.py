import sqlite3
import json
import os

DB_NAME = "bot.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

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
    con.close()
