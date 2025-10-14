from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///data.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# ----- Таблица Продукции -----
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    article = Column(String)
    type = Column(String)
    price = Column(Float)

# ----- Таблица Партнёров -----
class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True)
    org_type = Column(String)
    org_name = Column(String)
    director = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    inn = Column(String)
    rating = Column(Integer)

# ----- Таблица Продаж -----
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    product = Column(String)
    quantity = Column(Integer)
    price = Column(Float)

# Создание таблиц
Base.metadata.create_all(engine)
