from apiflask import APIBlueprint
from utils.graphql import accounts, contracts, proposals, transactions
from utils.helper import is_graphql_timeout_error

contracts_bp = APIBlueprint("contracts", __name__)


@contracts_bp.route(
    "/<chain>/<network>/contracts/<contract_address>/table-counts", methods=["GET"]
)
def get_contract_table_counts(chain, network, contract_address):
    print("table counts")
    data = {
        "tx": None,
        "migration": None,
        "related_proposal": None,
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
        ] = contracts.get_graphql_migration_histories_by_contract_address(
            chain, network, contract_address
        )
    except Exception as e:
        print(e)
        if not is_graphql_timeout_error(e):
            del data["migration"]

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
