from typing import Dict, Any
from utils.graphql import execute_query


def get_graphql_lcd_tx_results(
    chain: str, network: str, tx_hash: str
) -> Dict[str, Any]:
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


def get_graphql_lcd_tx_responses(
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
