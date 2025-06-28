from models.user import UserModel

class AuthController:
    def register(self, username, email, password):
        return UserModel.create_user(username, email, password)

    def login(self, username, password):
        return UserModel.authenticate(username, password) 