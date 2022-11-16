import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import CheckConstraint


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key = True)
    publisher_name = sq.Column(sq.String(length=50), unique=True)

    def __str__(self):
        return f'id - {self.id}, name -{self.publisher_name}'


class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key = True)
    title = sq.Column(sq.String(length = 60), nullable = False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable = False)

    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'id - {self.id}, title_book - {self.title}'


class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key = True)
    shop_name = sq.Column(sq.String(length = 40), nullable = False)

    def __str__(self):
        return f'id - {self.id}, shop - {self.shop_name}'


class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key = True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable = False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable = False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref = "stock")
    shop = relationship(Shop, backref = "stock")


class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key = True)
    price =sq.Column(sq.Numeric, CheckConstraint ("price>0"))
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable = False)
    count = sq.Column(sq.Integer, CheckConstraint ("count>0"))

    stock = relationship(Stock, backref = "stock")

    def __str__(self):
        return f'id - {self.id}, date_sale - {self.date_sale}, count - {self.count}'


def create_tables(engine):
    Base.metadata.drop_all(engine)  #для удаления таблиц
    Base.metadata.create_all(engine) #для создания таблиц


