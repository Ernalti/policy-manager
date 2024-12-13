from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.dto import UserDto
from app.service.user_service import UserService
from app.storage.user_storage import UserStorage
from app.db import get_db

router = APIRouter()



@router.post("/users", response_model=UserDto, status_code=201)
async def create_user(data: UserDto, db=Depends(get_db)):
    """Создать нового пользователя"""
    user_service = UserService(db)
    user = await user_service.create_user(data.username, data.email, data.password)
    return UserDto.from_orm(user)

@router.get("/users/{user_id}", response_model=UserDto)
async def get_user(user_id: int, db=Depends(get_db)):
    """Получить информацию о пользователе по ID"""
    user_service = UserService(db)
    user =await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDto.from_orm(user)

@router.get("/users", response_model=list[UserDto])
async def get_users(db=Depends(get_db)):
    """Получить список пользователей"""
    user_service = UserService(db)
    users = await user_service.get_users()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    # Явное преобразование
    return [UserDto.from_orm(user) for user in users]

@router.post("/users/authenticate", response_model=bool)
async def authenticate_user(username: str, password: str, db=Depends(get_db)):
    """Аутентификация пользователя"""
    user_service = UserService(db)
    is_authenticated =await user_service.authenticate_user(username, password)
    if not is_authenticated:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return is_authenticated