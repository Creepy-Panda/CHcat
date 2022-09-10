from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.api.validators import (
    check_charity_project_before_delete, check_name_duplicate,
    check_charity_project_before_update, invested_rail
)
from app.core.user import current_superuser

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity(
    session: AsyncSession = Depends(get_async_session)
):
    all_charity = await charity_project_crud.get_all(session)
    return all_charity


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity(
    charity: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity.name, session)
    new_charity = await charity_project_crud.create(charity, session)
    await invested_rail(session=session)
    await session.refresh(new_charity)
    return new_charity


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity = await check_charity_project_before_update(charity_id=project_id, obj_in=obj_in, session=session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    charity = await charity_project_crud.update(charity, obj_in, session)
    await invested_rail(session)
    await session.refresh(charity)
    return charity


@router.delete(
    '/{charity_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity(
    charity_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity = await check_charity_project_before_delete(charity_id, session)
    charity = await charity_project_crud.remove(charity, session)
    return charity
