import sqlite3
from aiogram import *


base = sqlite3.connect('new.db')
cur = base.cursor()

def reg(id, stats, username):
    reg = cur.execute('INSERT INTO data VALUES(?,?,?)', (id,stats,username))

def udpate(user_id):
    update = cur.execute(f'UPDATE data SET stats == stats+1 WHERE id == {user_id}')
    base.commit()

def add(id, stats, username):
    add_user = cur.execute('INSERT INTO data VALUES(?,?,?)', (id, stats, username))
    base.commit()