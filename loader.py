from aiogram import Bot, Dispatcher, types
import ssl
from data import config
from data.config import WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares.language_middleware import setup_middleware


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
i18n = setup_middleware(dp)
_ = i18n.gettext

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
SSL_CERTIFICATE = open(WEBHOOK_SSL_CERT, "rb").read()
ssl_context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
