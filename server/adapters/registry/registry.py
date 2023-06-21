import os
import json


def load_asset_data(chain, network):
    global_assets_path = f"../registry/data/assets.json"
    relevant_assets_path = f"../registry/data/{chain}/{network}/assets.json"
    global_assets = []
    relevant_assets = []
    try:
        with open(global_assets_path) as f:
            global_assets = json.loads(f.read())
    except FileNotFoundError:
        pass
    try:
        with open(relevant_assets_path) as f:
            relevant_assets = json.loads(f.read())
    except FileNotFoundError:
        pass
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
        try:
            with open(path) as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            pass
    return data
