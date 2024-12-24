from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models import Base

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    iyear = Column(Integer)
    imonth = Column(Integer)
    iday = Column(Integer)
    attacktype_id = Column(Integer, ForeignKey('attack_types.attacktype_id', ondelete="CASCADE"))
    targettype_id = Column(Integer, ForeignKey('target_types.targettype_id', ondelete="CASCADE"))
    location_id = Column(Integer, ForeignKey('locations.location_id', ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey('groups.group_id', ondelete="CASCADE"))

    attacktype = relationship("AttackType", backref="events")
    targettype = relationship("TargetType", backref="events")
    location = relationship("Location", backref="events")
    group = relationship("Group", backref="events")
