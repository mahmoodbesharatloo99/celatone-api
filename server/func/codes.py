import json
import requests
import os

from func.constants import SCANWORKS_URL, GRAPHQL_DICT


def load_codes(chain, network):
    codes = []
    path = f"../registry/data/{chain}/{network}/codes.json"
    if os.path.exists(path):
        codes = json.load(open(path))
        verification_details = requests.get(
            f"{SCANWORKS_URL}/{chain}/contracts.json"
        ).json()["contracts"]
        for code in codes:
            if code["id"] in verification_details:
                code["verified"] = True
                code["verification_details"] = verification_details[code["id"]]
            else:
                code["verified"] = False
        code_id = [code["id"] for code in codes]
        payload = (
            """{"query":
    "query { codes(where:{id:{_in:%s}}) {id access_config_permission contracts_aggregate { aggregate{ count } } } }",
    "variables":{}}"""
            % code_id
        )
        code_response = requests.request(
            "POST", GRAPHQL_DICT[chain][network], data=payload
        ).json()["data"]["codes"]
        for i in range(len(code_response)):
            code["permission"] = code_response[i]["access_config_permission"]
            code["contracts"] = code_response[i]["contracts_aggregate"]["aggregate"][
                "count"
            ]
    return codes


def get_codes(chain, network):
    codes = load_codes(chain, network)
    return codes


def get_code(chain, network, code_id):
    codes = load_codes(chain, network)
    code = [code for code in codes if code["id"] == code_id][0]
    return code
