from .service import OsmosisTest4Service as Service
from ..osmosis_base_blueprint import OsmosisBaseBlueprint

service_instance = Service() 
name = 'osmo-test-4'
url_prefix = '/osmo-test-4'

blueprint_instance = OsmosisBaseBlueprint(service_instance, name, url_prefix)
blueprint = blueprint_instance.get_blueprint()