from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)