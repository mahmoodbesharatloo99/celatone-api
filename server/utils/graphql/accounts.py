from flask import abort
from .common import execute_query


def get_graphql_account_id_by_address(chain: str, network: str, address: str) -> int:
    """Get the account ID of an address.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        address (str): The address of the account.

    Returns:
        int: The account ID.
    """
    variables = {
        "address": address,
    }
    query = """
        query ($address: String!) {
            accounts_by_pk(address: $address) {
                id
            }
        }
    """
    res = execute_query(chain, network, query, variables).json().get("data", {})
    account_id = res.get("accounts_by_pk", {}).get("id")
    if account_id is None:
        abort("Account ID not found")
    return account_id
