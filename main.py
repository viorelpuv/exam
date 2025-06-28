from models.db import init_db
from models.user import UserModel
from views.main_view import MainView
from controllers.auth_controller import AuthController
from controllers.data_controller import DataController


def main():
    # Инициализация БД (создание соединения)
    init_db()
    # Запуск главного окна
    MainView().mainloop()

if __name__ == "__main__":
    main() 