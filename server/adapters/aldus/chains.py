import json
import requests
from typing import Dict, Any
from utils.constants import ALDUS_URL


class ChainManager:
    def __init__(self):
        """
        Initializes the ChainManager with chain data.
        """
        self.chains = self.load_chain_data()

    def load_chain_data(self) -> Dict[str, Any]:
        """
        Fetches chain data.

        Returns:
        Dict[str, Any]: The chain data.
        """
        chains = requests.get(f"{ALDUS_URL}/data/chains.json").json()
        return chains

    def get_chains(self) -> Dict[str, Any]:
        """
        Fetches chain data.

        Returns:
        Dict[str, Any]: The chain data.
        """
        return self.chains

    def get_chain(self, chain: str) -> Dict[str, Any]:
        """
        Fetches a specific chain by its name.

        Parameters:
        chain (str): The name of the chain.

        Returns:
        Dict[str, Any]: The chain data.
        """
        try:
            chain_data = next(
                chain_tuple
                for chain_tuple in self.chains.items()
                if chain_tuple[0].lower() == chain
            )
        except StopIteration:
            raise ValueError(f"Chain {chain} not found")
        return {chain_data[0]: chain_data[1]}
