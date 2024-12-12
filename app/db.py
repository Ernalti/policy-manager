from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Создание движка базы данных
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Создание фабрики сессий
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    """
    Функция для инициализации базы данных.
    Здесь можно выполнять миграции или другие стартовые задачи.
    """
    async with engine.begin() as conn:
        # Если используются Alembic миграции, можно вызвать их здесь
        # await conn.run_sync(Base.metadata.create_all)  # Создание таблиц, если их нет
        print("База данных инициализирована")