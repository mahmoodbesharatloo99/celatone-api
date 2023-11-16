from apiflask import APIBlueprint

from . import accounts, transactions

v1_bp = APIBlueprint("v1", __name__, url_prefix="/v1")

v1_bp.register_blueprint(accounts.accounts_bp)
v1_bp.register_blueprint(transactions.transactions_bp)
