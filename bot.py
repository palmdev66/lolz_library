import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from handlers import user
from utils import db as api

from config import TOKEN

async def prepare():
    await api.generate()
    logging.basicConfig(level=logging.INFO)

async def main():
    await prepare()

    bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    dp = Dispatcher()
    dp.include_routers(user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())