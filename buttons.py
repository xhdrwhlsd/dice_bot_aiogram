from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
b1 = KeyboardButton('🎲Первый')
b2 = KeyboardButton('🎲Второй')

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb1.add(b1)
kb_delete = ReplyKeyboardRemove()
kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb2.add(b2)

