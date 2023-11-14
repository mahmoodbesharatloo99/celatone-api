from apiflask import APIBlueprint
from . import (
    accounts,
    assets,
    cosmwasm,
    monitoring,
    icns,
    misc,
    registry,
    staking,
    transactions,
    initia,
)

legacy_bp = APIBlueprint("legacy", __name__)

legacy_bp.register_blueprint(accounts.accounts_bp)
legacy_bp.register_blueprint(assets.assets_bp)
legacy_bp.register_blueprint(cosmwasm.cosmwasm_bp)
legacy_bp.register_blueprint(monitoring.monitoring_bp)
legacy_bp.register_blueprint(icns.icns_bp)
legacy_bp.register_blueprint(misc.misc_bp)
legacy_bp.register_blueprint(registry.registry_bp)
legacy_bp.register_blueprint(staking.staking_bp)
legacy_bp.register_blueprint(transactions.transactions_bp)
legacy_bp.register_blueprint(initia.initia_bp)
