import asyncio
from aiogram import types
from data.config import SLEEP_TIME
from keyboards.inline.main_inline import  confirm_end
from loader import dp, bot
from utils.db_api.database import get_users
from aiogram.dispatcher import FSMContext
from filters.admin_filter import IsAdmin


@dp.message_handler(IsAdmin(), commands=["send"], state="*")
async def reklama_fun(message: types.Message, state: FSMContext):
    users_count = len(await get_users())
    await message.answer("🗣 Отправьте одно сообщение которое хотите разослать всем пользователям. Отправка сообщения занимает около {} секунды".format(int(users_count * SLEEP_TIME)))
    await state.set_state("reklama_data")


@dp.message_handler(IsAdmin(), content_types=types.ContentTypes.ANY, state="reklama_data")
async def reklama_data_fun(message: types.Message, state: FSMContext):
    if message.content_type in ["photo", "video", "audio", "animation"]:
        caption = message.caption
    else:
        caption = message.text
    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        caption=caption if caption is not None else "",
        reply_markup= await confirm_end(lang="ru")
    )
    await state.update_data(message_id=message.message_id)
    await state.set_state("confirmation_send")


@dp.callback_query_handler(text="confirm_end", state="confirmation_send")
async def send_data_to_users(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    message_some_id = (await call.message.answer("Отправка...🚀")).message_id
    users = await get_users()
    send_data, not_send = 0, 0
    data = await state.get_data()
    message_id = data.get('message_id')

    for user in users:
        try:
            await bot.copy_message(chat_id=user.user_id,
                                   from_chat_id=call.from_user.id,
                                   message_id=message_id)
            send_data += 1
            await asyncio.sleep(float(SLEEP_TIME))
        except Exception as err:
            print(err)
            not_send += 1
    await bot.delete_message(chat_id=call.from_user.id, message_id=message_some_id)
    await call.message.answer("📊 Статистика по вашему боту:\n✅️ Доставлено: {}\n⛔️ Не доставлено: {}".format(send_data, not_send))
    await state.finish()


@dp.callback_query_handler(text="cancel_end", state="confirmation_send")
async def cancel_data(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer("Отменено")
    await state.finish()