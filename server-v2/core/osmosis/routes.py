from flask import Blueprint
from .osmosis_1.routes import blueprint as osmosis1
from .osmo_test_4.routes import blueprint as osmo_test_4
from .osmo_test_5.routes import blueprint as osmo_test_5

blueprint = Blueprint("Osmosis", __name__,url_prefix="/osmosis")

blueprint.register_blueprint(osmosis1)
blueprint.register_blueprint(osmo_test_4)
blueprint.register_blueprint(osmo_test_5)

