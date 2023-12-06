from flask import request
from apiflask import APIBlueprint
from utils.rest import staking
from utils.graphql import validators

staking_bp = APIBlueprint("staking", __name__)


@staking_bp.route("/<chain>/<network>/staking/params", methods=["GET"])
def get_staking_params(chain, network):
    return staking.get_rest_params(chain, network)


@staking_bp.route("/<chain>/<network>/staking/delegations/<address>", methods=["GET"])
def get_delegations(chain, network, address):
    return staking.get_rest_delegations_legacy(chain, network, address)


@staking_bp.route("/<chain>/<network>/staking/unbondings/<address>", methods=["GET"])
def get_unbondings(chain, network, address):
    return staking.get_rest_unbondings_legacy(chain, network, address)


@staking_bp.route("/<chain>/<network>/staking/redelegations/<address>", methods=["GET"])
def get_redelegations(chain, network, address):
    return staking.get_rest_redelegations_legacy(chain, network, address)


@staking_bp.route("/<chain>/<network>/staking/validators", methods=["GET"])
def get_validators(chain, network):
    return validators.get_graphql_validators(chain, network)


@staking_bp.route(
    "/<chain>/<network>/staking/validators/<validator_address>", methods=["GET"]
)
def get_validator(chain, network, validator_address):
    return staking.get_rest_validator(chain, network, validator_address)
