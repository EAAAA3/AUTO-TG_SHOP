from emoji import emojize

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

from utils.dbs.database import Database, item_1, item_2


db = Database(item_1)
db2 = Database(item_2)
desc_n = db.get_netflix_items()
desc = db2.get_vk_instagram_items()



#profile.py
menu_profile = types.InlineKeyboardMarkup(row_width=1)
buttons = [
    types.InlineKeyboardButton(text='История заказов', callback_data='history'),
    types.InlineKeyboardButton(text='Активировать промокод', callback_data='promo')
]
menu_profile.add(*buttons)


#buy_items.py
activ_menu = types.InlineKeyboardMarkup(row_width=1)
buttons_1 = [
    types.InlineKeyboardButton(text=emojize(':heart_hands: Социальные сети :heart_hands:'), callback_data='vk/instagram'),
    types.InlineKeyboardButton(text=emojize(':television: Кино-сервисы :television:'), callback_data='netflix')
]
activ_menu.add(*buttons_1)


#buy_items.py
list_for_buy_vk_inst = types.InlineKeyboardMarkup(row_width=1)
buttons_2_v_i = [
    types.InlineKeyboardButton(text=f'{emojize(":customs:")}{desc[0]}{emojize(":customs:")} | {desc[1]} ₽ | Кол-во: {desc[2]} шт.', callback_data='accept_vk'),
    types.InlineKeyboardButton(text=f'{emojize(":sunrise:")}{desc[3]}{emojize(":sunrise:")} | {desc[4]} ₽ | Кол-во: {desc[5]} шт.', callback_data='accept_instagram'),
    types.InlineKeyboardButton(text='Назад ко всем категориям', callback_data='back_to_all')
]
list_for_buy_vk_inst.add(*buttons_2_v_i)


#buy_items.py
list_for_buy_netflix = types.InlineKeyboardMarkup(row_width=1)
buttons_2_n = [
    types.InlineKeyboardButton(text=f'{emojize(":popcorn:")}{desc_n[0]}{emojize(":popcorn:")} | {desc_n[1]} ₽ | Кол-во: {desc_n[2]} шт.', callback_data='accept_netflix'),
    types.InlineKeyboardButton(text='Назад ко всем категориям', callback_data='back_to_all')
]
list_for_buy_netflix.add(*buttons_2_n)


#buy_items.py
buy_netflix = types.InlineKeyboardMarkup(row_width=5)
buy_netflix.add(*[types.InlineKeyboardButton(text=i, callback_data=f'{i}_netflix') for i in range(1, desc_n[2]+1)])
buttons_3_n = [
    types.InlineKeyboardButton(text=emojize('Назад :right_arrow_curving_left:'), callback_data='back')
]
buttons_4_n = [
    types.InlineKeyboardButton(text=emojize('Назад ко всем категориям :clockwise_vertical_arrows:'), callback_data='back_to_all')
]
buy_netflix.add(*buttons_3_n)


#buy_items.py
buy_vk = types.InlineKeyboardMarkup(row_width=5)
buy_vk.add(*[types.InlineKeyboardButton(text=i, callback_data=f'{i}_vk') for i in range(1, desc[2]+1)])
buttons_3_v_i = [
    types.InlineKeyboardButton(text=emojize('Назад :right_arrow_curving_left:'), callback_data='back_1')
]
buttons_4_v_i = [
    types.InlineKeyboardButton(text=emojize('Назад ко всем категориям :clockwise_vertical_arrows:'), callback_data='back_to_all')
]
buy_vk.add(*buttons_3_v_i)
buy_vk.add(*buttons_4_v_i)


#buy_items.py
buy_inst = types.InlineKeyboardMarkup(row_width=5)
buy_inst.add(*[types.InlineKeyboardButton(text=i, callback_data=f'{i}_inst') for i in range(1, desc[5]+1)])
buy_inst.add(*buttons_3_v_i)
buy_inst.add(*buttons_4_v_i)


#buy_items.py
buy_buttons = types.InlineKeyboardMarkup(row_width=1)
buy_buttons_1 = [
    types.InlineKeyboardButton(text=emojize('Проверить оплату :check_mark_button:'), callback_data='paid'),
    types.InlineKeyboardButton(text=emojize('Отмена оплаты :cross_mark:'), callback_data='cancel')
]
buy_buttons.add(*buy_buttons_1)


#buy_items.py
return_to_menu = types.InlineKeyboardMarkup()
return_to_menu.add(*[types.InlineKeyboardButton(text=emojize('Назад ко всем категориям :clockwise_vertical_arrows:'), callback_data='back_to_all')])