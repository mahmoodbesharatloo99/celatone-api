from apiflask import APIBlueprint
from utils.graphql import accounts, contracts, proposals, transactions
from utils.helper import (
    get_query_param,
    is_graphql_timeout_error,
    validate_pagination_params,
)
from utils.rest import contracts as rest_contracts

contracts_bp = APIBlueprint("contracts", __name__)


@contracts_bp.route(
    "/<chain>/<network>/contracts/<contract_address>/table-counts", methods=["GET"]
)
def get_contract_table_counts(chain, network, contract_address):
    is_gov = get_query_param("is_gov", type=bool, default=False)

    data = {
        "tx": None,
        "migration": None,
    }

    try:
        account_id = accounts.get_graphql_account_id_by_address(
            chain, network, contract_address
        )
        data["tx"] = transactions.get_graphql_account_transactions_count(
            chain,
            network,
            account_id,
            is_wasm=False,
            search=None,
            is_signer=None,
            filters=None,
        )
    except Exception as e:
        if not is_graphql_timeout_error(e):
            del data["tx"]

    try:
        data[
            "migration"
        ] = contracts.get_graphql_migration_histories_count_by_contract_address(
            chain, network, contract_address
        )
    except Exception as e:
        if not is_graphql_timeout_error(e):
            del data["migration"]

    if is_gov:
        data["related_proposal"] = None
        try:
            data[
                "related_proposal"
            ] = proposals.get_graphql_related_proposals_count_by_contract_address(
                chain, network, contract_address
            )
        except Exception as e:
            if not is_graphql_timeout_error(e):
                del data["related_proposal"]

    return data


@contracts_bp.route(
    "/<chain>/<network>/contracts/<contract_address>/migrations", methods=["GET"]
)
def get_migrations(chain, network, contract_address):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    data = contracts.get_graphql_migration_histories_by_contract_address(
        chain, network, contract_address, limit, offset
    )

    for migration in data.get("items", []):
        migration["sender"] = migration["account"]["address"]
        migration["height"] = migration["block"]["height"]
        migration["timestamp"] = migration["block"]["timestamp"]
        migration["uploader"] = migration["code"]["account"]["address"]
        migration["cw2_contract"] = migration["code"]["cw2_contract"]
        migration["cw2_version"] = migration["code"]["cw2_version"]

        del migration["account"]
        del migration["block"]
        del migration["code"]

    return data


@contracts_bp.route(
    "/<chain>/<network>/contracts/<contract_address>/related-proposals", methods=["GET"]
)
def get_related_proposals(chain, network, contract_address):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    data = proposals.get_graphql_related_proposals_by_contract_address(
        chain, network, contract_address, limit, offset
    )
    for proposal in data.get("items", []):
        proposal["title"] = proposal["proposal"]["title"]
        proposal["status"] = proposal["proposal"]["status"]
        proposal["voting_end_time"] = proposal["proposal"]["voting_end_time"]
        proposal["deposit_end_time"] = proposal["proposal"]["deposit_end_time"]
        proposal["resolved_height"] = proposal["proposal"]["resolved_height"]
        proposal["type"] = proposal["proposal"]["type"]
        proposal["proposer"] = proposal["proposal"]["account"]["address"]
        proposal["is_expedited"] = proposal["proposal"]["is_expedited"]
        del proposal["proposal"]

    return data


@contracts_bp.route(
    "/<chain>/<network>/contracts/<contract_address>/states", methods=["GET"]
)
def get_contract_states(chain, network, contract_address):
    limit = get_query_param("limit", type=int, required=True)
    pagination_key = get_query_param("pagination_key", type=str)
    validate_pagination_params(limit, 0)

    return rest_contracts.get_rest_states(
        chain, network, contract_address, limit, pagination_key
    )
