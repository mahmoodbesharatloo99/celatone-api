import requests
from utils.gcs import get_network_data


def get_rest_states(chain, network, contract_address, limit, pagination_key):
    response = requests.get(
        f"{get_network_data(chain, network, 'lcd')}/cosmwasm/wasm/v1/contract/{contract_address}/state",
        {
            "pagination.limit": limit,
            "pagination.key": pagination_key,
        },
    )
    response.raise_for_status()
    return response.json()
