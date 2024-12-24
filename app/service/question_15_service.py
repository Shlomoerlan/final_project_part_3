from collections import defaultdict
from typing import List, Dict, Any
from toolz import curry, pipe
from app.repository.question_15 import fetch_target_preferences

GroupTargets = Dict[str, Dict[str, int]]


def calculate_target_distribution(data: List[Dict]) -> dict[Any, dict[Any, float]]:
    group_targets = defaultdict(lambda: defaultdict(int))
    group_totals = defaultdict(int)

    for row in data:
        group_targets[row['group_name']][row['targettype_name']] += row['attack_count']
        group_totals[row['group_name']] += row['attack_count']

    return {
        group: {
            target: (count * 100.0 / group_totals[group])
            for target, count in targets.items()
        }
        for group, targets in group_targets.items()
    }


def calculate_similarity(prefs1: Dict[str, float], prefs2: Dict[str, float]) -> float:
    all_targets = set(prefs1.keys()) | set(prefs2.keys())
    if not all_targets:
        return 0.0

    shared_targets = set(prefs1.keys()) & set(prefs2.keys())
    if not shared_targets:
        return 0.0

    similarity = sum(
        1 - abs(prefs1.get(target, 0) - prefs2.get(target, 0)) / 100
        for target in shared_targets
    ) / len(all_targets)

    return round(similarity * 100, 2)


@curry
def find_similar_groups(
        target_preferences: GroupTargets,
        similarity_threshold: float = 70.0
) -> Dict[str, List[Dict[str, Any]]]:
    groups = list(target_preferences.keys())
    similar_groups = defaultdict(list)

    for i, group1 in enumerate(groups):
        for group2 in groups[i + 1:]:
            similarity = calculate_similarity(
                target_preferences[group1],
                target_preferences[group2]
            )

            if similarity >= similarity_threshold:
                shared_targets = set(target_preferences[group1].keys()) & \
                                 set(target_preferences[group2].keys())

                similar_groups[group1].append({
                    'group': group2,
                    'similarity_score': similarity,
                    'shared_targets': list(shared_targets)
                })
                similar_groups[group2].append({
                    'group': group1,
                    'similarity_score': similarity,
                    'shared_targets': list(shared_targets)
                })

    return dict(similar_groups)


def create_analysis_summary(
        preferences: GroupTargets,
        similar_groups: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, Any]:
    return {
        'total_groups': len(preferences),
        'groups_with_similarities': len(similar_groups),
        'average_similarity_score': round(
            sum(
                score['similarity_score']
                for groups in similar_groups.values()
                for score in groups
            ) / sum(len(groups) for groups in similar_groups.values())
            if similar_groups else 0,
            2
        ),
        'most_common_targets': sorted(
            set(
                target
                for group_prefs in preferences.values()
                for target in group_prefs.keys()
            ),
            key=lambda t: sum(
                1 for prefs in preferences.values()
                if t in prefs
            ),
            reverse=True
        )[:5]
    }

def get_target_preferences_analysis(group_name=None, region=None, min_attacks=None, similarity_threshold=None):
    try:
        result = pipe(
            fetch_target_preferences(
                min_attacks=min_attacks,
                group_name=group_name,
                region=region
            ),
            lambda data: {
                'target_preferences': calculate_target_distribution(data),
                'raw_data': data
            },
            lambda data: {
                **data,
                'similar_groups': find_similar_groups(
                    data['target_preferences'],
                    similarity_threshold
                )
            },
            lambda data: {
                **data,
                'summary': create_analysis_summary(
                    data['target_preferences'],
                    data['similar_groups']
                )
            }
        )
        return result

    except Exception as e:
        return str(e)
