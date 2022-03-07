from loader import _
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

plus_minus_data = CallbackData("PS", "key", "purchase_id")


async def menu_button(lang):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("🛍 Products", locale=lang), callback_data="order_menu"),
            ],
            [
                InlineKeyboardButton(text=_("📥 Download price list", locale=lang), callback_data="download_price"),
            ],
            [
                InlineKeyboardButton(text=_("❓ F.A.Q", locale=lang), callback_data="faq"),
            ],
            [
                InlineKeyboardButton(text=_("📑 About us", locale=lang), callback_data="about_us"),
            ],

            [
                InlineKeyboardButton(text=_("🔄 Change language", locale=lang), callback_data="change_language")
            ]

        ]
    )
    return markup


async def languages_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="🇷🇺ru", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇺🇸en", callback_data="lang_en"),
            ],
        ]
    )
    return markup


async def contact_btn(lang):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("📧 Email", locale=lang), callback_data="email"),
                InlineKeyboardButton(text=_("📞 Phone", locale=lang), callback_data="phone"),
            ]
        ]
    )
    return markup


async def main_cart_button(purchases, lang):
    markup = InlineKeyboardMarkup(row_width=3)
    for purchase in purchases:
        markup.insert(
            InlineKeyboardButton(text=f"➖", callback_data=plus_minus_data.new(key="minus", purchase_id=purchase.id)))
        if lang == "ru":
            markup.insert(InlineKeyboardButton(text=f"{purchase.product.name_ru}", callback_data="no_call"))
        if lang == "en":
            markup.insert(InlineKeyboardButton(text=f"{purchase.product.name}", callback_data="no_call"))
        markup.insert(
            InlineKeyboardButton(text=f"➕", callback_data=plus_minus_data.new(key="plus", purchase_id=purchase.id)))

    markup.row(
        InlineKeyboardButton(text=_("🗑 Clear cart", locale=lang), callback_data="clear_cart"),
        InlineKeyboardButton(text=_("🧾 Confirm order", locale=lang), callback_data="confirm")
    )
    markup.row(InlineKeyboardButton(text=_("♻️ Order again", locale=lang), callback_data="back_to_menu_page"))
    return markup


async def confirm_end(lang):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("❌ Cancel", locale=lang), callback_data="cancel_end"),
                InlineKeyboardButton(text=_("✅ Confirm", locale=lang), callback_data="confirm_end"),
            ],
            [
                InlineKeyboardButton(text=_("◀️ Back"), callback_data="back_main"),
            ]

        ]
    )
    return markup


async def back_to_home(lang):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("◀️ Back", locale=lang), callback_data="back_home"),
            ]

        ]
    )
    return markup


async def about_us_btn(lang):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("🧾 Certificates", locale=lang), callback_data="certificate"),
            ],
            [
                InlineKeyboardButton(text=_("📷 Photo from events", locale=lang), callback_data="meeting_photos"),
            ],
            [
                InlineKeyboardButton(text=_("🎥 Video from events", locale=lang), callback_data="meeting_videos"),
            ],
            [
                InlineKeyboardButton(text=_("◀️ Back", locale=lang), callback_data="back_home"),
            ]

        ]
    )
    return markup


pagination_call = CallbackData("paginator", "key", "page")
show_item = CallbackData("show_item", "item_id")


async def get_page_keyboard(max_pages: int, key, lang, page: int = 1):
    previous_page = page - 1
    previous_page_text = "⬅️"



    next_page = page + 1
    next_page_text = "➡️"

    markup = InlineKeyboardMarkup(row_width=2)
    if previous_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key, page=previous_page)
            )
        )


    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key, page=next_page)
            )
        )

    markup.row(
        InlineKeyboardButton(text=_("◀️ Back", locale=lang), callback_data="back_about_us"),
    )
    return markup


back_button = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text=_("◀️ Back"), callback_data="back_main"),
            ]
    ]
)
