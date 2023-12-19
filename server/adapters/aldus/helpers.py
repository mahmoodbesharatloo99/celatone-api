import json

import requests
from utils.gcs import get_network_data


def get_upload_access(chain, network):
    res = requests.get(f"{get_network_data(chain,network,'lcd')}/wasm/params")
    if res.status_code == 200:
        return res.json().get("params", {}).get("code_upload_access", {})

    res = requests.get(
        f"{get_network_data(chain,network,'lcd')}/cosmwasm/wasm/v1/codes/params"
    )
    if res.status_code == 200:
        return res.json().get("params", {}).get("code_upload_access", {})

    res = requests.get(
        f"{get_network_data(chain,network,'lcd')}/cosmos/params/v1beta1/params?subspace=wasm&key=uploadAccess"
    ).json()
    res_value = json.loads(res["param"]["value"])
    permission = res_value["permission"]
    addresses = res_value.get("addresses", [])
    address = addresses[0] if permission == "OnlyAddress" else ""
    return {
        "permission": permission,
        "addresses": addresses,
        "address": address,
    }
