from typing import Any, List, Dict
from utils.registry import load_and_check_registry_data
from core.base.base_service import BaseService

class OsmosisBaseService(BaseService):
    def __init__(self):
        self._pools = load_and_check_registry_data(
            chain=self.chain,
            network=self.network, 
            content="pools"
        )

    @property
    def pools(self):
        return self._pools
    
    def get_pool(self, pool_id):
        pools = self.pools
        pool = next(filter(lambda pool: pool["id"] == int(pool_id), pools), None)
        return pool
    
    def get_asset_factory(self, creator, symbol):
        assets = self.get_assets_with_prices()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[f"factory/{creator}/{symbol}"]


    def get_asset_gamm(self, pool_id):
        assets = self.get_assets_with_prices()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[f"gamm/pool/{pool_id}"]
