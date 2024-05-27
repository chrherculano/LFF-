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

    # Criar tabela de sensores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES users(id)
    )
    ''')

    # Criar tabela de histórico de detecção de fumaça
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS historico_fumaca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (sensor_id) REFERENCES sensores(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()