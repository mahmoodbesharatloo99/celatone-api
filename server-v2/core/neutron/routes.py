from flask import Blueprint
from .neutron_1.routes import blueprint as neutron_1
from .pion_1.routes import blueprint as pion_1

blueprint = Blueprint("Neutron", __name__,url_prefix="/neutron")

blueprint.register_blueprint(neutron_1)
blueprint.register_blueprint(pion_1)

