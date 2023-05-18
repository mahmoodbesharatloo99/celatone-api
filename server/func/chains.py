import os
import json


def load_chain_data():
    path = f"../registry/data/chains.json"
    data = []
    if os.path.exists(path):
        data = json.load(open(path))
    return data


def get_chains():
    chains = load_chain_data()
    return chains


def get_chain(chain):
    chains = get_chains()
    chain_data = [chain_tuple for chain_tuple in chains.items() if chain_tuple[0].lower() == chain][0]

    return {chain_data[0]: chain_data[1]}
