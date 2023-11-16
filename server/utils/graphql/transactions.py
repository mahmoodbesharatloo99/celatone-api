from .common import execute_query


def get_graphql_transactions(
    chain: str, network: str, limit: int, offset: int, is_wasm: bool, is_move: bool
):
    """Get transaction list.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        limit (int): The maximum number of responses to return.
        offset (int): The starting slice to retain from responses.
        is_wasm (bool): The flag specifying if wasm-related columns are needed.
        is_move (bool): The flag specifying if move-related columns are needed.
    Returns:
        Dict[str, Any]: List of transactions and the latest transaction id.
    """
    variables = {
        "limit": limit,
        "offset": offset,
        "is_wasm": is_wasm,
        "is_move": is_move,
    }
    query = """
        query (
            $limit: Int!
            $offset: Int!
            $is_wasm: Boolean!
            $is_move: Boolean!
        ) {
            items: transactions(
            limit: $limit
            offset: $offset
            order_by: { block_height: desc }
            ) {
                block {
                    height
                    timestamp
                }
                account {
                    address
                }
                hash
                success
                messages
                is_send
                is_ibc
                is_clear_admin @include(if: $is_wasm)
                is_execute @include(if: $is_wasm)
                is_instantiate @include(if: $is_wasm)
                is_migrate @include(if: $is_wasm)
                is_store_code @include(if: $is_wasm)
                is_update_admin @include(if: $is_wasm)
                is_move_publish @include(if: $is_move)
                is_move_upgrade @include(if: $is_move)
                is_move_execute @include(if: $is_move)
                is_move_script @include(if: $is_move)
            }
            latest: transactions(limit: 1, order_by: { id: desc }) {
                id
            }
        }
    """
    res = execute_query(chain, network, query, variables).json()
    if res.get("errors") is not None:
        raise Exception(res.get("errors"))
    return res.get("data", {})
