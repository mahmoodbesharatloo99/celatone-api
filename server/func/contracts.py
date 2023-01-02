import json


def load_contracts(chain, network):
    contracts = json.load(open(f"../registry/data/{chain}/{network}/contracts.json"))
    return contracts


def get_contracts(chain, network):
    contracts = load_contracts(chain, network)
    return contracts


def get_contract(chain, network, contract_address):
    contracts = load_contracts(chain, network)
    contract = [
        contract for contract in contracts if contract["address"] == contract_address
    ][0]
    return contract
