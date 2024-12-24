from flask import render_template, request, jsonify, Blueprint
from toolz import pipe
from app.repository.question_14 import fetch_attack_data, get_all_regions_and_countries
from app.service.question_14_service import analyze_location_strategies, create_summary, process_strategies
from app.utils.map_utils import create_map_with_markers_q14

q_14_blueprint = Blueprint("q_14", __name__)

@q_14_blueprint.route('/')
def index():
     return render_template('index.html')

# http:/localhost:5000/v14/

@q_14_blueprint.route('/api/analysis/shared-strategies', methods=['GET'])
def get_shared_attack_strategies():
    try:
        region = request.args.get('region')
        country = request.args.get('country')

        result = pipe(
            fetch_attack_data(region=region, country=country),
            process_strategies,
            analyze_location_strategies,
            lambda analysis: {
                'locations': [data['location'] for data in analysis.values()],
                'analysis': analysis,
                'summary': create_summary(
                    analysis,
                    [data['location'] for data in analysis.values()]
                )
            }
        )

        if request.args.get('include_map', 'true').lower() == 'true':
            result['map_html'] = create_map_with_markers_q14(result['locations'])

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@q_14_blueprint.route('/api/filters', methods=['GET'])
def get_filters():
    try:
        return jsonify(get_all_regions_and_countries())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
