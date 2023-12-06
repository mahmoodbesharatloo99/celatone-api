from utils.address import addr_to_val
from utils.rest import staking
from utils.graphql.validators import get_graphql_validators


def get_delegations_by_address(chain, network, address):
    operator_address = addr_to_val(address)

    staking_params = staking.get_rest_params(chain, network)
    validators = get_graphql_validators(chain, network)["validators"]
    delegations = staking.get_rest_delegations(chain, network, address)
    unbondings = staking.get_rest_unbondings(chain, network, address)
    redelegations = staking.get_rest_redelegations(chain, network, address)
    delegations_rewards = staking.get_rest_delegations_rewards(chain, network, address)
    commission = staking.get_rest_commission(chain, network, operator_address)

    validators_dict = {v["operator_address"]: v for v in validators}

    delegations = [
        {
            "balance": d["balance"],
            "validator": {
                "validator_address": d["delegation"]["validator_address"],
                "moniker": validators_dict[d["delegation"]["validator_address"]].get(
                    "moniker", None
                ),
                "identity": validators_dict[d["delegation"]["validator_address"]].get(
                    "identity", None
                ),
            },
        }
        for d in delegations
    ]

    unbondings = [
        {
            "entries": u["entries"],
            "delegator_address": u["delegator_address"],
            "validator": {
                "validator_address": u["validator_address"],
                "moniker": validators_dict[u["validator_address"]].get("moniker", None),
                "identity": validators_dict[u["validator_address"]].get(
                    "identity", None
                ),
            },
        }
        for u in unbondings
    ]

    redelegations = [
        {
            "entries": r["entries"],
            "validator_src": {
                "validator_address": r["redelegation"]["validator_src_address"],
                "moniker": validators_dict[
                    r["redelegation"]["validator_src_address"]
                ].get("moniker", None),
                "identity": validators_dict[
                    r["redelegation"]["validator_src_address"]
                ].get("identity", None),
            },
            "validator_dst": {
                "validator_address": r["redelegation"]["validator_dst_address"],
                "moniker": validators_dict[
                    r["redelegation"]["validator_dst_address"]
                ].get("moniker", None),
                "identity": validators_dict[
                    r["redelegation"]["validator_dst_address"]
                ].get("identity", None),
            },
        }
        for r in redelegations
    ]

    delegations_rewards["rewards"] = [
        {
            "validator": {
                "validator_address": d["validator_address"],
                "moniker": validators_dict[d["validator_address"]].get("moniker", None),
                "identity": validators_dict[d["validator_address"]].get(
                    "identity", None
                ),
            },
            "reward": d["reward"],
        }
        for d in delegations_rewards["rewards"]
    ]

    return {
        "commissions": commission,
        "delegations": delegations,
        "delegations_rewards": delegations_rewards,
        "is_validator": bool(validators_dict.get(operator_address)),
        "redelegations": redelegations,
        "staking_params": staking_params["params"],
        "unbondings": unbondings,
    }
