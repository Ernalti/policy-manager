from .. import db
from flask_bcrypt import generate_password_hash, check_password_hash
from app.db import Base


class User(db.Base):
    """Модель пользователя для хранения данных о пользователе."""
    __tablename__ = 'users'

    # Уникальный идентификатор пользователя
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Имя пользователя, должно быть уникальным и не может быть пустым
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Электронная почта пользователя (не обязательная)
    email = db.Column(db.String(255), unique=True, nullable=True)
    # Хэш пароля, который хранится безопасно
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        """Пароль является только для записи."""
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        """Хеширует пароль и сохраняет его безопасно."""
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Сравнивает введённый пароль с сохранённым хэшем."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Строковое представление объекта пользователя."""
        return f"<User '{self.username}'>"

    def to_dict(self):
        """Метод для конвертации модели в словарь."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

    @classmethod
    def create_user(cls, username, password, email=None):
        """Метод для создания нового пользователя."""
        new_user = cls(username=username, email=email)
        new_user.password = password  # Автоматически хешируется
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_user_by_username(cls, username):
        """Метод для получения пользователя по имени пользователя."""

