from aiogram import executor, Dispatcher
from logger import logger
from telegram.loader import dp


async def on_startup(dispatcher: Dispatcher):
    from telegram.utils.set_commands import set_default_commands
    await set_default_commands(dispatcher)


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    logger.info("Start bot")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

