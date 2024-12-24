from sqlalchemy import Column, Integer, String
from app.db.models import Base


class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255), unique=True, nullable=False)