from emoji import emojize

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text=emojize(':floppy_disk: Добавить товары :floppy_disk:')),
            KeyboardButton(text=emojize(':bar_chart: Статистика :bar_chart:'))
        ],
        [
            KeyboardButton(text=emojize(':postbox: Рассылка :postbox:'))
        ]
    ], resize_keyboard=True
)