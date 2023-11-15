from .common import execute_query


def get_graphql_transactions(
    chain: str, network: str, is_wasm: bool, is_move: bool, limit: int, offset: int
):
    """Get transaction list.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        is_wasm (bool): The flag specifying if wasm-related columns are needed.
        is_move (bool): The flag specifying if move-related columns are needed.
        limit (int): The maximum number of responses to return.
        offset (int): The starting slice to retain from responses.
    Returns:
        Dict[str, Any]: List of transactions and the latest transaction id.
    """
    query = f"""
        query {{
            items: transactions(
            offset: {offset}
            limit: {limit}
            order_by: {{ block_height: desc }}
            ) {{
                block {{
                    height
                    timestamp
                }}
                account {{
                    address
                }}
                hash
                success
                messages
                is_send
                is_ibc
                {
                    '''
                    is_clear_admin 
                    is_execute
                    is_instantiate 
                    is_migrate
                    is_store_code 
                    is_update_admin
                    ''' if is_wasm else ''
                }
                {
                    '''
                    is_move_publish 
                    is_move_upgrade
                    is_move_execute 
                    is_move_script
                    ''' if is_move else ''
                }
            }}
            latest: transactions(limit: 1, order_by: {{ id: desc }}) {{
                id
            }}
        }}
    """
    res = execute_query(chain, network, query).json()
    if res.get("errors") is not None:
        raise Exception(res.get("errors"))
    return res.get("data", {})
