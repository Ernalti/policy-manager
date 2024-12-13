from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

Base = declarative_base()

# Создание движка базы данных
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Создание фабрики сессий
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Инициализация базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция для получения сессии
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session