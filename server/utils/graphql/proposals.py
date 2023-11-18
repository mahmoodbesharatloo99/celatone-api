from typing import List, Dict, Any
from .common import execute_query


def get_graphql_proposals_by_address(
    chain: str, network: str, limit: int, offset: int, address: str
) -> List[Dict[str, Any]]:
    """Get proposal list by address.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        limit (int): The maximum number of responses to return.
        offset (int): The starting slice to retain from responses.
        address (str): The address of the account.
    Returns:
        List[Dict[str, Any]]: List of proposals.
    """
    variables = {
        "limit": limit,
        "offset": offset,
        "address": address,
    }
    query = """
        query (
            $address: String!
            $limit: Int!
            $offset: Int!
        ) {
            items: proposals(
                where: { account: { address: { _eq: $address } } }
                order_by: { id: desc }
                offset: $offset
                limit: $limit
            ) {
                title
                status
                voting_end_time
                deposit_end_time
                type
                id
                is_expedited
                resolved_height
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})
