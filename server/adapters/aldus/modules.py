from typing import List, Dict, Any
from utils.aldus import get_aldus_chain_data


class ModuleManager:
    def __init__(self, chain: str, network: str):
        """
        Initializes the ModuleManager with module data.

        Parameters:
        chain (str): The blockchain chain.
        network (str): The network.
        """
        self.chain = chain
        self.network = network
        self.modules = self.load_modules(chain, network)

    def load_modules(self, chain: str, network: str) -> List[Dict[str, Any]]:
        """
        Fetches module data.

        Returns:
        List[Dict[str, Any]]: The module data.
        """
        modules = get_aldus_chain_data(chain, network, "modules")
        return modules

    def get_modules(self) -> List[Dict[str, Any]]:
        """
        Fetches module data.

        Returns:
        List[Dict[str, Any]]: The module data.
        """
        return self.modules

    def get_module(self, address: str, name: str) -> Dict[str, Any]:
        """
        Fetches a specific module by its address and name.

        Parameters:
        address (str): The module address.
        name (str): The module name.

        Returns:
        Dict[str, Any]: The module data.
        """
        try:
            return next(module for module in self.modules if module["address"] == address and module["name"] == name)
        except StopIteration:
            raise ValueError(f"Module {address}:{name} not found")
