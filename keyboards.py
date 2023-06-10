from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
b1 = KeyboardButton("найти собеседника")
b2 = KeyboardButton("не хочу искать")


i1=InlineKeyboardButton("sd",callback_data='i1')
i2=InlineKeyboardButton("aesrydj",callback_data='i2')
inline_keyboard = InlineKeyboardMarkup().insert(i1).insert(i2)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(b1).add(b2)
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard2.add(b2)
