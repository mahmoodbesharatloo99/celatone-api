import requests
from typing import Dict, Any
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


def get_graphql_health(chain: str, network: str) -> Dict[str, Any]:
    """Get the health of the GraphQL server.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.

    Returns:
        Dict[str, Any]: The health of the GraphQL server.
    """
    query = """
        query {
            blocks(limit: 1, order_by: {height: desc}) {
                height
            }
        }
    """
    return execute_query(chain, network, query)
