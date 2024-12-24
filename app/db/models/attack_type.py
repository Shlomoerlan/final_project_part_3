from sqlalchemy import Column, Integer, String
from app.db.models import Base


class AttackType(Base):
    __tablename__ = 'attack_types'
    attacktype_id = Column(Integer, primary_key=True, autoincrement=True)
    attacktype_name = Column(String(255), unique=True, nullable=False)