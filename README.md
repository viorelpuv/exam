# Tkinter + MySQL Users App

Приложение на Python с использованием Tkinter и MySQL для управления пользователями: регистрация, вход, просмотр, сортировка, фильтрация, поиск, пагинация.

## Установка

1. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
2. Создайте базу данных и таблицы с помощью скрипта из `migrations/init_db.sql`.
3. Запустите приложение:
   ```
   python main.py
   ```

## Структура проекта

- `models/` — работа с БД, бизнес-логика
- `controllers/` — обработка событий, связь между view и model
- `views/` — Tkinter-интерфейсы
- `utils/` — вспомогательные функции
- `migrations/` — SQL-скрипты для создания таблиц
- `main.py` — точка входа

## Функционал
- Регистрация и вход пользователей
- Просмотр списка пользователей
- Сортировка, фильтрация, поиск
- Пагинация

---

## Примеры функций (полный код)

### Фильтрация
```python
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

# Вызов:
users, total = UserModel.get_users(filter_by='email', filter_value='example@mail.com')
```

### Сортировка
```python
# Используйте параметры sort_by и sort_dir:
users, total = UserModel.get_users(sort_by='username', sort_dir='desc')
```

### Поиск
```python
# Используйте параметр search:
users, total = UserModel.get_users(search='alex')
```

### Вход
```python
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

# Вызов:
user = UserModel.authenticate('alex', 'password123')
if user:
    print('Вход успешен!')
else:
    print('Ошибка входа!')
```

### Регистрация
```python
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

# Вызов:
ok, err = UserModel.create_user('alex', 'alex@mail.com', 'password123')
if ok:
    print('Пользователь зарегистрирован!')
else:
    print(f'Ошибка: {err}')
```

### Пагинация
```python
# Используйте параметры page и per_page:
users, total = UserModel.get_users(page=2, per_page=5)
# users — пользователи со 2-й страницы, по 5 на страницу
```

--- 