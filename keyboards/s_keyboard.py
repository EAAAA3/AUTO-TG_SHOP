from emoji import emojize

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text=emojize(':open_book: Все категории :open_book:')),
            KeyboardButton(text=emojize(':bookmark_tabs: Наличие товаров :bookmark_tabs:'))
        ],
        [
            KeyboardButton(text=emojize(':bust_in_silhouette: Профиль :bust_in_silhouette:'))
        ],
        [
            KeyboardButton(text=emojize(':scroll: Правила :scroll:')),
            KeyboardButton(text=emojize(':red_heart: Помощь :red_heart:'))
        ]
    ], resize_keyboard=True
)