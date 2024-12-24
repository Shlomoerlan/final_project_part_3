from sqlalchemy import Column, Integer, String
from app.db.models import Base

class TargetType(Base):
    __tablename__ = 'target_types'
    targettype_id = Column(Integer, primary_key=True, autoincrement=True)
    targettype_name = Column(String(255), unique=True, nullable=False)
