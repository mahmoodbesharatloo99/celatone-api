from flask import request
from apiflask import APIBlueprint
from adapters.core import staking

staking_bp = APIBlueprint("staking", __name__)


@staking_bp.route("/<chain>/<network>/staking/params", methods=["GET"])
def get_staking_params(chain, network):
    return staking.get_params(chain, network)


@staking_bp.route("/<chain>/<network>/staking/delegations/<address>", methods=["GET"])
def get_delegations(chain, network, address):
    return staking.get_delegations(chain, network, address, request.args)


@staking_bp.route("/<chain>/<network>/staking/unbondings/<address>", methods=["GET"])
def get_unbondings(chain, network, address):
    return staking.get_unbondings(chain, network, address, request.args)


@staking_bp.route("/<chain>/<network>/staking/redelegations/<address>", methods=["GET"])
def get_redelegations(chain, network, address):
    return staking.get_redelegations(chain, network, address, request.args)


@staking_bp.route("/<chain>/<network>/staking/validators", methods=["GET"])
def get_validators(chain, network):
    return staking.get_validators(chain, network)


@staking_bp.route(
    "/<chain>/<network>/staking/validators/<validator_address>", methods=["GET"]
)
def get_validator(chain, network, validator_address):
    return staking.get_validator(chain, network, validator_address)
