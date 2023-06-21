import json
import requests

from constants import LCD_DICT


def get_upload_access(chain, network):
    upload_access = {}
    res = requests.get(
        f"{LCD_DICT[chain][network]}/cosmwasm/wasm/v1/codes/params"
    ).json()
    if "code_upload_access" in res["params"]:
        upload_access = res["params"]["code_upload_access"]
    else:
        res = requests.get(
            f"{LCD_DICT[chain][network]}/cosmos/params/v1beta1/params?subspace=wasm&key=uploadAccess"
        ).json()
        res_value = res["param"]["value"]
        res_value = json.loads(res_value.replace("\\", ""))
        permission = res_value["permission"]
        addresses = res_value.get("addresses", [])
        address = addresses[0] if permission == "OnlyAddress" else ""
        upload_access = {
            "permission": permission,
            "addresses": addresses,
            "address": address,
        }
    return upload_access
