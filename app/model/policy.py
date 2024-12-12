from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Policy(Base):
    """Policy model for storing policy details."""
    __tablename__ = 'policies'

    # Unique identifier for each policy
    id = Column(Integer, primary_key=True, autoincrement=True)
    # The text of the policy, cannot be null
    text = Column(Text, nullable=False)
    # The ID of the user who created the policy
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship to associate policies with their creators
    creator = relationship('User', back_populates='policies')

    def __repr__(self):
        """String representation of the policy object."""
        return f"<Policy '{self.id}'>"

    @staticmethod
    def get_policies_by_user(session, user_id):
        """Fetches all policies created by the user with the given ID."""
        return session.query(Policy).filter_by(creator_id=user_id).all()

    def to_dict(self):
        """Convert the model to a dictionary."""
        return {
            'id': self.id,
            'text': self.text,
            'creator_id': self.creator_id
        }
