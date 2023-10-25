import requests
from typing import List, Dict, Any
from utils.gcs import get_network_data


def execute_query(
    chain: str, network: str, query: str, endpoint: str = "graphql"
) -> Dict[str, Any]:
    """Execute a GraphQL query.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        query (str): The GraphQL query to execute.
        endpoint (str, optional): The endpoint to send the request to. Defaults to "graphql".

    Returns:
        Dict[str, Any]: The response from the GraphQL server.
    """
    response = requests.post(
        get_network_data(chain, network, endpoint), json={"query": query}
    )
    response.raise_for_status()
    return response


def get_contract_instantiator_admin(
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


def get_lcd_tx_results(chain: str, network: str, tx_hash: str) -> Dict[str, Any]:
    """Get LCD transaction results.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        tx_hash (str): The transaction hash.

    Returns:
        Dict[str, Any]: The LCD transaction results.
    """
    query = f"""
        query {{
            lcd_tx_results(where: {{transaction: {{hash: {{_eq: "\\\\x{tx_hash}"}}}}}}) {{
                result
            }}
        }}
    """
    return execute_query(chain, network, query).json().get("data", {})


def get_lcd_tx_responses(
    chain: str, network: str, tx_hash: str, limit: int
) -> Dict[str, Any]:
    """Get LCD transaction responses.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        tx_hash (str): The transaction hash.
        limit (int): The maximum number of responses to return.

    Returns:
        Dict[str, Any]: The LCD transaction responses.
    """
    query = f"""
        query {{
            lcd_tx_responses(where: {{hash: {{_eq: "{tx_hash}"}}}}, limit: {limit}, order_by: {{height: desc}}) {{
                result
            }}
        }}
    """
    return execute_query(chain, network, query, "graphql_test").json().get("data", {})


def get_graphql_health(chain: str, network: str) -> Dict[str, Any]:
    """Get the health of the GraphQL server.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.

    Returns:
        Dict[str, Any]: The health of the GraphQL server.
    """
    query = f"""
        query {{
            blocks(limit: 1, order_by: {{height: desc}}) {{
                height
            }}
        }}
    """
    return execute_query(chain, network, query)


def get_graphql_validators(chain: str, network: str) -> Dict[str, Any]:
    """Get the validators of the blockchain.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.

    Returns:
        Dict[str, Any]: The validators of the blockchain.
    """
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
    return execute_query(chain, network, query).json().get("data", {})
