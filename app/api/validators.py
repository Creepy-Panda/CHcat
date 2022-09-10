from typing import Union
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import CharityProjectUpdate
from app.models import CharityProject, Donation


async def check_name_duplicate(
    charity_name: str,
    session: AsyncSession
) -> None:
    charity_name = await charity_project_crud.get_charity_name(charity_name, session)
    if charity_name is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    charity_id: int,
    session: AsyncSession
) -> CharityProject:
    charity = await charity_project_crud.get(charity_id, session)
    if charity is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity


async def check_charity_project_before_update(
    charity_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    """Проверяем на наличие закрытых инвестиций
       и что сумма не меньше или равна инвестиций
    """
    charity = await check_charity_project_exists(
        charity_id, session
    )
    if charity.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    if (obj_in.full_amount and
            obj_in.full_amount < charity.invested_amount):
        raise HTTPException(
            status_code=422,
            detail='Нельзя внести сумму меньше инвестированной!'
        )
    return charity


async def check_charity_project_before_delete(
    charity_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверяем на наличие инвистиций перед удалением."""
    charity = await check_charity_project_exists(
        charity_id, session
    )
    if charity.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity


def close_project_invest(
    obj: Union[CharityProject, Donation]
) -> None:
    """Закрытие проекта на инвестиции."""
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def invested_rail(
    session: AsyncSession
) -> None:
    """Инвестиционные рельсы."""
    donations = await donation_crud.get_unusable_donations(session)
    open_invest = await charity_project_crud.get_open_invest(session)
    if not donations and not open_invest:
        return
    for donation in donations:
        for project in open_invest:
            to_invest = project.full_amount - project.invested_amount
            to_donate = donation.full_amount - donation.invested_amount
            leftover = to_invest - to_donate
            if leftover == 0:
                close_project_invest(donation)
                close_project_invest(project)
            if leftover < 0:
                donation.invested_amount += abs(leftover)
                close_project_invest(project)
            if leftover > 0:
                project.invested_amount += to_donate
                close_project_invest(donation)
    await session.commit()
