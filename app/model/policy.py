from .. import db

class Policy(db.Model):
    """Policy model for storing policy details."""
    __tablename__ = 'policies'

    # Unique identifier for each policy
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # The text of the policy, cannot be null
    text = db.Column(db.Text, nullable=False)
    # The ID of the user who created the policy
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship to associate policies with their creators
    creator = db.relationship('User', backref=db.backref('policies', lazy='dynamic'))

    def __repr__(self):
        """String representation of the policy object."""
        return f"<Policy '{self.id}'>"

    def get_policies_by_user(user_id):
        """Fetches all policies created by the user with the given ID."""
        return Policy.query.filter_by(creator_id=user_id).all()

    def to_dict(self):
        """Метод для конвертации модели в словарь."""
        return {
            'id': self.id,
            'text': self.text,
            'creator_id': self.creator_id
        }