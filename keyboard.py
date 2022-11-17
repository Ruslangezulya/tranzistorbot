from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

btn0=types.KeyboardButton('▲ Расшифровка транзистора')
btn1 = types.KeyboardButton('🧑 Мой профиль')
btn2 = types.KeyboardButton('💬 Связаться с разработчиком')


start.add(btn0, btn1, btn2)

