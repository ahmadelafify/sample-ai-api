from flask import Flask

from api.routes.ai import ai_bp


app = Flask(__name__)

app.register_blueprint(ai_bp)
