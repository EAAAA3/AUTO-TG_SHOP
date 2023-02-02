import config
import asyncio

from aiogram import Bot, Dispatcher
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from filters.admin_filter import AdminFilter

from handlers.users.start import register_cmd_start
from handlers.users.profile import register_cmd_profile
from handlers.users.rules import register_cmd_rules
from handlers.users.support_info import register_cmd_support_info
from handlers.users.list_items import register_list_items
from handlers.users.buy_items import register_cmd_buy_items
from handlers.admin.download import register_download
from handlers.admin.statistic import register_cmd_statistic
from handlers.admin.spaming import register_cmd_spaming



logger = logging.getLogger(__name__)


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    # Users commands
    register_cmd_start(dp)
    register_cmd_profile(dp)
    register_cmd_rules(dp)
    register_cmd_profile(dp)
    register_cmd_support_info(dp)
    register_list_items(dp)
    register_cmd_buy_items(dp)
    #Admins commands
    register_download(dp)
    register_cmd_statistic(dp)
    register_cmd_spaming(dp)
    #Test commands


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")


    #storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())


    register_all_filters(dp)
    register_all_handlers(dp)


    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")