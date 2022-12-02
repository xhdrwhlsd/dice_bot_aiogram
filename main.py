from aiogram import Bot, Dispatcher, executor, types

import db

import sqlite3

import config as cfg

import time

import asyncio

from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
                                      
from contextlib import suppress                                      
from aiogram.types import ReplyKeyboardRemove
import buttons




base = sqlite3.connect('new.db')
cur = base.cursor()






x = ['щелбан', 'фофан', 'лось', 'конь']

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

#ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12




async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()

async def on_startup(_):
    print('Бот вышел в онлайн')


@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer('Привет!\nДля начала игры ознакомьтесь с командами в /help',reply_markup=buttons.kb_delete)

@dp.message_handler(commands=['Первый'], commands_prefix = '🎲')
async def dice(message:types.Message):
    global first, firstid
    firstid = message.from_user.id
    first = message.from_user.username
    a = await message.answer('Первый участник есть! Кто второй?', reply_markup=buttons.kb2)
    asyncio.create_task(delete_message(a,30))
    print(first)
    await message.delete()




@dp.message_handler(commands=['Второй'], commands_prefix='🎲')
async def d(message:types.Message):
    global second, secondid
    secondid = message.from_user.id
    second = message.from_user.username
    await message.delete()
    print(second)

    if first == second:
        await message.answer('Второго участника нет! Дождитесь второго игрока.')
        print(second)
    
        

    else:
        c = await message.answer('Готово! Игра сейчас начнется', reply_markup=buttons.kb_delete)
        asyncio.create_task(delete_message(c,30))
        time.sleep(2)
        a =  await message.answer_dice('🎲')
        a
        time.sleep(4)
        b =  await message.answer_dice('🎲')
        time.sleep(4)
        c = a.dice.value
        d = b.dice.value
        if c>d:
            await message.answer(f'@{second}, ты проиграл')
            db.udpate(firstid)
            #await message.answer(f'Проигравшему {random.choice(x)}')
        elif d>c:
            await message.answer(f'@{first}, ты проиграл')
            db.udpate(secondid)
            #await message.answer(f'Проигравшему {random.choice(x)}')
        else:
            await message.answer('Ничья!')

@dp.message_handler(commands=['help'])
async def help(message:types.Message):
    await message.answer('/reg - команда регистрации для начала учета Ваших побед.\n/dice - команда для начала игры.\n/stats - количество Ваших побед.\nПриятной игры!')

@dp.message_handler(commands=['reg'])
async def reg(message:types.Message):
    try:
        db.add(message.from_user.id, 0, message.from_user.username)
        await message.answer('Вы успешно зарегистрировались.')
    except:
        await message.answer('Вы уже зарегистрированы!')

@dp.message_handler(commands=['dice'])
async def dice(message:types.Message):
    b = await message.answer( 'Кто хочет сыграть?', reply_markup=buttons.kb1)
    asyncio.create_task(delete_message(b,30))

@dp.message_handler(commands=['stats'])
async def stats(message:types.Message):
    users = message.from_user.id
    for a in cur.execute(f'SELECT stats FROM data WHERE id == {users}').fetchone():
        await message.answer(f'Вы выиграли {a} раз(-а)')





   


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)    