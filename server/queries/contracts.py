from typing import List, Dict, Any
from utils.graphql import execute_query


def get_graphql_contract_instantiator_admin(
    chain: str, network: str, contract_addresses: List[str]
) -> List[Dict[str, Any]]:
    """Get contract instantiator and admin details.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        contract_addresses (List[str]): List of contract addresses.

    Returns:
        List[Dict[str, Any]]: List of contract details.
    """
    queries = [
        f'{address}: contracts_by_pk(address: "{address}") {{ account {{ address }} accountByInitBy {{ address }} label }}'
        for address in contract_addresses
    ]
    query = "query {" + " ".join(queries) + "}"
    graphql_response = execute_query(chain, network, query).json().get("data", {})
    contract_data = [
        {
            "address": contract_address,
            "instantiator": data.get("accountByInitBy", {}).get("address", ""),
            "admin": data.get("account", {}).get("address", "")
            if data["account"] is not None
            else "",
            "label": data["label"],
        }
        for contract_address, data in graphql_response.items()
    ]
    return contract_data
