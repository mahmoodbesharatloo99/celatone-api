from flask import Blueprint
from adapters.core import transactions

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/txs/<chain>/<network>/<tx_hash>", methods=["GET"])
def get_tx(chain, network, tx_hash):
    return transactions.get_tx(chain, network, tx_hash)
