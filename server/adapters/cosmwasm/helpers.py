import json
import requests

from constants import LCD_DICT


def get_upload_access(chain, network):
    upload_access = {}
    try:
        res = requests.get(
            f"{LCD_DICT[chain][network]}/cosmwasm/wasm/v1/codes/params"
        ).json()
        upload_access = res["params"]["code_upload_access"]
    except:
        res = requests.get(
            f"{LCD_DICT[chain][network]}/cosmos/params/v1beta1/params?subspace=wasm&key=uploadAccess"
        ).json()
        res_value = json.loads(res["param"]["value"].replace("\\", ""))
        address = ""
        addresses = []
        if res_value["permission"] == "AnyOfAddresses":
            addresses = res_value["addresses"]
        upload_access = {
            "permission": res_value["permission"],
            "addresses": addresses,
            "address": address,
        }
    return upload_access
