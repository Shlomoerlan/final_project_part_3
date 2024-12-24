def movement_data(results):
    return [
        {
            "group_name": row.group_name,
            "from_city": row.from_city,
            "to_city": row.to_city,
            "from_coords": (row.from_lat, row.from_lon),
            "to_coords": (row.to_lat, row.to_lon)
        }
        for row in results
    ]