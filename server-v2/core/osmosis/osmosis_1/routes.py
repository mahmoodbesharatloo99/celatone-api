from ast import Dict, List
from apiflask import APIBlueprint
from .service import Osmosis1Service

service = Osmosis1Service()

blueprint = APIBlueprint("/osmosis/osmosis-1", __name__, tag="Osmosis-1", url_prefix="/osmosis-1")

### ACCOUNT ###
@blueprint.route("/accounts", methods=["GET"])
def accounts():
    return service.accounts

@blueprint.route("/account/<account_address>", methods=["GET"])
def account(account_address: str) :
    return service.get_account(account_address)


### ASSETS ###
@blueprint.route("/assets", methods=["GET"])
def get_assets():
    """Get All Assets

    Returns a list of all the known assets based on the input chain and network
    """
    return service.assets()


@blueprint.route('/assets/prices', methods=["GET"])
def get_assets_prices():
    """Get All Assets with Prices

    Returns a list of all the known assets based on the input chain and network
    """
    return service.get_assets_with_prices()


@blueprint.route('/assets/type/<asset_type>', methods=["GET"])
def get_assets_by_type(asset_type):
    """Get Assets by Type

    Returns a list of all the known assets based on the input chain, network, and asset_type
    """
    return service.get_assets_by_type(asset_type)


@blueprint.route('/assets/slug/<asset_slug>', methods=["GET"])
def get_asset_by_slug(asset_slug):
    return service.get_assets_by_slug(asset_slug)


@blueprint.route('/assets/<asset_id>', methods=["GET"])
def get_asset(asset_id):
    return service.get_asset(asset_id)
