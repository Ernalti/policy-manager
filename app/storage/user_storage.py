from flask import session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.user import User
from sqlalchemy.orm import sessionmaker
from app.db import SessionLocal

class UserStorage:
    """Storage class for user-related database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: User) -> User:
        """Add a new user to the database."""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by their ID."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> User | None:
        """Retrieve a user by their username."""
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def delete_user(self, user_id: int) -> None:
        """Delete a user by their ID."""
        user = await self.get_user_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()

    async def get_users(self) -> list[User] | None:
        result = await self.session.execute((select(User)))
        return result