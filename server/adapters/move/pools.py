import json

import requests
from flask import abort
from utils.gcs import get_network_data

POOLS_INFO_FN = {
    "stone-11": {
        "address": "0x38d2a65b2be5d2c1b9f329f5b45f708c7b7d9cf5",
        "module_name": "PoolInfo",
        "function_name": "get_all_pair_infos",
    }
}


def get_move_pools(chain, network):
    if network not in POOLS_INFO_FN:
        abort(404, f"invalid network ({network}).")

    endpoint = get_network_data(chain, network, "lcd")
    fn = POOLS_INFO_FN[network]
    pools = (
        requests.post(
            f"{endpoint}/initia/move/v1/accounts/{fn['address']}/modules/{fn['module_name']}/view_functions/{fn['function_name']}",
            {
                "type_args": {},
                "args": {},
            },
        )
        .json()
        .get("data", [])
    )
    return json.loads(pools)
