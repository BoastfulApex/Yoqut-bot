from aiogram import types
from backend.models import CartModel
from keyboards.inline.menu_button import select, item_keyboard, cart_callback, categories_keyboard, \
    about_callback, about_product_btn, pagination_about_call
from loader import dp, _
from utils.db_api.database import get_item, get_user, get_lang
from utils.misc.pages import get_page

@dp.callback_query_handler(text="no_call")
async def no_call_fun(call: types.CallbackQuery):
    await call.answer()


@dp.callback_query_handler(select.filter(key="num_choose"))
async def get_choosen_num(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    num = callback_data.get("data")
    selected = callback_data.get("choosen_data")
    item_id = int(callback_data.get("item_id"))
    item = await get_item(item_id)
    user = await get_user(call.from_user.id)
    if user.lang == "ru":
        category = item.category_name
    else:
        category = item.category_name
    user_id = call.from_user.id
    if int(selected) != 0:
        selected = f"{selected}" + num
        markup = await item_keyboard(category=category, item_id=item_id, selected=selected, lang=await get_lang(user_id))
        await call.message.edit_reply_markup(reply_markup=markup)
    else:
        selected = num
        markup = await item_keyboard(category=category, item_id=item_id, selected=selected, lang=await get_lang(user_id))
        await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(select.filter(key="delete_choosen"))
async def delete_choosen_num(call: types.CallbackQuery, callback_data):
    selected = callback_data.get("choosen_data")
    item_id = int(callback_data.get("item_id"))
    item = await get_item(item_id)
    user = await get_user(call.from_user.id)
    if user.lang == "ru":
        category = item.category_name_ru
    else:
        category = item.category_name
    user_id = call.from_user.id
    if int(selected) != 0:
        await call.answer()
        if len(selected) != 1:
            last_num = str(selected)[-1:]
            selected = str(selected).replace(last_num, "")
            if selected == "":
                selected = 0
            markup = await item_keyboard(category=item.category_name, item_id=item_id, selected=selected, lang=await get_lang(user_id))
            await call.message.edit_reply_markup(reply_markup=markup)
        else:
            markup = await item_keyboard(category=item.category_name, item_id=item_id, selected="0", lang=await get_lang(user_id))
            await call.message.edit_reply_markup(reply_markup=markup)
    else:
        selected = 0
        await call.answer(text=_("You have not selected anything yet"), show_alert=True)
        markup = await item_keyboard(category=category, item_id=item_id, selected=selected,lang=await get_lang(user_id))
        await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(cart_callback.filter())
async def go_cart_fun(call: types.CallbackQuery, callback_data: dict):
    item_id = callback_data.get("item_id")
    user_id = call.from_user.id
    choosen_data = callback_data.get("choosen_data")
    if int(choosen_data) != 0:
        item = await get_item(item_id)
        user = await get_user(user_id)
        cart = CartModel()
        cart.user = user
        cart.product = item
        cart.amount = choosen_data
        cart.total = int(choosen_data) * item.price
        cart.is_success = False
        cart.save()
        await call.answer(_("✅ Added to cart"), show_alert=True)
        await call.message.delete()
        markup = await categories_keyboard(lang=await get_lang(user_id))
        await call.message.answer(_("Product category"), reply_markup=markup)
    else:
        await call.answer(_("You have not selected anything yet"), show_alert=True)


@dp.callback_query_handler(about_callback.filter(key="about"))
async def about_product_fun(call: types.CallbackQuery, callback_data: dict):
    user = await get_user(call.from_user.id)
    item_id = callback_data.get("item_id")
    selected = callback_data.get("selected")
    item = await get_item(item_id)
    photo_list = []
    photo_2 = item.photo_2
    photo_3 = item.photo_3
    photo_4 = item.photo_4
    photo_5 = item.photo_5
    photo_6 = item.photo_6
    if photo_2:
        photo_list.append(photo_2)
    if photo_3:
        photo_list.append(photo_3)
    if photo_4:
        photo_list.append(photo_4)
    if photo_5:
        photo_list.append(photo_5)
    if photo_6:
        photo_list.append(photo_6)

    max_pages = len(photo_list)
    photo_id = get_page(photo_list)

    # max_pages: int, key, page: int = 1

    markup = await about_product_btn(item_id=item_id,
                                     selected=selected,
                                     lang=await get_lang(call.from_user.id),
                                     max_pages=max_pages,key=item_id)
    if user:
        await call.message.delete()
        if user.lang == "ru":
            await call.message.answer_photo(photo=photo_id, caption=item.description_2_ru, reply_markup=markup)
        else:
            await call.message.answer_photo(photo=photo_id, caption=item.description_2_en, reply_markup=markup)


@dp.callback_query_handler(pagination_about_call.filter())
async def pagination_about_fun(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    user = await get_user(call.from_user.id)
    item_id = int(callback_data.get("key"))
    current_page = int(callback_data.get("page"))
    selected = int(callback_data.get("selected"))
    item = await get_item(item_id)
    photo_list = []
    photo_2 = item.photo_2
    photo_3 = item.photo_3
    photo_4 = item.photo_4
    photo_5 = item.photo_5
    photo_6 = item.photo_6
    if photo_2:
        photo_list.append(photo_2)
    if photo_3:
        photo_list.append(photo_3)
    if photo_4:
        photo_list.append(photo_4)
    if photo_5:
        photo_list.append(photo_5)
    if photo_6:
        photo_list.append(photo_6)

    desc = ""
    if user.lang == "ru":
        desc = item.description_2_ru
    else:
        desc = item.description_2_en

    max_pages_photo = len(photo_list)
    photo_id = get_page(photo_list, current_page)
    media = types.InputMediaPhoto(photo_id, caption=desc)
    print(item_id)
    markup = await about_product_btn(item_id=item_id,selected=selected,lang=user.lang,max_pages=max_pages_photo, key=item_id,
                                     page=current_page)

    await call.message.edit_media(media=media, reply_markup=markup)



@dp.callback_query_handler(about_callback.filter(key="back_product"))
async def back_product_fun(call: types.CallbackQuery, callback_data: dict):
    selected = callback_data.get("selected")
    item_id = callback_data.get("item_id")
    item = await get_item(item_id)
    user = await get_user(call.from_user.id)
    if user.lang == "ru":
        description = item.description_ru
        item_name = item.name_ru
        category_name = item.category_name_ru
    else:
        description = item.description_en
        item_name = item.name
        category_name = item.category_name
    text = _("""
<b>{} >> {}</b>
Price: {} $

{}
""").format(
        category_name, item_name, item.price, description
    )
    markup = await item_keyboard(item.category_name, item_id, selected, lang=await get_lang(call.from_user.id))
    await call.message.delete()
    await call.message.answer_photo(photo=item.photo, caption=text, reply_markup=markup)




