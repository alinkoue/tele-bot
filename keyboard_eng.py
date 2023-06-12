from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram import types

buttons = ["A2", "B1", "B2", "не знаю"]
buttons_level = ['vocabulary','grammar']
b1 = KeyboardButton("стоп")

i1 = InlineKeyboardButton("sd", callback_data='i1')
i2 = InlineKeyboardButton("aesrydj", callback_data='i2')
inline_keyboard = InlineKeyboardMarkup().insert(i1).insert(i2)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*buttons)
keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard2.add(*buttons_level)
keyboard3 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard3.add(b1)
