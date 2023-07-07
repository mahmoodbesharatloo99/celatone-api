from ast import Dict, List
from apiflask import APIBlueprint
from .service import Osmosis1Service

service = Osmosis1Service()

blueprint = APIBlueprint('/osmosis/osmosis-1', __name__, tag='Osmosis-1', url_prefix='/osmosis-1')

@blueprint.route('/accounts')
def accounts():
    return service.accounts

@blueprint.route('/account/<account_address>')
def account(account_address: str) :
    return service.get_account(account_address)
