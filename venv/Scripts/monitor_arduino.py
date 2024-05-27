import serial
import sqlite3
import time
import os

# Substitua 'COMX' pela porta correta identificada no Gerenciador de Dispositivos
ser = serial.Serial('COM1', 9600)

# Caminho para o banco de dados
db_path = 'C:\\Users\\chrda\\Documents\\facu\\incendioteste\\lff_login_system\\lff_login_system.db'

# Verifique se o arquivo do banco de dados existe
if not os.path.exists(db_path):
    print(f"Erro: O banco de dados {db_path} não foi encontrado.")
    exit(1)

# Conecte ao banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verifique se a tabela 'sensores' existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sensores';")
if cursor.fetchone() is None:
    print("Erro: A tabela 'sensores' não existe no banco de dados.")
    exit(1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if "Smoke detected" in line:
            cursor.execute("INSERT INTO sensores (timestamp, data) VALUES (?, ?)", (time.strftime('%Y-%m-%d %H:%M:%S'), line))
            conn.commit()
            print("Smoke detected and logged.")