from adapters.aldus.assets import AssetManager
from apiflask import APIBlueprint
from flask import jsonify
from utils.helper import get_query_param

assets_bp = APIBlueprint("assets", __name__)


def get_assets_manager(chain, network):
    # Add input validation here
    return AssetManager(chain, network)


@assets_bp.route("/<chain>/<network>/assets", methods=["GET"])
def get_assets(chain, network):
    with_prices = get_query_param("with_prices", type=bool, default=False)
    if with_prices:
        return get_assets_manager(chain, network).get_assets_with_prices()
    return get_assets_manager(chain, network).get_assets()


@assets_bp.route("/<chain>/<network>/assets/type/<asset_type>", methods=["GET"])
def get_assets_by_type(chain, network, asset_type):
    return get_assets_manager(chain, network).get_assets_by_type(asset_type)


### NOTE: Commenting out unused routes

# @assets_bp.route("/assets/<chain>/<network>/slug/<asset_slug>", methods=["GET"])
# def get_asset_by_slug(chain, network, asset_slug):
#     return get_assets_manager(chain, network).get_asset_by_slug(asset_slug)


# @assets_bp.route("/assets/<chain>/<network>/<asset_id>", methods=["GET"])
# def get_asset(chain, network, asset_id):
#     return get_assets_manager(chain, network).get_asset(asset_id)


# @assets_bp.route("/assets/<chain>/<network>/ibc/<hash>", methods=["GET"])
# def get_asset_ibc(chain, network, hash):
#     return get_assets_manager(chain, network).get_asset_ibc(hash)


# @assets_bp.route(
#     "/assets/<chain>/<network>/factory/<creator>/<symbol>", methods=["GET"]
# )
# def get_asset_factory(chain, network, creator, symbol):
#     return get_assets_manager(chain, network).get_asset_factory(creator, symbol)


# @assets_bp.route("/assets/<chain>/<network>/gamm/pool/<pool_id>", methods=["GET"])
# def get_asset_gamm(chain, network, pool_id):
#     return get_assets_manager(chain, network).get_asset_gamm(pool_id)
