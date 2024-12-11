from ..model.user import User
from .. import db

class UserService:

    def get_all_users(self):
        """Получение всех пользователей."""
        try:
            users = User.query.all()
            return [user.to_dict() for user in users]  # Метод to_dict должен быть реализован в модели User
        except Exception as e:
            raise Exception(f"Error retrieving users: {str(e)}")

    def get_user_by_id(self, id):
        """Получение пользователя по ID."""
        try:
            user = User.query.get(id)
            if user:
                return user.to_dict()
            return None
        except Exception as e:
            raise Exception(f"Error retrieving user with id {id}: {str(e)}")

    def create_user(self, user_data):
        """Создание нового пользователя."""
        try:
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    def update_user(self, id, user_data):
        """Обновление пользователя."""
        try:
            user = User.query.get(id)
            if user:
                for key, value in user_data.items():
                    setattr(user, key, value)
                db.session.commit()
                return user.to_dict()
            return None
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating user with id {id}: {str(e)}")

    def delete_user(self, id):
        """Удаление пользователя."""
        try:
            user = User.query.get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting user with id {id}: {str(e)}")
