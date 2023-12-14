from apiflask import APIBlueprint

from . import accounts, assets, blocks, move, overviews, transactions

v1_bp = APIBlueprint("v1", __name__, url_prefix="/v1")

v1_bp.register_blueprint(accounts.accounts_bp)
v1_bp.register_blueprint(assets.assets_bp)
v1_bp.register_blueprint(blocks.blocks_bp)
v1_bp.register_blueprint(move.move_bp)
v1_bp.register_blueprint(overviews.overviews_bp)
v1_bp.register_blueprint(transactions.transactions_bp)
