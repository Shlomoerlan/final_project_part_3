from typing import List, Dict, Optional
from sqlalchemy import func
from toolz import curry
from app.db.database import session_maker
from app.db.models import Location, Region, Country, Group, Event, TargetType

SimilarityScore = float


@curry
def fetch_target_preferences(
        min_attacks: int = 5,
        group_name: Optional[str] = None,
        region: Optional[str] = None
) -> List[Dict]:
    """
    Fetch target preferences data for groups with minimum number of attacks.
    """
    with session_maker() as session:
        query = (
            session.query(
                Group.group_name,
                TargetType.targettype_name,
                func.count().label('attack_count'),
                func.count().label('total_attacks'),
                Region.region_name,
                Country.country_name
            )
            .select_from(Event)
            .join(Group, Event.group_id == Group.group_id)
            .join(TargetType, Event.targettype_id == TargetType.targettype_id)
            .join(Location, Event.location_id == Location.location_id)
            .join(Region, Location.region_id == Region.region_id)
            .join(Country, Location.country_id == Country.country_id)
            .group_by(
                Group.group_name,
                TargetType.targettype_name,
                Region.region_name,
                Country.country_name
            )
            .having(func.count() >= min_attacks)
        )

        if group_name:
            query = query.filter(Group.group_name.ilike(f"%{group_name}%"))
        if region:
            query = query.filter(Region.region_name.ilike(f"%{region}%"))

        return [row._asdict() for row in query.all()]


