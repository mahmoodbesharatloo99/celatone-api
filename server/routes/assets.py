from flask import Blueprint
from adapters.core import assets

assets_bp = Blueprint("assets", __name__)


@assets_bp.route("/assets/<chain>/<network>", methods=["GET"])
def get_assets(chain, network):
    """Get All Assets

    Returns a list of all the known assets based on the input chain and network
    """
    return assets.get_assets(chain, network)


@assets_bp.route("/assets/<chain>/<network>/prices", methods=["GET"])
def get_assets_prices(chain, network):
    """Get All Assets with Prices

    Returns a list of all the known assets based on the input chain and network
    """
    return assets.get_assets_with_prices(chain, network)


@assets_bp.route("/assets/<chain>/<network>/type/<asset_type>", methods=["GET"])
def get_assets_by_type(chain, network, asset_type):
    """Get Assets by Type

    Returns a list of all the known assets based on the input chain, network, and asset_type
    """
    return assets.get_assets_by_type(chain, network, asset_type)


@assets_bp.route("/assets/<chain>/<network>/slug/<asset_slug>", methods=["GET"])
def get_asset_by_slug(chain, network, asset_slug):
    return assets.get_assets_by_slug(chain, network, asset_slug)


@assets_bp.route("/assets/<chain>/<network>/<asset_id>", methods=["GET"])
def get_asset(chain, network, asset_id):
    return assets.get_asset(chain, network, asset_id)


@assets_bp.route("/assets/<chain>/<network>/ibc/<hash>", methods=["GET"])
def get_asset_ibc(chain, network, hash):
    return assets.get_asset_ibc(chain, network, hash)


@assets_bp.route("/assets/<chain>/<network>/factory/<creator>/<symbol>", methods=["GET"])
def get_asset_factory(chain, network, creator, symbol):
    return assets.get_asset_factory(chain, network, creator, symbol)


@assets_bp.route("/assets/<chain>/<network>/gamm/pool/<pool_id>", methods=["GET"])
def get_asset_gamm(chain, network, pool_id):
    return assets.get_asset_gamm(chain, network, pool_id)


@assets_bp.route("/native-assets/<chain>/<network>", methods=["GET"])
def get_native_assets(chain, network):
    """Get All Native Assets

    Returns a list of all the chain native assets based on the input chain and network
    """
    # TODO - Fix native assets
    return assets.get_assets_with_prices(chain, network)
