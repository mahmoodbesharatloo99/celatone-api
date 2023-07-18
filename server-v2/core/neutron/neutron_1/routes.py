from core.base.base_blueprint import BaseBlueprint
from .service import Neutron1Service as Service

service_instance = Service() 
name = 'neutron-1'
url_prefix = '/neutron-1'

base_blueprint = BaseBlueprint(service_instance, name, url_prefix)
blueprint = base_blueprint.get_blueprint()
