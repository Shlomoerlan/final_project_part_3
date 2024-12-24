from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models import Base


class Location(Base):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    country_id = Column(Integer, ForeignKey('countries.country_id', ondelete="CASCADE"))
    region_id = Column(Integer, ForeignKey('regions.region_id', ondelete="CASCADE"))
    city_id = Column(Integer, ForeignKey('cities.city_id', ondelete="CASCADE"))

    country = relationship("Country", backref="locations")
    region = relationship("Region", backref="locations")
    city = relationship("City", backref="locations")