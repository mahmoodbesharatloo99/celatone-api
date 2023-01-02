import requests


def get_contracts(registry_url, chain, network):
    contracts = requests.get(
        f"{registry_url}/data/{chain}/{network}/contracts.json"
    ).json()
    return contracts


def get_contract(registry_url, chain, network, contract_address):
    contracts = requests.get(
        f"{registry_url}/data/{chain}/{network}/contracts.json"
    ).json()
    contract = [
        contract for contract in contracts if contract["address"] == contract_address
    ][0]
    return contract
