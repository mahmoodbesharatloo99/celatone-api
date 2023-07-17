from .service import OsmosisTest5Service
from ..osmosis_base_blueprint import OsmosisBaseBlueprint

service = OsmosisTest5Service()
blueprint_instance = OsmosisBaseBlueprint(service, "osmo-test-5", "/osmo-test-5")
blueprint = blueprint_instance.get_blueprint()