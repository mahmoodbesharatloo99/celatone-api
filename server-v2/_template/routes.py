from core.base.base_blueprint import BaseBlueprint
from .service import TemplateService as Service

service_instance = Service() 
name = 'my_blueprint'
url_prefix = '/sth'

base_blueprint = BaseBlueprint(service_instance, name, url_prefix)
blueprint = base_blueprint.get_blueprint()
