from marshmallow import Schema, fields, validate
from ..model.policy import Policy
from ..model.user import User

class PolicyDto(Schema):
    # - `dump_only`: Поле доступно только для вывода (сериализации), но не для ввода.
    #   Это полезно, когда поле генерируется системой, например, `id`, или когда оно не должно быть изменено пользователем.
    #   Пример: `id = fields.Int(dump_only=True)` - поле только для вывода.

    # - `load_only`: Поле доступно только для ввода (десериализации), но не для вывода.
    #   Это полезно для таких полей, как `password`, которые должны быть переданы при создании или изменении объекта,
    #   но не должны возвращаться в ответах API.
    #   Пример: `password = fields.Str(load_only=True)` - поле только для ввода.

    # - `required`: Указывает, что поле обязательно должно присутствовать в данных, передаваемых через API.
    #   Если этого поля нет в запросе, будет вызвана ошибка валидации.
    #   Пример: `username = fields.Str(required=True)` - поле обязательно для ввода.

    # - `validate`: Позволяет задать условия для валидации данных в поле.
    #   Например, можно задать минимальную и максимальную длину строки, проверить, что поле соответствует формату email и т.д.
    #   Пример: `email = fields.Str(validate=validate.Email())` - валидация на корректный формат email.

    # - `default`: Определяет значение по умолчанию для поля, если оно не указано в данных ввода.
    #   Пример: `role = fields.Str(default='user')` - если поле `role` не указано, по умолчанию будет использоваться значение `'user'`.

    # - `missing`: Устанавливает значение, которое будет использоваться, если поле отсутствует в данных ввода.
    #   В отличие от `default`, `missing` применяется только в процессе десериализации.
    #   Пример: `role = fields.Str(missing='user')` - если поле не указано, будет использовано значение `'user'`.

    # - `allow_none`: Указывает, что поле может быть `None` (пустым).
    #   Это полезно, если поле может быть необязательным, но разрешено его отсутствие.
    #   Пример: `description = fields.Str(allow_none=True)` - поле может быть `None`, если не передано.

    """Schema for serializing and deserializing Policy data."""
    id = fields.Int(dump_only=True)  # только для вывода
    text = fields.Str(required=True, validate=validate.Length(min=1), description="Content of the policy")
    creator_id = fields.Int(required=True, description="ID of the policy creator")

    class Meta:
        # Определение полей для сериализации
        fields = ('id', 'text', 'creator_id')

    @classmethod
    def from_policy(cls, policy):
        """Метод для создания DTO из модели Policy."""
        return cls().dump(policy)

    @classmethod
    def to_policy(cls, data):
        """Метод для создания модели Policy из DTO."""
        return Policy(**data)

class UserDto(Schema):
    """Schema for serializing and deserializing User data."""
    id = fields.Int(dump_only=True)  # поле только для вывода
    username = fields.Str(required=True, validate=validate.Length(min=1, max=80), description="Username for the user")
    email = fields.Str(validate=validate.Email(), description="User's email address")
    password = fields.Str(load_only=True, required=True, description="Password for the user")  # поле только для ввода

    class Meta:
        # Определение полей для сериализации
        fields = ('id', 'username', 'email', 'password', 'public_id')

    @classmethod
    def from_user(cls, user):
        """Метод для создания DTO из модели User."""
        return cls().dump(user)

    @classmethod
    def to_user(cls, data):
        """Метод для создания модели User из DTO."""
        return User(**data)