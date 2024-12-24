import os
from flask import Blueprint, request, jsonify, render_template
from app.repository.question_11 import get_groups_with_shared_targets
from app.utils.map_utils import create_map_with_markers
from app.service.question_11_service import grouping_data, to_map_object

q_11_blueprint = Blueprint('question_11', __name__)


@q_11_blueprint.route('/groups/shared-targets-map', methods=['GET'])
def get_shared_targets_map():
    region = request.args.get('region')
    country = request.args.get('country')
    include_map = request.args.get('include_map', default='true') == 'true'
    results = get_groups_with_shared_targets(region=region, country=country)

    if not results:
        return jsonify({':<)': 'No data found.'}), 404

    groups_data = grouping_data(results)

    if include_map:
        map_html = create_map_with_markers(to_map_object(results))
        map_html_path = os.path.join('templates', 'shared_targets_map.html')
        map_html.save(map_html_path)
        return jsonify({ 'map': map_html._repr_html_() })

    return jsonify({'groups_data': groups_data})
