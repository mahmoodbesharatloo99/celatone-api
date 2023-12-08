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
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_latest_transaction_id(chain: str, network: str):
    """Get the latest transaction id.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
    Returns:
        int: The latest transaction id.
    """
    query = """
        query {
            latest: transactions(limit: 1, order_by: { id: desc }) {
                id
            }
        }
    """
    return execute_query(chain, network, query).json().get("data", {})


def get_graphql_account_transactions(
    chain: str,
    network: str,
    account_id: int,
    limit: int,
    offset: int,
    is_signer: bool | None,
    is_wasm: bool,
    is_move: bool,
    filters: dict,
):
    account_exp = {"account_id": {"_eq": account_id}}
    is_signer_exp = {"is_signer": {"_eq": is_signer}} if is_signer is not None else {}
    filter_exp = {k: {"_eq": v} for k, v in filters.items() if v}
    transaction_exp = {"transaction": {**filter_exp}} if filter_exp else {}

    variables = {
        "limit": limit,
        "offset": offset,
        "is_wasm": is_wasm,
        "is_move": is_move,
        "expression": {
            **account_exp,
            **is_signer_exp,
            **transaction_exp,
        },
    }
    query = """
        query (
            $offset: Int!
            $limit: Int!
            $expression: account_transactions_bool_exp
            $is_wasm: Boolean!
            $is_move: Boolean!
        ) {
            items: account_transactions(
                where: $expression
                order_by: { block_height: desc }
                offset: $offset
                limit: $limit
            ) {
                block {
                    height
                    timestamp
                }
                transaction {
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
                is_signer
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_account_transactions_count(
    chain: str,
    network: str,
    account_id: int | None,
    is_signer: bool | None,
    filters: dict | None,
) -> int:
    """Get the number of transactions of an account.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        account_id (int): The account ID.

    Returns:
        int: The number of transactions of the account.
    """
    if account_id is None:
        return 0

    account_exp = {"account_id": {"_eq": account_id}}
    is_signer_exp = {"is_signer": {"_eq": is_signer}} if is_signer is not None else {}
    filter_exp = {k: {"_eq": v} for k, v in filters.items() if v} if filters else {}
    transaction_exp = {"transaction": {**filter_exp}} if filter_exp else {}

    variables = {
        "expression": {
            **account_exp,
            **is_signer_exp,
            **transaction_exp,
        },
    }
    query = """
        query ($expression: account_transactions_bool_exp) {
            account_transactions_aggregate(where: $expression) {
                aggregate {
                    count
                }
            }
        }
    """
    res = execute_query(chain, network, query, variables).json().get("data", {})
    return (
        res.get("account_transactions_aggregate", {})
        .get("aggregate", {})
        .get("count", 0)
    )
