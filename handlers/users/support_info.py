from emoji import emojize

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text


async def cmd_support(message: types.Message):
    await message.answer(f'{emojize(":minus:")*15}\n'
                         f'{emojize(":gear:")}| По всем вопросам писать в тех. поддержку: https://t.me/aloaloalolz\n'
                         f'{emojize(":telephone:")}| Отвечаем с 12:00 - 22:00 по МСК\n'
                         f'{emojize(":memo:")}| Совершая покупку через данный сервис, вы автоматически соглашаетесь со всеми требованиями и правилами нашего магазина!\n'
                         f'{emojize(":minus:")*15}\n'
                         f'Любое оскорбление в  сторону поддержки - бан.\n'
                         f'{emojize(":minus:")*15}')


def register_cmd_support_info(dp: Dispatcher):
    dp.register_message_handler(cmd_support, Text(equals=emojize(':red_heart: Помощь :red_heart:')))