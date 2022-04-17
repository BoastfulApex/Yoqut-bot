import os
import django
from aiogram import Bot, Dispatcher
import logging


async def on_startup(dp):
    from data.config import WEBHOOK_URL
    from loader import SSL_CERTIFICATE, bot
    import logging
    # webhook_info = await bot.get_webhook_info()
    # if webhook_info.url != WEBHOOK_URL:
    #     await bot.set_webhook(
    #         url=WEBHOOK_URL,
    #         certificate=SSL_CERTIFICATE
    #     )

    from utils.set_bot_commands import set_default_commands
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    await set_default_commands(dp)


API_TOKEN = '5159417073:AAFCHDzt8me0XQQffVmwZ1R2DtFMq530Xf4'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "admin.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


#
#
# if __name__ == '__main__':
#     setup_django()
#     from handlers import dp
#     from aiogram.utils.executor import start_webhook
#     from data.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
#     from loader import ssl_context
#     start_webhook(
#         dispatcher=dp,
#         webhook_path=WEBHOOK_PATH,
#         on_startup=on_startup,
#         on_shutdown=on_shutdown,
#         skip_updates=True,
#         host=WEBAPP_HOST,
#         port=WEBAPP_PORT,
#         ssl_context=ssl_context
#     )


if __name__ == '__main__':
    setup_django()

    from aiogram.utils import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
