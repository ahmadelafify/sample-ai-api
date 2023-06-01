from flask import Flask

from api.models.settings import settings
from api.routes.ai import ai_bp


app = Flask(__name__)
app.debug = settings.ENV_TYPE == "local"
app.config["SECRET_KEY"] = settings.SECRET_KEY

app.register_blueprint(ai_bp)
