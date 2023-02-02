import os
from emoji import emojize

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from utils.dbs.database import Database, item_1, item_2
from keyboards.admin_i_keyboard import load_n_del, items, accept_n_back_netflix, accept_n_back_vk_instagram, admin_list_items


db = Database(item_1)
db_2 = Database(item_2)


async def cmd_upload_items(message: types.Message):
    file_path = r'C:\Users\full_path_to_file' # Указываешь фулл путь до файла (этот файл чисто пример)
    caption = 'Отправь файл с товарами, которые будут загружены в БД, в формате .txt\n\n' \
              '(Тебе отправлен пример как должны выглядеть данные при отправке. ' \
              'Чтобы посмотреть какие товары находятся на продаже в данный момент, нажми на кнопку ниже)'
    await message.answer_document(open(file_path, 'rb'), caption=caption, reply_markup=admin_list_items)


async def call__list_items(call: types.CallbackQuery):
    name_netflix, price_netflix, amount_netflix = db.get_netflix_items()
    name_vk, price_vk, amount_vk, name_inst, price_inst, amount_inst = db_2.get_vk_instagram_items()
    caption_netflix = f'{emojize(":minus:")*3}<b>Netflix</b>{emojize(":minus:")*3}'
    caption_vk_tg_inst = f'{emojize(":minus:")*3}<b>VK/Instagram</b>{emojize(":minus:")*3}'
    caption_music = f'{emojize(":minus:")*3}<b>Spotify</b>{emojize(":minus:")*3}'
    await call.message.answer(
        f'{caption_netflix}\n'
        f'   {emojize(":popcorn:")}{name_netflix}{emojize(":popcorn:")}. | '
        f'{price_netflix} ₽ | '
        f'<b>Кол-во</b>: {amount_netflix} шт.\n\n'
        f'{caption_vk_tg_inst}\n'
        f'   {emojize(":customs:")}{name_vk}{emojize(":customs:")}. | '
        f'{price_vk} ₽ | '
        f'<b>Кол-во</b>: {amount_vk} шт.\n'
        f'   {emojize(":sunrise:")}{name_inst}{emojize(":sunrise:")}. | '
        f'{price_inst} ₽ | '
        f'<b>Кол-во</b>: {amount_inst} шт.', parse_mode='HTML'
    )
    await call.answer()


async def cmd_download(message: types.Message):
    path = r'C:\Users\full_path_to_file' # Указываешь фулл путь до файла, куда он будет загружен
    await message.document.download(destination_file=path)
    await message.answer('Файл был успешно загружен.\n\nЗагрузить его в базу данных или Удалить?', reply_markup=load_n_del)


async def call_load(call: types.CallbackQuery):
    await call.message.edit_text('Выбери в какую базу данных необходимо загрузить файл', reply_markup=items)


async def call_delete(call: types.CallbackQuery):
    try:
        path = r'C:\Users\full_path_to_file' # Указываешь фулл путь до файла, отрый будет удален
        os.remove(path)
        await call.message.edit_text(f'Файл был успешно удалён {emojize(":check_mark_button:")}')
    except:
        await call.message.edit_text(f'Папка с загруженными файлами пуста {emojize(":wastebasket:")}')


async def call__netflix(call: types.CallbackQuery):
    await call.message.edit_text(f'Вы хотите загрузить данные из файла в раздел {emojize(":television:")}<b>Кино-сервисы</b>{emojize(":television:")}?',
                                 reply_markup=accept_n_back_netflix, parse_mode='HTML')


async def call__vk_instagram(call: types.CallbackQuery):
    await call.message.edit_text(f'Вы хотите загрузить данные из файла в раздел {emojize(":heart_hands:")}<b>Социальные сети</b>{emojize(":heart_hands:")}?',
                                 reply_markup=accept_n_back_vk_instagram, parse_mode='HTML')


async def call__accept_netflix(call: types.CallbackQuery):
    path = r'C:\Users\full_path_to_file' # Указываешь фулл путь до файла, из которого будут загружать данные в БД
    with open(path, encoding='UTF-8') as f:
        for line in f:
            spl = line.split(',')
            print(spl)
            db.upload_netflix(
                (
                    f'{spl[0]}',
                    f'{spl[1]}',
                    f'{spl[2]}',
                    f'{spl[3]}'
                )
            )
    os.remove(path)
    await call.message.edit_text(f'Данные были успешно загружены в раздел {emojize(":television:")}<b>Кино-сервисы</b>{emojize(":television:")}',
                                 parse_mode='HTML')


async def call__accept_vk_instagram(call: types.CallbackQuery):
    path = r'C:\Users\full_path_to_file' # Указываешь фулл путь до файла, из которого будут загружать данные в БД
    with open(path, encoding='UTF-8') as f:
        for line in f:
            spl = line.split(',')
            print(spl)
            db_2.upload_vk_inst(
                (
                    f'{spl[0]}',
                    f'{spl[1]}',
                    f'{spl[2]}',
                    f'{spl[3]}'
                )
            )
    os.remove(path)
    await call.message.edit_text(f'Данные были успешно загружены в раздел {emojize(":heart_hands:")}<b>Социальные сети</b>{emojize(":heart_hands:")}',
                                 parse_mode='HTML')


def register_download(dp: Dispatcher):
    dp.register_message_handler(cmd_upload_items, Text(equals=emojize(':floppy_disk: Добавить товары :floppy_disk:')), is_admin=True)
    dp.register_callback_query_handler(call__list_items, text='_list_items')
    dp.register_message_handler(cmd_download, content_types=types.ContentType.DOCUMENT, is_admin=True)
    dp.register_callback_query_handler(call_load, lambda c: c.data == 'load' or c.data == '_back')
    dp.register_callback_query_handler(call_delete, lambda c: c.data == 'delete' or c.data == '_delete')
    dp.register_callback_query_handler(call__netflix, text='_netflix')
    dp.register_callback_query_handler(call__vk_instagram, text='_vk_instagram')
    dp.register_callback_query_handler(call__accept_netflix, text='_accept_netflix')
    dp.register_callback_query_handler(call__accept_vk_instagram, text='_accept_vk_instagram')
