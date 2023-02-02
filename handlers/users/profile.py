from emoji import emojize

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.dbs.database import Database, name_1
from keyboards.i_keyboard import menu_profile


db = Database(name_1)

class Promo(StatesGroup):
    promo = State()


async def cmd_profile(message: types.Message):
    id, balance = db.get_id_n_balance(message.from_user.id)
    await message.answer(f'{emojize(":man_standing:")} <b>Имя</b>: {message.from_user.first_name}\n'
                         f'{emojize(":key:")} <b>ID</b>: {id}\n'
                         f'{emojize(":money_bag:")} <b>Баланс</b>: {balance} ₽', reply_markup=menu_profile, parse_mode='HTML')


async def call_history(call: types.CallbackQuery):
    await call.message.answer(f'<b>Всего у Вас заказов</b>: {db.get_purchases(call.from_user.id)}', parse_mode='HTML')
    await call.answer()

async def call_promo(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('<b>Введите промокод</b>:', parse_mode='HTML')
    await Promo.promo.set()


async def enter_promo(message: types.Message, state: FSMContext):
    await message.answer('Промокод не найден')
    await state.finish()
    

def register_cmd_profile(dp: Dispatcher):
    dp.register_message_handler(cmd_profile, Text(equals=emojize(':bust_in_silhouette: Профиль :bust_in_silhouette:')))
    dp.register_callback_query_handler(call_history, text='history')
    dp.register_callback_query_handler(call_promo, text='promo', state='*')
    dp.register_message_handler(enter_promo, state=Promo.promo)