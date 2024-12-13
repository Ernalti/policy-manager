from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from app.model.policy import Policy
from app.model.user import User

class PolicyDto(BaseModel):
    """DTO для сериализации и десериализации данных о политике."""
    id: Optional[int] = Field(None, alias="policy_id")  # только для вывода
    text: str = Field(..., min_length=1, description="Содержание политики")
    creator_id: int = Field(..., description="ID создателя политики")

    class Config:
        # Переименование полей
        orm_mode = True
        from_attributes = True
        allow_population_by_field_name = True

    @classmethod
    def from_policy(cls, policy):
        """Метод для создания DTO из модели Policy."""
        return cls.from_orm(policy)

    @classmethod
    def to_policy(cls, data):
        """Метод для создания модели Policy из DTO."""
        return Policy(**data)

class UserDto(BaseModel):
    """DTO для сериализации и десериализации данных о пользователе."""
    id: Optional[int] = Field(None, alias="user_id")  # только для вывода
    username: str = Field(..., min_length=1, max_length=80, description="Имя пользователя")
    email: Optional[EmailStr] = Field(None, description="Электронная почта пользователя")
    password: Optional[str] = Field(None, min_length=6, description="Пароль пользователя")  # Make it optional

    class Config:
        # Переименование полей для работы с ORM
        orm_mode = True
        allow_population_by_field_name = True
        from_attributes = True

    @classmethod
    def from_user(cls, user: User) -> 'UserDto':
        """Метод для создания DTO из модели User."""
        return cls.from_orm(user)

    @classmethod
    def to_user(cls, data: dict) -> User:
        """Метод для создания модели User из DTO."""
        return User(**data)