from aiogram import Bot, types

from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML, validate_token=True)
