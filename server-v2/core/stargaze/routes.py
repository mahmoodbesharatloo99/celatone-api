from flask import Blueprint
from .stargaze_1.routes import blueprint as stargaze_1

blueprint = Blueprint("Stargaze", __name__,url_prefix="/stargaze")

blueprint.register_blueprint(stargaze_1)

