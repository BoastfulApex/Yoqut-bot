from loader import _
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.database import get_items, get_categories

menu_cd = CallbackData("show_menu", "level", "category", "item_id")
buy_item = CallbackData("buy", "item_id")
main_select = CallbackData("main_select", "key", "data")
select = CallbackData("select", "key", "data", "choosen_data", "item_id")
cart_callback = CallbackData("cart", "choosen_data", "item_id")
about_callback = CallbackData("about", "key", "item_id", "selected")

pagination_about_call = CallbackData("paginator_about", "key", "page", "selected")

def make_callback_data(level, category="0", item_id="0"):
    return menu_cd.new(level=level, category=category, item_id=item_id)


async def categories_keyboard(lang):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)
    categories = await get_categories()
    for category in categories:
        if lang == "ru":
            button_text = f"{category.category_name_ru}"
        else:
            button_text = f"{category.category_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text=_("◀️ Back", locale=lang), callback_data="back_home"),
        InlineKeyboardButton(text=_("🛒 Cart", locale=lang), callback_data="cart"),
    )

    return markup


async def items_keyboard(category, lang):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()
    items = await get_items(category)
    for item in items:
        if lang == "ru":
            button_text = f"{item.name_ru}"
        else:
            button_text = f"{item.name}"

        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, item_id=item.id)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text=_("◀️ Back", locale=lang),
            callback_data="back_category")
    )
    return markup


async def item_keyboard(category, item_id, selected, lang):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text=_("Selected {} Ton", locale=lang).format(selected), callback_data="no_call"))
    markup.row(InlineKeyboardButton(text=f"1",
                                    callback_data=select.new(key="num_choose", data="1", choosen_data=selected,
                                                             item_id=item_id)))
    for i in range(2, 10):
        markup.insert(InlineKeyboardButton(text=f"{i}", callback_data=select.new(key="num_choose", data=f"{i}",
                                                                                 choosen_data=selected,
                                                                                 item_id=item_id)))

    markup.row(
        InlineKeyboardButton(text=f"0", callback_data=select.new(key="num_choose", data="0", choosen_data=selected,
                                                                 item_id=item_id)),
        InlineKeyboardButton(text=_(f"🗑 Empty cart", locale=lang),
                             callback_data=select.new(key="delete_choosen", data="0", choosen_data=selected,
                                                      item_id=item_id))
    )

    markup.row(
        InlineKeyboardButton(
            text=_("📄 About product", locale=lang),
            callback_data=about_callback.new(key="about", item_id=item_id, selected=selected)),
        InlineKeyboardButton(
            text=_("🛒 Add to cart", locale=lang),
            callback_data=cart_callback.new(choosen_data=selected, item_id=item_id))
    )
    print("ss",category, item_id)
    markup.row(
        InlineKeyboardButton(
            text=_("◀️ Back",locale=lang),
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category, item_id=item_id))
    )


    return markup


async def about_product_btn(item_id, selected, lang, max_pages: int, key, page: int = 1):
    markup = InlineKeyboardMarkup(row_width=2)

    previous_page = page - 1
    previous_page_text = "⬅️"

    next_page = page + 1
    next_page_text = "➡️"

    if previous_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_about_call.new(key=key, page=previous_page, selected=selected)
            )
        )

    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_about_call.new(key=key, page=next_page,selected=selected)
            )
        )

    markup.row(InlineKeyboardButton(text=_("◀️ Back",locale=lang),
                                    callback_data=about_callback.new(key="back_product", item_id=item_id,
                                                                     selected=selected)))
    return markup

