import base64
from func.registry import load_and_check_registry_data
from func.prices import get_prices


def encode_base64(string):
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def get_assets(chain, network):
    assets = load_and_check_registry_data(chain, network, "assets")
    assets = [dict(asset, **{"price": 1.00}) for asset in assets]
    return assets


def get_assets_by_type(chain, network, asset_type):
    assets = get_assets(chain, network)
    assets = [asset for asset in assets if asset["type"] == asset_type]
    return assets


def get_assets_by_slug(chain, network, asset_slug):
    assets = get_assets(chain, network)
    assets = [asset for asset in assets if asset_slug in asset["slugs"]]
    return assets


def get_asset(chain, network, asset_id):
    assets = get_assets(chain, network)
    asset = [asset for asset in assets if asset["id"] == asset_id][0]
    return asset


def get_asset_ibc(chain, network, hash):
    assets = get_assets(chain, network)
    asset = [asset for asset in assets if asset["id"] == f"ibc/{hash}"][0]
    return asset


# Osmosis Assets


def get_asset_factory(chain, network, creator, symbol):
    assets = get_assets(chain, network)
    asset = [asset for asset in assets if asset["id"] == f"factory/{creator}/{symbol}"][0]
    return asset


def get_asset_gamm(chain, network, pool_id):
    assets = get_assets(chain, network)
    asset = [asset for asset in assets if asset["id"] == f"gamm/pool/{pool_id}"][0]
    return asset
