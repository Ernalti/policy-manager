from ..model.policy import Policy
from ..utils.dto import  PolicyDto  # Импортируем PolicyDto
from .. import db
from app.storage.policy_storage import PolicyStorage


class PolicyService:

    def get_all_policies(self):
        """Получение всех политик."""
        try:
            policies = Policy.query.all()
            return [PolicyDto.from_policy(policy).dict() for policy in policies]  # Преобразуем в DTO
        except Exception as e:
            raise Exception(f"Error retrieving policies: {str(e)}")

    def get_policy_by_id(self, id):
        """Получение политики по её ID."""
        try:
            policy = Policy.query.get(id)
            if policy:
                return PolicyDto.from_policy(policy).dict()  # Преобразуем в DTO
            return None
        except Exception as e:
            raise Exception(f"Error retrieving policy with id {id}: {str(e)}")

    def create_policy(self, policy_data):
        """Создание новой политики."""
        try:
            # Преобразуем DTO в модель Policy
            policy = PolicyDto.to_policy(policy_data)
            PolicyStorage.add_policy(policy)
            return PolicyDto.from_policy(policy).dict()  # Возвращаем DTO
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating policy: {str(e)}")

    def update_policy(self, id, policy_data):
        """Обновление существующей политики."""
        try:
            policy = Policy.query.get(id)
            if policy:
                for key, value in policy_data.items():
                    setattr(policy, key, value)
                db.session.commit()
                return PolicyDto.from_policy(policy).dict()  # Возвращаем DTO
            return None
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating policy with id {id}: {str(e)}")

    def delete_policy(self, id):
        """Удаление политики по её ID."""
        try:
            policy = Policy.query.get(id)
            if policy:
                db.session.delete(policy)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting policy with id {id}: {str(e)}")

    def validate_policy_text_for_id(self, policy_id, text):
        policy = Policy.query.get(policy_id)
        if not policy:
            return False

        # Проверяем, совпадает ли первый символ текста с первым символом существующей политики
        return text[0].lower() == policy.text[0].lower()
