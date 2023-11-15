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
    query = f"""
        query {{
            blocks(limit: {limit}, offset: {offset}, order_by: {{ height: desc }}) {{
                hash
                height
                timestamp
                transactions_aggregate {{
                    aggregate {{
                    count
                    }}
                }}
                validator {{
                    moniker
                    operator_address
                    identity
                }}
            }}
            total: blocks(limit: 1, order_by: {{ height: desc }}) {{
                height
            }}
        }}
    """
    return execute_query(chain, network, query).json().get("data", {})
