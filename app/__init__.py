from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import settings
from app.controller.policy_controller import router as policy_router
from app.controller.user_controller import router as user_router
from app.storage.user_storage import UserStorage
from app.service.user_service import UserService
from app.db import init_db


# Создаем приложение FastAPI
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )

    # Подключение маршрутов
    app.include_router(policy_router, prefix="")
    app.include_router(user_router, prefix="")

    # События приложения
    @app.on_event("startup")
    async def startup():
        # Инициализация базы данных
        await init_db()

    @app.on_event("shutdown")
    async def shutdown():
        # Здесь можно добавить логику для завершения работы (например, закрытие подключений)
        pass

    # Обработка глобальных ошибок
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        # Логирование исключений можно добавить, например, в систему мониторинга
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "details": str(exc)}
        )

    return app


# Экспортируем приложение для использования в run.py
app = create_app()
