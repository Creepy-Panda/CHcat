from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_update_value, spreadsheets_create
)

router = APIRouter()


@router.get(
    '/',
    response_model=dict(),
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    create_date: datetime,
    close_date: datetime,
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    charity = await charity_project_crud.get_projects_by_completion_rate(
        create_date=create_date, close_date=close_date, session=session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    charity,
                                    wrapper_services)
    return charity