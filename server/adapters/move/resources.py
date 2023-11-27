import requests
from flask import abort
from utils.gcs import get_network_data


def get_move_resources(
    chain: str, network: str, address: str, pagination_key: str | None
):
    if chain != "initia":
        return abort(404, f"invalid chain ({chain}).")
    endpoint = get_network_data(chain, network, "lcd")
    return requests.get(
        f"{endpoint}/initia/move/v1/accounts/{address}/resources",
        params={"pagination.key": pagination_key} if pagination_key else {},
    ).json()
