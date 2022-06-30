from aiogram import types, Dispatcher
from create_bot import bot, CHAT_ID
import sqlite_db
import pyqrcode as pq
from datetime import datetime
import os


async def cmd_start(msg: types.Message):
    await msg.delete()
    await bot.send_sticker(chat_id=msg.from_user.id, \
                           sticker=r"CAACAgIAAxkBAAEFFCFirujxpjEHNPWGViBr9VbjWx1T-AACpxQAAujW4hKEnFMX5yBTnyQE")
    await msg.answer(text=f'{msg.from_user.first_name}, всё изи!!\n' + \
                     'Чтобы р̶а̶з̶б̶у̶д̶и̶т̶ь ̶Q̶R̶-̶к̶о̶т̶а̶ сделать QR-код, просто отправь ему любой текст:)')    
  
# генерация и отправка qr
async def run_qr(msg: types.Message):
    await bot.send_sticker(chat_id=msg.from_user.id, \
                           sticker=r"CAACAgIAAxkBAAEFFCVirulIFb8BuMm31xatlD2zw9EuegACrBQAAujW4hKEaMxpKiLYHyQE")
    await msg.answer(text=f'{msg.from_user.first_name}, кот принял текст в обработку!\nПожалуйста, подожди!')      
   
    pic_png = await gen_qr(msg.text)  

    if pic_png.startswith('epicfail'):
        await bot.send_sticker(chat_id=msg.from_user.id, \
                            sticker=r"CAACAgIAAxkBAAEFFDRirvuQM-E0eLtt5S5gAqF6UvnO7AACqRQAAujW4hJOskENePr_2CQE")
        await msg.answer(text='Что-то пошло не так.., но мой хозяин уже разбирается в причинах.\n' + \
                         'Попробуй пока отправить другой текст.')
        originalphoto = pic_png

    else:
        with open(file=pic_png, mode='rb') as photo:
            infophoto = await bot.send_photo(chat_id=msg.from_user.id, photo=photo)
            originalphoto = infophoto["photo"][-1]["file_id"]
            await bot.send_sticker(chat_id=msg.from_user.id, \
                            sticker=r"CAACAgIAAxkBAAEFFBtirudFNzomxganOM7ivV48JURXWwACoBQAAujW4hLYaepq9tQKPyQE")
            await msg.answer(text='всё изи! QR-кот готов и уже скучает!\nПросто отправь ему текст:)')
            
        os.remove(pic_png)   
        
    qr_dict = {}
    qr_dict['text'] = msg.text    
    qr_dict['img_id'] = originalphoto
    qr_dict['user_id'] = msg.from_user.id
    qr_dict['user_full_name'] = msg.from_user.full_name
    qr_dict['inline'] = False    

    await sqlite_db.sql_add_cmd(qr_dict)

async def gen_qr(text: str) -> str:    
    try:
        #t = text.encode('utf-8')
        qr_code = pq.create(text, encoding='utf-8')
        dt = str(datetime.now()) 
        qr_code.png(file=(pic:=(f'qr_code_' + dt + '.png')), \
                    scale=6)        
        return pic 
    except Exception as err:
        print(texterr:=f'Ошибка генерации QR-кода для запроса {text}: {err}')
        await bot.send_message(chat_id=CHAT_ID, text=texterr)
        return f'epicfail: {err}'

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start', 'help'])    
    dp.register_message_handler(run_qr)