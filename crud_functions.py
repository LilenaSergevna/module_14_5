import sqlite3


def initiate_db():
    connection = sqlite3.connect("ProductsDB.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect("ProductsDB.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    all_prod=cursor.fetchall()
    connection.commit()
    connection.close()
    return all_prod

def add_user(username, email,age):
    connection = sqlite3.connect("ProductsDB.db")
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, 1000)',
    (username, email, age))
    connection.commit()

def is_included(username):
    connection = sqlite3.connect("ProductsDB.db")
    cursor = connection.cursor()
    check_user=cursor.execute("SELECT * FROM Users WHERE username=?",(username,))
    if check_user.fetchone() is None:
        return False
    else:
        return True

initiate_db()




