import base64
from func.registry import load_and_check_registry_data
from func.prices import get_prices


def encode_base64(string):
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def get_assets(chain, network):
    assets = load_and_check_registry_data(chain, network, "assets")
    assets = [dict(asset, **{"price": 0.00}) for asset in assets]
    return assets


def get_assets_with_prices(chain, network):
    assets = get_assets(chain, network)
    priced_assets = [asset for asset in assets if asset["coingecko"] != ""]
    priced_asset_ids = [asset["id"] for asset in priced_assets]
    prices = get_prices(chain, network, priced_asset_ids)
    for id, price in prices.items():
        for asset in priced_assets:
            if asset["id"] == id:
                asset["price"] = price
    return priced_assets


def get_assets_by_type(chain, network, asset_type):
    assets = get_assets_with_prices(chain, network)
    assets = [asset for asset in assets if asset["type"] == asset_type]
    return assets


def get_assets_by_slug(chain, network, asset_slug):
    assets = get_assets_with_prices(chain, network)
    assets = [asset for asset in assets if asset_slug in asset["slugs"]]
    return assets


def get_asset(chain, network, asset_id):
    assets = get_assets_with_prices(chain, network)
    asset = [asset for asset in assets if asset["id"] == asset_id][0]
    return asset


def get_asset_ibc(chain, network, hash):
    assets = get_assets_with_prices(chain, network)
    asset = [asset for asset in assets if asset["id"] == f"ibc/{hash}"][0]
    return asset


# Osmosis Assets


def get_asset_factory(chain, network, creator, symbol):
    assets = get_assets_with_prices(chain, network)
    asset = [asset for asset in assets if asset["id"] == f"factory/{creator}/{symbol}"][0]
    return asset


def get_asset_gamm(chain, network, pool_id):
    assets = get_assets_with_prices(chain, network)
    asset = [asset for asset in assets if asset["id"] == f"gamm/pool/{pool_id}"][0]
    return asset
