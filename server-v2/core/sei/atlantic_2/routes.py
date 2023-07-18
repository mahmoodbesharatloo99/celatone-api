from core.base.base_blueprint import BaseBlueprint
from .service import Atlantic2Service as Service

service_instance = Service() 
name = 'atlantic-2'
url_prefix = '/atlantic-2'

base_blueprint = BaseBlueprint(service_instance, name, url_prefix)
blueprint = base_blueprint.get_blueprint()
