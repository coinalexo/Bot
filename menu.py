from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

menu_messages = {}

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Deposit", callback_data="deposit"),
            InlineKeyboardButton(text="💸 Withdraw", callback_data="withdraw"),
        ],
        [InlineKeyboardButton(text="💳 Balance", callback_data="balance")],
        [
            InlineKeyboardButton(text="⚡ Buy 25%", callback_data="buy_25"),
            InlineKeyboardButton(text="⚡ Buy 50%", callback_data="buy_50"),
            InlineKeyboardButton(text="⚡ Buy Max", callback_data="buy_max"),
        ],
        [
            InlineKeyboardButton(text="🔻 Sell 25%", callback_data="sell_25"),
            InlineKeyboardButton(text="🔻 Sell 50%", callback_data="sell_50"),
            InlineKeyboardButton(text="🔻 Sell Max", callback_data="sell_max"),
        ],
    ])

async def update_menu(bot, user_id: int, text: str):
    # если уже есть сообщение — пробуем редактировать
    if user_id in menu_messages:
        try:
            await bot.edit_message_text(
                text,
                chat_id=user_id,
                message_id=menu_messages[user_id],
                reply_markup=main_menu(),
                parse_mode="HTML"
            )
            return
        except TelegramBadRequest as e:
            # ❗ игнорируем ситуацию "message is not modified"
            if "message is not modified" in str(e):
                return
            # если сообщение удалено — отправим новое
        except Exception:
            pass

    # отправляем новое сообщение
    msg = await bot.send_message(
        user_id,
        text,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )
    menu_messages[user_id] = msg.message_id
