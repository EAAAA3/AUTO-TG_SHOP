from emoji import emojize
import random
from datetime import datetime, timedelta
from glQiwiApi import QiwiWrapper
from glQiwiApi.qiwi.clients.p2p.types import Bill

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import SECRET_P2P
from utils.dbs.database import Database, item_1, item_2
from keyboards.i_keyboard import activ_menu, list_for_buy_vk_inst, list_for_buy_netflix, buy_vk, buy_inst, buy_netflix, buy_buttons, return_to_menu


db = Database(item_1)
db2 = Database(item_2)

now = datetime.now()
future_15 = now + timedelta(minutes=15)

wallet = QiwiWrapper(secret_p2p=SECRET_P2P)


class CheckQiwi(StatesGroup):
    check_paid = State()


def random_int():
    number = random.randrange(100000, 1000000)
    return number


async def cmd_buy_items(message: types.Message):
    await message.answer('<b>Активные категории в магазине</b>:', reply_markup=activ_menu, parse_mode='HTML')


async def call_back_to_all(call: types.CallbackQuery):
    await call.message.edit_text('<b>Активные категории в магазине</b>:', reply_markup=activ_menu, parse_mode='HTML')


async def call_netflix(call: types.CallbackQuery):
    await call.message.edit_text(f'{emojize(":page_with_curl:")} <b>Категория</b>: {emojize(":television:")} Кино-сервисы {emojize(":television:")}\n'
                                 f'{emojize(":page_with_curl:")} <b>Описание</b>: После ворка, нужно расслабиться, '
                                 f'для тебя мой друг, есть отличные сервисы для просмотра фильмов {emojize(":red_heart:")}',
                                 reply_markup=list_for_buy_netflix, parse_mode='HTML')


async def call_vk_instagram(call: types.CallbackQuery):
    await call.message.edit_text(f'{emojize(":page_with_curl:")} <b>Категория</b>: {emojize(":heart_hands:")} Социальные сети {emojize(":heart_hands:")}\n'
                                 f'{emojize(":page_with_curl:")} <b>Описание</b>: VK/Instagram аккаунты', reply_markup=list_for_buy_vk_inst, parse_mode='HTML')


async def call_accept_netflix(call: types.CallbackQuery):
    description = db.get_netflix_items()
    text = '{2} <b>Товар</b>: {0}\n' \
           '{3} <b>Цена</b>: <b>{1}</b> ₽\n' \
           '{4} <b>Описание</b>: Аккаунт {0}, гарантия 3 дня с момента покупки.\n' \
           'Данные предоставляются в формате Логин/Пароль\n\n' \
           'Выберите количество товара, которое хотите купить:'
    await call.message.edit_text(text.format(description[0], description[1], emojize(":page_with_curl:"), emojize(":money_bag:"),
                                                 emojize(":page_with_curl:")), reply_markup=buy_vk, parse_mode='HTML')


async def call_accept_vk_intagram(call: types.CallbackQuery):
    description = db2.get_vk_instagram_items()
    text = '{2} <b>Товар</b>: {0}\n' \
           '{3} <b>Цена</b>: <b>{1}</b> ₽\n' \
           '{4} <b>Описание</b>: Аккаунт {0}, гарантия 3 дня с момента покупки.\n' \
           'Данные предоставляются в формате Логин/Пароль\n\n' \
           'Выберите количество товара, которое хотите купить:'
    if call.data == 'accept_vk':
        await call.message.edit_text(text.format(description[0],description[1], emojize(":page_with_curl:"), emojize(":money_bag:"),
                                                 emojize(":page_with_curl:")), reply_markup=buy_vk, parse_mode='HTML')
    if call.data == 'accept_instagram':
        await call.message.edit_text(text.format(description[3], description[4], emojize(":page_with_curl:"), emojize(":money_bag:"),
                                                 emojize(":page_with_curl:")), reply_markup=buy_inst, parse_mode='HTML')


async def call_choice_netflix(call: types.CallbackQuery):
    description = db.get_netflix_items()
    number = random_int()
    text = '{8}\n' \
           '{9} <b>Товар</b>: {0}\n' \
           '{10} <b>Цена</b>: {1} ₽\n' \
           '{11} <b>Кол-во</b>: {5} шт.\n' \
           '{12} <b>Заказ</b>: {7}\n' \
           '{13} <b>Время заказа</b>: {3}\n' \
           '{14} <b>Итоговая сумма</b>: {2} ₽\n' \
           '{15} <b>Способ оплаты</b>: QIWI\n' \
           '{8}\n' \
           '{14} <b>Сумма</b>: {2} ₽\n' \
           '{16} <b>Комментарий</b>: {7}\n' \
           '{17} <b>Время на оплату</b>: 15 минут\n' \
           '{18} <b>Необходимо оплатить до {4}</b>\n' \
           '{8}\n' \
           '{19} {6} {19}\n' \
           '{8}'
    if call.data == '1_netflix':    # При необходимости можно дописать и больше
        bill = await wallet.create_p2p_bill(amount=description[1], comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1],
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 1,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '2_netflix':
        bill = await wallet.create_p2p_bill(amount=description[1]*2, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1]*2,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 2,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '3_netflix':
        bill = await wallet.create_p2p_bill(amount=description[1]*3, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1]*3,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 3,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '4_netflix':
        bill = await wallet.create_p2p_bill(amount=description[1]*4, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1]*4,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 4,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '5_netflix':
        bill = await wallet.create_p2p_bill(amount=description[1]*5, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1]*5,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 5,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)


async def call_choice_vk_instagram(call: types.CallbackQuery, state: FSMContext): # c.data == True
    description = db2.get_vk_instagram_items()
    print(description)
    number = random_int()
    text = '{8}\n' \
           '{9} <b>Товар</b>: {0}\n' \
           '{10} <b>Цена</b>: {1} ₽\n' \
           '{11} <b>Кол-во</b>: {5} шт.\n' \
           '{12} <b>Заказ</b>: {7}\n' \
           '{13} <b>Время заказа</b>: {3}\n' \
           '{14} <b>Итоговая сумма</b>: {2} ₽\n' \
           '{15} <b>Способ оплаты</b>: QIWI\n' \
           '{8}\n' \
           '{14} <b>Сумма</b>: {2} ₽\n' \
           '{16} <b>Комментарий</b>: {7}\n' \
           '{17} <b>Время на оплату</b>: 15 минут\n' \
           '{18} <b>Необходимо оплатить до {4}</b>\n' \
           '{8}\n' \
           '{19} {6} {19}\n' \
           '{8}'
    # Вот тут надо использовать статистику (заказ)
    print(call.data)
    if call.data == '1_vk':
        bill = await wallet.create_p2p_bill(amount=description[1], comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1],
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 1,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '1_inst':
        bill = await wallet.create_p2p_bill(amount=description[4], comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[3], description[4], description[4],
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 1,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '2_vk':
        bill = await wallet.create_p2p_bill(amount=description[1]*2, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1]*2,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 2,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '2_inst':
        bill = await wallet.create_p2p_bill(amount=description[4]*2, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[3], description[4], description[4]*2,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 2,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '3_vk':
        bill = await wallet.create_p2p_bill(amount=description[1]*3, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1]*3,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 3,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '3_inst':
        bill = await wallet.create_p2p_bill(amount=description[4]*3, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[3], description[4], description[4]*3,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 3,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '4_vk':
        bill = await wallet.create_p2p_bill(amount=description[1]*4, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1]*4,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 4,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '4_inst':
        bill = await wallet.create_p2p_bill(amount=description[4]*4, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[3], description[4], description[4]*4,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 4,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '5_vk':
        bill = await wallet.create_p2p_bill(amount=description[1]*5, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[0], description[1], description[1]*5,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 5,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)
    if call.data == '5_inst':
        bill = await wallet.create_p2p_bill(amount=description[4]*5, comment=number, life_time=future_15)
        await call.message.edit_text(text.format(description[3], description[4], description[4]*5,
                                                 now.strftime('%Y-%m-%d %H:%M'), future_15.strftime('%H:%M'), 5,
                                                 f'<a href="{bill.pay_url}">Перейти к оплате</a>', number, emojize(":minus:") * 12,
                                                 emojize(":page_with_curl:"), emojize(":money_bag:"), emojize(":package:"), emojize(":light_bulb:"),
                                                 emojize(":one_o’clock:"), emojize(":money_with_wings:"), emojize(":heavy_dollar_sign:"),
                                                 emojize(":pager:"), emojize(":alarm_clock:"), emojize(":hourglass_not_done:"),
                                                 emojize(":green_circle:")),
                                     reply_markup=buy_buttons, parse_mode='HTML')
        await CheckQiwi.check_paid.set()
        await state.update_data(bill=bill, bill_id=bill.id, item_name=call.data)


async def call_paid(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        bill: qiwi_types.Bill = data.get('bill')
        if await wallet.check_if_bill_was_paid(bill) and data.get('item_name').endswith('_vk'): # VK
            if data.get('item_name').startswith('1'):
                login_passwd = db2.get_vk_login_pass()[0]
                await call.message.edit_text(f'Держи данные от аккаунта\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин: `{login_passwd[0]}`\n'
                                             f'{emojize(":locked_with_key:")} Пароль: `{login_passwd[1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
            if data.get('item_name').startswith('2'):
                login_passwd = db2.get_vk_login_pass()[1]
                await call.message.edit_text(f'Держи данные от аккаунтов\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин:\n\n'
                                             f'    1\. `{login_passwd[0][0]}`\n\n'
                                             f'    2\. `{login_passwd[1][0]}`\n\n'
                                             f'{emojize(":locked_with_key:")} Пароль:\n\n'
                                             f'    1\. `{login_passwd[0][1]}`\n'
                                             f'    2\. `{login_passwd[1][1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
            if data.get('item_name').startswith('3'):
                login_passwd = db2.get_vk_login_pass()[2]
                await call.message.edit_text(f'Держи данные от аккаунтов\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин:\n\n'
                                             f'    1\. `{login_passwd[0][0]}`\n\n'
                                             f'    2\. `{login_passwd[1][0]}`\n\n'
                                             f'    3\. `{login_passwd[2][0]}`\n\n'
                                             f'{emojize(":locked_with_key:")} Пароль:\n\n'
                                             f'    1\. `{login_passwd[0][1]}`\n'
                                             f'    2\. `{login_passwd[1][1]}`\n'
                                             f'    3\. `{login_passwd[2][1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
            if data.get('item_name').startswith('4'):
                login_passwd = db2.get_vk_login_pass()[3]
                await call.message.edit_text(f'Держи данные от аккаунтов\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин:\n\n'
                                             f'    1\. `{login_passwd[0][0]}`\n\n'
                                             f'    2\. `{login_passwd[1][0]}`\n\n'
                                             f'    3\. `{login_passwd[2][0]}`\n\n'
                                             f'    4\. `{login_passwd[3][0]}`\n\n'
                                             f'{emojize(":locked_with_key:")} Пароль:\n\n'
                                             f'    1\. `{login_passwd[0][1]}`\n'
                                             f'    2\. `{login_passwd[1][1]}`\n'
                                             f'    3\. `{login_passwd[2][1]}`\n'
                                             f'    4\. `{login_passwd[3][1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
            if data.get('item_name').startswith('5'):
                login_passwd = db2.get_vk_login_pass()[4]
                await call.message.edit_text(f'Держи данные от аккаунтов\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин:\n\n'
                                             f'    1\. `{login_passwd[0][0]}`\n\n'
                                             f'    2\. `{login_passwd[1][0]}`\n\n'
                                             f'    3\. `{login_passwd[2][0]}`\n\n'
                                             f'    4\. `{login_passwd[3][0]}`\n\n'
                                             f'    5\. `{login_passwd[4][0]}`\n\n'
                                             f'{emojize(":locked_with_key:")} Пароль:\n\n'
                                             f'    1\. `{login_passwd[0][1]}`\n'
                                             f'    2\. `{login_passwd[1][1]}`\n'
                                             f'    3\. `{login_passwd[2][1]}`\n'
                                             f'    4\. `{login_passwd[3][1]}`\n'
                                             f'    5\. `{login_passwd[4][1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
        if await wallet.check_if_bill_was_paid(bill) and data.get('item_name').endswith('_inst'): # INSTAGRAM
            if data.get('item_name').startswith('1'):
                login_passwd = db2.get_inst_login_pass()[0]
                await call.message.edit_text(f'Держи данные от аккаунта\.\n\n'
                                             f'Логин: `{login_passwd[0]}`\n'
                                             f'{emojize(":locked_with_key:")} Пароль: `{login_passwd[1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
            if data.get('item_name').startswith('2'):
                login_passwd = db2.get_inst_login_pass()[1]
                await call.message.edit_text(f'Держи данные от аккаунтов\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин:\n\n'
                                             f'    1\. `{login_passwd[0][0]}`\n\n'
                                             f'    2\. `{login_passwd[1][0]}`\n\n'
                                             f'{emojize(":locked_with_key:")} Пароль:\n\n'
                                             f'    1\. `{login_passwd[0][1]}`\n'
                                             f'    2\. `{login_passwd[1][1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
            if data.get('item_name').startswith('3'):
                login_passwd = db2.get_inst_login_pass()[2]
                await call.message.edit_text(f'Держи данные от аккаунтов\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин:\n\n'
                                             f'    1\. `{login_passwd[0][0]}`\n\n'
                                             f'    2\. `{login_passwd[1][0]}`\n\n'
                                             f'    3\. `{login_passwd[2][0]}`\n\n'
                                             f'{emojize(":locked_with_key:")} Пароль:\n\n'
                                             f'    1\. `{login_passwd[0][1]}`\n'
                                             f'    2\. `{login_passwd[1][1]}`\n'
                                             f'    3\. `{login_passwd[2][1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
            if data.get('item_name').startswith('4'):
                login_passwd = db2.get_inst_login_pass()[3]
                await call.message.edit_text(f'Держи данные от аккаунтов\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин:\n\n'
                                             f'    1\. `{login_passwd[0][0]}`\n\n'
                                             f'    2\. `{login_passwd[1][0]}`\n\n'
                                             f'    3\. `{login_passwd[2][0]}`\n\n'
                                             f'    4\. `{login_passwd[3][0]}`\n\n'
                                             f'{emojize(":locked_with_key:")} Пароль:\n\n'
                                             f'    1\. `{login_passwd[0][1]}`\n'
                                             f'    2\. `{login_passwd[1][1]}`\n'
                                             f'    3\. `{login_passwd[2][1]}`\n'
                                             f'    4\. `{login_passwd[3][1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
            if data.get('item_name').startswith('5'):
                login_passwd = db2.get_inst_login_pass()[4]
                await call.message.edit_text(f'Держи данные от аккаунтов\.\n\n'
                                             f'{emojize(":billed_cap:")} Логин:\n\n'
                                             f'    1\. `{login_passwd[0][0]}`\n\n'
                                             f'    2\. `{login_passwd[1][0]}`\n\n'
                                             f'    3\. `{login_passwd[2][0]}`\n\n'
                                             f'    4\. `{login_passwd[3][0]}`\n\n'
                                             f'    5\. `{login_passwd[4][0]}`\n\n'
                                             f'{emojize(":locked_with_key:")} Пароль:\n\n'
                                             f'    1\. `{login_passwd[0][1]}`\n'
                                             f'    2\. `{login_passwd[1][1]}`\n'
                                             f'    3\. `{login_passwd[2][1]}`\n'
                                             f'    4\. `{login_passwd[3][1]}`\n'
                                             f'    5\. `{login_passwd[4][1]}`\n'
                                             f'Спасибо за покупку, приходите к нам ещё {emojize(":red_heart:")}', parse_mode='MarkdownV2')
                await state.finish()
        else:
            try:
                await call.message.edit_text(f'{emojize(":no_entry:")} Счет не был оплачен {emojize(":no_entry:")}', reply_markup=buy_buttons)
            except:
                pass
            

async def call_cancel(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await wallet.reject_bill_by_id(bill_id=data.get('bill_id'))
        await state.finish()
        await call.message.edit_text(f'{emojize(":prohibited:")} Данная заявка на оплату была отменена {emojize(":prohibited:")}', reply_markup=return_to_menu)


def register_cmd_buy_items(dp: Dispatcher):
    dp.register_message_handler(cmd_buy_items, Text(equals=emojize(':open_book: Все категории :open_book:')))
    dp.register_callback_query_handler(call_back_to_all, text='back_to_all')
    dp.register_callback_query_handler(call_netflix, lambda c: c.data == 'netflix' or c.data == 'back')
    dp.register_callback_query_handler(call_vk_instagram, lambda c: c.data == 'vk/instagram' or c.data == 'back_1')
    dp.register_callback_query_handler(call_accept_netflix, text='accept_netflix')
    dp.register_callback_query_handler(call_accept_vk_intagram, lambda c: c.data == 'accept_vk' or c.data == 'accept_instagram')
    dp.register_callback_query_handler(call_choice_netflix, lambda c: c.data.endswith('_netflix'), state='*')
    dp.register_callback_query_handler(call_choice_vk_instagram,
                                       lambda c: c.data.endswith('_inst') or c.data.endswith('_vk'), state='*')
    dp.register_callback_query_handler(call_paid, text='paid', state=CheckQiwi.check_paid)
    dp.register_callback_query_handler(call_cancel, text='cancel', state=CheckQiwi.check_paid)
