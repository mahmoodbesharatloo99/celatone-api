from flask import Blueprint, jsonify
from adapters.aldus.assets import AssetManager

assets_bp = Blueprint("assets", __name__)


def get_assets_manager(chain, network):
    # Add input validation here
    return AssetManager(chain, network)


@assets_bp.route("/assets/<chain>/<network>", methods=["GET"])
def get_assets(chain, network):
    try:
        return get_assets_manager(chain, network).get_assets()
    except Exception as e:
        return jsonify(error=str(e)), 500


@assets_bp.route("/assets/<chain>/<network>/prices", methods=["GET"])
def get_assets_prices(chain, network):
    try:
        return get_assets_manager(chain, network).get_assets_with_prices()
    except Exception as e:
        return jsonify(error=str(e)), 500


@assets_bp.route("/assets/<chain>/<network>/type/<asset_type>", methods=["GET"])
def get_assets_by_type(chain, network, asset_type):
    try:
        return get_assets_manager(chain, network).get_assets_by_type(asset_type)
    except Exception as e:
        return jsonify(error=str(e)), 500


@assets_bp.route("/assets/<chain>/<network>/slug/<asset_slug>", methods=["GET"])
def get_asset_by_slug(chain, network, asset_slug):
    try:
        return get_assets_manager(chain, network).get_asset_by_slug(asset_slug)
    except Exception as e:
        return jsonify(error=str(e)), 500


@assets_bp.route("/assets/<chain>/<network>/<asset_id>", methods=["GET"])
def get_asset(chain, network, asset_id):
    try:
        return get_assets_manager(chain, network).get_asset(asset_id)
    except Exception as e:
        return jsonify(error=str(e)), 500


@assets_bp.route("/assets/<chain>/<network>/ibc/<hash>", methods=["GET"])
def get_asset_ibc(chain, network, hash):
    try:
        return get_assets_manager(chain, network).get_asset_ibc(hash)
    except Exception as e:
        return jsonify(error=str(e)), 500


@assets_bp.route("/assets/<chain>/<network>/factory/<creator>/<symbol>", methods=["GET"])
def get_asset_factory(chain, network, creator, symbol):
    try:
        return get_assets_manager(chain, network).get_asset_factory(creator, symbol)
    except Exception as e:
        return jsonify(error=str(e)), 500


@assets_bp.route("/assets/<chain>/<network>/gamm/pool/<pool_id>", methods=["GET"])
def get_asset_gamm(chain, network, pool_id):
    try:
        return get_assets_manager(chain, network).get_asset_gamm(pool_id)
    except Exception as e:
        return jsonify(error=str(e)), 500
