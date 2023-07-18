from .service import Osmosis1Service
from ..osmosis_base_blueprint import OsmosisBaseBlueprint

service = Osmosis1Service()
blueprint_instance = OsmosisBaseBlueprint(service, "osmosis-1", "/osmosis-1")
blueprint = blueprint_instance.get_blueprint()