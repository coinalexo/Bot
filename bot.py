import asyncio
from aiogram import Bot, Dispatcher
from handlers import router
from config import BOT_TOKEN
from db import init_db   # ✅ ДОБАВИТЬ

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

init_db()   # ✅ создаёт таблицы

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
