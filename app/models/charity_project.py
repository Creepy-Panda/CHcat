from sqlalchemy import Column, String, Text

from .base import BaseDB


class CharityProject(BaseDB):
    """Модель проектов пожертвований."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)