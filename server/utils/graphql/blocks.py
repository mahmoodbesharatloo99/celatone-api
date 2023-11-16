from .common import execute_query


def get_graphql_blocks(chain: str, network: str, limit: int, offset: int):
    """Get block list.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        limit (int): The maximum number of responses to return.
        offset (int): The starting slice to retain from responses.

    Returns:
        Dict[str, Any]: List of blocks and the current latest block height.
    """
    variables = {
        "limit": limit,
        "offset": offset,
    }
    query = """
        query (
            $limit: Int!
            $offset: Int!
        ) {
            items: blocks(limit: $limit, offset: $offset, order_by: { height: desc }) {
                hash
                height
                timestamp
                transactions_aggregate {
                    aggregate {
                    count
                    }
                }
                validator {
                    moniker
                    operator_address
                    identity
                }
            }
            latest: blocks(limit: 1, order_by: { height: desc }) {
                height
            }
        }
    """
    res = execute_query(chain, network, query, variables).json()
    if res.get("errors") is not None:
        raise Exception(res.get("errors"))
    return res.get("data", {})
