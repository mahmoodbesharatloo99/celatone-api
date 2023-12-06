from flask import abort
from utils.data_fetcher import fetch_paginated_data
from utils.gcs import get_network_data


def get_move_modules(chain: str, network: str, address: str):
    if chain != "initia":
        abort(404, f"invalid chain ({chain}).")

    endpoint = get_network_data(chain, network, "lcd")

    return fetch_paginated_data(
        f"{endpoint}/initia/move/v1/accounts/{address}/modules",
        "modules",
        "module_name",
    )
