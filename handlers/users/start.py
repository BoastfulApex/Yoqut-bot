from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.main_inline import menu_button, languages_markup, contact_btn, back_to_home, about_us_btn
from utils.db_api import database as commands
from loader import dp, _
import validators
from utils.db_api.database import get_faq, get_price_list, get_about_us, get_user
import phonenumbers
from filters.admin_filter import IsAdmin

@dp.message_handler(IsAdmin(), content_types=types.ContentType.DOCUMENT)
async def send_file_id(message: types.Message):
    await message.answer(f"FILE ID:\n\n<pre>{message.document.file_id}</pre>")


@dp.message_handler(IsAdmin(), content_types=types.ContentType.PHOTO)
async def send_image_id(message: types.Message):
    await message.answer(f"Image ID:\n\n<pre>{message.photo[-1].file_id}</pre>")


@dp.message_handler(IsAdmin(), content_types=types.ContentType.VIDEO)
async def send_vide_id(message: types.Message):

    await message.answer(f"Vide ID:\n\n<pre>{message.video.file_id}</pre>")


@dp.callback_query_handler(text="back_home")
async def back_home_fun(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    user_id = call.from_user.id
    menu = await menu_button(lang=await commands.get_lang(user_id))
    await call.message.answer(_("Welcome👋.\nClick the Products button to order!"), reply_markup=menu)


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user = await commands.get_user(user_id)
    if user:
        if user.is_active:
            menu = await menu_button(lang=await commands.get_lang(user_id))
            await message.answer(_("Welcome👋.\nClick the Products button to order!"), reply_markup=menu)
        else:
            markup = await languages_markup()
            await message.answer("Choose your language!\n\nВыберите удобный Вам язык!.",
                                 reply_markup=markup)
            await state.set_state("get_lang")
    else:
        markup = await languages_markup()
        await message.answer("Choose your language!\n\nВыберите удобный Вам язык!.",
                             reply_markup=markup)
        await state.set_state("get_lang")


@dp.callback_query_handler(text_contains="lang", state="get_lang")
async def change_lang(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.from_user.id
    await call.message.edit_reply_markup()
    lang = call.data[-2:]
    await state.update_data(lang=lang)
    await commands.add_user(user_id=user_id, name="", phone="", email="", lang=lang)
    await call.message.answer(
        _("<b>Enter you conatcs for registration.</b>\n\nEnter your name...", locale=lang))
    await state.set_state("name")


@dp.message_handler(state="name")
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    user_id = message.from_user.id
    markup = await contact_btn(lang=await commands.get_lang(user_id))
    await message.answer(_("You can enter Phone or Email to register."), reply_markup=markup)
    await state.set_state("phone_or_email")


@dp.callback_query_handler(text="phone", state="phone_or_email")
async def get_phone(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(_("Enter the number in international format\nFor example: +998901234567"))
    await state.set_state("phone")


@dp.callback_query_handler(text="email", state="phone_or_email")
async def get_email(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(_("Enter your email.\nExample: example@gmail.com"))
    await state.set_state("email")


@dp.message_handler(state="email")
async def get_email(message: types.Message, state: FSMContext):
    email_user = message.text
    check = validators.email(email_user)
    user_id = message.from_user.id
    data = await state.get_data()
    name = data.get("name")
    if check:
        await state.update_data(email=email_user)
        await commands.get_user(user_id)
        user = await commands.get_user(user_id)
        user.name = name
        user.email = email_user
        user.is_active = True
        user.save()
        await state.finish()
        menu = await menu_button(lang=await commands.get_lang(user_id))
        await message.answer(_("Welcome👋.\nClick the Products button to order!"), reply_markup=menu)
    else:
        await message.answer(_("Enter your email.\nExample: example@gmail.com"))
        await state.set_state("email")


@dp.message_handler(state="phone")
async def get_confirm_secret_phone(message: types.Message, state: FSMContext):
    phone = message.text
    try:
        my_number = phonenumbers.parse(f"{phone}", "GB")
        if phonenumbers.is_valid_number(my_number):
            user_id = message.from_user.id
            data = await state.get_data()
            name = data.get("name")
            user = await commands.get_user(user_id)
            user.name = name
            user.phone = phone
            user.is_active = True
            user.save()
            await state.finish()
            menu = await menu_button(lang=await commands.get_lang(user_id))
            await message.answer(_("Welcome👋.\nClick the Products button to order!"), reply_markup=menu)
        else:
            await message.answer(_("Enter the number in international format\nFor example: +998901234567"))
            await state.set_state("phone")
    except:
        await message.answer(_("Enter the number in international format\nFor example: +998901234567"))
        await state.set_state("phone")


@dp.callback_query_handler(text="faq")
async def faq_fun(call: types.CallbackQuery):
    faq = await get_faq()
    if faq is not None:
        await call.answer()
        user_id = call.from_user.id
        markup = await back_to_home(lang=await commands.get_lang(user_id))
        await call.message.edit_text(faq, reply_markup=markup)
    else:
        await call.answer(_("Nothing else"), show_alert=True)


@dp.callback_query_handler(text="download_price")
async def download_price_fun(call: types.CallbackQuery):
    price_list = await get_price_list()
    if price_list is not None:
        await call.answer()
        await call.message.delete()
        user_id = call.from_user.id
        markup = await back_to_home(lang=await commands.get_lang(user_id))
        await call.message.answer_document(document=price_list.pirce_list, caption=_("<b>Price list</b>\n"),
                                           reply_markup=markup)
    else:
        await call.answer(_("Nothing else"), show_alert=True)


@dp.callback_query_handler(text="about_us")
async def about_us_fun(call: types.CallbackQuery):

    about_us = await get_about_us()
    if about_us:
        await call.answer()
        photo = about_us.logo
        user = await get_user(call.from_user.id)
        await call.message.delete()
        markup = await about_us_btn(lang=await commands.get_lang(call.from_user.id))
        if user:
            if user.lang == "ru":
                await call.message.answer_photo(photo=photo, caption=about_us.description_ru, reply_markup=markup)
            else:
                await call.message.answer_photo(photo=photo, caption=about_us.description_en, reply_markup=markup)
    else:
        await call.answer(_("Nothing else"), show_alert=True)

@dp.callback_query_handler(text="back_about_us")
async def back_to_about_us(call: types.CallbackQuery):
    await call.answer()
    about_us = await get_about_us()
    photo = about_us.logo
    user = await get_user(call.from_user.id)
    await call.message.delete()
    markup = await about_us_btn(lang=await commands.get_lang(call.from_user.id))
    if user:
        if user.lang == "ru":
            await call.message.answer_photo(photo=photo, caption=about_us.description_ru, reply_markup=markup)
        else:
            await call.message.answer_photo(photo=photo, caption=about_us.description_en, reply_markup=markup)


@dp.callback_query_handler(text="change_language")
async def change_language_fun(call: types.CallbackQuery):
    await call.answer()
    markup = await languages_markup()
    await call.message.edit_text("Choose your language!\n\nВыберите удобный Вам язык!.",
                                 reply_markup=markup)


@dp.callback_query_handler(text_contains="lang")
async def change_lang_fun(call: types.CallbackQuery):
    await call.answer()
    lang = call.data[-2:]
    user = await get_user(call.from_user.id)
    user.lang = lang
    user.save()
    await call.message.delete()
    menu = await menu_button(lang=await commands.get_lang(call.from_user.id))
    await call.message.answer(_("Welcome👋.\nClick the Products button to order!", locale=lang), reply_markup=menu)
