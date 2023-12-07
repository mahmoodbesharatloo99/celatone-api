from utils.graphql.common import execute_query


def get_graphql_modules(chain: str, network: str, limit: int, offset: int):
    """Get a list of modules.
    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        limit (int): The maximum number of responses to return.
        offset (int): The starting slice to retain from responses.
    Returns:
        Dict[str, Any]: List of modules and the total count.
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
            items: modules(
                limit: $limit
                offset: $offset
                order_by: { id: desc }
            ) {
                name
                vm_address {
                    accounts {
                        address
                    }
                }
                module_histories(order_by: { block_height: desc }, limit: 1) {
                    block {
                        height
                        timestamp
                    }
                }
                module_histories_aggregate {
                    aggregate {
                        count
                    }
                }
                is_verify
            }
            latest: modules(limit: 1, order_by: { id: desc }) {
                id
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_module_id(
    chain: str, network: str, vm_address: str, name: str
) -> int | None:
    """Get the module ID of a module.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        vm_address (str): The vm_address of the module.
        name (str): The name of the module.
    Returns:
        int: The module ID.
    """
    variables = {
        "vm_address": vm_address,
        "name": name,
    }
    query = """
        query (
            $vm_address: String!
            $name: String!
        ) {
            modules(
                where: {
                    vm_address: { vm_address: { _eq: $vm_address } }
                    name: { _eq: $name }
                }
            ) {
                id
            }
        }
    """
    res = execute_query(chain, network, query, variables).json()
    modules_data = res.get("data", {}).get("modules")
    return modules_data[0].get("id") if len(modules_data) > 0 else None


def get_graphql_module_txs(
    chain: str,
    network: str,
    module_id: int,
    limit: int,
    offset: int,
    is_initia: bool,
):
    print(module_id, limit, offset, is_initia)
    variables = {
        "module_id": module_id,
        "limit": limit,
        "offset": offset,
        "is_initia": is_initia,
    }
    query = """
        query (
            $module_id: Int!
            $limit: Int!
            $offset: Int!
            $is_initia: Boolean!
        ) {
            items: module_transactions(
                where: { module_id: { _eq: $module_id } }
                limit: $limit
                offset: $offset
                order_by: { block_height: desc }
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
                    is_move_execute
                    is_move_execute_event
                    is_move_publish
                    is_move_script
                    is_move_upgrade
                    is_opinit @include(if: $is_initia)
                }
            }
            module_transactions_aggregate(where: { module_id: { _eq: $module_id } }) {
                aggregate {
                    count
                }
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})
