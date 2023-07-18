from core.base.base_blueprint import BaseBlueprint
from .service import Phoenix1Service as Service

service_instance = Service() 
name = 'phoenix-1'
url_prefix = '/phoenix-1'

base_blueprint = BaseBlueprint(service_instance, name, url_prefix)
blueprint = base_blueprint.get_blueprint()
