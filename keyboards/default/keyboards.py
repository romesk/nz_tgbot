from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton

btn = KeyboardButton('Новини')
news_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)

