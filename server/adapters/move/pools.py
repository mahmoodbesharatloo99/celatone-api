import json

import requests
from utils.gcs import get_network_data

POOLS_INFO_FN = {
    "stone-11": {
        "address": "0xa36bd0a54fad4bd931c4c00e3e74815f99a6c6b4",
        "moduleName": "PoolInfo",
        "functionName": "get_all_pair_infos",
    }
}


def get_move_pools(chain, network):
    endpoint = get_network_data(chain, network, "lcd")
    fn = POOLS_INFO_FN[network]
    pools = (
        requests.post(
            f"{endpoint}/initia/move/v1/accounts/{fn['address']}/modules/{fn['moduleName']}/view_functions/{fn['functionName']}",
            {
                "type_args": {},
                "args": {},
            },
        )
        .json()
        .get("data", [])
    )
    return json.loads(pools)
