from aiogram.dispatcher.filters.state import State, StatesGroup

class AddProduct(StatesGroup):
    name = State()
    price = State()
    description = State()
    category_id = State()
    image = State()
