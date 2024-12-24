from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict
import math
from sqlalchemy import func, desc
from toolz import curry
from app.db.database import session_maker
from app.db.models import Location, Region, Country, Group, AttackType, Event

StrategyDict = Dict[str, Dict[str, int]]
GroupData = Dict[str, Dict[str, int]]


@curry
def fetch_attack_data(region: Optional[str] = None, country: Optional[str] = None) -> List[Dict]:
    with session_maker() as session:
        query = (
            session.query(
                Location.latitude.label('lat'),
                Location.longitude.label('lon'),
                Region.region_name.label('region'),
                Country.country_name.label('country'),
                Group.group_name,
                AttackType.attacktype_name,
                func.count().label('attack_count')
            )
            .select_from(Event)
            .join(Location, Event.location_id == Location.location_id)
            .join(Region, Location.region_id == Region.region_id)
            .join(Country, Location.country_id == Country.country_id)
            .join(Group, Event.group_id == Group.group_id)
            .join(AttackType, Event.attacktype_id == AttackType.attacktype_id)
            .filter(
                Location.latitude.isnot(None),
                Location.longitude.isnot(None)
            )
        )

        if region:
            query = query.filter(Region.region_name.ilike(f"%{region}%"))
        if country:
            query = query.filter(Country.country_name.ilike(f"%{country}%"))

        return [
            row._asdict() for row in query.group_by(
                Location.latitude,
                Location.longitude,
                Region.region_name,
                Country.country_name,
                Group.group_name,
                AttackType.attacktype_name
            )
            .having(func.count() > 0)
            .order_by(desc('attack_count'))
            .all()
        ]


def get_all_regions_and_countries() -> Dict[str, List[str]]:
    with session_maker() as session:
        return {
            'regions': [r[0] for r in session.query(Region.region_name)
            .distinct()
            .order_by(Region.region_name)
            .all()],
            'countries': [c[0] for c in session.query(Country.country_name)
            .distinct()
            .order_by(Country.country_name)
            .all()]
        }
