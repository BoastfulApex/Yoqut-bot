from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.db_api import database as commands
from loader import dp, _, bot
import validators
# from utils.db_api.database import get_faq, get_price_list, get_about_us, get_user
import phonenumbers
from keyboards.inline.main_inline import menu_keyboard, category_keyboard, product_keyboard, confirm_keyboard, \
    storage_keyboard

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
            await message.answer(text='32Tovar sonini qaytadan kiriting')
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

