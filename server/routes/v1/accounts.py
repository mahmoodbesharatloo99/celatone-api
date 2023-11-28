from apiflask import APIBlueprint
from flask import abort
from adapters.aldus.accounts import AccountManager
from adapters.aldus import projects
from adapters.icns.resolver import get_icns_names
from adapters.move import modules, resources
from utils.helper import get_query_param, validate_pagination_params
from utils.graphql import accounts, codes, contracts, proposals, transactions

accounts_bp = APIBlueprint("accounts", __name__)


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/info", methods=["GET"]
)
def get_account_info(chain, network, account_address):
    public_info = AccountManager(chain, network).get_account(account_address)

    project_info = projects.get_project(chain, network, public_info.get("slug")).get(
        "details"
    )

    icns = get_icns_names(account_address)
    icns_primary_name = icns.get("primary_name")
    if len(icns_primary_name) == 0:
        icns = None

    return {"project_info": project_info, "public_info": public_info, "icns": icns}


@accounts_bp.route("/<chain>/<network>/accounts/<address>/table-count", methods=["GET"])
def get_account_table_count(chain, network, account_address):
    is_wasm = get_query_param("is_wasm", type=bool, default=False)
    account_id = accounts.get_graphql_account_id_by_address(
        chain, network, account_address
    )
    txs_count = transactions.get_graphql_account_transactions_count(
        chain, network, account_id
    )

    proposals_count = proposals.get_graphql_proposals_count_by_address(
        chain, network, account_address
    )

    if not is_wasm:
        return {"tx": txs_count, "proposal": proposals_count}

    codes_count = codes.get_graphql_codes_count_by_address(
        chain, network, account_address
    )
    instantiated_count = contracts.get_graphql_instantiated_count_by_address(
        chain, network, account_address
    )
    contract_by_admin_count = contracts.get_graphql_contract_count_by_admin(
        chain, network, account_address
    )

    return {
        "tx": txs_count,
        "proposal": proposals_count,
        "code": codes_count,
        "instantiated": instantiated_count,
        "contract_by_admin": contract_by_admin_count,
    }


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/proposals", methods=["GET"]
)
def get_proposals(chain, network, account_address):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    data = proposals.get_graphql_proposals_by_address(
        chain, network, limit, offset, account_address
    )
    for proposal in data.get("items", []):
        proposal["proposer"] = account_address
    data["total"] = data["proposals_aggregate"]["aggregate"]["count"]
    del data["proposals_aggregate"]

    return data


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/wasm/admin-contracts",
    methods=["GET"],
)
def get_admin_contracts(chain, network, account_address):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    data = contracts.get_graphql_admin_contracts_by_address(
        chain, network, limit, offset, account_address
    )
    for contract in data.get("items", []):
        contract["admin"] = contract["admin"]["address"]
        contract["instantiator"] = contract["account_by_init_by"]["address"]
        contract["latest_updater"] = contract["contract_histories"][0]["account"][
            "address"
        ]
        contract["latest_updated"] = contract["contract_histories"][0]["block"][
            "timestamp"
        ]
        contract["remark"] = contract["contract_histories"][0]["remark"]
        del contract["account_by_init_by"]
        del contract["contract_histories"]

    data["total"] = data["contracts_aggregate"]["aggregate"]["count"]
    del data["contracts_aggregate"]

    return data


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/wasm/instantiated-contracts",
    methods=["GET"],
)
def get_instantiated_contracts(chain, network, account_address):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    data = contracts.get_graphql_instantiated_by_address(
        chain,
        network,
        limit,
        offset,
        account_address,
    )
    for contract in data.get("items", []):
        contract["admin"] = contract["admin"]["address"] if contract["admin"] else None
        contract["instantiator"] = contract["account_by_init_by"]["address"]
        contract["latest_updater"] = contract["contract_histories"][0]["account"][
            "address"
        ]
        contract["latest_updated"] = contract["contract_histories"][0]["block"][
            "timestamp"
        ]
        contract["remark"] = contract["contract_histories"][0]["remark"]
        del contract["account_by_init_by"]
        del contract["contract_histories"]

    data["total"] = data["contracts_aggregate"]["aggregate"]["count"]
    del data["contracts_aggregate"]

    return data


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/wasm/codes",
    methods=["GET"],
)
def get_codes(chain, network, account_address):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    data = codes.get_graphql_codes_by_address(
        chain,
        network,
        limit,
        offset,
        account_address,
    )
    for code in data.get("items", []):
        code["uploader"] = code["account"]["uploader"]
        code["contract_count"] = code["contracts_aggregate"]["aggregate"]["count"]
        code["permission_addresses"] = code["access_config_addresses"]
        code["instantiate_permission"] = code["access_config_permission"]

        del code["account"]
        del code["access_config_addresses"]
        del code["access_config_permission"]
        del code["contracts_aggregate"]

    data["total"] = data["codes_aggregate"]["aggregate"]["count"]
    del data["codes_aggregate"]

    return data


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/move/resources",
    methods=["GET"],
)
def get_move_resources(chain, network, account_address):
    return resources.get_move_resources(chain, network, account_address)


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/move/modules",
    methods=["GET"],
)
def get_move_modules(chain, network, account_address):
    return modules.get_move_modules(chain, network, account_address)
