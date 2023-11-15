from typing import List, Dict, Any
from utils.aldus import get_aldus_chain_data
from utils.graphql.contracts import get_graphql_contract_instantiator_admin


class ContractManager:
    def __init__(self, chain: str, network: str):
        """
        Initializes the ContractManager with contract data.

        Parameters:
        chain (str): The blockchain chain.
        network (str): The network.
        """
        self.chain = chain
        self.network = network
        self.contracts = self.load_contracts(chain, network)

    def load_contracts(self, chain: str, network: str) -> List[Dict[str, Any]]:
        """
        Fetches contract data.

        Returns:
        List[Dict[str, Any]]: The contract data.
        """
        contracts = get_aldus_chain_data(chain, network, "contracts")
        codes = get_aldus_chain_data(chain, network, "codes")
        contract_addresses = [contract["address"] for contract in contracts]
        instantiator_admin_data = get_graphql_contract_instantiator_admin(
            chain, network, contract_addresses
        )
        code_map = {code["id"]: code for code in codes}
        instantiator_admin_map = {
            data["address"]: {
                "instantiator": data["instantiator"],
                "admin": data["admin"],
                "label": data["label"],
            }
            for data in instantiator_admin_data
        }
        for contract in contracts:
            if contract["code"] not in code_map:
                contract.update(
                    {
                        "description": "",
                        "github": "",
                        **instantiator_admin_map.get(contract["address"], {}),
                    }
                )
            else:
                code = code_map[contract["code"]]
                contract.update(
                    {
                        "description": code["description"],
                        "github": code["github"],
                        **instantiator_admin_map.get(contract["address"], {}),
                    }
                )
        return contracts

    def get_contracts(self) -> List[Dict[str, Any]]:
        """
        Fetches contract data.

        Returns:
        List[Dict[str, Any]]: The contract data.
        """
        return self.contracts

    def get_contract(self, contract_address: str) -> Dict[str, Any]:
        """
        Fetches a specific contract by its address.

        Parameters:
        contract_address (str): The address of the contract.

        Returns:
        Dict[str, Any]: The contract data.
        """
        try:
            return next(
                contract
                for contract in self.contracts
                if contract["address"] == contract_address
            )
        except StopIteration:
            raise ValueError(f"Contract {contract_address} not found")
