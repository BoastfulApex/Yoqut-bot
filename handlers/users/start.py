from datetime import datetime, timedelta

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

# from utils.db_api.database import get_faq, get_price_list, get_about_us, get_user
from keyboards.inline.main_inline import menu_keyboard, category_keyboard, product_keyboard, confirm_keyboard, \
    storage_keyboard, storage_menu, get_or_back, month_keyboards, back_to
from loader import dp, _, bot
from utils.db_api import database as commands

import os

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
        await bot.send_message(chat_id=message.from_user.id, text="Parol tog'ri\nBosh menyuga xush kelibsiz",
                               reply_markup=markup)
        await state.set_state('menu')
    else:
        await message.answer("Xatokuuu bu")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Shaxsingizni tasdiqlash uchun iltimos parolni qayta kiriting kiriting")
        await state.set_state("check_password")


@dp.callback_query_handler(state='menu')
async def menu(call: types.CallbackQuery, state: FSMContext):
    command = call.data

    if command == 'add_product':
        await call.message.edit_text(text='Tovar maxsus raqamini kiriting')
        await state.set_state('get_name')
    elif command == 'add_to_storage':
        markup = await product_keyboard()
        await call.message.edit_text(text='Tovar tanlang', reply_markup=markup)
        await state.set_state('get_product')
    elif command == "sell_from_storage":
        markup = await storage_keyboard()
        await call.message.edit_text(text='Tovar tanlang', reply_markup=markup)
        await state.set_state('get_product_from_storage')
    elif command == "storage":
        markup = await storage_menu()
        await call.message.edit_text(text='Kerakli buyruqni tanlang', reply_markup=markup)
        await state.set_state('get_storage_command')


@dp.message_handler(content_types=types.ContentType.TEXT, state="get_name")
async def get_serial_name(message: types.Message, state: FSMContext):
    serial_name = message.text
    await message.answer(text="Kirim narxini kiriting")
    await state.update_data(serial_name=serial_name)
    await state.set_state('get_first_cost')


@dp.message_handler(content_types=types.ContentType.TEXT, state="get_first_cost")
async def get_first_cost(message: types.Message, state: FSMContext):
    try:
        first_cost = int(message.text)
        await message.answer(text="Chiqim narxini kiriting")
        await state.update_data(first_cost=first_cost)
        await state.set_state('get_last_cost')
    except:
        await message.answer(text='Kirim narxini qaytadan kiriting:')
        await state.set_state('get_first_cost')


@dp.message_handler(content_types=types.ContentType.TEXT, state='get_last_cost')
async def get_last_cost(message: types.Message, state: FSMContext):
    try:
        first_cost = int(message.text)
        markup = await category_keyboard()
        await message.answer(text="Tovar kategoriyasini tanlang", reply_markup=markup)
        await state.update_data(last_cost=first_cost)
        await state.set_state('get_category')
    except Exception as ex:
        print(ex)
        await message.answer(text='Chiqim narxini qaytadan kiriting:')
        await state.set_state('get_last_cost')


@dp.callback_query_handler(state='get_category')
async def get_category(call: types.CallbackQuery, state: FSMContext):
    category_id = int(call.data)
    category = await commands.get_category(category_id)
    data = await state.get_data()
    await commands.add_product(unique_name=data['serial_name'], kirish_narxi=int(data['first_cost']),
                               chiqish_narxi=int(data['last_cost']), category=category)
    markup = await menu_keyboard()
    await call.message.edit_text(text="Tovar qo'shildi\nBosh menyu",
                                 reply_markup=markup)
    await state.set_state('menu')


@dp.callback_query_handler(state="get_product")
async def get_product(call: types.CallbackQuery, state: FSMContext):
    product_id = call.data
    await state.update_data(product_id=product_id)
    await bot.send_message(chat_id=call.from_user.id, text="Tovar sonini kiriting")
    await state.set_state('get_product_count')


@dp.message_handler(content_types=types.ContentType.TEXT, state="get_product_count")
async def get_product_count(message: types.Message, state: FSMContext):
    try:
        product_count = int(message.text)
        data = await state.get_data()
        product = await commands.get_product(data["product_id"])
        markup = await confirm_keyboard()
        text = f"Tovar: <b>{product.unique_name}</b>\n" \
               f"Soni: <b>{product_count}</b>\n\n" \
               f"Haqiqatdan skladga qo'shishni istaysizmi"
        await message.answer(text=_(text), reply_markup=markup)
        await state.update_data(product_count=product_count)
        await state.set_state('confirm_add')
    except Exception as ex:
        print(ex)
        await message.answer(text='Tovar sonini qaytadan kiriting')
        await state.set_state('get_product_count')


@dp.callback_query_handler(state="confirm_add")
async def confirm_add(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == "confirm":
        data_state = await state.get_data()
        product = await commands.get_product(int(data_state["product_id"]))
        storages = await commands.get_storage()
        storage_ides = []
        for store in storages:
            storage_ides.append(store.product.id)
        if product.id in storage_ides:
            for i in storages:
                if product.id == i.product.id:
                    i.count += int(data_state["product_count"])
                    i.save()
        else:
            await commands.add_Storage(product=product, count=int(data_state["product_count"]))
        markup = await menu_keyboard()
        await call.message.edit_text(text="Tovar skladga qo'shildi\n\nBosh menyu",
                                     reply_markup=markup)
        await state.set_state("menu")

    elif data == "cancel":
        markup = await menu_keyboard()
        await call.message.edit_text(text="Tovar skladga qo'shilmadi\n\nBosh menyu",
                                     reply_markup=markup)
        await state.set_state("menu")


@dp.callback_query_handler(state="get_product_from_storage")
async def storage_product(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data
    print(call_data)
    await state.update_data(storage_id=call_data)
    await call.message.edit_text(text="Maxssulot sonini kiriting")
    await state.set_state("get_storage_count")


@dp.message_handler(content_types=types.ContentType.TEXT, state="get_storage_count")
async def get_storage_count(message: types.Message, state: FSMContext):
    try:
        product_count = int(message.text)
        data = await state.get_data()
        product_storage = await commands.get_storage_product(int(data["storage_id"]))
        if product_count > product_storage.count:
            await message.answer(text='Tovar sonini qaytadan kiriting')
            await state.set_state('get_storage_count')
        else:
            markup = await confirm_keyboard()
            text = f"Tovar: <b>{product_storage.product.unique_name}</b>\n" \
                   f"Soni: <b>{product_count}</b>\n\n" \
                   f"Haqiqatdan skladdan chiqarinshni istaysizmi"
            await message.answer(text=_(text), reply_markup=markup)
            await state.update_data(product_count=product_count)
            await state.set_state('confirm_sell')
    except Exception as ex:
        print(ex)
        await message.answer(text='Tovar sonini qaytadan kiriting')
        await state.set_state('get_storage_count')


@dp.callback_query_handler(state="confirm_sell")
async def confirm_add(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == "confirm":
        data_state = await state.get_data()
        product_storage = await commands.get_storage_product(int(data_state["storage_id"]))
        await commands.sell_Storage(product=product_storage.product, count=int(data_state["product_count"]))
        product_storage.count -= int(data_state["product_count"])
        product_storage.save()
        markup = await menu_keyboard()
        await call.message.edit_text(text="Tovar skladdan chiqarildi\n\nBosh menyu",
                                     reply_markup=markup)
        await state.set_state("menu")

    elif data == "cancel":
        markup = await menu_keyboard()
        await call.message.edit_text(text="Tovar skladdan chiqarilmadi\n\nBosh menyu",
                                     reply_markup=markup)
        await state.set_state("menu")


@dp.callback_query_handler(state="get_storage_command")
async def grt_storage_command(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data
    if call_data == "products_in_storage":
        storage = await commands.get_storage()
        text = ''
        markup = await get_or_back()
        k = 1
        kirim = []
        chiqim = []
        qolgan = []
        nomi = []
        tr = []
        os.remove("./xisobot.xlsx")
        for i in storage:
            text += f"{k}) Tovar: <b>{i.product.unique_name}</b>\n" \
                    f"Soni: <b>{i.count}</b>\n" \
                    f"<b>---------------------------------</b>\n"
            kirim.append(i.product.kirish_narxi)
            nomi.append(i.product.unique_name)
            chiqim.append(i.product.chiqish_narxi)
            qolgan.append(i.count)
            k += 1
            df = pd.DataFrame({'Maxsulot': nomi,
                               'Kirim narxi': kirim,
                               'Chiqish narxi': chiqim,
                               'Qolgan miqdori': qolgan})
            df.to_excel('./xisobot.xlsx')
        await call.message.edit_text(text=_(text), reply_markup=markup)
        await state.set_state("get_or_back")
    elif call_data == "back_main":
        markup = await menu_keyboard()
        await call.message.edit_text(text="Bosh menyu",
                                     reply_markup=markup)
        await state.set_state('menu')
    elif call_data == "sells_in_this_week":
        storage = await commands.sell_Storages_get()
        time_begin = datetime.now().date() - timedelta(days=7)
        sells = []
        for i in storage:
            if time_begin <= i.date <= datetime.now().date():
                sells.append(i)
        text = ''
        os.remove("./xisobot.xlsx")
        nomi = []
        kirim = []
        chiqim = []
        soni = []
        sana = []
        jami = []
        k = 1
        markup = await get_or_back()
        for i in sells:
            text += f"{k}) Tovar: <b>{i.product.unique_name}</b>\n" \
                    f"Soni: <b>{i.count}</b>\n" \
                    f"<b>---------------------------------</b>\n"
            nomi.append(i.product.unique_name)
            kirim.append(i.product.kirish_narxi)
            chiqim.append(i.product.chiqish_narxi)
            soni.append(i.count)
            sana.append(str(i.date))
            jami.append(i.product.chiqish_narxi * i.count)
            k += 1
        df = pd.DataFrame({'Maxsulot': nomi,
                           'Kirim narxi': kirim,
                           'Chiqish narxi': chiqim,
                           'Soni': soni,
                           'Sana': sana,
                           'Jami': jami,})
        df.to_excel('./xisobot.xlsx')
        await call.message.edit_text(text=_(text), reply_markup=markup)
        await state.set_state("get_or_back")
    elif call_data == "sells_in_this_month":
        month = datetime.now().month
        storage = await commands.sell_Storages_get()
        sells = []
        text = ''
        for i in storage:
            if i.date.month == month:
                sells.append(i)
        os.remove("./xisobot.xlsx")
        nomi = []
        kirim = []
        chiqim = []
        soni = []
        sana = []
        jami = []
        k = 1
        markup = await get_or_back()
        for i in sells:
            text += f"{k}) Tovar: <b>{i.product.unique_name}</b>\n" \
                    f"Soni: <b>{i.count}</b>\n" \
                    f"<b>---------------------------------</b>\n"
            nomi.append(i.product.unique_name)
            kirim.append(i.product.kirish_narxi)
            chiqim.append(i.product.chiqish_narxi)
            soni.append(i.count)
            sana.append(str(i.date))
            jami.append(i.product.chiqish_narxi * i.count)
            k += 1
        df = pd.DataFrame({'Maxsulot': nomi,
                           'Kirim narxi': kirim,
                           'Chiqish narxi': chiqim,
                           'Soni': soni,
                           'Sana': sana,
                           'Jami': jami,})
        df.to_excel('./xisobot.xlsx')
        await call.message.edit_text(text=_(text), reply_markup=markup)
        await state.set_state("get_or_back")
    elif call_data == 'sells_by_product':
        await call.message.edit_text(text=_('Tovarning maxsus seria nomini kiriting'))
        await state.set_state('for_by_serial')
    elif call_data == 'sells_in_day':
        storage = await commands.sell_Storages_get()
        sells = []
        text = ''
        for i in storage:
            if i.date.day == datetime.now().day:
                sells.append(i)
        os.remove("./xisobot.xlsx")
        nomi = []
        kirim = []
        chiqim = []
        soni = []
        sana = []
        jami = []
        k = 1
        markup = await get_or_back()
        for i in sells:
            text += f"{k}) Tovar: <b>{i.product.unique_name}</b>\n" \
                    f"Soni: <b>{i.count}</b>\n" \
                    f"<b>---------------------------------</b>\n"
            nomi.append(i.product.unique_name)
            kirim.append(i.product.kirish_narxi)
            chiqim.append(i.product.chiqish_narxi)
            soni.append(i.count)
            sana.append(str(i.date))
            jami.append(i.product.chiqish_narxi * i.count)
            k += 1
        df = pd.DataFrame({'Maxsulot': nomi,
                           'Kirim narxi': kirim,
                           'Chiqish narxi': chiqim,
                           'Soni': soni,
                           'Sana': sana,
                           'Jami': jami,})
        df.to_excel('./xisobot.xlsx')
        await call.message.edit_text(text=_(text), reply_markup=markup)
        await state.set_state("get_or_back")
    elif call_data == "sells_in_month":
        markup = await month_keyboards()
        await call.message.edit_text(text=_("Kerakli oyni tanlang"), reply_markup=markup)
        await state.set_state("get_month")
    elif call_data == "product_by_category":
        markup = await category_keyboard()
        await call.message.edit_text(text="Kerakli kategoriyani tanlang", reply_markup=markup)
        await state.set_state("get_sell_category")


@dp.callback_query_handler(state="get_sell_category")
async def get_sell_category(call: types.CallbackQuery, state: FSMContext):
    storage = await commands.sell_Storages_get()
    print("ID: ", call.data)
    sells = []
    for i in storage:
        if i.product.category.id == int(call.data):
            sells.append(i)
    text = ''
    if len(sells) == 0:
        await call.answer(text=_("Tanlangan oy bo'sh\nQaytadan tanlang"), show_alert=True)
    else:
        os.remove("./xisobot.xlsx")
        nomi = []
        kirim = []
        chiqim = []
        soni = []
        sana = []
        jami = []
        k = 1
        markup = await get_or_back()
        for i in sells:
            text += f"{k}) Tovar: <b>{i.product.unique_name}</b>\n" \
                    f"Soni: <b>{i.count}</b>\n" \
                    f"<b>---------------------------------</b>\n"
            nomi.append(i.product.unique_name)
            kirim.append(i.product.kirish_narxi)
            chiqim.append(i.product.chiqish_narxi)
            soni.append(i.count)
            sana.append(str(i.date))
            jami.append(i.product.chiqish_narxi * i.count)
            k += 1
        df = pd.DataFrame({'Maxsulot': nomi,
                           'Kirim narxi': kirim,
                           'Chiqish narxi': chiqim,
                           'Soni': soni,
                           'Sana': sana,
                           'Jami': jami, })
        df.to_excel('./xisobot.xlsx')
        await call.message.edit_text(text=_(text), reply_markup=markup)
        await state.set_state("get_or_back")


@dp.callback_query_handler(state="get_month")
async def get_month(call: types.CallbackQuery, state: FSMContext):
    if call.data != "back":
        month_id = call.data
        storage = await commands.sell_Storages_get()
        sells = []
        for i in storage:
            if i.date.month == int(month_id):
                sells.append(i)
        text = ''
        if len(sells) == 0:
            await call.answer(text=_("Tanlangan oy bo'sh\nQaytadan tanlang"), show_alert=True)
            await state.set_state("get_month")
        else:
            os.remove("./xisobot.xlsx")
            nomi = []
            kirim = []
            chiqim = []
            soni = []
            sana = []
            jami = []
            k = 1
            markup = await get_or_back()
            for i in sells:
                text += f"{k}) Tovar: <b>{i.product.unique_name}</b>\n" \
                        f"Soni: <b>{i.count}</b>\n" \
                        f"<b>---------------------------------</b>\n"
                nomi.append(i.product.unique_name)
                kirim.append(i.product.kirish_narxi)
                chiqim.append(i.product.chiqish_narxi)
                soni.append(i.count)
                sana.append(str(i.date))
                jami.append(i.product.chiqish_narxi * i.count)
                k += 1
            df = pd.DataFrame({'Maxsulot': nomi,
                               'Kirim narxi': kirim,
                               'Chiqish narxi': chiqim,
                               'Soni': soni,
                               'Sana': sana,
                               'Jami': jami, })
            df.to_excel('./xisobot.xlsx')
            await call.message.edit_text(text=_(text), reply_markup=markup)
            await state.set_state("get_or_back")
    else:
        markup = await storage_menu()
        await call.message.edit_text(text="Kerakli bo'limni tanlang", reply_markup=markup)
        await state.set_state("get_storage_command")


@dp.message_handler(content_types=types.ContentType.TEXT, state="for_by_serial")
async def getSerial(message: types.Message, state: FSMContext):
    serial = message.text
    sells = await commands.get_by_serial(serial=serial)
    text = ''
    if len(sells) != 0:
        os.remove("./xisobot.xlsx")
        nomi = []
        kirim = []
        chiqim = []
        soni = []
        sana = []
        jami = []
        k = 1
        markup = await get_or_back()
        for i in sells:
            text += f"{k}) Tovar: <b>{i.product.unique_name}</b>\n" \
                    f"Soni: <b>{i.count}</b>\n" \
                    f"<b>---------------------------------</b>\n"
            nomi.append(i.product.unique_name)
            kirim.append(i.product.kirish_narxi)
            chiqim.append(i.product.chiqish_narxi)
            soni.append(i.count)
            sana.append(str(i.date))
            jami.append(i.product.chiqish_narxi * i.count)
            k += 1
        df = pd.DataFrame({'Maxsulot': nomi,
                           'Kirim narxi': kirim,
                           'Chiqish narxi': chiqim,
                           'Soni': soni,
                           'Sana': sana,
                           'Jami': jami, })
        df.to_excel('./xisobot.xlsx')
        await bot.send_message(chat_id=message.from_user.id, text=_(text), reply_markup=markup)
        await state.set_state("get_or_back")
    else:
        await bot.send_message(chat_id=message.from_user.id, text=_("Xech nima topilmadi\nQaytadan kiriting"))
        await state.set_state("for_by_serial")


@dp.callback_query_handler(state="get_or_back")
async def get_file(call: types.CallbackQuery, state: FSMContext):
    command = call.data
    if command == 'get':
        file = open('./xisobot.xlsx', 'rb')
        markup = await back_to()
        await call.message.delete()
        await bot.send_document(chat_id=call.from_user.id, document=file, reply_markup=markup, caption="Xisobot")
    else:
        markup = await storage_menu()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang', reply_markup=markup)
        await state.set_state('get_storage_command')
