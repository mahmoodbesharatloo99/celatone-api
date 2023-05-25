import base64
from func.registry import load_and_check_registry_data
from func.prices import get_prices


def encode_base64(string):
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def get_assets(chain, network):
    assets = load_and_check_registry_data(chain, network, "assets")
    return [dict(asset, **{"price": 0.00}) for asset in assets]


def get_assets_with_prices(chain, network):
    assets = get_assets(chain, network)
    priced_assets = filter(lambda asset: asset["coingecko"], assets)
    priced_asset_ids = [asset["id"] for asset in priced_assets]
    prices = get_prices(chain, network, priced_asset_ids)
    asset_prices = {id: prices.get(id, 0.00) for id in priced_asset_ids}
    for asset in assets:
        asset["price"] = asset_prices.get(asset["id"], 0.00)
    return assets


def get_assets_by_type(chain, network, asset_type):
    assets = get_assets(chain, network)
    return list(filter(lambda asset: asset["type"] == asset_type, assets))


def get_assets_by_slug(chain, network, asset_slug):
    assets = get_assets(chain, network)
    return list(filter(lambda asset: asset_slug in asset["slugs"], assets))


def get_asset(chain, network, asset_id):
    assets = get_assets(chain, network)
    asset_map = {asset["id"]: asset for asset in assets}
    return asset_map[asset_id]


def get_asset_ibc(chain, network, hash):
    assets = get_assets(chain, network)
    asset_map = {asset["id"]: asset for asset in assets}
    return asset_map[f"ibc/{hash}"]


# Osmosis Assets


def get_asset_factory(chain, network, creator, symbol):
    assets = get_assets_with_prices(chain, network)
    asset_map = {asset["id"]: asset for asset in assets}
    return asset_map[f"factory/{creator}/{symbol}"]


def get_asset_gamm(chain, network, pool_id):
    assets = get_assets_with_prices(chain, network)
    asset_map = {asset["id"]: asset for asset in assets}
    return asset_map[f"gamm/pool/{pool_id}"]