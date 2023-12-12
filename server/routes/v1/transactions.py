from adapters.core import transactions
from apiflask import APIBlueprint
from utils.graphql.transactions import get_graphql_transactions
from utils.helper import get_query_param, validate_pagination_params

transactions_bp = APIBlueprint("transactions", __name__)


@transactions_bp.route("/<chain>/<network>/txs", methods=["GET"])
def get_txs(chain, network):
    limit = get_query_param("limit", type=int, required=True)
    offset = get_query_param("offset", type=int, required=True)
    is_wasm = get_query_param("is_wasm", type=bool, default=False)
    is_move = get_query_param("is_move", type=bool, default=False)
    is_initia = get_query_param("is_initia", type=bool, default=False)
    validate_pagination_params(limit, offset)

    data = get_graphql_transactions(
        chain, network, limit, offset, is_wasm, is_move, is_initia
    )
    for tx in data.get("items", []):
        tx["height"] = tx["block"]["height"]
        tx["created"] = tx["block"]["timestamp"]
        tx["sender"] = tx["account"]["address"]
        del tx["account"]
        del tx["block"]
    data["total"] = data["latest"][0]["id"]
    del data["latest"]

    return data


@transactions_bp.route("/<chain>/<network>/txs/<tx_hash>", methods=["GET"])
def get_tx(chain, network, tx_hash):
    return transactions.get_tx(chain, network, tx_hash)
