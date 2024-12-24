from sqlalchemy import select, func
from app.db.database import session_maker
from app.db.models import Location, Group, Event, City
from app.service.question_12_service import movement_data


def get_groups_expanding_to_new_regions():
    with session_maker() as session:
        stmt = (
            select(
                Group.group_name.label("group_name"),
                Location.latitude.label("from_lat"),
                Location.longitude.label("from_lon"),
                City.city_name.label("from_city"),
                func.min(Location.latitude).label("to_lat"),
                func.min(Location.longitude).label("to_lon"),
                func.min(City.city_name).label("to_city")
            )
            .join(Event, Event.group_id == Group.group_id)
            .join(Location, Event.location_id == Location.location_id)
            .join(City, Location.city_id == City.city_id)
            .where(
                Group.group_name != 'Unknown',
                City.city_name != 'Unknown',
                Location.region_id != None,
            )
            .group_by(Group.group_name, Location.latitude, Location.longitude, City.city_name)
        )
        results = session.execute(stmt).fetchall()
        return movement_data(results)
