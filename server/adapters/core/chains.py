import json
import requests
from utils.constants import ALDUS_URL


def load_chain_data():
    chains = requests.get(f"{ALDUS_URL}/data/chains.json").json()
    return chains


def get_chains():
    chains = load_chain_data()
    return chains


def get_chain(chain):
    chains = get_chains()
    try:
        chain_data = next(chain_tuple for chain_tuple in chains.items() if chain_tuple[0].lower() == chain)
    except StopIteration:
        raise ValueError(f"Chain {chain} not found")
    return {chain_data[0]: chain_data[1]}
