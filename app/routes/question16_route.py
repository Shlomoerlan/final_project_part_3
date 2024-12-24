from flask import request, jsonify, render_template, Blueprint
from toolz import pipe
from app.repository.question_16 import fetch_group_activity_data
from app.service.question_16_service import process_group_activity, analyze_group_activity, \
    create_activity_summary
from app.utils.map_utils import create_activity_map

q_16_blueprint = Blueprint('question_16', __name__)

# http://localhost:5000/v16/api/analysis/group-activity?year=1970&region=Middle%20East&min_events=5

@q_16_blueprint.route('/api/analysis/group-activity', methods=['GET'])
def get_group_activity_analysis():
    try:
        year = request.args.get('year', type=int)
        region = request.args.get('region')
        min_events = request.args.get('min_events', 5, type=int)
        result = pipe(
            fetch_group_activity_data(
                min_events=min_events,
                year=year,
                region=region
            ),
            process_group_activity,
            analyze_group_activity,
            lambda analysis: {
                'locations': [
                    {**data['location'], 'metrics': data['metrics']}
                    for data in analysis.values()
                ],
                'analysis': analysis,
                'summary': create_activity_summary(analysis)
            }
        )
        create_activity_map(result['locations'])
        return render_template('q_16_index.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
