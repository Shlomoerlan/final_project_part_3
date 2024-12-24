def grouping_data(results):
    return [
        {
            'group_name': row.group_name,
            'target_name': row.target_name,
            'region': row.region,
            'country': row.country,
            'attack_count': row.attack_count,
        }
        for row in results
    ]

def to_map_object(results):
    return [
        {
                'lat': row.latitude,
                'lon': row.longitude,
                'popup':
                    f"Group: {row.group_name}<br>"
                    f"Target: {row.target_name}<br>"
                    f"Region: {row.region}<br>"
                    f"Country: {row.country}<br>"
                    f"Attacks: {row.attack_count}"
        }
            for row in results
    ]
