from apiflask import APIBlueprint
from flask import jsonify
from adapters.aldus.accounts import AccountManager
from adapters.aldus import projects
from adapters.icns.resolver import get_icns_names
from utils.graphql.accounts import get_graphql_account_id_by_address
from utils.graphql.contracts import (
    get_graphql_instantiated_count_by_address,
    get_graphql_contract_count_by_admin,
)
from utils.graphql.codes import get_graphql_codes_count_by_address
from utils.graphql.proposals import get_graphql_proposals_count_by_address
from utils.graphql.transactions import get_graphql_account_transactions_count

accounts_bp = APIBlueprint("accounts", __name__)


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/info", methods=["GET"]
)
def get_account_info(chain, network, account_address):
    try:
        public_info = AccountManager(chain, network).get_account(account_address)

        project_info = projects.get_project(
            chain, network, public_info.get("slug")
        ).get("details")

        icns = get_icns_names(account_address)
        icns_primary_name = icns.get("primary_name")
        if len(icns_primary_name) == 0:
            icns = None

    except Exception as e:
        return jsonify(error=str(e)), 500

    return {"project_info": project_info, "public_info": public_info, "icns": icns}, 200


@accounts_bp.route("/<chain>/<network>/accounts/<address>/table-count", methods=["GET"])
def get_account_table_count(chain, network, account_address):
    account_id = get_graphql_account_id_by_address(chain, network, account_address)
    txs_count = get_graphql_account_transactions_count(chain, network, account_id)

    codes_count = get_graphql_codes_count_by_address(chain, network, account_address)

    proposals_count = get_graphql_proposals_count_by_address(
        chain, network, account_address
    )
    instantiated_count = get_graphql_instantiated_count_by_address(
        chain, network, account_address
    )
    contract_by_admin_count = get_graphql_contract_count_by_admin(
        chain, network, account_address
    )
    return {
        "tx": txs_count,
        "proposal": proposals_count,
        "code": codes_count,
        "instantiated": instantiated_count,
        "contract_by_admin": contract_by_admin_count,
    }, 200
