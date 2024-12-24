import math
from collections import defaultdict
from typing import Dict, Any, List, Tuple
from toolz import curry

ActivityMetrics = Dict[str, Any]
LocationKey = Tuple[float, float]

def validate_location(location: Dict[str, Any]) -> bool:
    try:
        return all([
            isinstance(location.get('lat'), (int, float)),
            isinstance(location.get('lon'), (int, float)),
            not math.isnan(location['lat']),
            not math.isnan(location['lon']),
            -90 <= location['lat'] <= 90,
            -180 <= location['lon'] <= 180
        ])
    except (KeyError, TypeError):
        return False


def extract_location_info(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'lat': row['lat'],
        'lon': row['lon'],
        'region': row['region_name'],
        'country': row['country_name']
    }


@curry
def process_group_activity(data: List[Dict]) -> Dict[LocationKey, Dict[str, Any]]:
    activity_data = defaultdict(lambda: {
        'location': None,
        'groups': defaultdict(int),
        'total_events': 0
    })

    for row in data:
        if not validate_location(row):
            continue

        loc_key = (row['lat'], row['lon'])
        if not activity_data[loc_key]['location']:
            activity_data[loc_key]['location'] = extract_location_info(row)

        activity_data[loc_key]['groups'][row['group_name']] += row['event_count']
        activity_data[loc_key]['total_events'] += row['event_count']

    return activity_data


def calculate_diversity_metrics(groups: Dict[str, int]) -> ActivityMetrics:
    total_events = sum(groups.values())
    unique_groups = len(groups)

    if not total_events or not unique_groups:
        return {
            'unique_groups': 0,
            'total_events': 0,
            'activity_density': 0,
            'group_diversity': 0
        }

    group_proportions = [count / total_events for count in groups.values()]
    diversity_index = -sum(p * math.log(p) for p in group_proportions)
    normalized_diversity = diversity_index / math.log(unique_groups) if unique_groups > 1 else 0

    return {
        'unique_groups': unique_groups,
        'total_events': total_events,
        'activity_density': total_events / unique_groups,
        'group_diversity': round(normalized_diversity * 100, 2)
    }


@curry
def analyze_group_activity(activity_data: Dict[LocationKey, Dict[str, Any]]) -> Dict[str, Any]:
    analysis_results = {}

    for loc_key, data in activity_data.items():
        location_key = f"{data['location']['region']}/{data['location']['country']}"
        metrics = calculate_diversity_metrics(data['groups'])

        analysis_results[location_key] = {
            'location': data['location'],
            'metrics': metrics,
            'groups': [
                {
                    'name': group,
                    'events': count,
                    'percentage': round(count * 100 / metrics['total_events'], 2)
                }
                for group, count in sorted(
                    data['groups'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            ]
        }

    return analysis_results


def create_activity_summary(analysis_results: Dict[str, Dict]) -> Dict[str, Any]:
    if not analysis_results:
        return {
            'total_locations': 0,
            'total_unique_groups': 0,
            'average_group_diversity': 0,
            'most_diverse_location': None
        }

    all_groups = set(
        group['name']
        for result in analysis_results.values()
        for group in result['groups']
    )

    return {
        'total_locations': len(analysis_results),
        'total_unique_groups': len(all_groups),
        'average_group_diversity': round(
            sum(loc['metrics']['group_diversity']
                for loc in analysis_results.values()) / len(analysis_results),
            2
        ),
        'most_diverse_location': max(
            analysis_results.items(),
            key=lambda x: x[1]['metrics']['group_diversity']
        )[0]
    }
