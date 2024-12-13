from app.model.user import User
from app import db
from app.storage.user_storage import UserStorage
class UserService:
    """Service for handling user-related operations."""

    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        """Create a new user and save to the database."""
        user = User(username=username, email=email)
        user.password = password  # This will hash the password
        UserStorage.add_user(user)
        return user

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Retrieve a user by their ID."""
        return User.query.get(user_id)

    @staticmethod
    def authenticate_user(username: str, password: str) -> bool:
        """Check if the provided username and password match."""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return True
        return False