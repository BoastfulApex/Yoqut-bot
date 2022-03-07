from typing import Union
from aiogram import types
from aiogram.types import CallbackQuery, Message
from keyboards.inline.menu_button import menu_cd, categories_keyboard, items_keyboard, item_keyboard
from loader import dp, _
from utils.db_api.database import get_item, get_category_by_name, get_user, get_lang


@dp.callback_query_handler(text="order_menu")
async def show_menu(call: types.CallbackQuery):
    await call.answer()
    await list_categories(call.message)


async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    if isinstance(message, Message):
        user_id = message.chat.id
        markup = await categories_keyboard(lang=await get_lang(user_id))
        await message.edit_text(_("Select one of the categories👇"), reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        markup = await categories_keyboard(lang=await get_lang(call.from_user.id))
        await call.message.edit_reply_markup(markup)


async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    await callback.answer()
    await callback.message.delete()
    markup = await items_keyboard(category, lang=await get_lang(callback.from_user.id))
    c = await get_category_by_name(category)
    if c.category_photo:
        photo = c.category_photo
        text = _("Select one of the products👇")
        await callback.message.answer_photo(photo=photo, caption=text, reply_markup=markup)


async def list_items(callback: CallbackQuery, category, item_id, **kwargs):
    await callback.answer()
    await callback.message.delete()
    markup = await item_keyboard(category, item_id=item_id, selected=0, lang=await get_lang(callback.from_user.id))
    item = await get_item(item_id)
    photo = item.photo
    user = await get_user(callback.from_user.id)
    if user.lang == "ru":
        description = item.description_ru
        item_name = item.name_ru
        category_name = item.category_name_ru
    else:
        description = item.description_en
        item_name = item.name
        category_name = item.category_name
    if photo:
        text = _("""
<b>{} >> {}</b>
Price: {} $

{}
""").format(category_name, item_name, item.price, description)
        await callback.message.answer_photo(photo=photo, caption=text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    current_level = callback_data.get("level")
    category = callback_data.get("category")
    item_id = int(callback_data.get("item_id"))
    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
    }
    current_level_function = levels[current_level]
    await current_level_function(
        call,
        category=category,
        item_id=item_id
    )


@dp.callback_query_handler(text="back_category")
async def back_category_fun(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    markup = await categories_keyboard(lang=await get_lang(call.from_user.id))
    await call.message.answer(_("Select one of the categories👇"), reply_markup=markup)
