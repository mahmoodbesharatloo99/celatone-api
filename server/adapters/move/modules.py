import requests
from flask import abort
from utils.gcs import get_network_data


def get_move_modules(chain: str, network: str, address: str):
    if chain != "initia":
        return abort(404, f"invalid chain ({chain}).")

    result = []
    pagination_key = None
    endpoint = get_network_data(chain, network, "lcd")

    while True:
        url = f"{endpoint}/initia/move/v1/accounts/{address}/modules"
        if pagination_key:
            url += f"?pagination.key={pagination_key}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        result.extend(data["modules"])

        pagination_key = (
            data["pagination"].get("next_key") if "pagination" in data else None
        )
        if not pagination_key:
            break

    return {
        "items": sorted(result, key=lambda x: x["module_name"]),
        "total": len(result),
    }
