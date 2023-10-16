from flask import Blueprint
from adapters.core import accounts

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/accounts/<chain>/<network>", methods=["GET"])
def get_accounts(chain, network):
    """Get All Accounts

    Returns a list of all the known accounts based on the input chain and network
    """
    return accounts.get_accounts(chain, network)


@accounts_bp.route("/accounts/<chain>/<network>/<account_address>", methods=["GET"])
def get_account(chain, network, account_address):
    """Get Account by ID

    Returns a specific account based on the input chain, network, and account_address
    """
    return accounts.get_account(chain, network, account_address)
