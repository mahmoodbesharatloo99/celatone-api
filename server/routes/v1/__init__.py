from apiflask import APIBlueprint
from . import accounts

v1_bp = APIBlueprint('v1', __name__, url_prefix='/v1')

v1_bp.register_blueprint(accounts.accounts_bp)
