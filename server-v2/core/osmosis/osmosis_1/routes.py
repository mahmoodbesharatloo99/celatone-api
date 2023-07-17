from apiflask import APIBlueprint
from .service import Osmosis1Service

service = Osmosis1Service()

blueprint = APIBlueprint("osmosis-1", __name__, url_prefix="/osmosis-1")

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
    return service.assets


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


## Project ##
@blueprint.route("/projects", methods=["GET"])
def get_projects():
    return service.projects


@blueprint.route("/projects/<slug>", methods=["GET"])
def get_project(slug):
    return service.get_project(slug)


## Cosmos Rest ##
@blueprint.route("/rest/<path:path>", methods=["GET"])
def get_some_rest(path):
    return service.get_rest(path)


# Transactions

@blueprint.route("/txs/<tx_hash>", methods=["GET"])
def get_tx(tx_hash):
    return service.get_tx(tx_hash)

## Osmosis - Pools ##
@blueprint.route("/pools", methods=["GET"])
def get_pools():
    """Get All Pools

    Returns a list of all the known Osmosis pools based on the input chain and network
    """
    return service.pools


@blueprint.route("/pool/<pool_id>", methods=["GET"])
def get_pool(pool_id):
    """Get Pool by ID

    Returns a specific Osmosis pool based on the input chain, network, and code_id
    """
    return service.get_pool(pool_id)
