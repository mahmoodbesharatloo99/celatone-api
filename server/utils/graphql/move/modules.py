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
