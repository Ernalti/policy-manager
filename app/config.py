import os
from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    """Конфигурация приложения."""

    # Основные параметры
    APP_NAME: str = "Policy Manager"
    VERSION: str = "1.0"
    DEBUG: bool = True

    # Настройки базы данных
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db" # SQLite по умолчанию, можно заменить на PostgreSQL/MySQL

    # Секретный ключ для токенов или других операций
    SECRET_KEY: str = "super-secret-key"

    # Настройки для разработки и продакшена
    ENV: str = "development"
    RELOAD: bool = True

    class Config:
        env_file = ".env"  # Загружаем переменные из файла .env


# Создаем объект настроек, который можно использовать в приложении
settings = Settings()