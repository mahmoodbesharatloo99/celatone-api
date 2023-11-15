import logging

import requests
from flask import Response, abort
from utils.gcs import get_network_data
from utils.graphql.validators import get_graphql_validators


def _get_network_base_denom(chain, network):
    response = requests.get(
        f"{get_network_data(chain,network,'lcd')}/cosmos/staking/v1beta1/params"
    )
    response.raise_for_status()
    return response.json()["params"]["bond_denom"]


def get_params(chain, network):
    try:
        if chain == "initia":
            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/initia/mstaking/v1/params"
            )
            response.raise_for_status()
            return response.json()
        else:
            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/cosmos/staking/v1beta1/params"
            )
            response.raise_for_status()
            json_response = response.json()

            json_response["params"]["bond_denoms"] = [
                json_response["params"]["bond_denom"]
            ]
            del json_response["params"]["bond_denom"]

            return json_response
    except requests.HTTPError as _:
        abort(
            Response(
                response=response.content,
                status=response.status_code,
                headers=response.headers.items(),
            )
        )


def get_delegations(chain, network, address, params):
    try:
        if chain == "initia":
            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/initia/mstaking/v1/delegations/{address}",
                params=params,
            )
            response.raise_for_status()
            return response.json()
        else:
            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/cosmos/staking/v1beta1/delegations/{address}"
            )
            response.raise_for_status()
            json_response = response.json()

            for delegation in json_response["delegation_responses"]:
                denom = delegation["balance"]["denom"]
                delegation["delegation"]["shares"] = [
                    {
                        "denom": denom,
                        "amount": delegation["delegation"]["shares"],
                    }
                ]
                delegation["balance"] = [delegation["balance"]]

            return json_response
    except requests.HTTPError as _:
        abort(
            Response(
                response=response.content,
                status=response.status_code,
                headers=response.headers.items(),
            )
        )


def get_unbondings(chain, network, address, params):
    try:
        if chain == "initia":
            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/initia/mstaking/v1/delegators/{address}/unbonding_delegations",
                params=params,
            )
            response.raise_for_status()
            return response.json()
        else:
            base_denom = _get_network_base_denom(chain, network)

            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/cosmos/staking/v1beta1/delegators/{address}/unbonding_delegations"
            )
            response.raise_for_status()
            json_response = response.json()

            for unbonding in json_response["unbonding_responses"]:
                for entry in unbonding["entries"]:
                    entry["initial_balance"] = [
                        {
                            "denom": base_denom,
                            "amount": entry["initial_balance"],
                        }
                    ]
                    entry["balance"] = [
                        {
                            "denom": base_denom,
                            "amount": entry["balance"],
                        }
                    ]

            return json_response
    except requests.HTTPError as _:
        abort(
            Response(
                response=response.content,
                status=response.status_code,
                headers=response.headers.items(),
            )
        )


def get_redelegations(chain, network, address, params):
    try:
        if chain == "initia":
            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/initia/mstaking/v1/delegators/{address}/redelegations",
                params=params,
            )
            response.raise_for_status()
            return response.json()
        else:
            base_denom = _get_network_base_denom(chain, network)

            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/cosmos/staking/v1beta1/delegators/{address}/redelegations"
            )
            response.raise_for_status()
            json_response = response.json()

            for redelegation in json_response["redelegation_responses"]:
                for entry in redelegation["entries"]:
                    entry["redelegation_entry"]["initial_balance"] = [
                        {
                            "denom": base_denom,
                            "amount": entry["redelegation_entry"]["initial_balance"],
                        }
                    ]
                    entry["redelegation_entry"]["shares_dst"] = [
                        {
                            "denom": base_denom,
                            "amount": entry["redelegation_entry"]["shares_dst"],
                        }
                    ]
                    entry["balance"] = [
                        {
                            "denom": base_denom,
                            "amount": entry["balance"],
                        }
                    ]

            return json_response
    except requests.HTTPError as _:
        abort(
            Response(
                response=response.content,
                status=response.status_code,
                headers=response.headers.items(),
            )
        )


# in-place modification via reference
def _format_validator(validator, base_denom):
    validator["tokens"] = [{"denom": base_denom, "amount": validator["tokens"]}]
    validator["delegator_shares"] = [
        {"denom": base_denom, "amount": validator["delegator_shares"]}
    ]


def get_validators(chain, network):
    try:
        graphql_res = get_graphql_validators(chain, network)
        graphql_res.raise_for_status()
        return graphql_res.json()["data"]
    except Exception as e:
        logging.error(f"Error getting validators: {e}")


def get_validator(chain, network, validator_address):
    try:
        if chain == "initia":
            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/initia/mstaking/v1/validators/{validator_address}"
            )
            response.raise_for_status()
            return response.json()
        else:
            base_denom = _get_network_base_denom(chain, network)

            response = requests.get(
                f"{get_network_data(chain,network,'lcd')}/cosmos/staking/v1beta1/validators/{validator_address}"
            )
            response.raise_for_status()
            json_response = response.json()

            _format_validator(json_response["validator"], base_denom)

            return json_response
    except requests.HTTPError as _:
        abort(
            Response(
                response=response.content,
                status=response.status_code,
                headers=response.headers.items(),
            )
        )
