from emoji import emojize

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types


#download.py
load_n_del = types.InlineKeyboardMarkup(row_width=1)
buttons = [
    types.InlineKeyboardButton(text=emojize('Загрузить :inbox_tray:'), callback_data='load'),
    types.InlineKeyboardButton(text=emojize('Удалить :outbox_tray:'), callback_data='delete')
]
load_n_del.add(*buttons)


#download.py
items = types.InlineKeyboardMarkup(row_width=1)
buttons_2 = [
    types.InlineKeyboardButton(text='Netflix', callback_data='_netflix'),
    types.InlineKeyboardButton(text='VK/Instagram', callback_data='_vk_instagram'),
    types.InlineKeyboardButton(text=emojize('Удалить :outbox_tray:'), callback_data='_delete')
]
items.add(*buttons_2)


#download.py
accept_n_back_netflix = types.InlineKeyboardMarkup(row_width=1)
buttons_3 = [
    types.InlineKeyboardButton(text=emojize('Подтвердить :check_mark_button:'), callback_data='_accept_netflix'),
    types.InlineKeyboardButton(text=emojize('Назад :right_arrow_curving_left:'), callback_data='_back')
]
accept_n_back_netflix.add(*buttons_3)


#download.py
accept_n_back_vk_instagram = types.InlineKeyboardMarkup(row_width=1)
buttons_4 = [
    types.InlineKeyboardButton(text=emojize('Подтвердить :check_mark_button:'), callback_data='_accept_vk_instagram'),
    types.InlineKeyboardButton(text=emojize('Назад :right_arrow_curving_left:'), callback_data='_back')
]
accept_n_back_vk_instagram.add(*buttons_4)


#download.py
admin_list_items = types.InlineKeyboardMarkup(row_width=1)
button_1 = [
    types.InlineKeyboardButton(text=emojize('Наличие товаров :clipboard:'), callback_data='_list_items'),
]
admin_list_items.add(*button_1)