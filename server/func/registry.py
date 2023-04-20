import os
import json


def load_asset_data(chain, network):
    global_assets_path = f"../registry/data/assets.json"
    relevant_assets_path = f"../registry/data/{chain}/{network}/assets.json"
    global_assets = []
    relevant_assets = []
    if os.path.exists(global_assets_path):
        global_assets = json.load(open(global_assets_path))
    if os.path.exists(relevant_assets_path):
        relevant_assets = json.load(open(relevant_assets_path))
    assets = []
    for asset in global_assets:
        if chain in asset["id"] and network in asset["id"][chain]:
            asset["id"] = asset["id"][chain][network]
            assets.append(asset)
    return assets


def load_and_check_registry_data(chain, network, content):
    path = f"../registry/data/{chain}/{network}/{content}.json"
    data = []
    if content == "assets":
        data = load_asset_data(chain, network)
    else:
        if os.path.exists(path):
            data = json.load(open(path))
    return data
