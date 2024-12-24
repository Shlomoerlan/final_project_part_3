from sqlalchemy.orm import aliased
from sqlalchemy import func, and_
from app.db.database import session_maker
from app.db.models import Event, Location, Group, TargetType, Region, Country


def get_groups_with_shared_targets(region=None, country=None):
    with session_maker() as session:
        EventAlias1 = aliased(Event)
        EventAlias2 = aliased(Event)
        LocationAlias1 = aliased(Location)
        # LocationAlias2 = aliased(Location)

        query = (
            session.query(
                Group.group_name.label('group_name'),
                TargetType.targettype_name.label('target_name'),
                Region.region_name.label('region'),
                Country.country_name.label('country'),
                LocationAlias1.latitude.label('latitude'),
                LocationAlias1.longitude.label('longitude'),
                func.count(EventAlias1.event_id).label('attack_count')
            )
            .join(EventAlias1, EventAlias1.group_id == Group.group_id)
            .join(TargetType, EventAlias1.targettype_id == TargetType.targettype_id)
            .join(LocationAlias1, EventAlias1.location_id == LocationAlias1.location_id)
            .join(Region, LocationAlias1.region_id == Region.region_id)
            .join(Country, LocationAlias1.country_id == Country.country_id)
            .join(EventAlias2, and_(
                EventAlias1.targettype_id == EventAlias2.targettype_id,
                EventAlias1.location_id == EventAlias2.location_id,
                EventAlias1.event_id != EventAlias2.event_id
            ))
            .group_by(
                Group.group_name,
                TargetType.targettype_name,
                Region.region_name,
                Country.country_name,
                LocationAlias1.latitude,
                LocationAlias1.longitude
            )
            .order_by(func.count(EventAlias1.event_id).desc())
        )

        if region:
            query = query.filter(Region.region_name == region)

        if country:
            query = query.filter(Country.country_name == country)

        return query.all()

