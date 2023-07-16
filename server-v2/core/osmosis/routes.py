from flask import Blueprint
from .osmosis_1.routes import blueprint as osmosis1

blueprint = Blueprint("Osmosis", __name__,url_prefix="/osmosis")

blueprint.register_blueprint(osmosis1)

