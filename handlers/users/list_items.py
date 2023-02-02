from emoji import emojize

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from utils.dbs.database import Database, item_1, item_2


db = Database(item_1)
db_2 = Database(item_2)


async def cmd_list_items(message: types.Message):   # Если БД пустая, то нужно сюда написать if ... == 0, выводиться пустой текст
    name_netflix, price_netflix, amount_netflix = db.get_netflix_items()
    name_vk, price_vk, amount_vk, name_inst, price_inst, amount_inst = db_2.get_vk_instagram_items()
    caption_netflix = f'{emojize(":minus:")*3}<b>Netflix</b>{emojize(":minus:")*3}'
    caption_vk_tg_inst = f'{emojize(":minus:")*3}<b>VK/Instagram</b>{emojize(":minus:")*3}'
    caption_music = f'{emojize(":minus:")*3}<b>Spotify</b>{emojize(":minus:")*3}'
    await message.answer(f'{caption_netflix}\n'
                         f'   {emojize(":popcorn:")}{name_netflix}{emojize(":popcorn:")}. | '
                         f'{price_netflix} ₽ | '
                         f'<b>Кол-во</b>: {amount_netflix} шт.\n\n'
                         f'{caption_vk_tg_inst}\n'
                         f'   {emojize(":customs:")}{name_vk}{emojize(":customs:")}. | '
                         f'{price_vk} ₽ | '
                         f'<b>Кол-во</b>: {amount_vk} шт.\n'
                         f'   {emojize(":sunrise:")}{name_inst}{emojize(":sunrise:")}. | '
                         f'{price_inst} ₽ | '
                         f'<b>Кол-во</b>: {amount_inst} шт.', parse_mode='HTML')   # Сделать сумму и кол-во жирным шрифтом


def register_list_items(dp: Dispatcher):
    dp.register_message_handler(cmd_list_items, Text(equals=emojize(':bookmark_tabs: Наличие товаров :bookmark_tabs:')))