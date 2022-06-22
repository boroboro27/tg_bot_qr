import sqlite3 as sq
from create_bot import bot, CHAT_ID

def sql_start():
    global base, cur
    base = sq.connect('bot.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS qr_codes(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, img_id TEXT, user_id TEXT, user_full_name TEXT, inline INTEGER, datetimeUTC0 TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    base.commit()

async def sql_add_cmd(qr_dic: dict):
    try:
        cur.execute('INSERT INTO qr_codes (text, img_id, user_id, user_full_name, inline) VALUES(?, ?, ?, ?, ?)', \
                    tuple(qr_dic.values()))
        base.commit()        
    except Exception as err:
        
        print(texterr:=f'Ошибка БД: {err}, {qr_dic}')
        await bot.send_message(chat_id=CHAT_ID, text=texterr)

async def sql_read_all_cmd():
    return cur.execute('SELECT * FROM qr_codes').fetchall()

async def sql_delete_cmd(data):
    cur.execute('DELETE FROM recipes WHERE name == ?', (data,))
    base.commit()