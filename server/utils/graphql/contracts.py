from typing import Any, Dict, List

from .common import execute_query


def get_graphql_contract_instantiator_admin(
    chain: str, network: str, contract_addresses: List[str]
) -> List[Dict[str, Any]]:
    """Get contract instantiator and admin details.

    Args:
        chain (str): The blockchain chain.
        network (str): The blockchain network.
        contract_addresses (List[str]): List of contract addresses.

    Returns:
        List[Dict[str, Any]]: List of contract details.
    """
    queries = [
        f'{address}: contracts_by_pk(address: "{address}") {{ account {{ address }} accountByInitBy {{ address }} label }}'
        for address in contract_addresses
    ]
    query = "query {" + " ".join(queries) + "}"
    graphql_response = execute_query(chain, network, query).json().get("data", {})
    contract_data = [
        {
            "address": contract_address,
            "instantiator": data.get("accountByInitBy", {}).get("address", ""),
            "admin": data.get("account", {}).get("address", "")
            if data["account"] is not None
            else "",
            "label": data["label"],
        }
        for contract_address, data in graphql_response.items()
    ]
    return contract_data


def get_graphql_admin_contracts_by_address(
    chain: str, network: str, address: str, limit: int, offset: int
):
    variables = {
        "address": address,
        "limit": limit,
        "offset": offset,
    }
    query = """
        query (
            $address: String!
            $limit: Int!
            $offset: Int!
        ) {
            items: contracts(
                where: { account: { address: { _eq: $address } } }
                limit: $limit
                offset: $offset
                order_by: { transaction: { block: { timestamp: desc } } }
            ) {
                contract_address: address
                label
                admin: account {
                    address
                }
                account_by_init_by: accountByInitBy {
                    address
                }
                contract_histories(order_by: { block: { timestamp: desc } }, limit: 1) {
                    block {
                        timestamp
                    }
                    account {
                        address
                    }
                    remark
                }
            }
            contracts_aggregate(where: { account: { address: { _eq: $address } } }) {
                aggregate {
                    count
                }
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_contract_count_by_admin(chain: str, network: str, address: str) -> int:
    variables = {
        "address": address,
    }
    query = """
        query ($address: String!) {
            contracts_aggregate(where: { account: { address: { _eq: $address } } }) {
                aggregate {
                    count
                }
            }
        }
    """
    res = execute_query(chain, network, query, variables).json().get("data", {})
    return res.get("contracts_aggregate", {}).get("aggregate", {}).get("count", 0)


def get_graphql_instantiated_by_address(
    chain: str, network: str, address: str, limit: int, offset: int
):
    variables = {
        "address": address,
        "limit": limit,
        "offset": offset,
    }
    query = """
        query (
            $address: String!
            $limit: Int!
            $offset: Int!
        ) {
            items: contracts(
                where: { accountByInitBy: { address: { _eq: $address } } }
                limit: $limit
                offset: $offset
                order_by: {
                    contract_histories_aggregate: { max: { block_height: desc } }
                }
            ) {
                contract_address: address
                label
                admin: account {
                    address
                }
                account_by_init_by: accountByInitBy {
                    address
                }
                contract_histories(order_by: { block: { timestamp: desc } }, limit: 1) {
                    block {
                        timestamp
                    }
                    account {
                        address
                    }
                    remark
                }
            }
            contracts_aggregate(where: { accountByInitBy: { address: { _eq: $address } } }) {
                aggregate {
                    count
                }
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_instantiated_count_by_address(
    chain: str, network: str, address: str
) -> int:
    variables = {
        "address": address,
    }
    query = """
        query ($address: String!) {
            contracts_aggregate(where: { accountByInitBy: { address: { _eq: $address } } }) {
                aggregate {
                    count
                }
            }
        }
    """
    res = execute_query(chain, network, query, variables).json().get("data", {})
    return res.get("contracts_aggregate", {}).get("aggregate", {}).get("count", 0)


def get_graphql_migration_histories_by_contract_address(
    chain: str,
    network: str,
    contract_address: str,
    limit: int,
    offset: int,
) -> int:
    variables = {
        "contract_address": contract_address,
        "limit": limit,
        "offset": offset,
    }
    query = """
        query (
            $contract_address: String!
            $limit: Int!
            $offset: Int!
        ) {
            items: contract_histories(
                where: { contract: { address: { _eq: $contract_address } } }
                limit: $limit
                offset: $offset
                order_by: { block: { timestamp: desc } }
            ) {
                code_id
                account {
                    address
                }
                block {
                    height
                    timestamp
                }
                remark
                code {
                    account {
                        address
                    }
                    cw2_contract
                    cw2_version
                }
            }
        }
    """
    return execute_query(chain, network, query, variables).json().get("data", {})


def get_graphql_migration_histories_count_by_contract_address(
    chain: str, network: str, contract_address: str
) -> int:
    variables = {
        "contract_address": contract_address,
    }
    query = """
        query ($contract_address: String!) {
            contract_histories_aggregate(
                where: { contract: { address: { _eq: $contract_address } } }
            ) {
                aggregate {
                    count
                }
            }
        }
    """
    res = execute_query(chain, network, query, variables).json().get("data", {})
    return (
        res.get("contract_histories_aggregate", {}).get("aggregate", {}).get("count", 0)
    )
