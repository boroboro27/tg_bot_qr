from contextlib import suppress
from datetime import datetime
from aiogram.types import InputTextMessageContent, InlineQueryResultCachedPhoto
from aiogram import types, Dispatcher
from create_bot import dp, bot, CHAT_ID
import hashlib
import os
import client
import sqlite_db
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)


async def inline_handler(querry: types.InlineQuery):
    text = querry.query
    if text == "":
        pass
    else:
        result_id = hashlib.md5(text.encode()).hexdigest()
        
        pic_png = await client.gen_qr(text) 
        if pic_png.startswith('epicfail'):
            pass

        else:
            with open(pic_png, 'rb') as f: 
                infophoto = await bot.send_photo(chat_id=CHAT_ID, photo=f)
        
            #thumbphoto = infophoto["photo"][0]["file_id"]
            originalphoto = infophoto["photo"][-1]["file_id"]
            os.remove(pic_png) 

            qr_code = [types.InlineQueryResultCachedPhoto(
                    id=result_id,
                    title="CachedPhoto",
                    photo_file_id=originalphoto,
                    parse_mode='MarkdownV2',
                    description=text)
                ]
            await querry.answer(qr_code, cache_time=2, is_personal=False, switch_pm_text='Нажми на код или заходи в гости к коту', \
                                switch_pm_parameter='go')
            with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
                await infophoto.delete()
            
        qr_dict = {}
        qr_dict['text'] = text    
        qr_dict['img_id'] = originalphoto
        qr_dict['user_id'] = querry.from_user.id
        qr_dict['user_full_name'] = querry.from_user.full_name  
        qr_dict['inline'] = True   

        await sqlite_db.sql_add_cmd(qr_dict)

    

def register_handlers_other(dp : Dispatcher):
    dp.register_inline_handler(inline_handler)    
    