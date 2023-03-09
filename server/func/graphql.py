import requests
from func.constants import GRAPHQL_DICT
from func.constants import GRAPHQL_TEST_DICT


def get_contract_instantiator_admin(chain, network, contract_addresses):
    contract_data = []
    query = "query {"
    for contract_address in contract_addresses:
        query += f"""
        {contract_address}: contracts_by_pk(address: "{contract_address}") {{
          account {{
            address
          }}
          accountByInitBy {{
            address
          }}
          label
        }}
        """
    query += "}"
    graphql_response = requests.post(
        GRAPHQL_DICT[chain][network], json={"query": query}
    ).json()["data"]
    for contract_address, data in graphql_response.items():
        if data["account"] is None:
            data["account"] = {"address": ""}
        if data["accountByInitBy"] is None:
            data["accountByInitBy"] = {"address": ""}
        contract_data.append(
            {
                "address": contract_address,
                "instantiator": data["accountByInitBy"]["address"],
                "admin": data["account"]["address"],
                "label": data["label"],
            }
        )
    return contract_data


def get_graphql_code_details(chain, network, code_ids):
    code_data = []
    query = "query {"
    for code_id in code_ids:
        query += f"""
        a{code_id}: codes_by_pk(id: {code_id}) {{
          account {{
            address
          }}
          cw2_contract
          cw2_version
          contract_instantiated
          access_config_permission
          access_config_addresses
        }}
        """
    query += "}"
    graphql_response = requests.post(
        GRAPHQL_DICT[chain][network], json={"query": query}
    ).json()["data"]
    for code_id, data in graphql_response.items():
        if data["account"] is None:
            data["account"] = {"address": ""}
        code_data.append(
            {
                "code_id": int(code_id[1:]),
                "cw2_contract": data["cw2_contract"],
                "cw2_version": data["cw2_version"],
                "creator": data["account"]["address"],
                "contract_instantiated": data["contract_instantiated"],
                "access_config_permission": data["access_config_permission"],
                "access_config_addresses": data["access_config_addresses"],
            }
        )
    return code_data


def get_graphql_transaction(chain, network, tx_hash, limit):
    query = f"""
        query {{
            lcd_tx_responses(where: {{hash: {{_eq: "{tx_hash}"}}}}, limit: {limit}, order_by: {{height: desc}}) {{
                result
            }}
        }}
    """
    return requests.post(GRAPHQL_TEST_DICT[chain][network], json={"query": query})


if __name__ == "__main__":
    print(
        get_graphql_code_details(
            "osmosis",
            "osmosis-1",
            [
                1,
            ],
        )
    )
