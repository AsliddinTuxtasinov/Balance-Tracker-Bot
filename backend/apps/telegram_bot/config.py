from aiogram import Bot, Dispatcher
from decouple import config

BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")  # .env orqali token olishni tavsiya qilaman

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)
