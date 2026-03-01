import base64
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction
from solana.rpc.async_api import AsyncClient

from wallet_manager import get_or_create_wallet
from db import get_user, update_balance
from menu import update_menu
from states import pending_withdraw, user_token, reset_state
from config import RPC_URL

router = Router()

# ========= SAFE DELETE =========
async def safe_delete(msg: Message):
    try:
        await msg.delete()
    except:
        pass

# ========= START =========
@router.message(lambda m: m.text == "/start")
async def start(msg: Message, bot):
    uid = msg.from_user.id
    reset_state(uid)

    pub, _ = get_or_create_wallet(str(uid))

    await update_menu(bot, uid,
        "🚀 <b>Solana Bot</b>\n\n"
        f"Deposit address:\n<code>{pub}</code>"
    )

# ========= BALANCE =========
@router.callback_query(lambda c: c.data == "balance")
async def balance_cb(cb: CallbackQuery, bot):
    await cb.answer()
    uid = cb.from_user.id
    reset_state(uid)

    user = get_user(str(uid))
    await update_menu(bot, uid, f"💳 <b>SOL:</b> {user['sol']:.4f}")

# ========= DEPOSIT =========
@router.callback_query(lambda c: c.data == "deposit")
async def deposit_cb(cb: CallbackQuery, bot):
    await cb.answer()
    uid = cb.from_user.id
    reset_state(uid)

    pub, _ = get_or_create_wallet(str(uid))
    await update_menu(bot, uid, f"Send SOL to:\n<code>{pub}</code>")

# ========= WITHDRAW =========
@router.callback_query(lambda c: c.data == "withdraw")
async def withdraw_cb(cb: CallbackQuery, bot):
    await cb.answer()
    uid = cb.from_user.id

    if uid in pending_withdraw:
        await update_menu(bot, uid, "⚠️ Finish current withdrawal.")
        return

    pending_withdraw[uid] = {"step": 1}
    await update_menu(bot, uid, "📤 Send withdrawal address:")

@router.message()
async def withdraw_flow(msg: Message, bot):
    uid = msg.from_user.id

    if uid not in pending_withdraw:
        return

    await safe_delete(msg)
    state = pending_withdraw[uid]

    # STEP 1
    if state["step"] == 1:
        try:
            Pubkey.from_string(msg.text)
        except:
            pending_withdraw.pop(uid)
            await update_menu(bot, uid, "❌ Invalid address.")
            return

        state["address"] = msg.text
        state["step"] = 2
        await update_menu(bot, uid, "💰 Enter amount in SOL:")
        return

    # STEP 2
    try:
        amount = float(msg.text)
    except:
        pending_withdraw.pop(uid)
        await update_menu(bot, uid, "❌ Invalid amount.")
        return

    user = get_user(str(uid))
    if amount <= 0 or amount > user["sol"]:
        pending_withdraw.pop(uid)
        await update_menu(bot, uid, "❌ Not enough SOL.")
        return

    pub, secret = get_or_create_wallet(str(uid))

    async with AsyncClient(RPC_URL) as client:
        tx = Transaction(fee_payer=Pubkey.from_string(pub)).add(
            transfer(
                TransferParams(
                    from_pubkey=Pubkey.from_string(pub),
                    to_pubkey=Pubkey.from_string(state["address"]),
                    lamports=int(amount * 1e9),
                )
            )
        )
        recent = await client.get_latest_blockhash()
        tx.recent_blockhash = recent.value.blockhash

        kp = Keypair.from_bytes(base64.b64decode(secret))
        await client.send_transaction(tx, kp)

    update_balance(str(uid), sol=user["sol"] - amount)
    pending_withdraw.pop(uid)

    await update_menu(bot, uid, "✅ Withdrawal sent!")

# ========= TOKEN =========
@router.message(lambda m: 32 <= len(m.text) <= 44 and not m.text.startswith("/"))
async def set_token(msg: Message, bot):
    uid = msg.from_user.id
    if uid in pending_withdraw:
        return

    await safe_delete(msg)
    user_token[str(uid)] = msg.text
    await update_menu(bot, uid, "✅ Token saved. Use Buy buttons.")
