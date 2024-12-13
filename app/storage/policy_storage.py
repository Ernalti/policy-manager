from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.policy import Policy

class PolicyStorage:
    """Storage class for policy-related database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_policy(self, policy: Policy) -> Policy:
        """Add a new policy to the database."""
        self.session.add(policy)
        await self.session.commit()
        await self.session.refresh(policy)
        return policy

    async def get_policy_by_id(self, policy_id: int) -> Policy | None:
        """Retrieve a policy by its ID."""
        result = await self.session.execute(select(Policy).where(Policy.id == policy_id))
        return result.scalars().first()

    async def get_policies_by_user_id(self, user_id: int) -> list[Policy]:
        """Retrieve all policies created by a specific user."""
        result = await self.session.execute(select(Policy).where(Policy.user_id == user_id))
        return result.scalars().all()

    async def delete_policy(self, policy_id: int) -> None:
        """Delete a policy by its ID."""
        policy = await self.get_policy_by_id(policy_id)
        if policy:
            await self.session.delete(policy)
            await self.session.commit()