from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.crud.base import CRUDBase
from app.models import Donation, User


class DonationCRUD(CRUDBase):

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

    async def get_unusable_donations(
        self,
        session: AsyncSession
    ):
        charity = await session.execute(select(Donation).where(
            Donation.fully_invested == false())
        )

        return charity.scalars().all()


donation_crud = DonationCRUD(Donation)