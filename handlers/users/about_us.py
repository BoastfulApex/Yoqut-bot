from aiogram import types
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo
from keyboards.inline.main_inline import get_page_keyboard, pagination_call
from utils.db_api.database import get_photos, get_videos, get_certificate, get_lang
from loader import dp, _
from utils.misc.pages import get_page


@dp.callback_query_handler(text="certificate")
async def show_certificate(call: types.CallbackQuery):
    await call.answer()
    list_of_data = await get_certificate()
    lang = await get_lang(call.from_user.id)
    if len(list_of_data) != 0:
        await call.message.delete()
        text = get_page(list_of_data)
        max_pages_photo = len(list_of_data)
        if lang == "ru":
            desc = text.description_ru
        else:
            desc = text.description_en
        await call.message.answer_photo(photo=text.photo, caption=desc + _("\n\nCertificates 1/{}👇").format(max_pages_photo),
                                        reply_markup=await get_page_keyboard(max_pages=max_pages_photo, key="Certificates", lang=await get_lang(call.from_user.id)))


@dp.callback_query_handler(text="meeting_photos")
async def show_photos(call: types.CallbackQuery):
    await call.answer()
    list_of_data = await get_photos()
    lang = await get_lang(call.from_user.id)
    if len(list_of_data) != 0:
        await call.message.delete()
        text = get_page(list_of_data)
        max_pages_photo = len(list_of_data)
        if lang == "ru":
            desc = text.description_ru
        else:
            desc = text.description_en
        await call.message.answer_photo(photo=text.photo, caption=desc + _("\n\nImages 1/{}👇").format(max_pages_photo),
                                        reply_markup=await get_page_keyboard(max_pages=max_pages_photo, key="Images",
                                                                             lang=await get_lang(call.from_user.id)))


@dp.callback_query_handler(text="meeting_videos")
async def show_videos(call: types.CallbackQuery):
    await call.answer()
    list_of_data = await get_videos()
    if len(list_of_data) != 0:
        await call.message.delete()
        text = get_page(list_of_data)
        max_pages_photo = len(list_of_data)
        lang = await get_lang(call.from_user.id)
        if lang == "ru":
            desc = text.description_ru
        else:
            desc = text.description_en
        await call.message.answer_video(video=text.video,
                                        caption=desc + _("\n\nVideos 1/{}👇").format(max_pages_photo),
                                        reply_markup=await get_page_keyboard(max_pages=max_pages_photo, key="Videos",
                                                                             lang=await get_lang(call.from_user.id)))


@dp.callback_query_handler(pagination_call.filter(page="current_page"))
async def current_page_error(call: CallbackQuery):
    await call.answer()


@dp.callback_query_handler(pagination_call.filter())
async def show_chosen_page(call: CallbackQuery, callback_data: dict):
    await call.answer()
    list_of_data = []
    key = callback_data.get("key")
    current_page = int(callback_data.get("page"))
    lang = await get_lang(call.from_user.id)
    if key == "Certificates":
        list_of_data = await get_certificate()
        max_pages_photo = len(list_of_data)
        main_data = get_page(list_of_data, current_page)
        if lang == "ru":
            desc = main_data.description_ru
        else:
            desc = main_data.description_en
        media = InputMediaPhoto(main_data.photo,
                                caption=desc + _("\n\n{} {}/{}👇").format(key, current_page,
                                                                                      max_pages_photo))

    if key == "Images":
        list_of_data = await get_photos()
        max_pages_photo = len(list_of_data)
        main_data = get_page(list_of_data, current_page)
        if lang == "ru":
            desc = main_data.description_ru
        else:
            desc = main_data.description_en
        media = InputMediaPhoto(main_data.photo,
                                caption=desc + _("\n\n{} {}/{}👇").format(key, current_page,
                                                                                      max_pages_photo))

    if key == "Videos":
        list_of_data = await get_videos()
        max_pages_photo = len(list_of_data)
        main_data = get_page(list_of_data, current_page)
        if lang == "ru":
            desc = main_data.description_ru
        else:
            desc = main_data.description_en
        media = InputMediaVideo(main_data.video,
                                caption=desc + _("\n\n{} {}/{}👇").format(key, current_page,
                                                                                      max_pages_photo))
    else:
        await call.answer(_("Nothing else"), show_alert=True)

    markup = await get_page_keyboard(max_pages=max_pages_photo, key=key, lang=await get_lang(call.from_user.id),
                                     page=current_page)
    await call.message.edit_media(media=media, reply_markup=markup)
