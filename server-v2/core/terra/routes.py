from flask import Blueprint
from .phoenix_1.routes import blueprint as phoenix_1
from .pisco_1.routes import blueprint as pisco_1

blueprint = Blueprint("Terra", __name__,url_prefix="/terra")

blueprint.register_blueprint(phoenix_1)
blueprint.register_blueprint(pisco_1)

