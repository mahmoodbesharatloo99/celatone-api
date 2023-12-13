from apiflask import APIBlueprint
from utils.graphql.blocks import get_graphql_block_details, get_graphql_blocks
from utils.graphql.transactions import get_graphql_block_transactions
from utils.helper import get_query_param, validate_pagination_params

blocks_bp = APIBlueprint("blocks", __name__)


@blocks_bp.route("/<chain>/<network>/blocks", methods=["GET"])
def get_blocks(chain, network):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    validate_pagination_params(limit, offset)

    data = get_graphql_blocks(chain, network, limit, offset)
    for block in data.get("items", []):
        block["transaction_count"] = block["transactions_aggregate"]["aggregate"][
            "count"
        ]
        del block["transactions_aggregate"]
    data["total"] = data["latest"][0]["height"]
    del data["latest"]

    return data


@blocks_bp.route("/<chain>/<network>/blocks/<height>/details", methods=["GET"])
def get_block_details(chain, network, height):
    data = get_graphql_block_details(chain, network, height)

    gas = data.get("transactions_aggregate", {}).get("aggregate", {}).get("sum", {})
    # NOTE: null if no txs in a block
    data["gas_used"] = gas.get("gas_used")
    data["gas_limit"] = gas.get("gas_limit")
    del data["transactions_aggregate"]

    return data


@blocks_bp.route("/<chain>/<network>/blocks/<height>/txs", methods=["GET"])
def get_txs(chain, network, height):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    is_wasm = get_query_param("is_wasm", type=bool, default=False)
    is_move = get_query_param("is_move", type=bool, default=False)
    is_initia = get_query_param("is_initia", type=bool, default=False)
    validate_pagination_params(limit, offset)

    data = get_graphql_block_transactions(
        chain, network, height, limit, offset, is_wasm, is_move, is_initia
    )
    for tx in data.get("items", []):
        tx["height"] = tx["block"]["height"]
        tx["created"] = tx["block"]["timestamp"]
        tx["sender"] = tx["account"]["address"]
        del tx["account"]
        del tx["block"]
    data["total"] = data["latest"].get("aggregate", {}).get("count")
    del data["latest"]

    return data
