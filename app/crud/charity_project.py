from datetime import datetime
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_name(
        self,
        charity_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_charity_name = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_name
            )
        )
        return db_charity_name.scalars().first()

    async def get_open_invest(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        charity = await session.execute(select(CharityProject).where(
            CharityProject.fully_invested == false()).order_by(CharityProject.create_date)
        )
        return charity.scalars().all()

    async def get_projects_by_completion_rate(
        self,
        create_date: datetime,
        close_date: datetime,
        session: AsyncSession,
    ) -> dict():
        charity = await session.execute(
            select(CharityProject).where(
                CharityProject.create_date >= create_date,
                CharityProject.close_date <= close_date).order_by((func.julianday(CharityProject.close_date) - func.julianday(CharityProject.create_date))))
        charity = charity.scalars().all()
        return charity


charity_project_crud = CRUDCharityProject(CharityProject)