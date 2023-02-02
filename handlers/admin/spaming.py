import asyncio
from emoji import emojize

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import config
from utils.dbs.database import Database, name_1


bot_s = Bot(config.TOKEN)
db = Database(name_1)


class Spam_msg(StatesGroup):
    spam = State()


async def cmd_spaming(message: types.Message, state: FSMContext):
    await message.answer(f'Отправьте сообщение для рассылки {emojize(":memo:")}')
    await Spam_msg.spam.set()


async def spaming(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    for user in db.read():
        print(user)
        try:
            await bot_s.send_message(user, message.html_text)
            await asyncio.sleep(0.33)
        except:
            pass
    await message.answer(f'Рассылка успешно завершена {emojize(":outbox_tray:")}')


def register_cmd_spaming(dp: Dispatcher):
    dp.register_message_handler(cmd_spaming, Text(equals=emojize(':postbox: Рассылка :postbox:')), state='*', is_admin=True)
    dp.register_message_handler(spaming, state=Spam_msg.spam)
