import bcrypt
from models.db import get_connection

class UserModel:
    @staticmethod
    def create_user(username, email, password):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            conn.commit()
            return True, None
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def authenticate(username, password):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            return user
        return None

    @staticmethod
    def get_users(page=1, per_page=10, search=None, sort_by=None, sort_dir='asc', filter_by=None, filter_value=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users"
        params = []
        where = []
        if search:
            where.append("(username LIKE %s OR email LIKE %s)")
            params.extend([f"%{search}%", f"%{search}%"])
        if filter_by and filter_value:
            where.append(f"{filter_by} = %s")
            params.append(filter_value)
        if where:
            query += " WHERE " + " AND ".join(where)
        if sort_by:
            query += f" ORDER BY {sort_by} {sort_dir.upper()}"
        else:
            query += " ORDER BY id DESC"
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, (page-1)*per_page])
        cursor.execute(query, params)
        users = cursor.fetchall()
        # Получить общее количество
        cursor.execute("SELECT COUNT(*) as total FROM users" + (" WHERE " + " AND ".join(where) if where else ""), params[:-2])
        total = cursor.fetchone()['total']
        cursor.close()
        conn.close()
        return users, total 