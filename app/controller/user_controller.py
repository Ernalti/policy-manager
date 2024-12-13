from fastapi import APIRouter, HTTPException
from app.utils.dto import UserDto
from app.service.user_service import UserService

router = APIRouter()

@router.post("/users", response_model=UserDto, status_code=201)
async def create_user(data: UserDto):
    """Создать нового пользователя"""
    user = UserService.create_user(data.username, data.email, data.password)
    return UserDto.from_orm(user)

@router.get("/users/{user_id}", response_model=UserDto)
async def get_user(user_id: int):
    """Получить информацию о пользователе по ID"""
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDto.from_orm(user)

@router.post("/users/authenticate", response_model=bool)
async def authenticate_user(username: str, password: str):
    """Аутентификация пользователя"""
    is_authenticated = UserService.authenticate_user(username, password)
    if not is_authenticated:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return is_authenticated