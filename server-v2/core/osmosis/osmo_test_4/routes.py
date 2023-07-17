from .service import OsmosisTest4Service
from ..osmosis_base_blueprint import OsmosisBaseBlueprint

service = OsmosisTest4Service()
blueprint_instance = OsmosisBaseBlueprint(service, "osmo-test-4", "/osmo-test-4")
blueprint = blueprint_instance.get_blueprint()