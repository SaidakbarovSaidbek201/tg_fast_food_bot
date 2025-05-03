from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api.commands import get_all_categories, get_products_by_category, get_category_id, get_all_products
from utils.db_api.database import SessionLocal
main_menu_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("🍕 Menyu")],
        [KeyboardButton("📖 Mening buyurtmalarim"), KeyboardButton("🍕 Filiallarimiz")],
        [KeyboardButton("☎️ Qayta aloqa"), KeyboardButton("⚙️ Sozlamalar")]
    ]
)

main_admin_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("📊 Category qo'shish"), KeyboardButton("📊 Mahsulot qo'shish"), KeyboardButton("🛠️ Mahsulotlar")],
        [KeyboardButton("🗂️ Kategoriyalar"), KeyboardButton("📦 Buyurtmalar")],
        [KeyboardButton("🔙 Orqaga")]
    ]
)


def menu_keyboards():
    session = SessionLocal()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    categories = get_all_categories(session)
    for category in categories:
        keyboard.add(KeyboardButton(category.name))
    session.close()
    keyboard.add(KeyboardButton('🔙 Orqaga'))
    return keyboard


def product_keyboards():
    session = SessionLocal()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    category_id = get_category_id()
    products = get_products_by_category(session, category_id)
    for product in products:
        keyboard.add(KeyboardButton(product.name))
    session.close()
    keyboard.add(KeyboardButton('🔙 Orqaga'))
    return keyboard


def product_keyboards_by_category(category_id):
    session = SessionLocal()
    keyboard = InlineKeyboardMarkup()
    products = get_all_products(session)
    for product in products:
        if product.category_id == category_id:
            keyboard.add(InlineKeyboardButton(product.name, callback_data=str(product.id)))

    session.close()
    return keyboard


def product_keyboards_by_id(product_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🛒 Savatchaga qo\'shish', callback_data=f'add_to_cart_{product_id}'))
    keyboard.add(InlineKeyboardButton('🔙 Orqaga', callback_data='back'))
    return keyboard