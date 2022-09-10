from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDB, AllDonationDB
)
from app.api.validators import invested_rail
from app.core.user import current_superuser, current_user
from app.models import User

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(
        obj_in=donation,
        session=session,
        user=user
    )
    await invested_rail(session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[AllDonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователя, получение всех пожертвований."""
    all_donations = await donation_crud.get_all(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получает список всех пожертвований текущего пользователя."""
    user_donations = await donation_crud.get_by_user(
        user=user, session=session
    )
    return user_donations