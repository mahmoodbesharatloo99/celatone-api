from utils.helper import is_txhash

from .common import execute_query


def get_graphql_transactions(
    chain: str,
    network: str,
    limit: int,
    offset: int,
    is_wasm: bool,
    is_move: bool,
    is_initia: bool,
):
    """Get transaction list.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        limit (int): The maximum number of responses to return.
        offset (int): The starting slice to retain from responses.
        is_wasm (bool): The flag specifying if wasm-related columns are needed.
        is_move (bool): The flag specifying if move-related columns are needed.
        is_initia (bool): The flag specifying if opinit column is needed
    Returns:
        Dict[str, Any]: List of transactions and the latest transaction id.
    """
    variables = {
        "limit": limit,
        "offset": offset,
        "is_wasm": is_wasm,
        "is_move": is_move,
        "is_initia": is_initia,
    }
    query = """
        query (
            $limit: Int!
            $offset: Int!
            $is_wasm: Boolean!
            $is_move: Boolean!
            $is_initia: Boolean!
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
                is_opinit @include(if: $is_initia)
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


def get_graphql_block_transactions(
    chain: str,
    network: str,
    height: int,
    limit: int,
    offset: int,
    is_wasm: bool,
    is_move: bool,
    is_initia: bool,
):
    """Get block transaction list.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        limit (int): The maximum number of responses to return.
        offset (int): The starting slice to retain from responses.
        is_wasm (bool): The flag specifying if wasm-related columns are needed.
        is_move (bool): The flag specifying if move-related columns are needed.
        is_initia (bool): The flag specifying if opinit column is needed
    Returns:
        Dict[str, Any]: List of transactions and the latest transaction id.
    """
    variables = {
        "height": height,
        "limit": limit,
        "offset": offset,
        "is_wasm": is_wasm,
        "is_move": is_move,
        "is_initia": is_initia,
    }
    query = """
        query (
            $height: Int!
            $limit: Int!
            $offset: Int!
            $is_wasm: Boolean!
            $is_move: Boolean!
            $is_initia: Boolean!
        ) {
            items: transactions(
                limit: $limit
                offset: $offset
                where: { block_height: { _eq: $height } }
                order_by: { id: asc }
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
                is_opinit @include(if: $is_initia)
            }
            transactions_aggregate(where: { block_height: { _eq: $height } }) {
                aggregate {
                    count
                }
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_account_transactions(
    chain: str,
    network: str,
    account_id: int,
    limit: int,
    offset: int,
    is_wasm: bool,
    is_move: bool,
    is_initia: bool,
    search: str | None,
    is_signer: bool | None,
    filters: dict,
):
    account_exp = {"account_id": {"_eq": account_id}}
    is_signer_exp = {"is_signer": {"_eq": is_signer}} if is_signer is not None else {}
    filter_exp = {k: {"_eq": v} for k, v in filters.items() if v}

    search_exp = []
    if search:
        search_exp.append(
            {"hash": {"_eq": f"\\x{search}" if is_txhash(search) else ""}}
        )
        if is_wasm:
            search_exp.append(
                {"contract_transactions": {"contract": {"address": {"_eq": search}}}}
            )

    transaction_exp = {
        "transaction": {
            **({**filter_exp} if filter_exp else {}),
            **({"_or": search_exp} if search else {}),
        }
    }

    variables = {
        "limit": limit,
        "offset": offset,
        "is_wasm": is_wasm,
        "is_move": is_move,
        "is_initia": is_initia,
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
            $is_initia: Boolean!
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
                    is_opinit @include(if: $is_initia)
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
    is_wasm: bool,
    search: str | None,
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

    search_exp = []
    if search:
        search_exp.append(
            {"hash": {"_eq": f"\\x{search}" if is_txhash(search) else ""}}
        )
        if is_wasm:
            search_exp.append(
                {"contract_transactions": {"contract": {"address": {"_eq": search}}}}
            )

    transaction_exp = {
        "transaction": {
            **({**filter_exp} if filter_exp else {}),
            **({"_or": search_exp} if search else {}),
        }
    }

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
