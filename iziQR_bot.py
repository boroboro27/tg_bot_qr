from aiogram.utils import executor
import client
import sqlite_db
import other
from create_bot import dp

async def on_startup(_):
    print('Бот iziQR вышел в онлайн')
    sqlite_db.sql_start()
    
client.register_handlers_client(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)