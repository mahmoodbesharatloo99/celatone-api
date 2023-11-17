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
