from typing import Dict, Any
from .common import execute_query


def get_graphql_validators(chain: str, network: str) -> Dict[str, Any]:
    """Get the validators of the blockchain.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.

    Returns:
        Dict[str, Any]: The validators of the blockchain.
    """
    query = """
        query {
            validators {
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
            }
        }
    """
    return execute_query(chain, network, query).json().get("data", {})
