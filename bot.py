
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import config
import keyboard 
import logging 
import sqlite3
storage = MemoryStorage() 
from config import TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
conn = sqlite3.connect('data.db')
cur = conn.cursor()
conn.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, username TEXT, latitude FLOAT, longitude FLOAT)')
conn.commit();
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,)
  
                    

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, f"Транзистор-Бот приветствует вас, *{message.from_user.first_name}*! \nВоспользуйтесь меню ниже для выбора нужной опции. \n P.S. На данный момент бот работает с кремниевыми биполярными высочастотными транзисторами средней мощности (от КТ626А до КТ646Б) ", reply_markup=keyboard.start, parse_mode='Markdown')
    try:
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users (user_id, username) VALUES("{message.from_user.id}", "@{message.from_user.username}")')
        conn.commit()
    except Exception as e:
        print(e)
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users (user_id) VALUES("{message.from_user.id}")')
        conn.commit()
          
@dp.message_handler(content_types=['text'])
async def get_message(message):
    
    if message.text == "▲ Расшифровка транзистора":
        await bot.send_message(message.chat.id, text = "*Введите команду в формате: /f название транзистора*", parse_mode='Markdown')        
    if message.text == "🧑 Мой профиль":
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        prem = 0               
        result = cur.fetchall()
        cur.execute(f'SELECT * FROM users WHERE user_id = "{message.chat.id}"')
        result = cur.fetchall()
        await bot.send_message(message.chat.id, f'🧑Ваше имя: {message.from_user.first_name}🧑\n🧑Ваш Telegram ID: {list(result[0])[0]}🧑')      
    if message.text == "💬 Связаться с разработчиком":
        await bot.send_message(message.chat.id, text = "*Разработчик - @greycatrapper*", parse_mode='Markdown')
    
        
    if "/f" in message.text:
        message_info = message.text[8:]
        if len(message_info) > 0:                       
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()              
            cur.execute(f'SELECT * FROM tranzistors WHERE name = "{message_info}"')
            result = cur.fetchall()
            conn.commit()  
            str_out = ""
            for i in range(len(result)):
                date = result[i]
                str_out += f'Название транзистора: {date[1]}. \nСтруктура транзистора: {date[2]}. \nМаксимально допустимое напряжение: {date[3]}. \nМаксимальная мощность коллектора: {date[4]}. \nОбратный ток коллектора: {date[5]} \n'
            print(str_out)
            await bot.send_message(message.chat.id, f'{str_out}')
        else:
            await bot.send_message(message.chat.id, text = "*Вы не ввели данные транзистора.*", parse_mode='Markdown')
        
           

if __name__ == '__main__':
    executor.start_polling(dp)


