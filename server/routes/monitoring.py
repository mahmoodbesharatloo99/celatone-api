from flask import Blueprint
from adapters.monitoring import health

monitoring_bp = Blueprint("monitoring", __name__)


@monitoring_bp.route("/<chain>/<network>/health", methods=["GET"])
def get_health(chain, network):
    return health.health_check(chain, network)
