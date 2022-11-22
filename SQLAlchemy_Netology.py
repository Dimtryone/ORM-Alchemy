import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from models_for_sqlalchemy import create_tables, Publisher, Book, Shop, Stock, Sale
from datetime import datetime
import json

# задание 1 и 2
path = os.getenv('HOMEPATH') + '\\PostgreSQL\\Connect_BD.txt'
print(path)
with open(path, 'r', encoding='utf-8') as file:
    parametrs = list(map(str.strip, file.readlines()))
username = parametrs[0]
password_BD = parametrs[1]
name_BD = parametrs[2]
name_host = parametrs[3]
num_host = parametrs[4]

DSN = f"postgresql://{username}:{password_BD}@{name_host}{num_host}/{name_BD}"
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

date_1 = datetime.now()
date_2 = 2022-11-14
sale_1 = Sale(price = 359.60, count = 2, date_sale = date_1,
              id_stock = session.query(Stock.id).join(Book.stock).filter(Book.title == 'Война и мир'))
sale_2 = Sale(price = 483.40, count = 1, date_sale = date_1,
              id_stock = session.query(Stock.id).join(Book.stock).filter(Book.title == 'Мастер и Маргарита'))

session.add_all([sale_1, sale_2])
session.commit()


def get_publisher(name=None, id=None):
    if name != None:
        for publisher in session.query(Publisher).filter(Publisher.publisher_name == name):
            return(publisher)
    else:
        for publisher in session.query(Publisher).filter(Publisher.id == id):
            return (publisher)


def get_shop(name=None, id=None):
    if name != None:
        for shop in session.query(Shop.shop_name).join(Stock).join(Sale).join(Book).join(Publisher).filter(Publisher.publisher_name == name).all():
            return(shop)
    else:
        for shop in session.query(Shop.shop_name).join(Stock).join(Sale).join(Book).join(Publisher).filter(Publisher.id == id).all():
            return(shop)

search_name_pub = input()
if type(search_name_pub) == str and len(search_name_pub) > 3:
    print(get_publisher(name=search_name_pub))
    print(get_shop(name=search_name_pub))
elif type(search_name_pub) == str and search_name_pub.isdigit():
    search_id = int(search_name_pub)
    print(get_publisher(id=search_id))
    print(get_shop(id=search_id))

session.close()


# задание 3
create_tables(engine)

def set_publisher(pk, name):
    publisher = Publisher(id = pk, publisher_name = name)
    session.add(publisher)
    session.commit()
    return f'publisher has {name} added'

def set_book(pk, name, id_pub):
    book = Book(id = pk, title = name, publisher_id = id_pub)
    session.add(book)
    session.commit()
    return f'Book {name} has added'

def set_shop(pk, name):
    shop = Shop(id = pk, shop_name = name,)
    session.add(shop)
    session.commit()
    return f'Shop {name} has added'

def set_stock(pk, id_shop, id_book, count):
    stock = Stock(id = pk, id_book = id_book, id_shop = id_shop, count = count)
    session.add(stock)
    session.commit()
    return f'Stock has added'

def set_sale(pk, price, date_sale, count, id_stock):
    sale = Sale(id=pk, price = price, count = count, date_sale = date_sale,
                id_stock = id_stock)
    session.add(sale)
    session.commit()
    return f'Sale {pk} has added'


name_file = '\data.json'
path = os.getcwd() + name_file
with open(path) as file:
    data = json.load(file)
    for item in data:
        pk = item['pk']
        if item['model'] == 'publisher':
            name = item['fields']['name']
            print(set_publisher(pk, name))
        if item['model'] == 'book':
            name = item['fields']['title']
            id_pub = item['fields']['id_publisher']
            print(set_book(pk, name, id_pub))
        if item['model'] == 'shop':
            name = item['fields']['name']
            print(set_shop(pk, name))
        if item['model'] == 'stock':
            id_shop = item['fields']['id_shop']
            id_book = item['fields']['id_book']
            count = item['fields']['count']
            print(set_stock(pk, id_shop, id_book, count))
        if item['model'] == 'sale':
            price = item['fields']['price']
            date_sale = item['fields']['date_sale']
            count = item['fields']['count']
            id_stock = item['fields']['id_stock']
            print(set_sale(pk, price, date_sale, count,id_stock))

session.close()

