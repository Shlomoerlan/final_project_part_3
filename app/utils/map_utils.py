import math
from typing import List, Dict, Any
import folium
from app.service.question_14_service import is_location_validate


def create_map_with_markers(locations):
    valid_locations = [
        loc for loc in locations
        if loc['lat'] is not None and loc['lon'] is not None
           and not math.isnan(loc['lat']) and not math.isnan(loc['lon'])
    ]

    if not valid_locations:
        raise ValueError("No valid locations to display on the map.")

    center_lat = sum(loc['lat'] for loc in valid_locations) / len(valid_locations)
    center_lon = sum(loc['lon'] for loc in valid_locations) / len(valid_locations)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    for loc in valid_locations:
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=folium.Popup(loc['popup'], max_width=300),
        ).add_to(m)

    return m


def create_group_movement_map(movements):
    my_map = folium.Map(location=[32.0, 34.0], zoom_start=7)

    for movement in movements:
        try:
            from_coords = movement['from_coords']
            to_coords = movement['to_coords']
            from_city = movement.get('from_city', 'Unknown')
            to_city = movement.get('to_city', 'Unknown')
            group_name = movement.get('group_name', 'Unknown Group')

            folium.Marker(
                location=from_coords,
                popup=f"From: {from_city} ({group_name})",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(my_map)

            folium.Marker(
                location=to_coords,
                popup=f"To: {to_city} ({group_name})",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(my_map)

            folium.PolyLine(
                locations=[from_coords, to_coords],
                color="green",
                weight=2.5,
                opacity=1,
            ).add_to(my_map)
        except KeyError as e:
            print(f"Missing data: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")

    return my_map


HTML_STR = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Group Movements Map</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Group Movements Map</h1>
        {{ map_html|safe }}
    </body>
    </html>
    """


def create_map_with_markers_q14(locations: List[Dict[str, Any]]) -> str:
    valid_locations = [loc for loc in locations if is_location_validate(loc)]

    if not valid_locations:
        return ""

    center_lat = sum(loc['lat'] for loc in valid_locations) / len(valid_locations)
    center_lon = sum(loc['lon'] for loc in valid_locations) / len(valid_locations)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    for loc in valid_locations:
        popup_content = f"""
           <div style='width: 200px'>
               <b>Region:</b> {loc['region']}<br>
               <b>Country:</b> {loc['country']}<br>
               <b>Groups:</b> {loc.get('total_groups', 0)}<br>
               <b>Strategies:</b> {loc.get('total_strategies', 0)}<br>
               <b>Similarity Score:</b> {loc.get('similarity_score', 0)}%
           </div>
       """

        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=popup_content,
            tooltip=f"{loc['country']} - Click for details"
        ).add_to(m)
    m.save(r'C:\Users\1\PycharmProjects\final_project_analyze_part_3\check_app\templates\index.html')
    return m._repr_html_()



def create_activity_map(locations: List[Dict[str, Any]]) -> str:
    if not locations:
        return ""

    valid_locations = [loc for loc in locations if is_location_validate(loc)]
    if not valid_locations:
        return ""

    center_lat = sum(loc['lat'] for loc in valid_locations) / len(valid_locations)
    center_lon = sum(loc['lon'] for loc in valid_locations) / len(valid_locations)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    for loc in valid_locations:
        popup_content = f"""
            <div style='width: 250px'>
                <h4>{loc['country']}</h4>
                <hr>
                <b>Region:</b> {loc['region']}<br>
                <b>Number of Groups:</b> {loc['metrics']['unique_groups']}<br>
                <b>Total Events:</b> {loc['metrics']['total_events']}<br>
                <b>Activity Density:</b> {loc['metrics']['activity_density']:.2f}<br>
                <b>Group Diversity:</b> {loc['metrics']['group_diversity']}%
            </div>
        """

        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color='red' if loc['metrics']['unique_groups'] > 1 else 'blue'),
            tooltip=f"{loc['country']} - {loc['metrics']['unique_groups']} groups"
        ).add_to(m)

        folium.Circle(
            location=[loc['lat'], loc['lon']],
            radius=loc['metrics']['total_events'] * 1000,
            color='red' if loc['metrics']['unique_groups'] > 1 else 'blue',
            fill=True,
            fillOpacity=0.2,
            weight=1
        ).add_to(m)

    legend_html = """
        <div style="position: fixed; bottom: 50px; left: 50px; z-index:1000; background-color: white;
                    padding: 10px; border: 2px solid grey; border-radius: 5px">
            <p><b>Legend</b></p>
            <p>
                <i class="fa fa-circle" style="color:red"></i> Multiple Groups<br>
                <i class="fa fa-circle" style="color:blue"></i> Single Group<br>
                Circle Size: Number of Events
            </p>
        </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    m.save(r'C:\Users\1\PycharmProjects\final_project_analyze_part_3\check_app\templates\q_16_index.html')
    return m._repr_html_()
