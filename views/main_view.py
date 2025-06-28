import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController
from controllers.data_controller import DataController

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Пользователи — Tkinter + MySQL')
        self.geometry('700x500')
        self.auth_controller = AuthController()
        self.data_controller = DataController()
        self.current_user = None
        self.page = 1
        self.per_page = 10
        self.search = None
        self.sort_by = None
        self.sort_dir = 'asc'
        self.filter_by = None
        self.filter_value = None
        self.total = 0
        self._build_login()

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _build_login(self):
        self._clear()
        frame = tk.Frame(self)
        frame.pack(expand=True)
        tk.Label(frame, text='Вход', font=('Arial', 16)).pack(pady=10)
        tk.Label(frame, text='Имя пользователя').pack()
        self.login_username = tk.Entry(frame)
        self.login_username.pack()
        tk.Label(frame, text='Пароль').pack()
        self.login_password = tk.Entry(frame, show='*')
        self.login_password.pack()
        tk.Button(frame, text='Войти', command=self._login).pack(pady=5)
        tk.Button(frame, text='Регистрация', command=self._build_register).pack()

    def _build_register(self):
        self._clear()
        frame = tk.Frame(self)
        frame.pack(expand=True)
        tk.Label(frame, text='Регистрация', font=('Arial', 16)).pack(pady=10)
        tk.Label(frame, text='Имя пользователя').pack()
        self.reg_username = tk.Entry(frame)
        self.reg_username.pack()
        tk.Label(frame, text='Email').pack()
        self.reg_email = tk.Entry(frame)
        self.reg_email.pack()
        tk.Label(frame, text='Пароль').pack()
        self.reg_password = tk.Entry(frame, show='*')
        self.reg_password.pack()
        tk.Button(frame, text='Зарегистрироваться', command=self._do_register).pack(pady=5)
        tk.Button(frame, text='Назад', command=self._build_login).pack()

    def _do_register(self):
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()
        if not username or not email or not password:
            messagebox.showerror('Ошибка', 'Заполните все поля!')
            return
        ok, err = self.auth_controller.register(username, email, password)
        if ok:
            messagebox.showinfo('Успех', 'Регистрация успешна!')
            self._build_login()
        else:
            messagebox.showerror('Ошибка', f'Ошибка регистрации: {err}')

    def _login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        user = self.auth_controller.login(username, password)
        if user:
            self.current_user = user
            self._build_main()
        else:
            messagebox.showerror('Ошибка', 'Неверные данные для входа!')

    def _build_main(self):
        self._clear()
        top = tk.Frame(self)
        top.pack(fill='x', pady=5)
        tk.Label(top, text=f'Пользователь: {self.current_user["username"]}', font=('Arial', 12)).pack(side='left', padx=10)
        tk.Button(top, text='Выйти', command=self._logout).pack(side='right', padx=10)
        # Поиск
        search_frame = tk.Frame(self)
        search_frame.pack(fill='x', pady=5)
        tk.Label(search_frame, text='Поиск:').pack(side='left')
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side='left')
        tk.Button(search_frame, text='Найти', command=self._search).pack(side='left', padx=5)
        tk.Button(search_frame, text='Сбросить', command=self._reset_search).pack(side='left')
        # Таблица
        columns = ('id', 'username', 'email', 'created_at')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort(c))
            self.tree.column(col, width=150)
        self.tree.pack(expand=True, fill='both', pady=10)
        # Пагинация
        pag_frame = tk.Frame(self)
        pag_frame.pack()
        self.prev_btn = tk.Button(pag_frame, text='<<', command=self._prev_page)
        self.prev_btn.pack(side='left', padx=5)
        self.page_label = tk.Label(pag_frame, text='')
        self.page_label.pack(side='left', padx=5)
        self.next_btn = tk.Button(pag_frame, text='>>', command=self._next_page)
        self.next_btn.pack(side='left', padx=5)
        self._load_users()

    def _logout(self):
        self.current_user = None
        self.page = 1
        self._build_login()

    def _search(self):
        self.search = self.search_entry.get().strip() or None
        self.page = 1
        self._load_users()

    def _reset_search(self):
        self.search = None
        self.search_entry.delete(0, tk.END)
        self.page = 1
        self._load_users()

    def _sort(self, col):
        if self.sort_by == col:
            self.sort_dir = 'desc' if self.sort_dir == 'asc' else 'asc'
        else:
            self.sort_by = col
            self.sort_dir = 'asc'
        self.page = 1
        self._load_users()

    def _prev_page(self):
        if self.page > 1:
            self.page -= 1
            self._load_users()

    def _next_page(self):
        if self.page * self.per_page < self.total:
            self.page += 1
            self._load_users()

    def _load_users(self):
        self.tree.delete(*self.tree.get_children())
        users, total = self.data_controller.get_users(
            page=self.page,
            per_page=self.per_page,
            search=self.search,
            sort_by=self.sort_by,
            sort_dir=self.sort_dir
        )
        self.total = total
        for user in users:
            self.tree.insert('', 'end', values=(user['id'], user['username'], user['email'], user['created_at']))
        self.page_label.config(text=f'Страница {self.page} из {max(1, (self.total + self.per_page - 1) // self.per_page)}')
        self.prev_btn.config(state='normal' if self.page > 1 else 'disabled')
        self.next_btn.config(state='normal' if self.page * self.per_page < self.total else 'disabled') 