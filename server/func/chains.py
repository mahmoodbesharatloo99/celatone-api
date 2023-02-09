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
    chain = [chain for chain in chains if chain["name"].lower() == chain][0]
    return chain
