from sqlalchemy import create_engine
from .models import Category, Product, Base
from sqlalchemy.orm import sessionmaker

# PostgreSQL database ulanishi (tokenlarni o'zgartiring)
DATABASE_URL = "postgresql://postgres:postgres@localhost/fastfoods_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# get all categories
def get_all_categories(session):
    return session.query(Category).all()

# add category
def add_category(session, name):
    new_category = Category(name=name)
    session.add(new_category)
    session.commit()
    return new_category

# get all products
def get_all_products(session):
    return session.query(Product).all()

# add product
def add_product(session, name, price, description, category_id, image_file_id):
    new_product = Product(
        name=name,
        price=price,
        description=description,
        category_id=category_id,
        image_file_id=image_file_id
    )
    session.add(new_product)
    session.commit()
    return new_product

# get products by category id
def get_products_by_category(session, category_id):
    return session.query(Product).filter(Product.category_id == category_id).all()


def get_category_id(session, category_name):
    category = session.query(Category).filter(Category.name == category_name).first()
    return category.id if category else None


def get_product_by_id(product_id):
    return session.query(Product).filter(Product.id == product_id).first()



# Namuna ishlatish:
if __name__ == "__main__":
    categories = get_all_categories(session)
    for cat in categories:
        print(f"Kategoriya: {cat.name}")

    products = get_all_products(session)
    for prod in products:
        print(f"Mahsulot: {prod.name}, Narxi: {prod.price}")


