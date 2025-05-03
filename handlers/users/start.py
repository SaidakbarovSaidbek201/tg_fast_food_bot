from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from  keyboards.default.start_kb import main_menu_kb, main_admin_kb, menu_keyboards, product_keyboards_by_category, product_keyboards_by_id
from loader import dp
from data.config import ADMINS
from utils.db_api.commands import add_category, add_product, get_all_categories, get_all_products,get_category_id, get_product_by_id
import logging
from aiogram.dispatcher import FSMContext
from utils.db_api.database import SessionLocal  
from utils.db_api.commands import add_category
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup  
from utils.db_api.state import AddProduct


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.from_user.id in ADMINS:
        try:
                await message.bot.send_message(chat_id=message.from_user.id, text=f"Salom, {message.from_user.full_name}!", reply_markup=main_admin_kb)
                return

        except Exception as err:
            logging.exception(err)
    else:
        await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=main_menu_kb)


@dp.message_handler(text="📊 Category qo'shish")
async def add_category_handler(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, kategoriya nomini kiriting:")
    await state.set_state("add_category")

@dp.message_handler(state="add_category")
async def process_add_category(message: types.Message, state: FSMContext):
    category_name = message.text
    session = SessionLocal()  # ✅ create session
    try:
        add_category(session, category_name)
        await message.answer(f"Kategoriya qo'shildi: {category_name}")
    finally:
        session.close()  # ✅ always close the session
    try:
        await state.finish()
    except KeyError:
        pass



@dp.message_handler(text="🗂️ Kategoriyalar")
async def process_get_categories(message: types.Message, state: FSMContext):
    await message.answer(f"Kategoriyalar:", reply_markup=menu_keyboards())
    try:
        await state.finish()
    except KeyError:
        pass




@dp.message_handler(text="🛠️ Mahsulotlar")
async def process_get_products(message: types.Message, state: FSMContext):
    session = SessionLocal()
    try:
        products = get_all_products(session)
        for p in products:
            text = f"📦 {p.name}\nNarxi: {p.price}\nTavsif: {p.description}"
            await message.answer(text)
    finally:
        session.close()
    try:
        await state.finish()
    except KeyError:
        pass


@dp.message_handler(Text(equals="📊 Mahsulot qo'shish"))
async def start_add_product(message: types.Message):
    session = SessionLocal()
    try:
        keyboard = menu_keyboards()
        await message.answer("📂 Kategoriya ID sini tanlang yoki kiriting:", reply_markup=keyboard)
    finally:
        session.close()
    await AddProduct.category_id.set()

@dp.message_handler(state=AddProduct.category_id)
async def product_category_handler(message: types.Message, state: FSMContext):
    session = SessionLocal()
    try:
        category_id = get_category_id(session, message.text)
        await state.update_data(category_id=category_id)
        await message.answer("📥 Mahsulot nomini kiriting:" )
    finally:
        session.close()
    await AddProduct.name.set()

@dp.message_handler(state=AddProduct.name)
async def product_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Narxini kiriting:")
    await AddProduct.price.set()    

@dp.message_handler(state=AddProduct.price)
async def product_price_handler(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
    except ValueError:
        await message.answer("❗ Narx noto‘g‘ri. Raqam yozing.")
        return
    await message.answer("📝 Mahsulot tavsifini yozing:")
    await AddProduct.description.set()

@dp.message_handler(state=AddProduct.description)
async def product_description_handler(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("🖼 Rasm yuboring:")
    await AddProduct.image.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=AddProduct.image)
async def product_image_handler(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    data = await state.get_data()

    session = SessionLocal()
    try:
        add_product(
            session=session,
            name=data['name'],
            price=data['price'],
            description=data['description'],
            category_id=data['category_id'],
            image_file_id=file_id
        )
        await message.answer("✅ Mahsulot muvaffaqiyatli qo‘shildi!", reply_markup=main_admin_kb)
    finally:
        session.close()

    try:
        await state.finish()
    except KeyError:
        pass




@dp.message_handler(text="🍕 Menyu")
async def process_get_categories(message: types.Message, state: FSMContext):
    await message.answer(f"Menu:", reply_markup=menu_keyboards())
    try:
        await state.finish()
    except KeyError:
        pass





@dp.message_handler()
async def category_handler(message: types.Message):
    session = SessionLocal()
    text = message.text
    category_id = get_category_id(session,text)
    session.close()
    await message.answer(text=f"{text}ni ichidagi mahsulotlar", reply_markup=product_keyboards_by_category(category_id))


@dp.callback_query_handler()
async def product_handler(call: types.CallbackQuery):
    if call.data == "back":
        await call.message.answer("Menu:", reply_markup=main_menu_kb)
        return

    product_id = int(call.data)  # если ID передаётся как строка числа
    mahsulot = get_product_by_id(product_id)

    if mahsulot:
        c = f"{mahsulot.name} - narxi: {mahsulot.price} so'm"
        await call.message.answer_photo(
            photo=mahsulot.image_file_id,
            caption=c,
            reply_markup=product_keyboards_by_id(product_id)
        )
    else:
        await call.message.answer("Mahsulot topilmadi.")
