from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .location import Location
from .event import Event
from .group import Group
from .attack_type import AttackType
from .attacker_statistic import AttackerStatistic
from .country import Country
from .city import City
from .region import Region
from .target_type import TargetType