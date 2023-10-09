import requests

from utils.constants import ALDUS_URL


def get_aldus_entities_data():
    entities = requests.get(f"{ALDUS_URL}/data/entities.json").json()
    return entities


def get_aldus_chain_data(chain, network, data_type):
    data = {}
    if data_type == "assets":
        all_assets = requests.get(f"{ALDUS_URL}/data/assets.json").json()
        filtered_assets = [
            dict(item, id=item["id"][chain][network])
            for item in all_assets
            if chain in item["id"] and network in item["id"][chain]
        ]
        filtered_assets = [dict(asset, **{"price": 0.00}) for asset in filtered_assets]
        data = filtered_assets
    else:
        data = requests.get(f"{ALDUS_URL}/data/{chain}/{network}/{data_type}.json").json()
    return data


if __name__ == "__main__":
    print(get_aldus_chain_data("osmosis", "osmosis-1", "assets")[0])
