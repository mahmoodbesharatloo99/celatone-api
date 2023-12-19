from typing import Any, Dict, List

from .common import execute_query


def get_graphql_proposals_count_by_address(
    chain: str, network: str, address: str
) -> int:
    """Get the number of proposals created by an address.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        address (str): The address of the account.

    Returns:
        int: The number of proposals created by the address.
    """
    varibles = {"address": address}
    query = """
        query ($address: String!) {
            proposals_aggregate(where: {account: {address: {_eq: $address}}}) {
                aggregate {
                    count
                }
            }
        }
    """

    res = execute_query(chain, network, query, varibles).json().get("data", {})
    return res.get("proposals_aggregate", {}).get("aggregate", {}).get("count", 0)


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
            proposals_aggregate(
                where: { account: { address: { _eq: $address } } }
            ) {
                aggregate {
                    count
                }
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_related_proposals_count_by_contract_address(
    chain: str, network: str, contract_address: str
) -> int:
    """Get the number of related proposals to a contract address.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        address (str): The address of the account.

    Returns:
        int: The number of proposals created by the address.
    """
    varibles = {"contract_address": contract_address}
    query = """
        query ($contract_address: String!) {
            contract_proposals_aggregate(
                where: { contract: { address: { _eq: $contract_address } } }
            ) {
                aggregate {
                    count
                }
            }
        }
    """

    res = execute_query(chain, network, query, varibles).json().get("data", {})
    return (
        res.get("contract_proposals_aggregate", {}).get("aggregate", {}).get("count", 0)
    )
