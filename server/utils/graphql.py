import requests
from utils.constants import GRAPHQL_DICT, GRAPHQL_TEST_DICT


def get_contract_instantiator_admin(chain, network, contract_addresses):
    contract_data = []
    queries = [
        f'{address}: contracts_by_pk(address: "{address}") {{ account {{ address }} accountByInitBy {{ address }} label }}'
        for address in contract_addresses
    ]
    query = "query {" + " ".join(queries) + "}"
    res = requests.post(GRAPHQL_DICT[chain][network], json={"query": query})
    res.raise_for_status()
    graphql_response = res.json()["data"]
    for contract_address, data in graphql_response.items():
        contract_data.append(
            {
                "address": contract_address,
                "instantiator": data.get("accountByInitBy", {}).get("address", ""),
                "admin": data.get("account", {}).get("address", "") if data["account"] is not None else "",
                "label": data["label"],
            }
        )
    return contract_data


def generate_code_query(code_id):
    return f"a{code_id}: codes_by_pk(id: {code_id}) {{\n  account {{\n    address\n  }}\n  cw2_contract\n  cw2_version\n  contract_instantiated\n  access_config_permission\n  access_config_addresses\n}}"


def get_graphql_code_details(chain, network, code_ids):
    query = "\n".join(generate_code_query(code_id) for code_id in code_ids)
    graphql_response = requests.post(GRAPHQL_DICT[chain][network], json={"query": f"query {{\n{query}\n}}"})
    graphql_data = graphql_response.json().get("data") or {}
    code_data = [
        {
            "code_id": int(code_id[1:]),
            "cw2_contract": data.get("cw2_contract", ""),
            "cw2_version": data.get("cw2_version", ""),
            "creator": data.get("account", {}).get("address", ""),
            "contract_instantiated": data.get("contract_instantiated", []),
            "access_config_permission": data.get("access_config_permission", ""),
            "access_config_addresses": data.get("access_config_addresses", []),
        }
        for code_id, data in graphql_data.items()
    ]
    return code_data


def get_lcd_tx_results(chain, network, tx_hash):
    query = f"""
        query {{
            lcd_tx_results(where: {{transaction: {{hash: {{_eq: "\\\\x{tx_hash}"}}}}}}) {{
                result
            }}
        }}
    """
    return requests.post(GRAPHQL_DICT[chain][network], json={"query": query})


def get_lcd_tx_responses(chain, network, tx_hash, limit):
    query = f"""
        query {{
            lcd_tx_responses(where: {{hash: {{_eq: "{tx_hash}"}}}}, limit: {limit}, order_by: {{height: desc}}) {{
                result
            }}
        }}
    """
    return requests.post(GRAPHQL_TEST_DICT[chain][network], json={"query": query})


def get_graphql_health(chain, network):
    query = f"""
        query {{
            blocks(limit: 1, order_by: {{height: desc}}) {{
                height
            }}
        }}
    """
    return requests.post(GRAPHQL_DICT[chain][network], json={"query": query})


def get_graphql_validators(chain, network):
    query = f"""
        query {{
            validators {{
            commission_max_change
            commission_max_rate
            commission_rate
            consensus_address
            details
            identity
            jailed
            moniker
            operator_address
            website
            }}
        }}
    """
    return requests.post(GRAPHQL_DICT[chain][network], json={"query": query})
