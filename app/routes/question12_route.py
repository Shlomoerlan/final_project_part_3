from flask import render_template_string, Blueprint
from app.repository.question_12 import get_groups_expanding_to_new_regions
from app.utils.map_utils import create_group_movement_map, HTML_STR

q_12_blueprint = Blueprint('question12', __name__)


@q_12_blueprint.route('/groups/movements-map')
def group_movements_map():
    movements = get_groups_expanding_to_new_regions()
    my_map = create_group_movement_map(movements)
    map_html = my_map._repr_html_()
    return render_template_string(HTML_STR  , map_html=map_html)



