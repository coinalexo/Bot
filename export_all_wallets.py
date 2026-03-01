import sqlite3
import base64

con = sqlite3.connect("bot.db")
cur = con.cursor()

print("\n=== ALL WALLETS ===\n")

for row in cur.execute("SELECT user_id, wallet_pub, wallet_secret FROM users"):
    user_id, pub, secret = row

    print(f"User ID: {user_id}")
    print(f"Address: {pub}")
    print(f"Private key (base64): {secret}")
    print(f"Private key (decoded): {base64.b64decode(secret)}")
    print("-" * 50)

con.close()
