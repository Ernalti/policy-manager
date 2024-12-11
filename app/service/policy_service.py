from ..model.policy import Policy
from .. import db

class PolicyService:

    def get_all_policies(self):
        """Получение всех политик."""
        try:
            policies = Policy.query.all()
            return [policy.to_dict() for policy in policies]
        except Exception as e:
            raise Exception(f"Error retrieving policies: {str(e)}")

    def get_policy_by_id(self, id):
        """Получение политики по её ID."""
        try:
            policy = Policy.query.get(id)
            if policy:
                return policy.to_dict()
            return None
        except Exception as e:
            raise Exception(f"Error retrieving policy with id {id}: {str(e)}")

    def create_policy(self, policy_data):
        """Создание новой политики."""
        try:
            policy = Policy(**policy_data)
            db.session.add(policy)
            db.session.commit()
            return policy.to_dict()
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
                return policy.to_dict()
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
