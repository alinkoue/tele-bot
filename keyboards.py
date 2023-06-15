from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram import types

buttons = ["A2", "B1", "B2", "не знаю"]
buttons_level = ['vocabulary', 'grammar']
buttons_answer = ["a", "b", "c", "d"]
b1 = KeyboardButton("стоп")

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*buttons)
keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard2.add(*buttons_level)
keyboard3 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard3.add(b1)
keyboard4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard4.add(*buttons_answer)
