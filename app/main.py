from flask import Flask
from app.routes.question11_route import q_11_blueprint
from app.routes.question12_route import q_12_blueprint
from app.routes.question14_route import q_14_blueprint
from app.routes.question15_route import q_15_blueprint
from app.routes.question16_route import q_16_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(q_11_blueprint, url_prefix='/v11')
app.register_blueprint(q_12_blueprint, url_prefix='/v12')
app.register_blueprint(q_14_blueprint, url_prefix='/v14')
app.register_blueprint(q_15_blueprint, url_prefix='/v15')
app.register_blueprint(q_16_blueprint, url_prefix='/v16')

if __name__ == '__main__':
    app.run(debug=True)