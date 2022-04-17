from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.db_api import database as commands
from loader import dp, _, bot
import validators
# from utils.db_api.database import get_faq, get_price_list, get_about_us, get_user
import phonenumbers
from keyboards.inline.main_inline import menu_keyboard

password = "1234"


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Assalomu alaykum Yoqut Sklad botiga xush kelibsiz shaxsingizni tasdiqlash uchun iltimos parolni kiriting")
    await state.set_state("check_password")


@dp.message_handler(content_types=types.ContentType.TEXT, state="check_password")
async def check_password(message: types.Message, state: FSMContext):
    pas = message.text
    if pas == password:
        await message.delete()
        markup = await menu_keyboard()
        await bot.send_message(chat_id=message.from_user.id, text="Parol tog'ri\nBosh menyuga xush kelibsiz")
    else:
        await message.answer("Xatokuuu bu")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Shaxsingizni tasdiqlash uchun iltimos parolni qayta kiriting kiriting")
        await state.set_state("check_password")
