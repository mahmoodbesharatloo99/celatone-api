from typing import List, Dict, Any
from utils.aldus import get_aldus_chain_data
from utils.graphql import get_graphql_code_details


class CodeManager:
    def __init__(self, chain: str, network: str):
        """
        Initializes the CodeManager with code data.

        Parameters:
        chain (str): The blockchain chain.
        network (str): The network.
        """
        self.chain = chain
        self.network = network
        self.codes = self.load_codes(chain, network)

    def load_codes(self, chain: str, network: str) -> List[Dict[str, Any]]:
        """
        Fetches code data.

        Returns:
        List[Dict[str, Any]]: The code data.
        """
        codes = get_aldus_chain_data(chain, network, "codes")
        code_ids = [code["id"] for code in codes]

        graphql_map = {}
        graphql_details = get_graphql_code_details(chain, network, code_ids)
        for detail in graphql_details:
            graphql_map[detail["code_id"]] = detail

        for code in codes:
            code_details = graphql_map[code["id"]]
            code.update(
                {
                    "cw2Contract": code_details["cw2_contract"],
                    "cw2Version": code_details["cw2_version"],
                    "uploader": code_details["creator"],
                    "contracts": code_details["contract_instantiated"],
                    "instantiatePermission": code_details["access_config_permission"],
                    "permissionAddresses": code_details["access_config_addresses"],
                }
            )

        return codes

    def get_codes(self) -> List[Dict[str, Any]]:
        """
        Fetches code data.

        Returns:
        List[Dict[str, Any]]: The code data.
        """
        return self.codes

    def get_code(self, code_id: str) -> Dict[str, Any]:
        """
        Fetches a specific code by its ID.

        Parameters:
        code_id (str): The ID of the code.

        Returns:
        Dict[str, Any]: The code data.
        """
        try:
            return next(code for code in self.codes if code["id"] == int(code_id))
        except StopIteration:
            raise ValueError(f"Code {code_id} not found")
