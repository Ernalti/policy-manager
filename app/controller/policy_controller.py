from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from ..utils.dto import PolicyDto
from ..service.policy_service import PolicyService

# Инициализация сервиса
policy_service = PolicyService()

# Создаем Blueprint для маршрутов, если необходимо
policy_bp = Blueprint('policy', __name__)

@policy_bp.route('/policies', methods=['GET'])
def get_policies():
    """Get list of policies"""
    try:
        policies = policy_service.get_all_policies()
        return jsonify(policies)
    except Exception as e:
        return {'message': str(e)}, 500

@policy_bp.route('/policies', methods=['POST'])
def create_policy():
    """Create a new policy"""
    data = request.get_json()
    try:
        # Валидируем входные данные через PolicyDto
        policy_data = PolicyDto().load(data)
        policy = policy_service.create_policy(policy_data)
        return {'message': 'Policy created successfully', 'policy': policy}, 201
    except ValidationError as e:
        return {'message': 'Validation failed', 'errors': e.messages}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@policy_bp.route('/policies/<int:id>', methods=['GET'])
def get_policy(id):
    """Get a policy by its ID"""
    try:
        policy = policy_service.get_policy_by_id(id)
        if policy:
            return jsonify(policy)
        else:
            return {'message': 'Policy not found'}, 404
    except Exception as e:
        return {'message': str(e)}, 500

@policy_bp.route('/policies/<int:id>', methods=['PUT'])
def update_policy(id):
    """Update an existing policy"""
    data = request.get_json()
    try:
        policy_data = PolicyDto().load(data)
        updated_policy = policy_service.update_policy(id, policy_data)
        if updated_policy:
            return {'message': 'Policy updated successfully', 'policy': updated_policy}, 200
        else:
            return {'message': 'Policy not found'}, 404
    except ValidationError as e:
        return {'message': 'Validation failed', 'errors': e.messages}, 400
    except Exception as e:
        return {'message': str(e)}, 500

@policy_bp.route('/policies/<int:id>', methods=['DELETE'])
def delete_policy(id):
    """Delete a policy by its ID"""
    try:
        success = policy_service.delete_policy(id)
        if success:
            return {'message': 'Policy deleted successfully'}, 200
        else:
            return {'message': 'Policy not found'}, 404
    except Exception as e:
        return {'message': str(e)}, 500

@policy_bp.route('/policies/<int:policy_id>/validate', methods=['POST'])
def validate_policy_text(policy_id):
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"message": "Text is required"}), 400

    # Валидация текста
    result = PolicyService.validate_policy_text_for_id(policy_id, data['text'])
    if result:
        return jsonify({"message": "Validation successful"}), 200
    else:
        return jsonify({"message": "Text does not match the first letter of the policy text"}), 400