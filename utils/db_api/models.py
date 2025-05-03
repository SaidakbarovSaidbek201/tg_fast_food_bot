from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Relationship (optional, helps with querying)
    products = relationship("Product", back_populates="category", cascade="all, delete")

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    image_file_id = Column(Text)
    

    # Relationship
    category = relationship("Category", back_populates="products")



