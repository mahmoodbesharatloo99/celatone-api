import json


def load_assets(chain, network):
    assets = json.load(open(f"../registry/data/{chain}/{network}/assets.json"))
    return assets


def get_assets(chain, network):
    assets = load_assets(chain, network)
    return assets


def get_asset_by_type(chain, network, asset_type):
    assets = load_assets(chain, network)
    asset = [asset for asset in assets if asset["type"] == asset_type]
    return asset


def get_asset_by_slug(chain, network, asset_slug):
    assets = load_assets(chain, network)
    asset = [asset for asset in assets if asset_slug in asset["slugs"]]
    return asset


def get_asset(chain, network, asset_id):
    assets = load_assets(chain, network)
    asset = [asset for asset in assets if asset["id"] == asset_id][0]
    return asset


def get_asset_ibc(chain, network, hash):
    assets = load_assets(chain, network)
    asset = [asset for asset in assets if asset["id"] == f"ibc/{hash}"][0]
    return asset


def get_asset_factory(chain, network, creator, symbol):
    assets = load_assets(chain, network)
    asset = [asset for asset in assets if asset["id"] == f"factory/{creator}/{symbol}"][
        0
    ]
    return asset
