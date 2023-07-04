from typing import List

class BaseChainService:
    def __init__(self):
        # Simulating some data
        self.accounts = [{"address": f"address{i}"} for i in range(10)]
        self.assets = [{"type": f"type{i%3}", "slug": f"slug{i}", "price": i, "id": i} for i in range(10)]

    def get_accounts(self) -> List[dict]:
        """
        Returns a list of accounts
        """
        return self.accounts

    def get_account(self, address: str) -> dict:
        """
        Returns the account associated with the given address
        """
        for account in self.accounts:
            if account['address'] == address:
                return account
        return None

    def get_assets(self) -> List[dict]:
        """
        Returns a list of assets
        """
        return self.assets

    def get_assets_with_prices(self) -> List[dict]:
        """
        Returns a list of assets along with their prices
        """
        return [asset for asset in self.assets if 'price' in asset]

    def get_assets_by_type(self, asset_type: str) -> List[dict]:
        """
        Returns a list of assets that match the given asset type
        """
        return [asset for asset in self.assets if asset['type'] == asset_type]

    def get_assets_by_slug(self, asset_slug: str) -> List[dict]:
        """
        Returns a list of assets that match the given asset slug
        """
        return [asset for asset in self.assets if asset['slug'] == asset_slug]

    def get_asset(self, asset_id: int) -> dict:
        """
        Returns the asset associated with the given id
        """
        for asset in self.assets:
            if asset['id'] == asset_id:
                return asset
        return None
