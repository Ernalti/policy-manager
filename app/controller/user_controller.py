from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from .dto.user import UserDto
from .service.user_service import UserService

# Инициализация сервиса
user_service = UserService()

# Создаем Blueprint для маршрутов
user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Получение списка пользователей"""
    try:
        users = user_service.get_all_users()
        return jsonify(users)
    except Exception as e:
        return {'message': str(e)}, 500

@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """Получение пользователя по ID"""
    try:
        user = user_service.get_user_by_id(id)
        if user:
            return jsonify(user)
        else:
            return {'message': 'User not found'}, 404
    except Exception as e:
        return {'message': str(e)}, 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Создание нового пользователя"""
    data = request.get_json()
    try:
        # Валидируем входные данные через UserDto
        user_data = UserDto().load(data)
        user = user_service.create_user(user_data)
        return {'message': 'User created successfully', 'user': user}, 201
    except ValidationError as e:
        return {'message': 'Validation failed', 'errors': e.messages}, 400
    except Exception as e:
        return {'message': str(e)}, 500

@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """Обновление существующего пользователя"""
    data = request.get_json()
    try:
        user_data = UserDto().load(data)
        updated_user = user_service.update_user(id, user_data)
        if updated_user:
            return {'message': 'User updated successfully', 'user': updated_user}, 200
        else:
            return {'message': 'User not found'}, 404
    except ValidationError as e:
        return {'message': 'Validation failed', 'errors': e.messages}, 400
    except Exception as e:
        return {'message': str(e)}, 500

@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Удаление пользователя по ID"""
    try:
        success = user_service.delete_user(id)
        if success:
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404
    except Exception as e:
        return {'message': str(e)}, 500