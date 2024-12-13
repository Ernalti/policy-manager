from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from fastapi import Depends
from app.model.user import User  # Ваши модели
from sqlalchemy.future import select
from app.storage.user_storage import UserStorage

class UserService:
    """Service for handling user-related operations."""

    def __init__(self, db):
        self.user_storage = UserStorage(db)

    async def create_user(self, username: str, email: str, password: str) -> User:
        """Create a new user and save to the database."""
        user = User(username=username, email=email)
        user.password = password  # This will hash the password
        return await self.user_storage.add_user(user)

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by their ID."""
        return await self.user_storage.get_user_by_id(user_id)

    async def get_users(self) -> list[User]:
        """Retrieve all users."""

        result = await self.user_storage.get_users()
        print(result)
        return result

    async def authenticate_user(self, username: str, password: str) -> bool:
        """Check if the provided username and password match."""
        user = await self.user_storage.get_user_by_username(username)
        if user and user.check_password(password):
            return True
        return False
