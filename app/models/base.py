from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime

from app.core.db import Base


class BaseDB(Base):
    """Абстрактная модель БД."""
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)