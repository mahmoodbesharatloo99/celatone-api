import requests


def get_assets(registry_url, chain, network):
    assets = requests.get(f"{registry_url}/data/{chain}/{network}/assets.json").json()
    return assets


def get_asset_by_type(registry_url, chain, network, asset_type):
    assets = requests.get(f"{registry_url}/data/{chain}/{network}/assets.json").json()
    asset = [asset for asset in assets if asset["type"] == asset_type]
    return asset


def get_asset_by_slug(registry_url, chain, network, asset_slug):
    assets = requests.get(f"{registry_url}/data/{chain}/{network}/assets.json").json()
    asset = [asset for asset in assets if asset_slug in asset["slugs"]]
    return asset


def get_asset(registry_url, chain, network, asset_id):
    assets = requests.get(f"{registry_url}/data/{chain}/{network}/assets.json").json()
    asset = [asset for asset in assets if asset["id"] == asset_id][0]
    return asset
