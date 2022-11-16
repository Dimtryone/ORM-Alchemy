import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_for_sqlalchemy import create_tables, Publisher, Book, Shop, Stock, Sale
from datetime import datetime


username = "postgres"
password_BD = "Zrhfcfdxbr"
name_BD = "Learning_ORM"

DSN = f"postgresql://{username}:{password_BD}@localhost:5432/{name_BD}"
engine = sqlalchemy.create_engine(DSN, echo=True, future=True)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher_1 = Publisher(publisher_name = 'Михаил Афанасьевич Булгаков')
publisher_2 = Publisher(publisher_name = 'Фет Афанасий Афанасьевич')
publisher_3 = Publisher(publisher_name = 'Толстой Лев Николаевич')
session.add_all([publisher_1, publisher_2, publisher_3])
session.commit()

book_1 = Book(title = 'Мастер и Маргарита', publisher_id = session.query(Publisher.id).filter(Publisher.publisher_name == 'Михаил Афанасьевич Булгаков'))
book_2 = Book(title = 'Собачье сердце', publisher_id = session.query(Publisher.id).filter(Publisher.publisher_name == 'Михаил Афанасьевич Булгаков'))
book_3 = Book(title = 'Соловей и Роза', publisher_id = session.query(Publisher.id).filter(Publisher.publisher_name == 'Фет Афанасий Афанасьевич'))
book_4 = Book(title = 'Биография Фета', publisher_id = session.query(Publisher.id).filter(Publisher.publisher_name == 'Фет Афанасий Афанасьевич'))
book_5 = Book(title = 'Война и мир', publisher_id = session.query(Publisher.id).filter(Publisher.publisher_name == 'Толстой Лев Николаевич'))
book_6 = Book(title = 'Анна Каренина', publisher_id = session.query(Publisher.id).filter(Publisher.publisher_name == 'Толстой Лев Николаевич'))

session.add_all([book_1, book_2, book_3, book_4, book_5, book_6])
session.commit()

shop_1 = Shop(shop_name = 'Книжный №1')
shop_2 = Shop(shop_name = 'Книжный №2')
session.add(shop_1)
session.add(shop_2)
session.commit()

st_1 = Stock(id_book = session.query(Book.id).filter(Book.title == 'Мастер и Маргарита'),
             id_shop = session.query(Shop.id).filter(Shop.shop_name == 'Книжный №1'),
             count = 10)
st_2 = Stock(id_book = session.query(Book.id).filter(Book.title == 'Анна Каренина'),
             id_shop = session.query(Shop.id).filter(Shop.shop_name == 'Книжный №1'),
             count = 8)
st_3 = Stock(id_book = session.query(Book.id).filter(Book.title == 'Война и мир'),
             id_shop = session.query(Shop.id).filter(Shop.shop_name == 'Книжный №2'),
             count = 5)

session.add_all([st_1, st_2, st_3])
session.commit()

# print('<<<<<<<>>>>>>>>>>>>>>>>>')
# print('!!!!!!!!!!!!!!!!!!')
#
# for c in session.query(Stock).join(Book.stock).filter(Book.title == 'Война и мир').all():
#     print(c)

date_1 = datetime.now()
date_2 = 2022-11-14

sale_1 = Sale(price = 359.60, count = 2, date_sale = date_1,
              id_stock = session.query(Stock.id).join(Book.stock).filter(Book.title == 'Война и мир'))
sale_2 = Sale(price = 483.40, count = 1, date_sale = date_1,
              id_stock = session.query(Stock.id).join(Book.stock).filter(Book.title == 'Мастер и Маргарита'))

session.add_all([sale_1, sale_2])
session.commit()

search_name_pub = input()

for publisher in session.query(Publisher).filter(Publisher.publisher_name == search_name_pub):
    print(publisher)

#subq = session.query(Publisher).join(Book.publisher).join(Stock.book).join(Sale.stock).filter(Publisher.publisher_name == search_name_pub).subquery()

for shop in session.query(Shop.shop_name).join(Stock).join(Sale).join(Book).join(Publisher).filter(Publisher.publisher_name == search_name_pub).all():
# Как правильно выполнить подзапрос?
    print(shop)

session.close()

