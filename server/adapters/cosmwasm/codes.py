from utils.aldus import get_aldus_chain_data
from utils.graphql import get_graphql_code_details


def load_codes(chain, network):
    codes = get_aldus_chain_data(chain, network, "codes")
    code_ids = [code["id"] for code in codes]

    graphql_map = {}
    graphql_details = get_graphql_code_details(chain, network, code_ids)
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
