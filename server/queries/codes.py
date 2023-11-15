from typing import List, Dict, Any
from utils.graphql import execute_query


def generate_code_query(code_id: str) -> str:
    """Generate a GraphQL query for a code.

    Args:
        code_id (str): The ID of the code.

    Returns:
        str: The generated GraphQL query.
    """
    return f"a{code_id}: codes_by_pk(id: {code_id}) {{\n  account {{\n    address\n  }}\n  cw2_contract\n  cw2_version\n  contract_instantiated\n  access_config_permission\n  access_config_addresses\n}}"


def get_graphql_code_details(
    chain: str, network: str, code_ids: List[str]
) -> List[Dict[str, Any]]:
    """Get details of multiple codes.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        code_ids (List[str]): List of code IDs.

    Returns:
        List[Dict[str, Any]]: List of code details.
    """
    query = "\n".join(generate_code_query(code_id) for code_id in code_ids)
    graphql_response = (
        execute_query(chain, network, f"query {{\n{query}\n}}").json().get("data", {})
    )
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
        for code_id, data in graphql_response.items()
    ]
    return code_data
