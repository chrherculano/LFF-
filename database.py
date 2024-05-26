import sqlite3

def init_db():
    conn = sqlite3.connect('lff_login_system.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    picture BLOB
    )
    ''')
    conn.commit()
    conn.close()
