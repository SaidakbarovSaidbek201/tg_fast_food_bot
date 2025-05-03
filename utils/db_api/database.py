from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from .models import Base

engine = create_engine("postgresql://postgres:postgres@localhost/fastfoods_db")

SessionLocal = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)
