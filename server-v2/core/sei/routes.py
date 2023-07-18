from flask import Blueprint
from .atlantic_2.routes import blueprint as atlantic_2
from .pacific_1.routes import blueprint as pacific_1

blueprint = Blueprint("Sei", __name__,url_prefix="/sei")

blueprint.register_blueprint(atlantic_2)
blueprint.register_blueprint(pacific_1)

