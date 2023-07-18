from .service import OsmosisTest5Service as Service
from ..osmosis_base_blueprint import OsmosisBaseBlueprint

service_instance = Service() 
name = 'osmo-test-5'
url_prefix = '/osmo-test-5'

blueprint_instance = OsmosisBaseBlueprint(service_instance, name, url_prefix)
blueprint = blueprint_instance.get_blueprint()
