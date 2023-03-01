import json
import requests
import os
import base64

from func.constants import SCANWORKS_URL, LCD_DICT
from func.graphql import get_graphql_code_details


def get_cw2_details(chain, network, code_id):
    cw2_info = ""
    try:
        lcd = LCD_DICT[chain][network]
        contract = requests.get(
            f"{lcd}/cosmwasm/wasm/v1/code/{code_id}/contracts"
        ).json()["contracts"][0]
        cw2_details = requests.get(
            f"{lcd}/cosmwasm/wasm/v1/contract/{contract}/raw/Y29udHJhY3RfaW5mbw%3D%3D"
        ).json()
        cw2_parsed = json.loads(base64.b64decode(cw2_details["data"]).decode("utf-8"))
        cw2_info = f"{cw2_parsed['contract']} ({cw2_parsed['version']})"
    except Exception as e:
        print(e)
        pass
    return cw2_info


def load_codes(chain, network):
    codes = []
    path = f"../registry/data/{chain}/{network}/codes.json"
    if os.path.exists(path):
        codes = json.load(open(path))
        if len(codes) > 0:
            graphql_details = get_graphql_code_details(
                chain, network, [code["id"] for code in codes]
            )
            verification_details = requests.get(
                f"{SCANWORKS_URL}/{chain}/contracts.json"
            ).json()["contracts"]
            for code in codes:
                code_graphql_detail = [
                    detail
                    for detail in graphql_details
                    if detail["code_id"] == code["id"]
                ][0]
                code["uploader"] = code_graphql_detail["creator"]
                code["contracts"] = code_graphql_detail["contract_instantiated"]
                code["instantiatePermission"] = code_graphql_detail[
                    "access_config_permission"
                ]
                code["permissionAddresses"] = code_graphql_detail[
                    "access_config_addresses"
                ]
                if code["id"] in verification_details:
                    code["verified"] = True
                    code["verificationDetails"] = verification_details[code["id"]]
                else:
                    code["verified"] = False
    return codes


def get_codes(chain, network):
    codes = load_codes(chain, network)
    return codes


def get_code(chain, network, code_id):
    codes = load_codes(chain, network)
    code = [item for item in codes if int(item["id"]) == int(code_id)][0]
    return code
