import json

from utils.graphql import get_graphql_code_details


def load_codes(chain, network):
    codes = []
    path = f"../registry/data/{chain}/{network}/codes.json"
    try:
        with open(path) as f:
            codes = json.load(f)
    except FileNotFoundError:
        pass
    if len(codes) > 0:
        graphql_details = get_graphql_code_details(
            chain, network, [code["id"] for code in codes]
        )
        graphql_map = {detail["code_id"]: detail for detail in graphql_details}
        for code in codes:
            code_graphql_detail = graphql_map[code["id"]]
            code["cw2Contract"] = code_graphql_detail["cw2_contract"]
            code["cw2Version"] = code_graphql_detail["cw2_version"]
            code["uploader"] = code_graphql_detail["creator"]
            code["contracts"] = code_graphql_detail["contract_instantiated"]
            code["instantiatePermission"] = code_graphql_detail[
                "access_config_permission"
            ]
            code["permissionAddresses"] = code_graphql_detail["access_config_addresses"]
    return codes


def get_codes(chain, network):
    codes = load_codes(chain, network)
    return codes


def get_code(chain, network, code_id):
    codes = load_codes(chain, network)
    code = [code for code in codes if code["id"] == int(code_id)][0]
    return code
