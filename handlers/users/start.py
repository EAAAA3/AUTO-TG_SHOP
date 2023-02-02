from emoji import emojize

from aiogram import types, Dispatcher

from config import ADMINS
from utils.dbs.database import Database, name_1
from keyboards.s_keyboard import menu
from keyboards.admin_keyboard import admin_menu


db = Database(name_1)


async def cmd_start(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer(f'Привет, вот твоя админ-панель {emojize(":briefcase:")}', reply_markup=admin_menu)
    elif message.from_user.id not in db.read() and message.from_user.id not in ADMINS:
        db.add_user(
            (
                f'{message.from_user.id}',
                f'{0}',
                f'{0}'
            )
        )
        await message.answer(f'Добро пожаловать, это бот авто-продаж LOLZIK. Тут есть все необходимое что тебе нужно '
                             f'ещё и по вкусным ценам {emojize(":money-mouth_face:")}', reply_markup=menu)
    else:
        await message.answer(f'Добро пожаловать, это бот авто-продаж LOLZIK. Тут есть все необходимое что тебе нужно '
                             f'ещё и по вкусным ценам {emojize(":money-mouth_face:")}', reply_markup=menu)


def register_cmd_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')