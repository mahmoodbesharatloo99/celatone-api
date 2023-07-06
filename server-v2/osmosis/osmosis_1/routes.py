from apiflask import APIBlueprint
from .service import Osmosis1Service

service = Osmosis1Service()

osmosis_1_blueprint = APIBlueprint('/osmosis/osmosis-1', __name__, tag='Osmosis-1')

@osmosis_1_blueprint.route('/accounts')
def accounts():
    return service.accounts
