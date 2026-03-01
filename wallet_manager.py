from solders.keypair import Keypair
from db import get_user, create_user
import base64


def get_or_create_wallet(user_id: str):
    user = get_user(user_id)

    # если кошелек уже есть
    if user and user.get("pub") and user.get("secret"):
        return user["pub"], user["secret"]

    # создаём новый
    wallet = Keypair()
    pub = str(wallet.pubkey())
    secret = base64.b64encode(bytes(wallet)).decode()

    if user:
        # пользователь есть → обновляем кошелек
        import sqlite3
        con = sqlite3.connect("bot.db")
        cur = con.cursor()
        cur.execute(
            "UPDATE users SET wallet_pub=?, wallet_secret=? WHERE user_id=?",
            (pub, secret, user_id),
        )
        con.commit()
        con.close()
    else:
        # пользователя нет → создаём
        create_user(user_id, pub, secret)

    return pub, secret
