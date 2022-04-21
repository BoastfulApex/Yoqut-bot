from loader import _
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import get_categories, get_products, get_storage

plus_minus_data = CallbackData("PS", "key", "purchase_id")


async def menu_keyboard():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Tovar yaratish"), callback_data="add_product")],
            [InlineKeyboardButton(text=_("Skladga tovar olib kirish"), callback_data="add_to_storage")],
            [InlineKeyboardButton(text=_("Skladdagi tovarni sotish"), callback_data="sell_from_storage")],
            [InlineKeyboardButton(text=_("Sklad"), callback_data="storage")],
        ]
    )
    return markup


async def category_keyboard():
    categories = await get_categories()
    inline_keyboard = []
    for i in categories:
        inline_keyboard.append([InlineKeyboardButton(text=i.category_name, callback_data=i.id)])

    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


async def product_keyboard():
    products = await get_products()
    inline_keyboard = []
    for i in products:
        inline_keyboard.append([InlineKeyboardButton(text=i.unique_name, callback_data=i.id)])

    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


async def confirm_keyboard():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("❌ Yo'q"), callback_data=f"cancel"),
                InlineKeyboardButton(text=_("✅ Ha"), callback_data=f"confirm"),
            ],
        ]
    )
    return markup


async def storage_keyboard():
    products = await get_storage()
    inline_keyboard = []
    for i in products:
        inline_keyboard.append([InlineKeyboardButton(text=i.product.unique_name, callback_data=i.id)])

    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


async def storage_menu():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Skladdagi tovarlarni ko'rish"), callback_data="products_in_storage")],
            [InlineKeyboardButton(text=_("Shu hafta uchun savdoni ko'rish"), callback_data="sells_in_this_week")],
            [InlineKeyboardButton(text=_("Oy uchun savdoni ko'rish"), callback_data="sells_in_month")],
            [InlineKeyboardButton(text=_("Shu oy uchun savdoni ko'rish"), callback_data="sells_in_this_month")],
            [InlineKeyboardButton(text=_("Tovar nomi bo'yicha savdoni ko'rish"), callback_data="sells_by_product")],
            [InlineKeyboardButton(text=_("Kunlik savdoni ko'rish"), callback_data="sells_in_day")],
            [InlineKeyboardButton(text=_("Kategoriya bo'yicha tovarlar"), callback_data="product_by_category")],
            [InlineKeyboardButton(text=_("🔙 Orqaga"), callback_data=f"back_main")],
        ]
    )
    return markup


async def get_or_back():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("🔙 Orqaga"), callback_data=f"back"),
                InlineKeyboardButton(text=_("📑 Excell hujjatni yuklash"), callback_data=f"get"),
            ],
        ]
    )
    return markup


async def back_to():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("🔙 Orqaga"), callback_data=f"back"),
            ],
        ]
    )
    return markup


async def month_keyboards():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('January', callback_data='01'),
             InlineKeyboardButton('February', callback_data='02'),
             InlineKeyboardButton('March', callback_data='03'),
             InlineKeyboardButton('April', callback_data='04')],

            [InlineKeyboardButton('May', callback_data='05'),
             InlineKeyboardButton('June', callback_data='06'),
             InlineKeyboardButton('July', callback_data='07'),
             InlineKeyboardButton('August', callback_data='08')],

            [InlineKeyboardButton('September', callback_data='09'),
             InlineKeyboardButton('October', callback_data='10'),
             InlineKeyboardButton('November', callback_data='11'),
             InlineKeyboardButton('December', callback_data='12')],

            [InlineKeyboardButton("◀️Back", callback_data="back")]
        ])
    return keyboard


async def menu_button(lang):
    main_menu_uz = ['Mahsulotlar', "Narxlar ro'yxatini yuklab olish", "F.A.Q", "Biz haqimizda", "Biz bilan bog'lanish ",
                    "Tilni o'zgartirish"]
    main_menu_kr = ["Маҳсулотлар", "Нархлар рўйхатини юклаб олиш", "F.A.Q", "Биз ҳақимизда", "Биз билан боғланиш",
                    "Тилни ўзгартириш"]
    main_menu_ru = ['Продукты', "Скачать прайс-лист", "F.A.Q", "О нас", "Связаться с нами", "Изменить язык"]
    if lang == "ru":
        texs = main_menu_ru
    elif lang == "uz":
        texs = main_menu_uz
    else:
        texs = main_menu_kr

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"🛍 {texs[0]}"), callback_data="order_menu"),
            ],
            [
                InlineKeyboardButton(text=_(f"📥 {texs[1]}"), callback_data="download_price"),
            ],
            [
                InlineKeyboardButton(text=_(f"❓ {texs[2]}"), callback_data="faq"),
            ],
            [
                InlineKeyboardButton(text=_(f"📑 {texs[3]}"), callback_data="about_us"),
            ],

            [
                InlineKeyboardButton(text=_(f"✍️{texs[4]}"), callback_data="ask_us"),
            ],

            [
                InlineKeyboardButton(text=_(f"🔄 {texs[5]}"), callback_data="change_language")
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
                InlineKeyboardButton(text="🇺🇿uz", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇺🇿уз", callback_data="lang_kr"),
            ],
        ]
    )
    return markup


async def contact_btn(lang):
    mains_ru = ["Электронная почта" "Телефон"]
    mains_uz = ["Elektron pochta", "Telefon"]
    mains_kr = ["Электрон почта", "Телефон"]
    if lang == "ru":
        texs = mains_ru
    elif lang == "uz":
        texs = mains_uz
    else:
        texs = mains_kr
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"📧 {texs[0]}"), callback_data="email"),
                InlineKeyboardButton(text=_(f"📞 {texs[1]}"), callback_data="phone"),
            ]
        ]
    )
    return markup


back = ["Назад", "Orqaga", "Орқага"]


async def payment_options_btn(lang):
    mains = ["Онлине" "Оффлайн"]
    mains_uz = ["Online", "Offline"]
    if lang == "ru":
        texs = mains
        bask = back[0]
    elif lang == "uz":
        texs = mains_uz
        bask = back[1]
    else:
        texs = mains
        bask = back[2]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"💳 {texs[0]}"), callback_data="online"),
                InlineKeyboardButton(text=_(f"💵 {texs[1]}"), callback_data="offline"),
            ],
            [
                InlineKeyboardButton(text=_(f"◀️ {bask}"), callback_data="back"),
            ]
        ]
    )
    return markup


async def answer_btn(user_id, lang):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Answer", locale=lang), callback_data=f"answer-{user_id}"),
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
        if lang == "uz":
            markup.insert(InlineKeyboardButton(text=f"{purchase.product.name_latin}", callback_data="no_call"))
        if lang == "kr":
            markup.insert(InlineKeyboardButton(text=f"{purchase.product.name_kiril}", callback_data="no_call"))
        markup.insert(
            InlineKeyboardButton(text=f"➕", callback_data=plus_minus_data.new(key="plus", purchase_id=purchase.id)))

    mainkart_ru = ["Очистить корзину", "Подтвердить заказ", "Заказать снова"]
    mainkart_uz = ["Savatni bo'shatish", "Buyurtmani tasdiqlash", "Qaytadan buyurtma berish"]
    mainkart_kr = ["Саватни бўшатиш", "Буюртмани тасдиқлаш", "Қайтадан буюртма бериш"]
    if lang == "ru":
        texs = mainkart_ru
    elif lang == "uz":
        texs = mainkart_uz
    else:
        texs = mainkart_kr
    markup.row(
        InlineKeyboardButton(text=_(f"🗑 {texs[0]}"), callback_data="clear_cart"),
        InlineKeyboardButton(text=_(f"🧾 {texs[1]}"), callback_data="confirm")
    )
    markup.row(InlineKeyboardButton(text=_(f"♻️ {texs[2]}"), callback_data="back_to_menu_page"))
    return markup


confirm_ru = ["Подтвердить", "Отмена"]
confirm_uz = ["Tasdiqlash", "Bekor qilish"]
confirm_kr = ["Тасдиқлаш", "Бекор қилиш"]


async def confirm_end(lang):
    if lang == "ru":
        texs = confirm_ru
        bask = back[0]
    elif lang == "uz":
        texs = confirm_uz
        bask = back[1]
    else:
        texs = confirm_kr
        bask = back[2]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"❌ {texs[1]}"), callback_data="back_card"),
                # InlineKeyboardButton(text=_("❌ Cancel", locale=lang), callback_data="cancel_end"),
                # InlineKeyboardButton(text=_("✅ Confirm", locale=lang), callback_data="confirm_end"),
                InlineKeyboardButton(text=_(f"✅ {texs[0]}"), callback_data="go_payment"),
            ],
            [
                InlineKeyboardButton(text=_(f"◀️ {bask}"), callback_data="back_main"),
            ]

        ]
    )
    return markup


async def confirm_all(lang):
    if lang == "ru":
        texs = confirm_ru
        bask = back[0]
    elif lang == "uz":
        texs = confirm_uz
        bask = back[1]
    else:
        texs = confirm_kr
        bask = back[2]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                # InlineKeyboardButton(text=_("❌ Cancel", locale=lang), callback_data="back_card"),
                InlineKeyboardButton(text=_(f"❌ {texs[0]}"), callback_data="cancel_end"),
                InlineKeyboardButton(text=_(f"✅ {texs[1]}"), callback_data="confirm_end"),
                # InlineKeyboardButton(text=_("✅ Confirm", locale=lang), callback_data="go_payment"),
            ],
            [
                InlineKeyboardButton(text=_(f"◀️ {bask}"), callback_data="back_main"),
            ]

        ]
    )
    return markup


async def confirm_payment_btn_20(lang, order_id, user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("❌ Cancel", locale=lang), callback_data=f"cancel20-{order_id}-{user_id}"),
                InlineKeyboardButton(text=_("✅ Confirm", locale=lang), callback_data=f"confirm20-{order_id}-{user_id}"),
            ],
        ]
    )
    return markup


async def confirm_payment_btn_80(lang, order_id, user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("❌ Cancel", locale=lang), callback_data=f"cancel80-{order_id}-{user_id}"),
                InlineKeyboardButton(text=_("✅ Confirm", locale=lang), callback_data=f"confirm80-{order_id}-{user_id}"),
            ],
        ]
    )
    return markup


entity_ru = ["Физическое лицо", "Юридическое лицо"]
entity_uz = ["Jismoniy shaxs", "Yuridik shaxs"]
entity_kr = ["Жисмоний шахс", "Юридик шахс"]


async def entity_keyboard(lang):
    if lang == "ru":
        texs = entity_ru
        bask = back[0]
    elif lang == "uz":
        texs = entity_uz
        bask = back[1]
    else:
        texs = entity_kr
        bask = back[2]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"👥 {texs[1]}"), callback_data="entity"),
                InlineKeyboardButton(text=_(f"👤 {texs[0]}"), callback_data="personal"),
            ],
            [
                InlineKeyboardButton(text=_(f"◀️ {bask}"), callback_data="check_entity"),
            ]

        ]
    )
    return markup


async def back_to_home(lang):
    if lang == "ru":
        bask = back[0]
    elif lang == "uz":
        bask = back[1]
    else:
        bask = back[2]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"◀️ {bask}"), callback_data="back_home"),
            ]

        ]
    )
    return markup


about_ru = ["Фото с мероприятий", "Видео с мероприятий", ]
about_uz = ["Voqealardan fotolar", "Voqealardan video"]
about_kr = ["Воқеалардан фотолар", "Воқеалардан видео"]


async def about_us_btn(lang):
    if lang == "ru":
        texs = about_ru
        bask = back[0]
    elif lang == "uz":
        texs = about_uz
        bask = back[1]
    else:
        texs = about_kr
        bask = back[2]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"📷 {texs[0]}"), callback_data="meeting_photos"),
            ],
            [
                InlineKeyboardButton(text=_(f"🎥 {texs[1]}"), callback_data="meeting_videos"),
            ],
            [
                InlineKeyboardButton(text=_(f"◀️ {bask}"), callback_data="back_home"),
            ]

        ]
    )
    return markup


pagination_call = CallbackData("paginator", "key", "page")
show_item = CallbackData("show_item", "item_id")


async def get_page_keyboard(max_pages: int, key, lang, page: int = 1):
    if lang == "ru":
        bask = back[0]
    elif lang == "uz":
        bask = back[1]
    else:
        bask = back[2]
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
        InlineKeyboardButton(text=_(f"◀️ {bask}"), callback_data="back_about_us"),
    )
    return markup


back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("◀️ Back"), callback_data="back_main"),
        ]
    ]
)


async def back_order(lang):
    if lang == "ru":
        bask = back[0]
    elif lang == "uz":
        bask = back[1]
    else:
        bask = back[2]

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"◀️ {bask}"), callback_data="back_main"),
            ]
        ]
    )
    return markup


async def back_home():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("◀️ Back"), callback_data="home"),
            ]
        ]
    )
    return markup
