from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.base import BaseDB


class Donation(BaseDB):
    """Модель для пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)