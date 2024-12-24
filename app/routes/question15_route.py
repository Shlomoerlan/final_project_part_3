from flask import jsonify, request, Blueprint
from app.db.database import session_maker
from app.db.models import Group
from app.service.question_15_service import  get_target_preferences_analysis
from app.utils.graph_utils import create_target_preferences_graph, HTML_TEMPLATE

q_15_blueprint = Blueprint('question_15', __name__)

# http://localhost:5000/v15/target-preferences

@q_15_blueprint.route('/api/analysis/target-preferences/graph', methods=['GET'])
def get_target_preferences_graph():
    try:
        group_name = request.args.get('group')
        region = request.args.get('region')
        min_attacks = int(request.args.get('min_attacks', 5))
        similarity_threshold = float(request.args.get('similarity_threshold', 70.0))

        data = get_target_preferences_analysis(group_name, region, min_attacks, similarity_threshold)
        graph = create_target_preferences_graph(data)
        return jsonify(graph)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@q_15_blueprint.route('/api/groups', methods=['GET'])
def get_available_groups():
    try:
        with session_maker() as session:
            groups = (
                session.query(Group.group_name)
                .distinct()
                .order_by(Group.group_name)
                .all()
            )
            return jsonify({
                'groups': [g[0] for g in groups]
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@q_15_blueprint.route('/target-preferences')
def show_target_preferences():
    return HTML_TEMPLATE