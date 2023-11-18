from apiflask import APIBlueprint
from flask import jsonify, abort
from adapters.aldus.accounts import AccountManager
from adapters.aldus import projects
from adapters.icns.resolver import get_icns_names
from utils.helper import get_query_param
from utils.graphql.proposals import get_graphql_proposals_by_address

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


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/proposals", methods=["GET"]
)
def get_proposals(chain, network, account_address):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    if limit < 0 or offset < 0:
        abort(400, "Limit and offset must be non-negative")

    data = get_graphql_proposals_by_address(
        chain, network, limit, offset, account_address
    )
    for proposal in data.get("items", []):
        proposal["proposer"] = account_address
    return data
