# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
from handlers import cmd_start, jup_checker_handler, kiloex_checker_handler, hyperlane_checker_handler, process_addresses
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Регистрация хэндлеров
router.message.register(cmd_start, Command("start"))
router.message.register(jup_checker_handler, lambda message: message.text == "JUP checker")
router.message.register(kiloex_checker_handler, lambda message: message.text == "KiloEx checker")
router.message.register(hyperlane_checker_handler, lambda message: message.text == "Hyperlane checker")
router.message.register(process_addresses)

dp.include_router(router)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
