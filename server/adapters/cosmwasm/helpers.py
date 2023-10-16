import json
import requests

from utils.gcs import get_network_data


def get_upload_access(chain, network):
    upload_access = {}
    res = requests.get(f"{get_network_data(chain,network,'lcd')}/wasm/params")
    if res.status_code == 200:
        upload_access = res.json().get("params", {}).get("code_upload_access", {})
    else:
        res = requests.get(
            f"{get_network_data(chain,network,'lcd')}/cosmos/params/v1beta1/params?subspace=wasm&key=uploadAccess"
        ).json()
        res_value = json.loads(res["param"]["value"])
        permission = res_value["permission"]
        addresses = res_value.get("addresses", [])
        address = addresses[0] if permission == "OnlyAddress" else ""
        upload_access = {
            "permission": permission,
            "addresses": addresses,
            "address": address,
        }
    return upload_access
