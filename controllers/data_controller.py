from models.user import UserModel

class DataController:
    def get_users(self, page=1, per_page=10, search=None, sort_by=None, sort_dir='asc', filter_by=None, filter_value=None):
        return UserModel.get_users(page, per_page, search, sort_by, sort_dir, filter_by, filter_value) 