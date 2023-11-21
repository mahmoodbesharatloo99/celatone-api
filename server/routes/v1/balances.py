from adapters.core import balances
from apiflask import APIBlueprint

balances_bp = APIBlueprint("balances", __name__)


@balances_bp.route("/<chain>/<network>/balances/<address>", methods=["GET"])
def get_balances(chain, network, account_address):
    return balances.get_balances(chain, network, account_address)
