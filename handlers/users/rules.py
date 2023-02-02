from emoji import emojize

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text


async def cmd_rules(message: types.Message):
    await message.answer('Правила замены не валидного товара:\n'
                         '-Замена товара от 7 дней в зависимости от категории товара.\n'
                         '-При замене товара предоставляется скрин.\n'
                         '-Если Вы пытались сменить данные, то на такие товары гарантия не распространяется\n'
                         f'{emojize(":double_exclamation_mark:")} Незнание правил не освобождает от ответственности {emojize(":double_exclamation_mark:")}\n'
                         f'{emojize(":minus:")*15}\n'
                         '1. Номер заказа\n'
                         '2. Какой товар вы купили\n'
                         '3. Скриншот/Доказательство что аккаунт нерабочий.\n'
                         f'{emojize(":minus:")*15}')


def register_cmd_rules(dp: Dispatcher):
    dp.register_message_handler(cmd_rules, Text(equals=emojize(':scroll: Правила :scroll:')))