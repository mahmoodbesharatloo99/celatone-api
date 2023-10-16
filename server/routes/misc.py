from flask import Blueprint, request
from adapters.core import misc, balances

misc_bp = Blueprint("misc", __name__)

# Balances


@misc_bp.route("/balances/<chain>/<network>/<account_address>", methods=["GET"])
def get_balances(chain, network, account_address):
    return balances.get_balances(chain, network, account_address)


# Cosmos Rest


@misc_bp.route("/rest/<chain>/<network>/<path:path>", methods=["GET"])
def get_rest(chain, network, path):
    return misc.get_rest(chain, network, path, request.args)
