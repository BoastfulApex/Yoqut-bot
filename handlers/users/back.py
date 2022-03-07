from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.main_inline import back_button
from .cart import cart_fun, confirm_fun, phone_cart_fun, emain_cart_fun, company_name_fun, address_name_fun
from loader import _

@dp.callback_query_handler(text="back_main", state="name_cart")
async def back_cart(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await cart_fun(call)


@dp.callback_query_handler(text="back_main", state="phone_cart")
async def back_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter your name..."), reply_markup=back_button)
    await state.set_state("name_cart")


@dp.callback_query_handler(text="back_main", state="email_cart")
async def back_phone(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter the number in international format\nFor example: +998901234567"),reply_markup=back_button)
    await state.set_state("phone_cart")


@dp.callback_query_handler(text="back_main", state="company_name")
async def back_email(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter your email..."), reply_markup=back_button)
    await state.set_state("email_cart")


@dp.callback_query_handler(text="back_main", state="address")
async def back_company(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter your company name..."), reply_markup=back_button)
    await state.set_state("company_name")



@dp.callback_query_handler(text="back_main", state="confirm_state")
async def back_address(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Address company...\n\nExample: 360 Monmouth Rd, Elizabeth, NJ 07208, United States"),
                         reply_markup=back_button)
    await state.set_state("address")
