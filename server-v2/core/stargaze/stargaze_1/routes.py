from core.base.base_blueprint import BaseBlueprint
from .service import Stargaze1Service as Service

service_instance = Service() 
name = 'stargaze-1'
url_prefix = '/stargaze-2'

base_blueprint = BaseBlueprint(service_instance, name, url_prefix)
blueprint = base_blueprint.get_blueprint()
