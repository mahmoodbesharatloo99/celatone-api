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
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_latest_block(chain: str, network: str):
    """Get the latest block.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
    Returns:
        int: The latest block.
    """
    query = """
        query {
            latest: blocks(limit: 1, order_by: { height: desc }) {
                height
                timestamp
            }
        }
    """
    return execute_query(chain, network, query).json().get("data", {})


def get_graphql_latest_informative_block(chain: str, network: str):
    """Get the latest block.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
    Returns:
        int: The latest informative block.
    """
    query = """
        query {
            latest: tracking {
                height: latest_informative_block_height
            }
        }
    """
    return execute_query(chain, network, query).json().get("data", {})


def get_graphql_block_times(chain: str, network: str):
    """Get the list of block times
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
    Returns:
        str[]: The list of block timestamps
    """
    if chain == "sei":
        data = get_graphql_latest_informative_block(chain, network)
    else:
        data = get_graphql_latest_block(chain, network)

    variables = {
        "max_height": data["latest"][0]["height"],
    }
    query = """
        query (
            $max_height: Int!
        ) {
            blocks(where: { height: { _lte: $max_height } }, limit: 100, order_by: { height: desc }) {
                timestamp
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_block_details(chain: str, network: str, height: int):
    """Get block details.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        height (int): Height of the queried block

    Returns:
        Dict[str, Any]: List of blocks and the current latest block height.
    """
    variables = {
        "height": height,
    }
    query = """
        query (
            $height: Int!
        ) {
            blocks_by_pk(height: $height) {
                hash
                height
                timestamp
                transactions_aggregate {
                    aggregate {
                        sum {
                            gas_used
                            gas_limit
                        }
                    }
                }
                validator {
                    moniker
                    operator_address
                    identity
                }
            }
        }
    """
    return (
        execute_query(chain, network, query, variables)
        .json()
        .get("data", {})
        .get("blocks_by_pk", {})
    )
