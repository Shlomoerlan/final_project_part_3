from sqlalchemy import Column, Integer, String
from app.db.models import Base


class City(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(255), unique=True, nullable=False)