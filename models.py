import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def register(email, password, name, birthday):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return False
        hashed_password = generate_password_hash(password)
        default_picture_path = 'static/defaultpfp.png'
        cursor.execute('INSERT INTO users (email, password, name, birthday, picture) VALUES (?, ?, ?, ?, ?)', 
                       (email, hashed_password, name, birthday, default_picture_path))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def login(email, password):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            return User(user[0], user[1], user[2], user[3], user[4], user[5])
        return None

    @staticmethod
    def update_profile(user_id, email, password, picture, name, birthday):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        if password:
            hashed_password = generate_password_hash(password)
            cursor.execute('UPDATE users SET email = ?, password = ?, name = ?, birthday = ? WHERE id = ?', 
                           (email, hashed_password, name, birthday, user_id))
        else:
            cursor.execute('UPDATE users SET email = ?, name = ?, birthday = ? WHERE id = ?', 
                           (email, name, birthday, user_id))
        if picture:
            picture_path = f'static/user_{user_id}_profile.png'
            with open(picture_path, 'wb') as f:
                f.write(picture)
            cursor.execute('UPDATE users SET picture = ? WHERE id = ?', 
                           (picture_path, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_picture(user_id):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT picture FROM users WHERE id = ?', (user_id,))
        picture = cursor.fetchone()
        conn.close()
        return picture[0] if picture else None

    def __init__(self, id, email, password, name, birthday, picture=None):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.birthday = birthday
        self.picture = picture

class Sensor:
    @staticmethod
    def get_sensors_by_user(user_id):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sensores WHERE usuario_id = ?', (user_id,))
        sensors = cursor.fetchall()
        conn.close()
        return sensors

    @staticmethod
    def update_status(sensor_id, status):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE sensores SET status = ? WHERE id = ?', (status, sensor_id))
        conn.commit()
        conn.close()

    @staticmethod
    def add_sensor(nome, user_id):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sensores (nome, usuario_id, status) VALUES (?, ?, ?)', 
                       (nome, user_id, 'inactive'))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_sensor(sensor_id):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sensores WHERE id = ?', (sensor_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_sensor_data(sensor_id):
        conn = sqlite3.connect('lff_login_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM historico_fumaca WHERE sensor_id = ?', (sensor_id,))
        data = cursor.fetchall()
        conn.close()
        return data
