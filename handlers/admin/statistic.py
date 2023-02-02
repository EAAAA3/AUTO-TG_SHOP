from emoji import emojize

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from utils.dbs.database import Database, name_1, item_1, item_2


db = Database(name_1)
db1 = Database(item_1)
db2 = Database(item_2)


async def cmd_statistic(message: types.Message):
    result = db.get_all_users_for_stats()
    vk, inst = db2.get_vk_instagram_items()[2], db2.get_vk_instagram_items()[5]
    netflix = db1.get_netflix_items()[2]
    await message.answer(f'{emojize(":person_juggling:")} Всего пользователей магазина: {result}\n'
                         f'{emojize(":receipt:")} Товаров на продаже:\n'
                         f'      1. {emojize(":popcorn:")} *Netflix* {emojize(":popcorn:")}: {netflix} позиций.\n'
                         f'      2. {emojize(":customs:")} *VK* {emojize(":customs:")}: {vk} позиций.\n'
                         f'      3. {emojize(":sunrise:")} *Intagram* {emojize(":sunrise:")}: {inst} позиций.\n', parse_mode='Markdown')


def register_cmd_statistic(dp: Dispatcher):
    dp.register_message_handler(cmd_statistic, Text(equals=emojize(':bar_chart: Статистика :bar_chart:')), is_admin=True)