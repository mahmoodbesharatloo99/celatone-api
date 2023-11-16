from adapters.core import balances, misc
from apiflask import APIBlueprint
from flask import request

misc_bp = APIBlueprint("misc", __name__)

# Balances


@misc_bp.route("/balances/<chain>/<network>/<account_address>", methods=["GET"])
def get_balances(chain, network, account_address):
    return balances.get_balances_legacy(chain, network, account_address)


# Cosmos Rest


@misc_bp.route("/rest/<chain>/<network>/<path:path>", methods=["GET", "POST"])
def get_rest(chain, network, path):
    if request.method == "GET":
        return misc.get_rest(chain, network, path, request.args)
    if request.method == "POST":
        return misc.post_rest(chain, network, path, request.data)
