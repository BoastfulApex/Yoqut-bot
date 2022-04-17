# from backend.models import Order
from loader import dp, bot, _
from aiogram import types
from aiogram.dispatcher import FSMContext
# from utils.db_api.database import get_user, get_purchase, get_purchase_by_id, delete_purchase, update_purchase, get_lang
import validators
import phonenumbers
from utils.date_time_format import df
