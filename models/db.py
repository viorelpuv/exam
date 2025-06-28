import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # измените при необходимости
    'password': 'UM8$7I9o',  # измените при необходимости
    'database': 'exam_app',
    'autocommit': True
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        with open('migrations/init_db.sql', encoding='utf-8') as f:
            sql = f.read()
            for statement in sql.split(';'):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Ошибка инициализации БД: {e}") 