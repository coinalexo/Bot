import base64
import json
import base58
from solders.keypair import Keypair

wallet_secret = "Y02bc0B0rgSemmGLWGUFHh2ZJEdvOAOxaqj4ZxwVvnpGPyXwMQ+RmDixX6TkSiVzJoZnl8M01ejSYLYC1xyE/g=="

raw = base64.b64decode(wallet_secret)
kp = Keypair.from_bytes(raw)

print("Public key:", kp.pubkey())
print("\nBase58 private key:\n")
print(base58.b58encode(raw).decode())
