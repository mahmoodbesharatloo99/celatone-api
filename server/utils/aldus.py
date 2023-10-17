import requests
from typing import Any, Dict
from utils.constants import ALDUS_URL


def fetch_json(url: str) -> Dict[str, Any]:
    """Fetch JSON data from a URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Dict[str, Any]: The fetched JSON data.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}


def get_aldus_entities_data() -> Dict[str, Any]:
    """Fetch Aldus entities data.

    Returns:
        Dict[str, Any]: The fetched Aldus entities data.
    """
    return fetch_json(f"{ALDUS_URL}/data/entities.json")


def get_aldus_chain_data(chain: str, network: str, data_type: str) -> Dict[str, Any]:
    """Fetch Aldus chain data.

    Args:
        chain (str): The chain to fetch data for.
        network (str): The network to fetch data for.
        data_type (str): The type of data to fetch.

    Returns:
        Dict[str, Any]: The fetched Aldus chain data.
    """
    data = {}
    if data_type == "assets":
        all_assets = fetch_json(f"{ALDUS_URL}/data/assets.json")
        filtered_assets = [
            dict(item, id=item["id"][chain][network])
            for item in all_assets
            if chain in item["id"] and network in item["id"][chain]
        ]
        filtered_assets = [dict(asset, **{"price": 0.00}) for asset in filtered_assets]
        data = filtered_assets
    else:
        data = fetch_json(f"{ALDUS_URL}/data/{chain}/{network}/{data_type}.json")
    return data
