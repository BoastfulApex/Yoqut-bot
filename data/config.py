import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
GROUPS_ID = str(os.getenv("GROUPS_ID")).split(" ")
DATABASE = str(os.getenv("DATABASE"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))

SLEEP_TIME = .3


ip = str(os.getenv("ip"))

# webhook settings
WEBHOOK_HOST = ip
WEBHOOK_PATH = f'/bot/{BOT_TOKEN}'
PORT = 5432
WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{PORT}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"  # or ip
WEBAPP_PORT = 5432



I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'

WEBHOOK_SSL_CERT = BASE_DIR / "webhook_cert.pem"
WEBHOOK_SSL_PRIV = BASE_DIR / "webhook_pkey.pem"

