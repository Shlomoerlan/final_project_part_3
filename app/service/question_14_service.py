import math
from collections import defaultdict
from typing import Dict, Any, List, Set, Tuple
from functools import reduce
from toolz import curry

LocationKey = Tuple[float, float]

def is_location_validate(data: Dict[str, Any]) -> bool:
    try:
        return all([
            isinstance(data.get('lat'), (int, float)),
            isinstance(data.get('lon'), (int, float)),
            not math.isnan(data['lat']),
            not math.isnan(data['lon']),
            isinstance(data.get('region'), str),
            isinstance(data.get('country'), str),
            bool(data['region'].strip()),
            bool(data['country'].strip())
        ])
    except (KeyError, TypeError, AttributeError):
        return False


def extract_location_info(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'lat': row['lat'],
        'lon': row['lon'],
        'region': row['region'],
        'country': row['country']
    }


@curry
def process_strategies(data: List[Dict]) -> Dict[LocationKey, Dict[str, Any]]:
    location_data = defaultdict(lambda: {
        'groups': set(),
        'strategies': defaultdict(lambda: defaultdict(int)),
        'location': None
    })

    for row in filter(is_location_validate, data):
        loc_key = (row['lat'], row['lon'])
        if not location_data[loc_key]['location']:
            location_data[loc_key]['location'] = extract_location_info(row)

        location_data[loc_key]['groups'].add(row['group_name'])
        location_data[loc_key]['strategies'][row['group_name']][row['attacktype_name']] += row['attack_count']

    return location_data


def calculate_similarity_score(groups: Set[str], shared_strategies: Dict) -> float:
    if len(groups) <= 1:
        return 0.0

    total_comparisons = len(groups) * (len(groups) - 1) / 2
    shared_count = sum(1 for strat in shared_strategies.values()
                       for _ in strat['groups'])

    return round((shared_count / total_comparisons) * 100, 2) if total_comparisons > 0 else 0.0


@curry
def get_groups_from_data(data: Dict[str, Any]) -> List[str]:
    return list(data['groups'])


@curry
def extract_all_strategies(data: Dict[str, Dict[str, int]]) -> Set[str]:
    return reduce(lambda acc, x: acc | set(x.keys()),
                  data['strategies'].values(),
                  set())


@curry
def find_groups_with_strategy(groups: List[str],
                              strategies_data: Dict[str, Dict[str, int]],
                              strategy: str) -> List[str]:
    return [g for g in groups if strategy in strategies_data[g]]


@curry
def calculate_strategy_usage(groups: List[str],
                             strategies_data: Dict[str, Dict[str, int]],
                             strategy: str) -> int:
    return sum(strategies_data[g][strategy]
               for g in groups
               if strategy in strategies_data[g])


@curry
def calculate_strategy_percentage(groups_with_strategy: List[str],
                                  total_groups: int) -> float:
    return round(len(groups_with_strategy) * 100 / total_groups, 2)


@curry
def create_strategy_metrics(strategy: str,
                            groups: List[str],
                            strategies_data: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
    groups_with_strategy = find_groups_with_strategy(groups, strategies_data, strategy)

    if len(groups_with_strategy) <= 1:
        return None

    return {
        'groups': groups_with_strategy,
        'usage_count': calculate_strategy_usage(groups, strategies_data, strategy),
        'percentage': calculate_strategy_percentage(groups_with_strategy, len(groups))
    }


@curry
def create_location_metrics(groups: List[str],
                            all_strategies: Set[str],
                            shared_strategies: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    return {
        'total_groups': len(groups),
        'total_strategies': len(all_strategies),
        'shared_strategies': len(shared_strategies),
        'similarity_score': calculate_similarity_score(groups, shared_strategies),
        'unique_strategies': len(all_strategies) - len(shared_strategies),
        'most_shared_strategy': get_most_shared_strategy(shared_strategies)
    }


def get_most_shared_strategy(shared_strategies: Dict[str, Dict[str, Any]]) -> str:
    if not shared_strategies:
        return None
    return max(
        shared_strategies.items(),
        key=lambda x: x[1]['usage_count'],
        default=('None', {'usage_count': 0})
    )[0]


@curry
def process_location(data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    location_key = f"{data['location']['region']}/{data['location']['country']}"
    groups = get_groups_from_data(data)
    all_strategies = extract_all_strategies(data)

    shared_strategies = {
        strategy: metrics
        for strategy in all_strategies
        if (metrics := create_strategy_metrics(strategy, groups, data['strategies'])) is not None
    }

    return location_key, {
        'location': data['location'],
        'groups': groups,
        'metrics': create_location_metrics(groups, all_strategies, shared_strategies),
        'shared_strategies': shared_strategies
    }


@curry
def analyze_location_strategies(location_data: Dict[LocationKey, Dict[str, Any]]) -> Dict[str, Any]:
    return dict(map(process_location, location_data.values()))


def create_summary(analysis_results: Dict[str, Any],
                   locations: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        'total_locations': len(locations),
        'total_groups': len({
            group
            for result in analysis_results.values()
            for group in result['groups']
        }),
        'locations_with_shared_strategies': sum(
            1 for loc in analysis_results.values()
            if loc['metrics']['shared_strategies'] > 0
        ),
        'most_active_location': max(
            analysis_results.items(),
            key=lambda x: x[1]['metrics']['total_strategies'],
            default=(None, {'metrics': {'total_strategies': 0}})
        )[0],
        'average_similarity_score': round(
            sum(loc['metrics']['similarity_score']
                for loc in analysis_results.values()) / len(analysis_results)
            if analysis_results else 0,
            2
        )
    }
