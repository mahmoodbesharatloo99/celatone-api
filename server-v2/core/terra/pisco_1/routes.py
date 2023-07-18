from core.base.base_blueprint import BaseBlueprint
from .service import Pisco1Service as Service

service_instance = Service() 
name = 'pisco-1'
url_prefix = '/pisco-1'

base_blueprint = BaseBlueprint(service_instance, name, url_prefix)
blueprint = base_blueprint.get_blueprint()
