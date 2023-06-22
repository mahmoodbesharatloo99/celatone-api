import json
import os.path

from utils.graphql import get_graphql_code_details


def load_codes(chain, network):
    codes = []
    path = f"../registry/data/{chain}/{network}/codes.json"
    if os.path.exists(path):
        with open(path) as f:
            codes = json.load(f)

    code_ids = []
    for code in codes:
        code_ids.append(code["id"])

    graphql_details = get_graphql_code_details(chain, network, code_ids)

    graphql_map = {}
    for detail in graphql_details:
        graphql_map[detail["code_id"]] = detail

    for code in codes:
        code_details = graphql_map[code["id"]]
        code.update(
            {
                "cw2Contract": code_details["cw2_contract"],
                "cw2Version": code_details["cw2_version"],
                "uploader": code_details["creator"],
                "contracts": code_details["contract_instantiated"],
                "instantiatePermission": code_details["access_config_permission"],
                "permissionAddresses": code_details["access_config_addresses"],
            }
        )

    return codes


def get_codes(chain, network):
    codes = load_codes(chain, network)
    return codes


def get_code(chain, network, code_id):
    codes = load_codes(chain, network)
    code = [code for code in codes if code["id"] == int(code_id)][0]
    return code
