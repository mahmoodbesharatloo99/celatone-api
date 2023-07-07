from ast import Dict, List
from apiflask import APIBlueprint
from .osmosis_1.routes import blueprint as osmosis1

blueprint = APIBlueprint('/osmosis', __name__, url_prefix='/osmosis')

blueprint.register_blueprint(osmosis1)

