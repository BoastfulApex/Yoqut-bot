from backend.models import Order
from handlers.users.menu_handler import list_categories
from keyboards.inline.main_inline import main_cart_button, plus_minus_data, confirm_end, back_button
from keyboards.inline.menu_button import categories_keyboard
from loader import dp, bot, _
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.db_api.database import get_user, get_purchase, get_purchase_by_id, delete_purchase, update_purchase, get_lang
import validators
import phonenumbers
from utils.date_time_format import df

@dp.callback_query_handler(text="cart")
async def cart_fun(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = await get_user(user_id)

    purchases = await get_purchase(user)
    total = 0
    final_total = 0
    text = ""
    if purchases:
        await call.answer()
        i = 1
        for purchase in purchases:
            item = purchase.product
            if user.lang == "ru":
                item_name = item.name_ru
                category_name = item.category_name_ru
            else:
                item_name = item.name
                category_name = item.category_name
            amount = purchase.amount
            price = purchase.product.price
            total = int(amount) * price
            text += f'<b>{i}) {category_name}\n   └{item_name}</b> {amount} x {price} = {total} $\n\n'
            i += 1
            final_total += total
        markup = await main_cart_button(purchases, lang=await get_lang(user_id))
        text += "Total: " + str(final_total) + " $"
        await call.message.edit_text(text=text, reply_markup=markup)
    else:
        await call.answer(_("You haven't products in your cart 🤷‍♂️"), show_alert=True)


@dp.callback_query_handler(plus_minus_data.filter())
async def plus_minus_fun(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    purchase_id = callback_data.get("purchase_id")
    key = callback_data.get("key")
    purchase = await get_purchase_by_id(purchase_id)
    user_id = call.from_user.id
    user = await get_user(user_id)
    purchases = await get_purchase(user)
    total = 0
    final_total = 0
    text = ""
    if key == "minus" and purchase.amount == 1:
        await delete_purchase(int(purchase_id))

    if key == "minus" and purchase.amount > 1:
        purchase.amount -= 1
        purchase.save()

    if key == "plus":
        purchase.amount += 1
        purchase.save()
    i = 1
    for purchase in purchases:
        item = purchase.product
        if user.lang == "ru":
            item_name = item.name_ru
            category_name = item.category_name_ru
        else:
            item_name = item.name
            category_name = item.category_name
        amount = purchase.amount
        price = purchase.product.price
        total = int(amount) * price
        text += f'<b>{i}) {category_name}\n   └{item_name}</b> {amount} x {price} = {total} $\n\n'
        final_total += total
    markup = await main_cart_button(purchases,lang=await get_lang(user_id))
    await call.message.edit_text(text=text + _("Total: ") + str(final_total) + " $", reply_markup=markup)


@dp.callback_query_handler(text="back_to_menu_page")
async def back_to_menu_page(call: types.CallbackQuery):
    await call.answer()
    await list_categories(call.message)


@dp.callback_query_handler(text="confirm")
async def confirm_fun(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter your name..."), reply_markup=back_button)
    await state.set_state("name_cart")


@dp.message_handler(state="name_cart")
async def name_cart_fun(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(_("Enter the number in international format\nFor example: +998901234567"),reply_markup=back_button)
    await state.set_state("phone_cart")


@dp.message_handler(state="phone_cart")
async def phone_cart_fun(message: types.Message, state: FSMContext):
    phone = message.text
    try:
        my_number = phonenumbers.parse(f"{phone}", "GB")
        if phonenumbers.is_valid_number(my_number):
            await state.update_data(phone=phone)
            await message.answer(_("Enter your email..."), reply_markup=back_button)
            await state.set_state("email_cart")
        else:
            await message.answer(_("Enter the number in international format\nFor example: +998901234567"),reply_markup=back_button)
            await state.set_state("phone_cart")
    except:
        await message.answer(_("Enter the number in international format\nFor example: +998901234567"),reply_markup=back_button)
        await state.set_state("phone_cart")


@dp.message_handler(state="email_cart")
async def emain_cart_fun(message: types.Message, state: FSMContext):
    email = message.text
    check = validators.email(email)
    if check:
        await state.update_data(email=email)
        await message.answer(_("Enter your company name..."),reply_markup=back_button)
        await state.set_state("company_name")
    else:
        await message.answer(_("Enter your email..."),reply_markup=back_button)
        await state.set_state("email_cart")


@dp.message_handler(state="company_name")
async def company_name_fun(message: types.Message, state: FSMContext):
    company_name = message.text
    await state.update_data(company_name=company_name)
    await message.answer(_("Address company...\n\nExample: 360 Monmouth Rd, Elizabeth, NJ 07208, United States"),reply_markup=back_button)
    await state.set_state("address")


@dp.message_handler(state="address")
async def address_name_fun(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = await get_user(message.from_user.id)
    address_company = message.text
    name = data.get("name")
    phone = data.get("phone")
    if phone is None:
        phone = user.phone
    email = data.get("email")
    if email is None:
        email = user.email
    company_name = data.get("company_name")
    purchases = await get_purchase(user)
    text = _(
        "<b>Name:</b> {}\n<b>Phone:</b> {}\n<b>Email: </b>{}\n<b>Company name: </b>{}\n<b>Address company:</b> {}\n\n").format(
        name, phone, email, company_name, address_company)
    final_total = 0
    total = 0
    i = 1
    for purchase in purchases:
        item = purchase.product
        if user.lang == "ru":
            item_name = item.name_ru
            category_name = item.category_name_ru
        else:
            item_name = item.name
            category_name = item.category_name
        amount = purchase.amount
        price = purchase.product.price
        total = int(amount) * price
        text += '<b>{}) {}\n   └{}</b> {} x {} = {} $\n\n'.format(
            i, category_name, item_name, amount, price, total
        )
        i += 1
        final_total += total
    text += _("Total: ") + str(final_total) + " $"
    await state.update_data(text=text, address_company=address_company, name=name, phone=phone, email=email,
                            company_name=company_name, final_total=final_total)
    markup = await confirm_end(lang=await get_lang(message.from_user.id))
    await message.answer(text, reply_markup=markup)
    await state.set_state("confirm_state")


@dp.callback_query_handler(text="confirm_end", state="confirm_state")
async def confirm_end_fun(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    company_name = data.get("company_name")
    address_company = data.get("address_company")
    final_total = data.get("final_total")
    user = await get_user(call.from_user.id)
    purchases = await get_purchase(user)
    purchase_text = ""
    i = 1
    for purchase in purchases:
        item = purchase.product
        if user.lang == "ru":
            item_name = item.name_ru
            category_name = item.category_name_ru
        else:
            item_name = item.name
            category_name = item.category_name
        amount = purchase.amount
        price = purchase.product.price
        total = int(amount) * price
        purchase_text += f'{i}) {category_name}\n   └{item_name} {amount} x {price} = {total} $\n'
        i += 1
    try:
        order = Order()
        order.user = user
        order.name = name
        order.email = email
        order.phone = phone
        order.purchases = purchase_text
        order.company_name = company_name
        order.address = address_company
        order.total = final_total
        order.is_success = False
        order.save()
        await update_purchase(user)
        date_time = await df()
        await bot.send_message(chat_id="-1001621437022", text=f"# {date_time}\n" + _("<b>Order ID: {}\n</b>").format(order.id)+text)
        await bot.send_message(chat_id="-1001724658753", text=f"# {date_time}\n" + _("<b>Order ID: {}\n</b>").format(order.id)+text)
        await call.message.edit_reply_markup()
        await call.answer(_("Your order has been accepted."), show_alert=True)
        await state.finish()
        markup = await categories_keyboard(lang=await get_lang(call.from_user.id))
        await call.message.answer(_("Select one of the categories👇"), reply_markup=markup)
    except Exception as err:
        print(err)
        pass


@dp.callback_query_handler(text="cancel_end", state="confirm_state")
async def cancel_end_fun(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(_("Your order was canceled.But not deleted."), show_alert=True)
    await call.message.delete()
    user = await get_user(call.from_user.id)
    purchases = await get_purchase(user)
    total = 0
    final_total = 0
    text = ""
    if purchases:
        await call.answer()
        for purchase in purchases:
            item = purchase.product
            if user.lang == "ru":
                item_name = item.name_ru
                category_name = item.category_name_ru
            else:
                item_name = item.name
                category_name = item.category_name
            amount = purchase.amount
            price = purchase.product.price
            total = int(amount) * price
            text += f'<b>{category_name}\n   └{item_name}</b> {amount} x {price} = {total} $\n\n'
            final_total += total
        markup = await main_cart_button(purchases, lang = await get_lang(user.id))
        text += "Total: " + str(final_total) + " $"
        await call.message.answer(text=text, reply_markup=markup)
    else:
        await call.answer(_("You haven't products in your cart 🤷‍♂️"), show_alert=True)


@dp.callback_query_handler(text="clear_cart")
async def clear_cart_fun(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    purchases = await get_purchase(user)
    for purchase in purchases:
        await delete_purchase(purchase.id)
    await call.answer(_("Your order deleted"), show_alert=True)
    await list_categories(call.message)

