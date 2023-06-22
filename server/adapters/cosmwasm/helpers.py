import json
import requests

from constants import LCD_DICT


def get_upload_access(chain, network):
    upload_access = {}
    res = requests.get(f"{LCD_DICT[chain][network]}/wasm/params")
    if res.status_code == 200:
        upload_access = res.json().get("params", {}).get("code_upload_access", {})
    else:
        res = requests.get(
            f"{LCD_DICT[chain][network]}/cosmos/params/v1beta1/params?subspace=wasm&key=uploadAccess"
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
