import json
import os

from flask import Response

class ChainService():
    
    def __init__(self):
        if os.path.exists(f"../registry/data/chains.json"):
            with open("../registry/data/chains.json") as f:
                self._chains = json.load(f)
        else: self._chains = []

    @property
    def chains(self):
        return self._chains

    def get_chain(self, name):
        chains = self.chains
        try:
            chain_data = next(
                chain_tuple
                for chain_tuple in chains.items()
                if chain_tuple[0].lower() == name
            )
        except StopIteration:
            # raise ValueError(f"Chain {name} not found")
            return Response(f"Chain {name} not found", status=404)
        return {chain_data[0]: chain_data[1]}
    