import sqlite3
import base64
import base58
from solders.keypair import Keypair

con = sqlite3.connect("bot.db")
cur = con.cursor()

for user_id, secret in cur.execute("SELECT user_id, wallet_secret FROM users"):
    raw = base64.b64decode(secret)
    kp = Keypair.from_bytes(raw)

    print("\n==============================")
    print("User ID:", user_id)
    print("Public key:", kp.pubkey())
    print("Base58 private key:")
    print(base58.b58encode(raw).decode())

con.close()
