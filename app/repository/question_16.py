from typing import List, Dict, Optional
from sqlalchemy import func
from toolz import curry
from app.db.database import session_maker
from app.db.models import Location, Region, Country, Group, Event


@curry
def fetch_group_activity_data(
        min_events: int = 5,
        year: Optional[int] = None,
        region: Optional[str] = None
    ) -> List[Dict]:
    with session_maker() as session:
        query = (
            session.query(
                Location.latitude.label('lat'),
                Location.longitude.label('lon'),
                Region.region_name,
                Country.country_name,
                Group.group_name,
                func.count(Event.event_id).label('event_count')
            )
            .select_from(Event)
            .join(Location, Event.location_id == Location.location_id)
            .join(Region, Location.region_id == Region.region_id)
            .join(Country, Location.country_id == Country.country_id)
            .join(Group, Event.group_id == Group.group_id)
            .filter(
                Location.latitude.isnot(None),
                Location.longitude.isnot(None)
            )
            .group_by(
                Location.latitude,
                Location.longitude,
                Region.region_name,
                Country.country_name,
                Group.group_name
            )
            .having(func.count(Event.event_id) >= min_events)
        )

        if year:
            query = query.filter(Event.iyear == year)
        if region:
            query = query.filter(Region.region_name.ilike(f"%{region}%"))

        return [row._asdict() for row in query.all()]
