from adapters.aldus import projects
from adapters.aldus.accounts import AccountManager
from adapters.core import staking
from adapters.icns.resolver import get_icns_names
from adapters.move import modules, resources
from apiflask import APIBlueprint
from utils.graphql import accounts, codes, contracts, proposals, transactions
from utils.helper import (
    get_query_param,
    is_graphql_timeout_error,
    validate_pagination_params,
)

accounts_bp = APIBlueprint("accounts", __name__)


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/info", methods=["GET"]
)
def get_account_info(chain, network, account_address):
    try:
        public_info = AccountManager(chain, network).get_account(account_address)
    except:
        public_info = None

    try:
        project_info = projects.get_project(
            chain, network, public_info.get("slug")
        ).get("details")
    except:
        project_info = None

    try:
        icns = get_icns_names(account_address)
        icns_primary_name = icns.get("primary_name")
        if len(icns_primary_name) == 0:
            icns = None
    except:
        icns = None

    return {"project_info": project_info, "public_info": public_info, "icns": icns}


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/table-counts", methods=["GET"]
)
def get_account_table_counts(chain, network, account_address):
    is_wasm = get_query_param("is_wasm", type=bool, default=False)

    data = {
        "tx": None,
        "proposal": None,
        "code": None,
        "instantiated": None,
        "contract_by_admin": None,
    }

    try:
        account_id = accounts.get_graphql_account_id_by_address(
            chain, network, account_address
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
        data["proposal"] = proposals.get_graphql_proposals_count_by_address(
            chain, network, account_address
        )
    except Exception as e:
        if not is_graphql_timeout_error(e):
            del data["proposal"]

    if not is_wasm:
        del data["code"]
        del data["instantiated"]
        del data["contract_by_admin"]

        return data

    try:
        data["code"] = codes.get_graphql_codes_count_by_address(
            chain, network, account_address
        )
    except Exception as e:
        if not is_graphql_timeout_error(e):
            del data["code"]

    try:
        data["instantiated"] = contracts.get_graphql_instantiated_count_by_address(
            chain, network, account_address
        )
    except Exception as e:
        if not is_graphql_timeout_error(e):
            del data["instantiated"]

    try:
        data["contract_by_admin"] = contracts.get_graphql_contract_count_by_admin(
            chain, network, account_address
        )
    except Exception as e:
        if not is_graphql_timeout_error(e):
            del data["contract_by_admin"]

    return data


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


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/txs",
    methods=["GET"],
)
def get_transactions(chain, network, account_address):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    search = get_query_param("search", type=str)

    # common
    is_wasm = get_query_param("is_wasm", type=bool, default=False)
    is_move = get_query_param("is_move", type=bool, default=False)
    is_initia = get_query_param("is_initia", type=bool, default=False)
    is_signer = get_query_param("is_signer", type=bool)
    is_send = get_query_param("is_send", type=bool, default=False)
    is_ibc = get_query_param("is_ibc", type=bool, default=False)

    # initia
    is_opinit = get_query_param("is_opinit", type=bool, default=False)

    # wasm
    is_execute = get_query_param("is_execute", type=bool, default=False)
    is_instantiate = get_query_param("is_instantiate", type=bool, default=False)
    is_store_code = get_query_param("is_store_code", type=bool, default=False)
    is_migrate = get_query_param("is_migrate", type=bool, default=False)
    is_update_admin = get_query_param("is_update_admin", type=bool, default=False)
    is_clear_admin = get_query_param("is_clear_admin", type=bool, default=False)

    # move
    is_move_publish = get_query_param("is_move_publish", type=bool, default=False)
    is_move_upgrade = get_query_param("is_move_upgrade", type=bool, default=False)
    is_move_excute = get_query_param("is_move_excute", type=bool, default=False)
    is_move_script = get_query_param("is_move_script", type=bool, default=False)

    account_id = accounts.get_graphql_account_id_by_address(
        chain, network, account_address
    )

    if account_id is None:
        return {"items": []}

    data = transactions.get_graphql_account_transactions(
        chain=chain,
        network=network,
        account_id=account_id,
        limit=limit,
        offset=offset,
        is_wasm=is_wasm,
        is_move=is_move,
        is_initia=is_initia,
        search=search,
        is_signer=is_signer,
        filters={
            "is_send": is_send,
            "is_ibc": is_ibc,
            "is_execute": is_execute,
            "is_instantiate": is_instantiate,
            "is_store_code": is_store_code,
            "is_migrate": is_migrate,
            "is_update_admin": is_update_admin,
            "is_clear_admin": is_clear_admin,
            "is_move_publish": is_move_publish,
            "is_move_upgrade": is_move_upgrade,
            "is_move_excute": is_move_excute,
            "is_move_script": is_move_script,
            "is_opinit": is_opinit,
        },
    )
    for tx in data.get("items", []):
        tx["height"] = tx["block"]["height"]
        tx["created"] = tx["block"]["timestamp"]
        tx["hash"] = tx["transaction"]["hash"]
        tx["messages"] = tx["transaction"]["messages"]
        tx["sender"] = tx["transaction"]["account"]["address"]
        tx["success"] = tx["transaction"]["success"]
        tx["is_send"] = tx["transaction"]["is_send"]
        tx["is_ibc"] = tx["transaction"]["is_ibc"]

        if is_wasm:
            tx["is_clear_admin"] = tx["transaction"]["is_clear_admin"]
            tx["is_execute"] = tx["transaction"]["is_execute"]
            tx["is_instantiate"] = tx["transaction"]["is_instantiate"]
            tx["is_migrate"] = tx["transaction"]["is_migrate"]
            tx["is_store_code"] = tx["transaction"]["is_store_code"]
            tx["is_update_admin"] = tx["transaction"]["is_update_admin"]

        if is_move:
            tx["is_move_publish"] = tx["transaction"]["is_move_publish"]
            tx["is_move_upgrade"] = tx["transaction"]["is_move_upgrade"]
            tx["is_move_execute"] = tx["transaction"]["is_move_execute"]
            tx["is_move_script"] = tx["transaction"]["is_move_script"]

        if is_initia:
            tx["is_opinit"] = tx["transaction"]["is_opinit"]

        del tx["block"]
        del tx["transaction"]

    return data


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/txs-count",
    methods=["GET"],
)
def get_transactions_count(chain, network, account_address):
    # common
    is_wasm = get_query_param("is_wasm", type=bool, default=False)
    is_signer = get_query_param("is_signer", type=bool)
    is_send = get_query_param("is_send", type=bool, default=False)
    is_ibc = get_query_param("is_ibc", type=bool, default=False)

    search = get_query_param("search", type=str)

    # wasm
    is_execute = get_query_param("is_execute", type=bool, default=False)
    is_instantiate = get_query_param("is_instantiate", type=bool, default=False)
    is_store_code = get_query_param("is_store_code", type=bool, default=False)
    is_migrate = get_query_param("is_migrate", type=bool, default=False)
    is_update_admin = get_query_param("is_update_admin", type=bool, default=False)
    is_clear_admin = get_query_param("is_clear_admin", type=bool, default=False)

    # move
    is_move_publish = get_query_param("is_move_publish", type=bool, default=False)
    is_move_upgrade = get_query_param("is_move_upgrade", type=bool, default=False)
    is_move_excute = get_query_param("is_move_excute", type=bool, default=False)
    is_move_script = get_query_param("is_move_script", type=bool, default=False)

    data = {"count": None}

    try:
        account_id = accounts.get_graphql_account_id_by_address(
            chain, network, account_address
        )
        data["count"] = transactions.get_graphql_account_transactions_count(
            chain=chain,
            network=network,
            account_id=account_id,
            is_wasm=is_wasm,
            search=search,
            is_signer=is_signer,
            filters={
                "is_send": is_send,
                "is_ibc": is_ibc,
                "is_execute": is_execute,
                "is_instantiate": is_instantiate,
                "is_store_code": is_store_code,
                "is_migrate": is_migrate,
                "is_update_admin": is_update_admin,
                "is_clear_admin": is_clear_admin,
                "is_move_publish": is_move_publish,
                "is_move_upgrade": is_move_upgrade,
                "is_move_excute": is_move_excute,
                "is_move_script": is_move_script,
            },
        )
    except Exception as e:
        if not is_graphql_timeout_error(e):
            del data["count"]

    return data


@accounts_bp.route(
    "/<chain>/<network>/accounts/<account_address>/delegations",
    methods=["GET"],
)
def get_delegations(chain, network, account_address):
    return staking.get_delegations_by_address(chain, network, account_address)
