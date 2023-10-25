from typing import List, Dict, Any
from utils.aldus import get_aldus_chain_data


class AccountManager:
    def __init__(self, chain: str, network: str):
        """
        Initializes the AccountManager with accounts data.

        Parameters:
        chain (str): The blockchain chain.
        network (str): The network.
        """
        self.chain = chain
        self.network = network
        self.accounts = get_aldus_chain_data(chain, network, "accounts")

    def get_accounts(self) -> List[Dict[str, Any]]:
        """
        Fetches accounts data.

        Returns:
        List[Dict[str, Any]]: A list of accounts.
        """
        return self.accounts

    def get_account(self, account_address: str) -> Dict[str, Any]:
        """
        Fetches a specific account by its address.

        Parameters:
        account_address (str): The address of the account.

        Returns:
        Dict[str, Any]: The account data.
        """
        try:
            return next(
                account
                for account in self.accounts
                if account["address"] == account_address
            )
        except StopIteration:
            raise ValueError(f"Account {account_address} not found")
