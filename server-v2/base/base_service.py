from abc import ABC, abstractmethod
from typing import List, Dict, Any
from utils.registry import load_and_check_registry_data
from utils.helper import encode_base64
from utils.price import get_prices

class BaseService(ABC):
    chain: str = None
    network: str = None

    def __init__(self):
        if self.chain is None or self.network is None:
            raise NotImplementedError("Subclasses must define `chain` and `network`.")
        
        self._accounts = load_and_check_registry_data(self.chain, self.network, "accounts")
        self._codes = load_and_check_registry_data(self.chain, self.network, "accounts")
        self._contracts = load_and_check_registry_data(self.chain, self.network, "contracts")
        self._assets = [
            dict(asset, **{"price": 0.00}) 
            for asset in load_and_check_registry_data(self.chain, self.network, "assets")
            ]
            
    @property
    def accounts(self) -> Any:
        return self._accounts

    @property
    def codes(self) -> Any:
        return self._codes

    @property
    def contracts(self) -> Any:
        return self._contracts
    
    @property
    def assets(self) -> Any:
        return self._assets

    def get_account(self, account_address: str) -> Dict:
        accounts = self.accounts()
        try:
            account = next(
                account for account in accounts if account["address"] == account_address
            )
        except StopIteration:
            raise ValueError(f"Account {account_address} not found")
        return account

    def get_assets_with_prices(self) -> List[Dict]:
        assets = self.assets()
        priced_assets = filter(lambda asset: asset["coingecko"], assets)
        priced_asset_ids = [asset["id"] for asset in priced_assets]
        prices = get_prices(self.chain, self.network, priced_asset_ids)
        asset_prices = {id: prices.get(id, 0.00) for id in priced_asset_ids}
        for asset in assets:
            asset["price"] = asset_prices.get(asset["id"], 0.00)
        return assets

    def get_assets_by_type(self, asset_type: str) -> List[Dict]:
        assets = self.assets()
        return list(filter(lambda asset: asset["type"] == asset_type, assets))

    def get_assets_by_slug(self, asset_slug: str) -> List[Dict]:
        assets = self.assets()
        return list(filter(lambda asset: asset_slug in asset["slugs"], assets))

    def get_asset(self, asset_id: int) -> Dict:
        assets = self.assets()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[asset_id]
    
    def get_asset_ibc(self, hash: str) -> List[Dict]:
        assets = self.assets()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[f"ibc/{hash}"]
    

