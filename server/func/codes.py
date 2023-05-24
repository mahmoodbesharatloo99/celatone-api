import json
import requests
import os
import base64

from func.constants import SCANWORKS_URL, LCD_DICT
from func.graphql import get_graphql_code_details


def load_codes(chain, network):
    codes = []
    path = f"../registry/data/{chain}/{network}/codes.json"
    if os.path.exists(path):
        codes = json.load(open(path))
        if len(codes) > 0:
            graphql_details = get_graphql_code_details(chain, network, [code["id"] for code in codes])
            for code in codes:
                code_graphql_detail = [detail for detail in graphql_details if detail["code_id"] == code["id"]][0]
                code["cw2Contract"] = code_graphql_detail["cw2_contract"]
                code["cw2Version"] = code_graphql_detail["cw2_version"]
                code["uploader"] = code_graphql_detail["creator"]
                code["contracts"] = code_graphql_detail["contract_instantiated"]
                code["instantiatePermission"] = code_graphql_detail["access_config_permission"]
                code["permissionAddresses"] = code_graphql_detail["access_config_addresses"]
                contract["imageUrl"] = "https://celatone-api.alleslabs.dev/images/entities/" + code["slug"]
    return codes


def get_codes(chain, network):
    codes = load_codes(chain, network)
    return codes


def get_code(chain, network, code_id):
    codes = load_codes(chain, network)
    code = [item for item in codes if int(item["id"]) == int(code_id)][0]
    return code
