import os
import json
import os


def load_asset_data(chain, network):
    global_assets_path = f"../registry/data/assets.json"
    if not os.path.exists(global_assets_path):
        return []
    with open(global_assets_path) as f:
        global_assets = json.load(f)
    assets = []
    for asset in global_assets:
        asset_id = asset["id"].get(chain, {}).get(network)
        if asset_id:
            asset["id"] = asset_id
            assets.append(asset)
    return assets


def load_and_check_registry_data(chain, network, content):
    path = f"../registry/data/{chain}/{network}/{content}.json"
    data = None
    if content == "assets":
        data = load_asset_data(chain, network)
    elif os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    return data or []
